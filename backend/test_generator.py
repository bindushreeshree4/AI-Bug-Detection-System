import ast


def convert_value(node):
    """Convert an AST literal into a Python value."""

    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.List):
        return [convert_value(x) for x in node.elts]

    if isinstance(node, ast.Tuple):
        return tuple(convert_value(x) for x in node.elts)

    if isinstance(node, ast.Dict):
        return {
            convert_value(k): convert_value(v)
            for k, v in zip(node.keys, node.values)
        }

    return None


def generate_value(param_name, index):
    """Generate practical test values."""

    name = param_name.lower()

    if "b" == name or "denominator" in name:
        return [10, 1, -5, 100][index]

    if "num" in name or "number" in name:
        return [10, 1, -10, 100][index]

    if "item" in name:
        return [10, 1, -10, 100][index]

    if "expression" in name:
        return ["2 + 3", "1", "-10", "10 * 10"][index]

    if "key" in name:
        return ["name", "id", "value", "missing"][index]

    if "data" in name:
        return [{"name": "Bindu"}, {"id": 1}, {}, {"value": 10}][index]

    if "items" in name:
        return [[1, 2], [], [-1, 0], [1, 2, 3]][index]

    return [10, 1, -10, 100][index]


def create_input(function_node, index):
    """Create input dictionary for a function."""

    arguments = function_node.args.args

    inputs = {}

    for argument in arguments:
        inputs[argument.arg] = generate_value(
            argument.arg,
            index
        )

    return inputs


def create_test_case(function_node, index):
    """Create one test case."""

    function_name = function_node.name

    inputs = create_input(
        function_node,
        index
    )

    return {
        "id": f"TC{index + 1:03d}",
        "description": (
            f"Test {function_name} "
            f"with generated input"
        ),
        "input": inputs
    }


def generate_special_tests(function_node, start_index):
    """Generate important exception/edge tests."""

    tests = []

    function_name = function_node.name
    arguments = [arg.arg for arg in function_node.args.args]

    # -----------------------------------------
    # Division test
    # -----------------------------------------

    if len(arguments) >= 2:

        second = arguments[1].lower()

        if second in ["b", "denominator", "divisor"]:

            inputs = {
                arguments[0]: 10,
                arguments[1]: 0
            }

            tests.append({
                "id": f"TC{start_index:03d}",
                "description": (
                    f"Test {function_name} "
                    "with division by zero"
                ),
                "input": inputs,
                "expected_exception": "ZeroDivisionError"
            })

    return tests


def generate_test_cases(code):
    """Generate test cases from Python source code."""

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []

    functions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    ]

    test_cases = []

    # -----------------------------------------
    # Generate normal tests
    # -----------------------------------------

    for function in functions:

        for index in range(4):

            test_cases.append(
                create_test_case(
                    function,
                    index
                )
            )

    # -----------------------------------------
    # Generate special tests
    # -----------------------------------------

    next_id = len(test_cases) + 1

    for function in functions:

        special_tests = generate_special_tests(
            function,
            next_id
        )

        test_cases.extend(
            special_tests
        )

        next_id = len(test_cases) + 1

    # Maximum 20 tests
    return test_cases[:20]