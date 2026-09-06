import ast


def normalize_value(value):
    """Convert values into JSON-friendly comparable forms."""

    if isinstance(value, tuple):
        return [normalize_value(item) for item in value]

    if isinstance(value, set):
        return sorted(
            [normalize_value(item) for item in value],
            key=str
        )

    if isinstance(value, dict):
        return {
            str(key): normalize_value(val)
            for key, val in value.items()
        }

    if isinstance(value, list):
        return [
            normalize_value(item)
            for item in value
        ]

    return value


def values_match(actual, expected):
    """Compare actual and expected outputs."""

    actual = normalize_value(actual)
    expected = normalize_value(expected)

    return actual == expected


def execute_test_cases(code, test_cases):
    """
    Execute generated test cases against Python code.
    """

    results = []

    # -----------------------------------------
    # Validate Python syntax
    # -----------------------------------------

    try:
        tree = ast.parse(code)
    except SyntaxError as error:

        results.append({
            "id": "TC001",
            "status": "FAIL",
            "message": f"Syntax Error: {error}"
        })

        return {
            "results": results,
            "total": 1,
            "passed": 0,
            "failed": 1,
            "pass_percentage": 0.0
        }

    # -----------------------------------------
    # Find functions
    # -----------------------------------------

    functions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    ]

    if not functions:

        return {
            "results": [{
                "id": "TC001",
                "status": "PASS",
                "message": (
                    "Python syntax is valid, "
                    "but no testable function was found."
                )
            }],
            "total": 1,
            "passed": 1,
            "failed": 0,
            "pass_percentage": 100.0
        }

    # -----------------------------------------
    # Execute submitted code
    # -----------------------------------------

    namespace = {}

    try:

        exec(
            compile(
                tree,
                filename="<user_code>",
                mode="exec"
            ),
            namespace
        )

    except Exception as error:

        results.append({
            "id": "TC001",
            "status": "FAIL",
            "message": (
                f"Code execution error: "
                f"{type(error).__name__}: {error}"
            )
        })

        return {
            "results": results,
            "total": 1,
            "passed": 0,
            "failed": 1,
            "pass_percentage": 0.0
        }

    # -----------------------------------------
    # Execute each test case
    # -----------------------------------------

    for test in test_cases:

        test_id = test.get("id", "UNKNOWN")

        description = test.get(
            "description",
            ""
        )

        inputs = test.get(
            "input",
            {}
        )

        expected_exception = test.get(
            "expected_exception"
        )

        has_expected_output = (
            "expected_output" in test
            or "expected" in test
        )

        expected_output = test.get(
            "expected_output",
            test.get("expected")
        )

        # -------------------------------------
        # Identify function
        # -------------------------------------

        function_name = None

        for function_node in functions:

            if function_node.name in description:

                function_name = function_node.name
                break

        # If only one function exists
        if function_name is None and len(functions) == 1:

            function_name = functions[0].name

        if function_name is None:

            results.append({
                "id": test_id,
                "status": "FAIL",
                "message": (
                    "Could not identify the function "
                    "for this test case."
                )
            })

            continue

        function = namespace.get(
            function_name
        )

        if function is None:

            results.append({
                "id": test_id,
                "status": "FAIL",
                "message": (
                    f"Function '{function_name}' "
                    "was not found."
                )
            })

            continue

        # -------------------------------------
        # Validate input
        # -------------------------------------

        if not isinstance(inputs, dict):

            results.append({
                "id": test_id,
                "status": "FAIL",
                "message": (
                    "Invalid test input. "
                    "Expected a dictionary."
                )
            })

            continue

        # -------------------------------------
        # Run test
        # -------------------------------------

        try:

            output = function(
                **inputs
            )

            # ---------------------------------
            # Expected exception but none
            # ---------------------------------

            if expected_exception:

                results.append({
                    "id": test_id,
                    "status": "FAIL",
                    "message": (
                        f"Expected {expected_exception}, "
                        "but no exception was raised."
                    ),
                    "actual_output": normalize_value(output),
                    "expected_exception": expected_exception
                })

                continue

            # ---------------------------------
            # Expected output comparison
            # ---------------------------------

            if has_expected_output:

                if values_match(
                    output,
                    expected_output
                ):

                    results.append({
                        "id": test_id,
                        "status": "PASS",
                        "message": (
                            "Test passed. "
                            "Actual output matches "
                            "expected output."
                        ),
                        "actual_output": normalize_value(output),
                        "expected_output": normalize_value(
                            expected_output
                        )
                    })

                else:

                    results.append({
                        "id": test_id,
                        "status": "FAIL",
                        "message": (
                            "Test failed. "
                            "Actual output does not "
                            "match expected output."
                        ),
                        "actual_output": normalize_value(output),
                        "expected_output": normalize_value(
                            expected_output
                        )
                    })

                continue

            # ---------------------------------
            # Normal successful execution
            # ---------------------------------

            results.append({
                "id": test_id,
                "status": "PASS",
                "message": (
                    "Test executed successfully. "
                    f"Output: {output}"
                ),
                "actual_output": normalize_value(
                    output
                )
            })

        # -------------------------------------
        # Exception handling
        # -------------------------------------

        except Exception as error:

            actual_exception = type(error).__name__

            if (
                expected_exception
                and actual_exception == expected_exception
            ):

                results.append({
                    "id": test_id,
                    "status": "PASS",
                    "message": (
                        f"Expected {actual_exception} "
                        "was raised correctly."
                    ),
                    "actual_exception": actual_exception,
                    "expected_exception": expected_exception
                })

            else:

                results.append({
                    "id": test_id,
                    "status": "FAIL",
                    "message": (
                        f"Test failed: "
                        f"{actual_exception}: {error}"
                    ),
                    "actual_exception": actual_exception
                })

    # -----------------------------------------
    # Statistics
    # -----------------------------------------

    total = len(results)

    passed = sum(
        1
        for result in results
        if result["status"] == "PASS"
    )

    failed = total - passed

    pass_percentage = (
        (passed / total) * 100
        if total > 0
        else 0
    )

    return {
        "results": results,
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_percentage": round(
            pass_percentage,
            2
        )
    }