from pearl_system import PearlSystemController

def main():
    sys_ctrl = PearlSystemController()

    print("--- Pearl Level 8 & 9: Extended System Control Test ---\n")

    # 1. Test System Health Stats
    stats = sys_ctrl.get_system_stats()
    print(f"[System Stats]: {stats}")

    # 2. Test Brightness Control
    bright_res = sys_ctrl.set_brightness(75)
    print(f"[Brightness]: {bright_res}")

    # 3. Test File Search
    file_res = sys_ctrl.find_file("assistant_brain")
    print(f"[File Search]: {file_res}")

if __name__ == "__main__":
    main()