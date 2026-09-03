import re
import ast
import operator

class RequestRouter:
    """
    Intelligent Request Router (Level 7)
    Classifies user queries into distinct intent types so Pearl can select
    the fastest execution path without querying heavy AI models unnecessarily.
    """

    INTENT_MATH = "MATH"
    INTENT_PC_CONTROL = "PC_CONTROL"
    INTENT_WEATHER = "WEATHER"
    INTENT_GENERAL_AI = "GENERAL_AI"

    # Supported safe math operators
    SAFE_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
    }

    def classify_intent(self, query: str) -> str:
        """Determines the category/intent of the incoming query."""
        clean_q = query.lower().strip()

        # 1. Check for Math Expressions (e.g., "what's 250 * 12?", "calculate 15 + 45")
        if self._is_math_query(clean_q):
            return self.INTENT_MATH

        # 2. Check for PC System Control Triggers
        pc_triggers = [
            "open ", "launch ", "start ", "lock pc", "lock computer", 
            "lock screen", "screenshot", "capture screen", "mute"
        ]
        if any(trigger in clean_q for trigger in pc_triggers):
            return self.INTENT_PC_CONTROL

        # 3. Check for Weather Requests
        weather_triggers = ["weather", "temperature", "forecast", "how hot", "how cold"]
        if any(trigger in clean_q for trigger in weather_triggers):
            return self.INTENT_WEATHER

        # 4. Fallback to General AI / LLM
        return self.INTENT_GENERAL_AI

    # =========================================================
    # FAST LOCAL MATH EVALUATOR (Safe AST Evaluation)
    # =========================================================

    def _is_math_query(self, query: str) -> bool:
        """Detects simple arithmetic expressions."""
        # Strip common prefixes
        cleaned = re.sub(r"^(what's|what is|calculate|solve|eval|evaluate)\s*", "", query, flags=re.IGNORECASE)
        cleaned = cleaned.rstrip("?").strip()
        
        # Check if remaining string consists mainly of numbers and math symbols
        return bool(re.match(r"^[\d\s\+\-\*\/\^\%\.\(\)]+$", cleaned)) and any(c.isdigit() for c in cleaned)

    def evaluate_math(self, query: str) -> str:
        """Safely evaluates basic arithmetic expressions using Python AST."""
        try:
            expr = re.sub(r"^(what's|what is|calculate|solve|eval|evaluate)\s*", "", query, flags=re.IGNORECASE)
            expr = expr.replace("^", "**").rstrip("?").strip()

            node = ast.parse(expr, mode='eval').body
            result = self._eval_node(node)
            
            # Format nicely (remove unnecessary trailing .0)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
                
            return f"The answer is {result}."
        except Exception:
            return "I couldn't solve that calculation."

    def _eval_node(self, node):
        if isinstance(node, ast.Num):  # Number
            return node.n
        elif isinstance(node, ast.Constant):  # Python 3.8+ Constant
            return node.value
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            if op_type in self.SAFE_OPERATORS:
                return self.SAFE_OPERATORS[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):  # -<number>
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in self.SAFE_OPERATORS:
                return self.SAFE_OPERATORS[op_type](operand)
        raise ValueError("Unsupported mathematical node")