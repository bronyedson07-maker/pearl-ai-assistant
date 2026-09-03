import sys
import math
import pyttsx3
import speech_recognition as sr
from PySide6.QtCore import Qt, QTimer, QRectF, QThread, Signal, QTime
from PySide6.QtGui import QColor, QPainter, QPen, QRadialGradient, QKeyEvent, QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QLabel,
    QPushButton, QStackedWidget, QLineEdit, QFileDialog,
    QHBoxLayout, QVBoxLayout, QScrollArea
)

from assistant_brain import AssistantBrain


# =========================================================
# VOICE OUTPUT WORKER (TEXT-TO-SPEECH)
# =========================================================

class TTSWorker(QThread):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 175)
            engine.setProperty('volume', 1.0)
            engine.say(self.text)
            engine.runAndWait()
        except Exception:
            pass


# =========================================================
# AUDIO INPUT WORKER (HIGH-SENSITIVITY SPEECH-TO-TEXT)
# =========================================================

class AudioWorker(QThread):
    status_changed = Signal(str)
    transcribed = Signal(str)
    error = Signal(str)

    def run(self):
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 0.8

        try:
            with sr.Microphone() as source:
                self.status_changed.emit("🎙 Listening... Speak normally")
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=12)
                self.status_changed.emit("⚡ Processing speech...")
                
                text = recognizer.recognize_google(audio)
                if text.strip():
                    self.transcribed.emit(text)
                else:
                    self.error.emit("No clear speech detected.")
        except sr.WaitTimeoutError:
            self.error.emit("Listening timed out (no speech heard).")
        except sr.UnknownValueError:
            self.error.emit("Could not understand what was said.")
        except Exception as e:
            self.error.emit(f"Microphone error: {str(e)}")


# =========================================================
# BRAIN PROCESSING WORKER
# =========================================================

class BrainWorker(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, brain, query):
        super().__init__()
        self.brain = brain
        self.query = query

    def run(self):
        try:
            response = self.brain.process_query(user_query=self.query)
            self.finished.emit(str(response))
        except Exception as e:
            self.error.emit(str(e))


# =========================================================
# COMPACT INPUT FIELD
# =========================================================

class MessageInput(QLineEdit):
    send_requested = Signal()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.send_requested.emit()
            event.accept()
        else:
            super().keyPressEvent(event)


# =========================================================
# PEARL ORB ANIMATION
# =========================================================

class PearlOrb(QWidget):
    def __init__(self, size=160):
        super().__init__()
        self.setFixedSize(size, size)
        self.phase = 0
        self.wave_radius = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

    def animate(self):
        self.phase += 0.04
        if self.phase > math.pi * 2:
            self.phase = 0

        self.wave_radius = (self.wave_radius + 1.2) % 60
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.width() / 2
        cy = self.height() / 2

        pulse = math.sin(self.phase) * 4
        radius = (self.width() * 0.24) + pulse

        for i in range(4):
            w_rad = (self.wave_radius + i * 18) % 65 + radius
            alpha = max(0, int(180 - (w_rad * 2.2)))
            painter.setPen(QPen(QColor(168, 85, 247, alpha), 1.5))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QRectF(cx - w_rad, cy - w_rad, w_rad * 2, w_rad * 2))

        glow = QRadialGradient(cx, cy, radius * 2.0)
        glow.setColorAt(0, QColor(168, 85, 247, 140))
        glow.setColorAt(0.4, QColor(126, 34, 206, 60))
        glow.setColorAt(1, QColor(11, 11, 18, 0))

        painter.setPen(Qt.NoPen)
        painter.setBrush(glow)
        painter.drawEllipse(QRectF(cx - radius * 2.0, cy - radius * 2.0, radius * 4.0, radius * 4.0))

        pearl = QRadialGradient(cx - 8, cy - 10, radius * 1.3)
        pearl.setColorAt(0, QColor(233, 213, 255))
        pearl.setColorAt(0.3, QColor(168, 85, 247))
        pearl.setColorAt(0.7, QColor(107, 33, 168))
        pearl.setColorAt(1, QColor(30, 10, 60))

        painter.setBrush(pearl)
        painter.drawEllipse(QRectF(cx - radius, cy - radius, radius * 2, radius * 2))


# =========================================================
# CHAT BUBBLE WIDGET
# =========================================================
# =========================================================
# CHAT BUBBLE WIDGET (LEFT / RIGHT ALIGNED)
# =========================================================

class MessageWidget(QWidget):
    def __init__(self, sender, text, timestamp, pearl=False):
        super().__init__()
        
        outer_layout = QHBoxLayout(self)
        outer_layout.setContentsMargins(0, 4, 0, 4)

        # Bubble frame
        bubble = QFrame()
        bubble.setMaximumWidth(520)
        bubble.setObjectName("pearlMessage" if pearl else "userMessage")

        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(14, 10, 14, 10)
        bubble_layout.setSpacing(4)

        header_layout = QHBoxLayout()
        sender_label = QLabel(sender)
        
        if pearl:
            sender_label.setStyleSheet("color: #c084fc; font-weight: 700; font-size: 12px;")
        else:
            sender_label.setStyleSheet("color: #38bdf8; font-weight: 700; font-size: 12px;")

        time_label = QLabel(timestamp)
        time_label.setStyleSheet("color: #64748b; font-size: 10px;")

        header_layout.addWidget(sender_label)
        header_layout.addStretch()
        header_layout.addWidget(time_label)

        message_label = QLabel(text)
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        message_label.setStyleSheet("color: #f1f5f9; font-size: 13.5px; line-height: 1.4;")

        bubble_layout.addLayout(header_layout)
        bubble_layout.addWidget(message_label)

        # Align User to RIGHT, Pearl to LEFT
        if pearl:
            outer_layout.addWidget(bubble)
            outer_layout.addStretch()
        else:
            outer_layout.addStretch()
            outer_layout.addWidget(bubble)


# =========================================================
# MAIN PEARL WINDOW
# =========================================================

class PearlWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.brain = AssistantBrain()
        self.worker = None
        self.audio_worker = None
        self.tts_worker = None
        self.is_sidebar_minimized = False

        self.setWindowTitle("Pearl AI")
        self.resize(1280, 800)
        self.setMinimumSize(1000, 650)

        self.build_ui()
        self.start_splash_sequence()

    def build_ui(self):
        central = QWidget()
        central.setStyleSheet("background-color: #0b0b12;")
        self.setCentralWidget(central)

        self.main_stack = QStackedWidget(central)
        window_layout = QVBoxLayout(central)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(self.main_stack)

        # Splash Screen
        self.splash_screen = QWidget()
        self.splash_screen.setStyleSheet("background-color: #07070c;")
        splash_layout = QVBoxLayout(self.splash_screen)
        splash_layout.setAlignment(Qt.AlignCenter)

        self.splash_orb = PearlOrb(size=220)
        splash_title = QLabel("P E A R L")
        splash_title.setStyleSheet("color: #ffffff; font-size: 28px; font-weight: 800; letter-spacing: 8px; margin-top: 20px;")
        splash_subtitle = QLabel("Initializing Intelligence...")
        splash_subtitle.setStyleSheet("color: #a855f7; font-size: 12px; font-weight: 500; letter-spacing: 2px;")

        splash_layout.addWidget(self.splash_orb, alignment=Qt.AlignCenter)
        splash_layout.addWidget(splash_title, alignment=Qt.AlignCenter)
        splash_layout.addWidget(splash_subtitle, alignment=Qt.AlignCenter)
        self.main_stack.addWidget(self.splash_screen)

        # Workspace Screen
        self.workspace_screen = QWidget()
        ws_layout = QHBoxLayout(self.workspace_screen)
        ws_layout.setContentsMargins(0, 0, 0, 0)
        ws_layout.setSpacing(0)

        self.create_sidebar(ws_layout)

        center_container = QWidget()
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        self.create_topbar(center_layout)
        self.home_page = self.create_home_page()
        center_layout.addWidget(self.home_page)

        ws_layout.addWidget(center_container, stretch=1)
        self.main_stack.addWidget(self.workspace_screen)

    def start_splash_sequence(self):
        self.main_stack.setCurrentIndex(0)
        QTimer.singleShot(2200, self.transition_to_main)

    def transition_to_main(self):
        self.main_stack.setCurrentIndex(1)

    def create_sidebar(self, parent_layout):
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(210)

        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(8)

        brand_layout = QHBoxLayout()
        self.sidebar_toggle = QPushButton("☰")
        self.sidebar_toggle.setFixedSize(28, 28)
        self.sidebar_toggle.setStyleSheet("background: transparent; border: none; color: #a855f7; font-size: 16px;")
        self.sidebar_toggle.clicked.connect(self.toggle_sidebar)

        self.brand_title = QLabel("PEARL")
        self.brand_title.setStyleSheet("color: #ffffff; font-size: 15px; font-weight: 800; letter-spacing: 3px;")

        brand_layout.addWidget(self.sidebar_toggle)
        brand_layout.addWidget(self.brand_title)
        brand_layout.addStretch()
        layout.addLayout(brand_layout)

        layout.addSpacing(12)

        self.new_chat_btn = QPushButton("+   New chat")
        self.new_chat_btn.setObjectName("newChatBtn")
        self.new_chat_btn.clicked.connect(self.reset_home_view)
        layout.addWidget(self.new_chat_btn)

        layout.addSpacing(12)

        nav_items = [("🏠", "Home"), ("💬", "Conversations"), ("🔔", "Reminders"), ("📁", "Files"), ("👁", "Vision")]
        for icon, name in nav_items:
            btn = QPushButton(f"  {icon}   {name}")
            btn.setObjectName("navButton")
            layout.addWidget(btn)

        layout.addStretch()
        parent_layout.addWidget(self.sidebar)

    def toggle_sidebar(self):
        self.is_sidebar_minimized = not self.is_sidebar_minimized
        self.sidebar.setFixedWidth(64 if self.is_sidebar_minimized else 210)
        self.brand_title.setVisible(not self.is_sidebar_minimized)
        self.new_chat_btn.setText("+" if self.is_sidebar_minimized else "+   New chat")

    def create_topbar(self, parent_layout):
        topbar = QFrame()
        topbar.setFixedHeight(45)
        topbar.setObjectName("topbar")
        top_layout = QHBoxLayout(topbar)
        top_layout.setContentsMargins(20, 0, 20, 0)

        title = QLabel("Pearl AI")
        title.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: 600;")
        top_layout.addWidget(title)
        top_layout.addStretch()

        status = QLabel("● Online")
        status.setStyleSheet("color: #22c55e; font-size: 11px; font-weight: 600;")
        top_layout.addWidget(status)

        parent_layout.addWidget(topbar)

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(chat_widget)
        self.chat_layout.setContentsMargins(100, 20, 100, 20)

        self.welcome_widget = QWidget()
        welcome_layout = QVBoxLayout(self.welcome_widget)
        welcome_layout.setContentsMargins(0, 50, 0, 20)

        self.home_orb = PearlOrb(size=130)
        welcome_layout.addWidget(self.home_orb, alignment=Qt.AlignCenter)

        self.greeting = QLabel("Good afternoon, Edson! 👋")
        self.greeting.setAlignment(Qt.AlignCenter)
        self.greeting.setStyleSheet("color: #ffffff; font-size: 26px; font-weight: 700; margin-top: 15px;")
        
        self.sub_greeting = QLabel("How can I help you today?")
        self.sub_greeting.setAlignment(Qt.AlignCenter)
        self.sub_greeting.setStyleSheet("color: #94a3b8; font-size: 14px; margin-top: 5px;")

        welcome_layout.addWidget(self.greeting)
        welcome_layout.addWidget(self.sub_greeting)

        self.chat_layout.addWidget(self.welcome_widget)

        self.messages_container = QVBoxLayout()
        self.chat_layout.addLayout(self.messages_container)

        self.chat_layout.addStretch()
        scroll.setWidget(chat_widget)
        layout.addWidget(scroll)

        # Bottom Action Bar
        input_container = QFrame()
        input_container.setObjectName("inputContainer")
        input_container.setFixedHeight(48)

        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(8, 2, 8, 2)
        input_layout.setSpacing(6)

        attach_btn = QPushButton("+")
        attach_btn.setObjectName("attachButton")
        attach_btn.setFixedSize(32, 32)
        attach_btn.setToolTip("Upload images or files")
        attach_btn.clicked.connect(self.open_file_dialog)

        self.input = MessageInput()
        self.input.setPlaceholderText("Message Pearl...")
        self.input.setObjectName("input")
        self.input.send_requested.connect(self.send_message)

        mic_btn = QPushButton("🎙")
        mic_btn.setObjectName("micButton")
        mic_btn.setFixedSize(32, 32)
        mic_btn.setToolTip("Voice recognition")
        mic_btn.clicked.connect(self.toggle_mic)

        send_btn = QPushButton("➤")
        send_btn.setObjectName("sendButton")
        send_btn.setFixedSize(32, 32)
        send_btn.clicked.connect(self.send_message)

        input_layout.addWidget(attach_btn)
        input_layout.addWidget(self.input)
        input_layout.addWidget(mic_btn)
        input_layout.addWidget(send_btn)

        wrapper = QWidget()
        w_layout = QVBoxLayout(wrapper)
        w_layout.setContentsMargins(140, 0, 140, 20)
        w_layout.addWidget(input_container)

        layout.addWidget(wrapper)
        return page

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Select File or Image", 
            "", 
            "All Files (*.*);;Images (*.png *.jpg *.jpeg);;Documents (*.pdf *.txt *.docx)"
        )
        if file_name:
            if self.welcome_widget.isVisible():
                self.welcome_widget.hide()
            now = QTime.currentTime().toString("hh:mm")
            self.add_message("You", f"📎 Attached file: {file_name.split('/')[-1]}", now, False)

    def toggle_mic(self):
        if self.welcome_widget.isVisible():
            self.welcome_widget.hide()

        self.input.setDisabled(True)
        self.input.setPlaceholderText("🎙 Initializing microphone...")

        self.audio_worker = AudioWorker()
        self.audio_worker.status_changed.connect(self.update_mic_status)
        self.audio_worker.transcribed.connect(self.handle_voice_input)
        self.audio_worker.error.connect(self.handle_voice_error)
        self.audio_worker.start()

    def update_mic_status(self, status_msg):
        self.input.setPlaceholderText(status_msg)

    def handle_voice_input(self, text):
        self.input.setDisabled(False)
        self.input.setPlaceholderText("Message Pearl...")
        self.input.setText(text)
        self.send_message()

    def handle_voice_error(self, err_msg):
        self.input.setDisabled(False)
        self.input.setPlaceholderText("Message Pearl...")
        now = QTime.currentTime().toString("hh:mm")
        self.add_message("Pearl", f"⚠️ {err_msg}", now, True)

    def send_message(self):
        text = self.input.text().strip()
        if not text:
            return

        if self.welcome_widget.isVisible():
            self.welcome_widget.hide()

        now = QTime.currentTime().toString("hh:mm")
        self.add_message("You", text, now, False)
        self.input.clear()

        self.worker = BrainWorker(self.brain, text)
        self.worker.finished.connect(self.handle_response)
        self.worker.start()

    def handle_response(self, response):
        now = QTime.currentTime().toString("hh:mm")
        self.add_message("Pearl", response, now, True)
        
        self.tts_worker = TTSWorker(response)
        self.tts_worker.start()

    def add_message(self, sender, text, timestamp, pearl):
        msg = MessageWidget(sender, text, timestamp, pearl)
        self.messages_container.addWidget(msg)

    def reset_home_view(self):
        self.welcome_widget.show()
        while self.messages_container.count():
            item = self.messages_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()


# =========================================================
# APPLICATION ENTRY & STYLES
# =========================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Inter", 10))

    app.setStyleSheet("""
        QMainWindow { background-color: #0b0b12; }
        QWidget { font-family: "Inter", "Segoe UI", sans-serif; }
        #sidebar { background-color: #0f0f18; border-right: 1px solid #1c1c2b; }
        #topbar { background-color: transparent; border-bottom: 1px solid #161624; }
        #newChatBtn { background: #7e22ce; color: #ffffff; border: none; border-radius: 8px; padding: 10px; font-weight: 600; font-size: 13px; }
        #newChatBtn:hover { background: #9333ea; }
        #navButton { background: transparent; color: #94a3b8; border: none; border-radius: 6px; padding: 8px; text-align: left; font-size: 13px; }
        #navButton:hover { background: #181826; color: #ffffff; }
        
        #inputContainer { background: #13131f; border: 1px solid #27273a; border-radius: 24px; }
        #inputContainer:focus-within { border: 1px solid #a855f7; }
        #input { background: transparent; border: none; color: #ffffff; font-size: 13.5px; }
        
        #attachButton { background: transparent; color: #94a3b8; border: none; font-size: 18px; font-weight: bold; border-radius: 16px; }
        #attachButton:hover { background: #1f1f33; color: #ffffff; }
        
        #micButton { background: transparent; color: #94a3b8; border: none; font-size: 14px; border-radius: 16px; }
        #micButton:hover { background: #1f1f33; color: #ffffff; }
        
        #sendButton { background: #a855f7; color: #ffffff; border: none; border-radius: 16px; font-size: 12px; }
        #sendButton:hover { background: #c084fc; }
        
        #userMessage { background: #1a172b; border: 1px solid #292345; border-radius: 12px; margin: 4px 0px; }
        #pearlMessage { background: #11111c; border: 1px solid #1e1e2e; border-radius: 12px; margin: 4px 0px; }
    """)

    window = PearlWindow()
    window.show()
    sys.exit(app.exec())