import mysql.connector
import os

from flask import Flask, request, jsonify , send_from_directory
from report_generator import generate_report
from flask_cors import CORS

from bug_detector import detect_bugs
from test_generator import generate_test_cases
from test_executor import execute_test_cases
from ai_analyzer import generate_ai_analysis, generate_ai_test_cases


app = Flask(__name__)
CORS(app)

# =========================================================
# FILE UPLOAD CONFIGURATION
# =========================================================

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "uploads"
)

ALLOWED_EXTENSIONS = {"py"}

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================================
# UPLOAD PYTHON FILE
# =========================================================

@app.route("/upload", methods=["POST"])
def upload_python_file():

    try:

        if "file" not in request.files:
            return jsonify({
                "error": "No file uploaded."
            }), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({
                "error": "No file selected."
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                "error": "Only Python (.py) files are allowed."
            }), 400

        code = file.read().decode("utf-8")

        if not code.strip():
            return jsonify({
                "error": "The uploaded Python file is empty."
            }), 400

        return jsonify({
            "message": "Python file uploaded successfully.",
            "filename": file.filename,
            "code": code
        })

    except UnicodeDecodeError:

        return jsonify({
            "error": "Unable to read the file. Please upload a UTF-8 encoded Python file."
        }), 400

    except Exception as error:

        print("❌ File upload error:", error)

        return jsonify({
            "error": str(error)
        }), 500

# =========================================================
# MYSQL CONFIGURATION
# =========================================================

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "MySQL@12345",
    "database": "ai_bug_testing"
}


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)


# =========================================================
# SAVE TEST HISTORY
# =========================================================

def save_history(bugs, total_tests, passed, failed, pass_rate):

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO test_history
            (bugs, total_tests, passed, failed, pass_rate)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            bugs,
            total_tests,
            passed,
            failed,
            pass_rate
        )

        cursor.execute(query, values)
        connection.commit()

        print("✅ Test history saved to MySQL.")

    except mysql.connector.Error as error:

        print("❌ MySQL save error:", error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "AI Bug Detection & Test Case Generation API is running!",
        "status": "success"
    })


# =========================================================
# ANALYZE CODE
# =========================================================

@app.route("/analyze", methods=["POST"])
def analyze_code():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Invalid request data."
            }), 400

        code = data.get("code", "")

        if not code.strip():

            return jsonify({
                "error": "No code provided."
            }), 400


        # -------------------------------------------------
        # 1. Detect Bugs
        # -------------------------------------------------

        print("🔍 Detecting bugs...")

        bugs = detect_bugs(code)


        # -------------------------------------------------
        # 2. AI Code Analysis
        # -------------------------------------------------

        print("🤖 Running AI analysis...")

        ai_analysis = generate_ai_analysis(
            code,
            bugs
        )


        # -------------------------------------------------
        # 3. Generate Test Cases
        # -------------------------------------------------

        print("🧪 Generating test cases...")

        test_cases = generate_test_cases(code)


        # -------------------------------------------------
        # 4. AI Generated Test Cases
        # -------------------------------------------------

        print("🤖 Generating AI test cases...")

        ai_test_cases = generate_ai_test_cases(code)


        # -------------------------------------------------
        # 5. Execute Test Cases
        # -------------------------------------------------

        print("▶️ Executing test cases...")

        execution_results = execute_test_cases(
            code,
            test_cases
        )


        # -------------------------------------------------
        # 6. Save History
        # -------------------------------------------------

        save_history(
            len(bugs),
            len(test_cases),
            execution_results.get("passed", 0),
            execution_results.get("failed", 0),
            execution_results.get("pass_percentage", 0)
        )


        # -------------------------------------------------
        # 7. Return Results
        # -------------------------------------------------

        return jsonify({

            "bugs": bugs,

            "total_bugs": len(bugs),

            "ai_analysis": ai_analysis,

            "test_cases": test_cases,

            "total_test_cases": len(test_cases),

            "ai_test_cases": ai_test_cases,

            "execution": execution_results

        })


    except Exception as error:

        print("❌ Analyze error:", error)

        return jsonify({
            "error": str(error)
        }), 500


# =========================================================
# RETEST CODE
# =========================================================

@app.route("/retest", methods=["POST"])
def retest_code():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Invalid request data."
            }), 400

        code = data.get("code", "")

        test_cases = data.get(
            "test_cases",
            []
        )

        if not code.strip():

            return jsonify({
                "error": "No code provided."
            }), 400


        # -------------------------------------------------
        # 1. Execute Tests Again
        # -------------------------------------------------

        print("🔄 Retesting code...")

        results = execute_test_cases(
            code,
            test_cases
        )


        # -------------------------------------------------
        # 2. Detect Remaining Bugs
        # -------------------------------------------------

        bugs = detect_bugs(code)


        # -------------------------------------------------
        # 3. Calculate Quality Score
        # -------------------------------------------------

        high_bugs = sum(
            1
            for bug in bugs
            if bug.get("severity") == "High"
        )

        medium_bugs = sum(
            1
            for bug in bugs
            if bug.get("severity") == "Medium"
        )

        low_bugs = sum(
            1
            for bug in bugs
            if bug.get("severity") == "Low"
        )

        quality_score = max(
            0,
            100
            - (high_bugs * 20)
            - (medium_bugs * 10)
            - (low_bugs * 5)
        )


        # -------------------------------------------------
        # 4. Return Retest Results
        # -------------------------------------------------

        return jsonify({

            "bugs": bugs,

            "total_bugs": len(bugs),

            "quality_score": quality_score,

            "execution": results

        })


    except Exception as error:

        print("❌ Retest error:", error)

        return jsonify({
            "error": str(error)
        }), 500


# =========================================================
# TEST HISTORY
# =========================================================

@app.route("/history", methods=["GET"])
def get_history():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                id,
                bugs,
                total_tests,
                passed,
                failed,
                pass_rate,
                created_at
            FROM test_history
            ORDER BY id DESC
        """)

        history = cursor.fetchall()


        # Convert MySQL datetime to JSON-safe string
        for item in history:

            if item.get("created_at"):

                item["created_at"] = (
                    item["created_at"]
                    .strftime("%Y-%m-%d %H:%M:%S")
                )


        return jsonify(history)


    except mysql.connector.Error as error:

        print("❌ MySQL history error:", error)

        return jsonify({
            "error": f"MySQL error: {error}"
        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

# =========================================================
# GENERATE PDF REPORT
# =========================================================

@app.route("/generate-report", methods=["POST"])
def generate_pdf_report():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No report data received"
            }), 400

        reports_folder = os.path.join(
            os.path.dirname(__file__),
            "reports"
        )

        os.makedirs(
            reports_folder,
            exist_ok=True
        )

        filename = os.path.join(
            reports_folder,
            "AI_Software_Testing_Report.pdf"
        )

        generate_report(
            data,
            filename
        )

        return jsonify({
            "message": "PDF report generated successfully",
            "filename": "AI_Software_Testing_Report.pdf"
        })

    except Exception as error:

        print("❌ PDF report error:", error)

        return jsonify({
            "error": str(error)
        }), 500

# =========================================================
        # DOWNLOAD PDF REPORT
# =========================================================

@app.route("/reports/<filename>", methods=["GET"])
def download_report(filename):

    reports_folder = os.path.join(
        os.path.dirname(__file__),
        "reports"
    )

    return send_from_directory(
        reports_folder,
        filename,
        as_attachment=True
    )



# =========================================================
# RUN FLASK SERVER
# =========================================================

if __name__ == "__main__":

    print("")
    print("==============================================")
    print("🚀 AI SOFTWARE TESTING ASSISTANT")
    print("==============================================")
    print("🌐 Backend: http://127.0.0.1:5000")
    print("📊 History: http://127.0.0.1:5000/history")
    print("📄 PDF Report: http://127.0.0.1:5000/generate-report")
    print("==============================================")
    print("")

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )