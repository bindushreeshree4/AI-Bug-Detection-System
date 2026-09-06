import ast


def detect_bugs(code):
    bugs = []

    # Check syntax
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        bugs.append({
            "type": "Syntax Error",
            "severity": "High",
            "line": e.lineno,
            "message": e.msg
        })
        return bugs

    for node in ast.walk(tree):

        # -----------------------------------
        # Division by Zero Detection
        # -----------------------------------

        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):

            denominator = node.right

            # Case 1: denominator is exactly zero
            if isinstance(denominator, ast.Constant) and denominator.value == 0:
                bugs.append({
                    "type": "Division by Zero",
                    "severity": "High",
                    "line": node.lineno,
                    "message": "The code divides by zero, which will cause ZeroDivisionError."
                })

            # Case 2: denominator is a variable
            elif isinstance(denominator, ast.Name):
                bugs.append({
                    "type": "Possible Division by Zero",
                    "severity": "Medium",
                    "line": node.lineno,
                    "message": f"Variable '{denominator.id}' is used as a denominator. Make sure it cannot be zero."
                })

        # -----------------------------------
        # Empty Exception Handler
        # -----------------------------------

        if isinstance(node, ast.ExceptHandler):

            if (
                len(node.body) == 1
                and isinstance(node.body[0], ast.Pass)
            ):
                bugs.append({
                    "type": "Empty Exception Handler",
                    "severity": "Medium",
                    "line": node.lineno,
                    "message": "Exception is caught but not handled."
                })

        # -----------------------------------
        # Bare Except
        # -----------------------------------

        if isinstance(node, ast.ExceptHandler):

            if node.type is None:
                bugs.append({
                    "type": "Bare Except",
                    "severity": "Low",
                    "line": node.lineno,
                    "message": "Bare except catches all exceptions and can hide unexpected errors."
                })

        # -----------------------------------
        # Mutable Default Argument
        # -----------------------------------

        if isinstance(node, ast.FunctionDef):

            for default in node.args.defaults:

                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    bugs.append({
                        "type": "Mutable Default Argument",
                        "severity": "Medium",
                        "line": node.lineno,
                        "message": "Using a mutable object as a default argument can cause unexpected behavior."
                    })

        # -----------------------------------
        # Unsafe eval()
        # -----------------------------------

        if isinstance(node, ast.Call):

            if (
                isinstance(node.func, ast.Name)
                and node.func.id == "eval"
            ):
                bugs.append({
                    "type": "Unsafe eval Usage",
                    "severity": "High",
                    "line": node.lineno,
                    "message": "eval() can execute arbitrary code and should be avoided with untrusted input."
                })

        # -----------------------------------
        # Infinite While Loop
        # -----------------------------------

        if isinstance(node, ast.While):

            if (
                isinstance(node.test, ast.Constant)
                and node.test.value is True
            ):
                bugs.append({
                    "type": "Possible Infinite Loop",
                    "severity": "Medium",
                    "line": node.lineno,
                    "message": "while True detected. Make sure the loop has a reachable break condition."
                })

    return bugs