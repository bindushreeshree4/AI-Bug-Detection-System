# 🤖 AI Software Testing Assistant

### AI-Based Software Bug Detection & Test Case Generation System

An AI-powered software testing assistant that analyzes Python source code, detects potential bugs, automatically generates test cases, executes them, provides AI-based recommendations and fixes, and generates professional PDF testing reports.

---

## 🚀 Features

* 🔍 **Static Bug Detection**

  * Detects syntax errors
  * Possible division by zero
  * Empty exception handlers
  * Bare `except`
  * Mutable default arguments
  * Unsafe `eval()` usage
  * Possible infinite loops

* 🧪 **Automatic Test Case Generation**

  * Generates normal test cases
  * Generates edge and exception test cases
  * Supports multiple Python functions

* ▶️ **Test Execution**

  * Executes generated test cases
  * Detects PASS / FAIL results
  * Reports actual exceptions and outputs
  * Calculates pass percentage

* 🤖 **AI Code Analysis**

  * Identifies root causes
  * Explains detected issues
  * Provides testing recommendations
  * Suggests corrective solutions

* 🛠️ **AI Code Fix**

  * Generates corrected Python code
  * Allows the user to review the fix
  * Supports applying and retesting the AI-generated solution

* 📊 **Testing Dashboard**

  * Total bugs
  * Total test cases
  * Passed and failed tests
  * Pass rate
  * Code quality score
  * Bug severity distribution
  * Test execution charts

* 📄 **PDF Test Reports**

  * Source code
  * Detected bugs
  * Generated test cases
  * Execution results
  * AI analysis
  * AI fixed code
  * Before/after comparison
  * Final assessment

* 🗄️ **Test History**

  * Stores previous testing results in MySQL
  * Displays historical test execution records

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │    React Frontend    │
                    │   Testing Dashboard  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Flask Backend    │
                    │      REST API        │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
      ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
      │ Bug Detector│   │Test Generator│   │Test Executor│
      │   Python    │   │    Python    │   │    Python   │
      └─────────────┘   └─────────────┘   └─────────────┘
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │    OpenAI Analysis   │
                    │   AI Fix Suggestions │
                    └──────────┬───────────┘
                               │
                  ┌────────────┴────────────┐
                  ▼                         ▼
           ┌──────────────┐          ┌──────────────┐
           │    MySQL     │          │  PDF Report  │
           │ Test History │          │  Generation   │
           └──────────────┘          └──────────────┘
```

---

## 🛠️ Technology Stack

### Frontend

* React.js
* Vite
* JavaScript
* HTML5
* CSS3
* Chart.js
* React Chart.js 2

### Backend

* Python
* Flask
* REST API

### AI

* OpenAI API

### Database

* MySQL

### Testing & Analysis

* Python AST
* Automated test execution
* Static code analysis

### Reporting

* ReportLab
* PDF report generation

### Development Tools

* VS Code
* Git
* GitHub

---

## 📂 Project Structure

```text
AI-Bug-Detection-System/
│
├── .gitignore
├── README.md
│
├── backend/
│   ├── app.py
│   ├── ai_analyzer.py
│   ├── bug_detector.py
│   ├── test_generator.py
│   ├── test_executor.py
│   ├── report_generator.py
│   └── reports/
│
└── frontend/
    ├── package.json
    ├── package-lock.json
    ├── index.html
    ├── vite.config.js
    │
    └── src/
        ├── App.jsx
        ├── App.css
        ├── index.css
        └── main.jsx
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/bindushreeshree4/AI-Bug-Detection-System.git
cd AI-Bug-Detection-System
```

---

## 🐍 Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python3 -m venv venv
```

Activate it:

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install flask python-dotenv openai reportlab mysql-connector-python
```

---

## 🔐 OpenAI API Configuration

Create a `.env` file inside the `backend` folder:

```text
OPENAI_API_KEY=your_openai_api_key
```

**Never commit your `.env` file or expose your API key publicly.**

The project `.gitignore` already excludes `.env`.

---

## 🗄️ MySQL Configuration

Configure your MySQL database according to the database settings used in `backend/app.py`.

The system uses MySQL to store previous testing execution records.

---

## ▶️ Run the Backend

From the `backend` directory:

```bash
python3 app.py
```

The Flask server runs at:

```text
http://127.0.0.1:5000
```

---

## ⚛️ Frontend Setup

Open another Terminal:

```bash
cd AI-Bug-Detection-System/frontend
```

Install dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

---

## 🧪 Example

Example Python code:

```python
def divide(a, b):
    return a / b
```

The system can identify:

```text
Possible Division by Zero
```

It can then generate test cases including:

```text
(a=10, b=10)
(a=1, b=1)
(a=-10, b=-5)
(a=100, b=100)
(a=10, b=0)
```

The final test case is used to verify the division-by-zero condition.

---

## 📊 Testing Workflow

```text
Paste Python Code
        ↓
Static Bug Detection
        ↓
Automatic Test Case Generation
        ↓
Test Execution
        ↓
AI Code Analysis
        ↓
AI Fix Recommendation
        ↓
Apply Fix & Retest
        ↓
Quality Score
        ↓
MySQL Test History
        ↓
PDF Test Report
```

---

## 🎯 Project Objective

The objective of this project is to simplify software testing by combining static analysis, automated test generation, test execution, AI-assisted code analysis, and reporting into a single web-based platform.

---

## 🔮 Future Enhancements

* Support for additional programming languages
* Advanced machine-learning-based bug prediction
* Selenium-based web testing
* File upload for source code
* Advanced code coverage analysis
* User authentication
* Cloud deployment
* CI/CD integration
* GitHub repository integration
* More advanced test-case generation

---

## 👩‍💻 Author

**Bindushree S**

Computer Science & Engineering

AI Software Testing Assistant — Full Stack AI Project

---

## 📌 GitHub Repository

[AI-Bug-Detection-System](https://github.com/bindushreeshree4/AI-Bug-Detection-System)
