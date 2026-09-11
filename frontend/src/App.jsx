import { useEffect, useRef, useState } from "react";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
} from "chart.js";

import {
  Pie,
  Bar
} from "react-chartjs-2";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
);

const API_URL = "http://127.0.0.1:5000";


function App() {

  // =========================================================
  // STATE
  // =========================================================

  const [code, setCode] = useState("");

  const [bugs, setBugs] = useState([]);
  const [testCases, setTestCases] = useState([]);

  const [aiTestCases, setAiTestCases] = useState("");
  const [aiAnalysis, setAiAnalysis] = useState([]);

  const [execution, setExecution] = useState(null);
  const [retestResult, setRetestResult] = useState(null);

  const [history, setHistory] = useState([]);
  const [historyError, setHistoryError] = useState("");

  const [fixedCode, setFixedCode] = useState("");

  const [activeFilter, setActiveFilter] = useState("ALL");

  const [loading, setLoading] = useState(false);
  const [backendStatus, setBackendStatus] =
    useState("Checking...");

  const [beforeFix, setBeforeFix] = useState(null);
  const [afterFix, setAfterFix] = useState(null);

  // Uploaded Python file
  const [uploadedFileName, setUploadedFileName] = useState("");
  const fileInputRef = useRef(null);


  // =========================================================
  // BUG COUNTS
  // =========================================================

  const highBugs = bugs.filter(
    (bug) => bug.severity === "High"
  ).length;

  const mediumBugs = bugs.filter(
    (bug) => bug.severity === "Medium"
  ).length;

  const lowBugs = bugs.filter(
    (bug) => bug.severity === "Low"
  ).length;


  // =========================================================
  // QUALITY SCORE
  // =========================================================

  const calculateQualityScore = (bugList = []) => {

    if (
      !Array.isArray(bugList) ||
      bugList.length === 0
    ) {
      return 100;
    }

    const high = bugList.filter(
      (bug) => bug.severity === "High"
    ).length;

    const medium = bugList.filter(
      (bug) => bug.severity === "Medium"
    ).length;

    const low = bugList.filter(
      (bug) => bug.severity === "Low"
    ).length;

    const score =
      100 -
      high * 20 -
      medium * 10 -
      low * 5;

    return Math.max(
      0,
      Math.min(100, score)
    );
  };


  const qualityScore =
    calculateQualityScore(bugs);


  // =========================================================
  // CHART DATA
  // =========================================================

  const bugChartData = {

    labels: [
      "High",
      "Medium",
      "Low"
    ],

    datasets: [
      {
        label: "Bugs",

        data: [
          highBugs,
          mediumBugs,
          lowBugs
        ]
      }
    ]
  };


  const testChartData = {

    labels: [
      "Passed",
      "Failed"
    ],

    datasets: [
      {
        label: "Tests",

        data: [
          execution?.passed || 0,
          execution?.failed || 0
        ]
      }
    ]
  };


  // =========================================================
  // LOAD HISTORY + BACKEND
  // =========================================================

  useEffect(() => {

    checkBackend();
    loadHistory();

  }, []);


  const checkBackend = async () => {

    try {

      const response =
        await fetch(`${API_URL}/`);

      if (response.ok) {

        setBackendStatus(
          "Backend Connected"
        );

      } else {

        setBackendStatus(
          "Backend Error"
        );

      }

    } catch (error) {

      console.error(
        "Backend connection error:",
        error
      );

      setBackendStatus(
        "Backend Offline"
      );

    }
  };


  const loadHistory = async () => {

    try {

      setHistoryError("");

      const response =
        await fetch(
          `${API_URL}/history`
        );

      const data =
        await response.json();

      if (!response.ok) {

        setHistoryError(
          data.error ||
          "Unable to load test history."
        );

        return;
      }

      if (Array.isArray(data)) {

        setHistory(data);

      } else {

        setHistory([]);

      }

    } catch (error) {

      console.error(
        "History loading error:",
        error
      );

      setHistoryError(
        "Unable to connect to the MySQL history endpoint."
      );

    }
  };


  // =========================================================
  // UPLOAD PYTHON FILE
  // =========================================================

  const handleFileUpload = (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    if (!file.name.toLowerCase().endsWith(".py")) {
      alert("Please upload a Python (.py) file.");
      event.target.value = "";
      return;
    }

    const reader = new FileReader();

    reader.onload = (e) => {
      const fileContent = e.target?.result;

      if (typeof fileContent !== "string") {
        alert("Unable to read the Python file.");
        return;
      }

      setCode(fileContent);
      setUploadedFileName(file.name);

      // Clear old results because new code was uploaded
      setBugs([]);
      setTestCases([]);
      setAiTestCases("");
      setAiAnalysis([]);
      setExecution(null);
      setRetestResult(null);
      setFixedCode("");
      setBeforeFix(null);
      setAfterFix(null);
      setActiveFilter("ALL");
    };

    reader.onerror = () => {
      alert("Unable to read the selected Python file.");
    };

    reader.readAsText(file);

    // Allow uploading the same file again
    event.target.value = "";
  };


  // =========================================================
  // ANALYZE CODE
  // =========================================================

  const analyzeCode = async () => {

    if (!code.trim()) {

      alert(
        "Please enter Python code."
      );

      return;
    }

    setLoading(true);

    try {

      const response =
        await fetch(
          `${API_URL}/analyze`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json"
            },

            body: JSON.stringify({
              code: code
            })
          }
        );

      const data =
        await response.json();

      if (!response.ok) {

        alert(
          data.error ||
          "Analysis failed."
        );

        setLoading(false);

        return;
      }


      const detectedBugs =
        data.bugs || [];


      const generatedTests =
        data.test_cases || [];


      const executionData =
        data.execution || null;


      setBugs(
        detectedBugs
      );

      setTestCases(
        generatedTests
      );

      setAiTestCases(
        data.ai_test_cases || ""
      );

      setAiAnalysis(
        data.ai_analysis || []
      );

      setExecution(
        executionData
      );

      setRetestResult(null);

      setFixedCode("");


      setBeforeFix({

        bugs:
          detectedBugs.length,

        tests:
          generatedTests.length,

        passed:
          executionData?.passed || 0,

        failed:
          executionData?.failed || 0,

        passRate:
          executionData?.pass_percentage || 0,

        qualityScore:
          calculateQualityScore(
            detectedBugs
          )

      });


      setAfterFix(null);

      setActiveFilter("ALL");

      await loadHistory();


    } catch (error) {

      console.error(
        "Analysis error:",
        error
      );

      alert(
        "Unable to connect to Flask backend. Make sure app.py is running."
      );

    }

    setLoading(false);
  };


  // =========================================================
  // CLEAR ALL
  // =========================================================

  const clearAll = () => {

    setCode("");

    setUploadedFileName("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }

    setBugs([]);

    setTestCases([]);

    setAiTestCases("");

    setAiAnalysis([]);

    setExecution(null);

    setRetestResult(null);

    setFixedCode("");

    setBeforeFix(null);

    setAfterFix(null);

    setActiveFilter("ALL");

  };


  // =========================================================
  // COPY AI FIX
  // =========================================================

  const copyFix = async () => {

    if (!fixedCode) {

      alert(
        "No AI fixed code available."
      );

      return;
    }

    try {

      await navigator.clipboard.writeText(
        fixedCode
      );

      alert(
        "AI fixed code copied."
      );

    } catch (error) {

      console.error(
        "Copy error:",
        error
      );

      alert(
        "Unable to copy the fixed code."
      );

    }

  };


  // =========================================================
  // APPLY AI FIX
  // =========================================================

  const applyAIFix = () => {

    if (!fixedCode) {

      alert(
        "No AI fixed code available."
      );

      return;
    }

    setCode(
      fixedCode
    );

    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });

  };


  // =========================================================
  // RETEST FIXED CODE
  // =========================================================

  const retestFixedCode = async () => {

    if (!fixedCode) {

      alert(
        "No fixed code available."
      );

      return;
    }

    if (!testCases.length) {

      alert(
        "No generated test cases available."
      );

      return;
    }

    setLoading(true);

    try {

      const response =
        await fetch(
          `${API_URL}/retest`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json"
            },

            body: JSON.stringify({

              code: fixedCode,

              test_cases:
                testCases

            })

          }
        );


      const data =
        await response.json();


      if (!response.ok) {

        alert(
          data.error ||
          "Retest failed."
        );

        setLoading(false);

        return;
      }


      const retestBugs =
        Array.isArray(data.bugs)
          ? data.bugs
          : [];


      const retestExecution =
        data.execution || {

          results: [],

          total: 0,

          passed: 0,

          failed: 0,

          pass_percentage: 0

        };


      const calculatedAfterQuality =
        calculateQualityScore(
          retestBugs
        );


      setBugs(
        retestBugs
      );

      setExecution(
        retestExecution
      );


      setRetestResult({

        ...data,

        quality_score:
          calculatedAfterQuality

      });


      setAfterFix({

        bugs:
          retestBugs.length,

        tests:
          retestExecution.total || 0,

        passed:
          retestExecution.passed || 0,

        failed:
          retestExecution.failed || 0,

        passRate:
          retestExecution.pass_percentage || 0,

        qualityScore:
          calculatedAfterQuality

      });


      setActiveFilter(
        "ALL"
      );

      await loadHistory();


    } catch (error) {

      console.error(
        "Retest error:",
        error
      );

      alert(
        "Unable to connect to backend."
      );

    }

    setLoading(false);

  };


  // =========================================================
  // GENERATE PDF
  // =========================================================

  const generatePDFReport = async () => {

    if (!execution) {

      alert(
        "Please analyze some Python code first."
      );

      return;
    }

    setLoading(true);

    try {

      const reportData = {

        code: code,

        bugs: bugs,

        test_cases:
          testCases,

        ai_test_cases:
          aiTestCases,

        ai_analysis:
          aiAnalysis,

        fixed_code:
          fixedCode,

        execution:
          execution,

        quality_score:
          qualityScore,

        before_fix:
          beforeFix,

        after_fix:
          afterFix

      };


      const response =
        await fetch(
          `${API_URL}/generate-report`,
          {

            method: "POST",

            headers: {

              "Content-Type":
                "application/json"

            },

            body:
              JSON.stringify(
                reportData
              )

          }
        );


      const data =
        await response.json();


      if (!response.ok) {

        alert(
          data.error ||
          "PDF generation failed."
        );

        return;
      }


      const pdfResponse =
        await fetch(
          `${API_URL}/reports/AI_Software_Testing_Report.pdf`
        );


      if (!pdfResponse.ok) {

        alert(
          "PDF was generated, but could not be downloaded."
        );

        return;
      }


      const blob =
        await pdfResponse.blob();


      const url =
        window.URL.createObjectURL(
          blob
        );


      const link =
        document.createElement(
          "a"
        );


      link.href =
        url;


      link.download =
        "AI_Software_Testing_Report.pdf";


      document.body.appendChild(
        link
      );


      link.click();


      link.remove();


      window.URL.revokeObjectURL(
        url
      );


      alert(
        "PDF report downloaded successfully!"
      );


    } catch (error) {

      console.error(
        "PDF generation error:",
        error
      );

      alert(
        "Unable to generate PDF report."
      );

    } finally {

      setLoading(false);

    }

  };


  // =========================================================
  // TEST FILTERING
  // =========================================================

  const filteredResults =
    execution?.results?.filter(
      (result) => {

        if (
          activeFilter === "ALL"
        ) {

          return true;

        }

        return (
          result.status ===
          activeFilter
        );

      }
    ) || [];


  // =========================================================
  // BEFORE / AFTER HELPERS
  // =========================================================

  const difference = (
    before,
    after
  ) => {

    return after - before;

  };


  const getDifferenceClass = (
    before,
    after,
    lowerIsBetter = false
  ) => {

    const diff =
      after - before;


    if (diff === 0) {

      return "same";

    }


    if (lowerIsBetter) {

      return diff < 0
        ? "improved"
        : "worse";

    }


    return diff > 0
      ? "improved"
      : "worse";

  };


  // =========================================================
  // IMPROVEMENT MESSAGE
  // =========================================================

  const getImprovementMessage = () => {

    if (
      !beforeFix ||
      !afterFix
    ) {

      return (
        "Apply an AI fix and run retesting to compare results."
      );

    }


    const bugChange =
      afterFix.bugs -
      beforeFix.bugs;


    const passChange =
      afterFix.passRate -
      beforeFix.passRate;


    const qualityChange =
      afterFix.qualityScore -
      beforeFix.qualityScore;


    if (
      bugChange < 0 ||
      passChange > 0 ||
      qualityChange > 0
    ) {

      return (
        "The AI-assisted fix improved the overall software quality."
      );

    }


    if (
      bugChange === 0 &&
      passChange === 0 &&
      qualityChange === 0
    ) {

      return (
        "The results remained unchanged. Review the generated fix and test cases."
      );

    }


    return (
      "The retest results changed. Review the remaining failures before accepting the fix."
    );

  };


  // =========================================================
  // RENDER
  // =========================================================

  return (

    <div className="app">


      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="header">

        <div>

          <h1>
            AI Software Testing Assistant
          </h1>

          <p>
            AI-Based Software Bug Detection
            & Test Case Generation
          </p>

        </div>


        <div className="backend-status">

          <span className="status-dot"></span>

          {backendStatus}

        </div>

      </header>


      <main className="container">


        {/* =================================================
            SOURCE CODE
        ================================================= */}

        <section className="card">

          <div className="section-header">

            <div>

              <h2>
                Source Code Analysis
              </h2>

              <p>
                Paste Python source code or upload
                a Python file to detect bugs and
                automatically generate test cases.
              </p>

            </div>

          </div>


          {/* =================================================
              FILE UPLOAD
          ================================================= */}

          <div className="button-row">

            <input
              id="python-file-upload"
              ref={fileInputRef}
              type="file"
              accept=".py,text/x-python,text/plain"
              onChange={handleFileUpload}
              disabled={loading}
              style={{
                display: "none"
              }}
            />

            <button
              type="button"
              className="secondary-button"
              onClick={() => fileInputRef.current?.click()}
              disabled={loading}
            >
              📁 Upload Python File
            </button>

            {uploadedFileName && (
              <span
                style={{
                  alignSelf: "center",
                  fontSize: "14px",
                  fontWeight: "500"
                }}
              >
                📄 {uploadedFileName}
              </span>
            )}

          </div>


          <textarea

            className="code-editor"

            value={code}

            onChange={(e) => {

              setCode(
                e.target.value
              );

              setUploadedFileName("");

            }}

            placeholder={`Paste Python code here...

Example:

def divide(a, b):
    return a / b`}

          />


          <div className="button-row">

            <button
              className="primary-button"
              onClick={analyzeCode}
              disabled={loading}
            >

              {loading
                ? "Analyzing..."
                : "Analyze Code"}

            </button>


            <button
              className="secondary-button"
              onClick={clearAll}
              disabled={loading}
            >

              Clear

            </button>

          </div>

        </section>


        {/* =================================================
            DASHBOARD
        ================================================= */}

        <section className="dashboard-section">

          <h2>
            Testing Dashboard
          </h2>


          <div className="stats-grid">

            <div className="stat-card">

              <span>
                Total Bugs
              </span>

              <strong>
                {bugs.length}
              </strong>

            </div>


            <div className="stat-card">

              <span>
                Total Tests
              </span>

              <strong>
                {execution?.total || 0}
              </strong>

            </div>


            <div className="stat-card">

              <span>
                Passed
              </span>

              <strong>
                {execution?.passed || 0}
              </strong>

            </div>


            <div className="stat-card">

              <span>
                Failed
              </span>

              <strong>
                {execution?.failed || 0}
              </strong>

            </div>


            <div className="stat-card">

              <span>
                Pass Rate
              </span>

              <strong>
                {execution?.pass_percentage || 0}%
              </strong>

            </div>


            <div className="stat-card">

              <span>
                Quality Score
              </span>

              <strong>
                {qualityScore}/100
              </strong>

            </div>

          </div>


          <div className="charts-grid">

            <div className="chart-card">

              <h3>
                Bug Severity Distribution
              </h3>

              <div className="chart-container">

                <Pie
                  data={bugChartData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false
                  }}
                />

              </div>

            </div>


            <div className="chart-card">

              <h3>
                Test Execution Results
              </h3>

              <div className="chart-container">

                <Bar
                  data={testChartData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                      y: {
                        beginAtZero: true,
                        ticks: {
                          precision: 0
                        }
                      }
                    }
                  }}
                />

              </div>

            </div>

          </div>


          <div className="metrics-grid">

            <div className="metric-card">

              <span className="metric-icon">
                🐛
              </span>

              <div>

                <h3>
                  Total Bugs
                </h3>

                <strong>
                  {bugs.length}
                </strong>

              </div>

            </div>


            <div className="metric-card">

              <span className="metric-icon">
                🧪
              </span>

              <div>

                <h3>
                  Test Cases
                </h3>

                <strong>
                  {testCases.length}
                </strong>

              </div>

            </div>


            <div className="metric-card">

              <span className="metric-icon">
                ✅
              </span>

              <div>

                <h3>
                  Passed Tests
                </h3>

                <strong>
                  {execution?.passed || 0}
                </strong>

              </div>

            </div>


            <div className="metric-card">

              <span className="metric-icon">
                ❌
              </span>

              <div>

                <h3>
                  Failed Tests
                </h3>

                <strong>
                  {execution?.failed || 0}
                </strong>

              </div>

            </div>


            <div className="metric-card">

              <span className="metric-icon">
                📈
              </span>

              <div>

                <h3>
                  Pass Rate
                </h3>

                <strong>

                  {execution
                    ? `${execution.pass_percentage}%`
                    : "0%"}

                </strong>

              </div>

            </div>


            <div className="metric-card quality-card">

              <span className="metric-icon">
                ⭐
              </span>

              <div>

                <h3>
                  Quality Score
                </h3>

                <strong>
                  {qualityScore}/100
                </strong>

              </div>

            </div>

          </div>


          <div className="button-row">

            <button
              className="primary-button"
              onClick={generatePDFReport}
              disabled={
                loading ||
                !execution
              }
            >

              {loading
                ? "Generating PDF..."
                : "📄 Download PDF Report"}

            </button>

          </div>

        </section>


        {/* =================================================
            BUG SEVERITY
        ================================================= */}

        <section className="card">

          <h2>
            Bug Severity Overview
          </h2>

          <div className="severity-grid">

            <div className="severity-box high">

              <span>
                High
              </span>

              <strong>
                {highBugs}
              </strong>

            </div>


            <div className="severity-box medium">

              <span>
                Medium
              </span>

              <strong>
                {mediumBugs}
              </strong>

            </div>


            <div className="severity-box low">

              <span>
                Low
              </span>

              <strong>
                {lowBugs}
              </strong>

            </div>

          </div>

        </section>


        {/* =================================================
            QUALITY SCORE
        ================================================= */}

        <section className="card">

          <div className="quality-header">

            <div>

              <h2>
                Code Quality Score
              </h2>

              <p>
                Score calculated from detected
                bug severity.
              </p>

            </div>


            <div className="quality-number">

              {qualityScore}

              <span>
                /100
              </span>

            </div>

          </div>


          <div className="progress-container">

            <div
              className="progress-bar"
              style={{
                width:
                  `${qualityScore}%`
              }}
            ></div>

          </div>

        </section>


        {/* =================================================
            DETECTED BUGS
        ================================================= */}

        <section className="card">

          <h2>
            Detected Bugs
          </h2>


          {bugs.length === 0 ? (

            <div className="empty-state">

              ✓ No bugs detected.

            </div>

          ) : (

            <div className="bug-list">

              {bugs.map(
                (bug, index) => (

                  <div
                    className="bug-item"
                    key={index}
                  >

                    <div className="bug-top">

                      <h3>
                        {bug.type}
                      </h3>

                      <span
                        className={`severity-tag ${bug.severity.toLowerCase()}`}
                      >
                        {bug.severity}
                      </span>

                    </div>


                    <p>

                      <strong>
                        Line:
                      </strong>{" "}

                      {bug.line}

                    </p>


                    <p>
                      {bug.message}
                    </p>

                  </div>

                )
              )}

            </div>

          )}

        </section>


        {/* =================================================
            GENERATED TEST CASES
        ================================================= */}

        <section className="card">

          <h2>
            Generated Test Cases
          </h2>


          {testCases.length === 0 ? (

            <div className="empty-state">

              No test cases generated yet.

            </div>

          ) : (

            <div className="table-container">

              <table>

                <thead>

                  <tr>

                    <th>
                      ID
                    </th>

                    <th>
                      Description
                    </th>

                    <th>
                      Input
                    </th>

                    <th>
                      Expected
                    </th>

                  </tr>

                </thead>


                <tbody>

                  {testCases.map(
                    (test) => (

                      <tr
                        key={test.id}
                      >

                        <td>
                          {test.id}
                        </td>

                        <td>
                          {test.description}
                        </td>

                        <td>

                          <code>

                            {JSON.stringify(
                              test.input
                            )}

                          </code>

                        </td>

                        <td>

                          {test.expected_exception
                            ? `Exception: ${test.expected_exception}`
                            : test.expected ||
                              "Execution Success"}

                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            </div>

          )}

        </section>


        {/* =================================================
            AI GENERATED TEST CASES
        ================================================= */}

        <section className="card">

          <h2>
            AI Generated Test Cases
          </h2>


          {aiTestCases ? (

            <pre className="ai-output">
              {aiTestCases}
            </pre>

          ) : (

            <div className="empty-state">

              AI-generated test cases
              will appear here.

            </div>

          )}

        </section>


        {/* =================================================
            AI ANALYSIS
        ================================================= */}

        <section className="card">

          <h2>
            AI Analysis & Recommendations
          </h2>


          {aiAnalysis.length === 0 ? (

            <div className="empty-state">

              AI analysis will appear
              after code analysis.

            </div>

          ) : (

            aiAnalysis.map(
              (analysis, index) => (

                <div
                  className="analysis-box"
                  key={index}
                >

                  <h3>
                    {analysis.title}
                  </h3>


                  <p>

                    <strong>
                      Summary:
                    </strong>{" "}

                    {analysis.summary}

                  </p>


                  <pre className="ai-output">

                    {analysis.explanation}

                  </pre>


                  <p>

                    <strong>
                      Recommendation:
                    </strong>{" "}

                    {analysis.suggestion}

                  </p>


                  {analysis.fix &&
                    analysis.fix !==
                      "No automatic fix available." && (

                      <div className="fix-section">

                        <h3>
                          AI Fixed Code
                        </h3>


                        <pre className="code-block">

                          {analysis.fix}

                        </pre>


                        <div className="button-row">

                          <button
                            className="secondary-button"
                            onClick={() =>
                              setFixedCode(
                                analysis.fix
                              )
                            }
                          >

                            Load AI Fix

                          </button>

                        </div>

                      </div>

                    )}

                </div>

              )
            )

          )}

        </section>


        {/* =================================================
            FIXED CODE
        ================================================= */}

        {fixedCode && (

          <section className="card">

            <div className="section-header">

              <div>

                <h2>
                  AI Fixed Code
                </h2>

                <p>
                  Review the AI-generated
                  correction before applying
                  and retesting it.
                </p>

              </div>

            </div>


            <pre className="code-block">

              {fixedCode}

            </pre>


            <div className="button-row">

              <button
                className="secondary-button"
                onClick={copyFix}
              >

                Copy Fix

              </button>


              <button
                className="primary-button"
                onClick={applyAIFix}
              >

                Apply AI Fix

              </button>


              <button
                className="success-button"
                onClick={retestFixedCode}
                disabled={loading}
              >

                {loading
                  ? "Retesting..."
                  : "Apply Fix & Retest"}

              </button>

            </div>

          </section>

        )}


        {/* =================================================
            RETEST RESULT
        ================================================= */}

        {retestResult && (

          <section className="card">

            <h2>
              Retest Results
            </h2>


            <div className="metrics-grid">

              <div className="metric-card">

                <h3>
                  Bugs
                </h3>

                <strong>
                  {afterFix?.bugs ?? 0}
                </strong>

              </div>


              <div className="metric-card">

                <h3>
                  Tests
                </h3>

                <strong>
                  {afterFix?.tests ?? 0}
                </strong>

              </div>


              <div className="metric-card">

                <h3>
                  Passed
                </h3>

                <strong>
                  {afterFix?.passed ?? 0}
                </strong>

              </div>


              <div className="metric-card">

                <h3>
                  Failed
                </h3>

                <strong>
                  {afterFix?.failed ?? 0}
                </strong>

              </div>


              <div className="metric-card">

                <h3>
                  Pass Rate
                </h3>

                <strong>
                  {afterFix?.passRate ?? 0}%
                </strong>

              </div>


              <div className="metric-card">

                <h3>
                  Quality Score
                </h3>

                <strong>
                  {afterFix?.qualityScore ?? 100}/100
                </strong>

              </div>

            </div>

          </section>

        )}


        {/* =================================================
            BEFORE VS AFTER
        ================================================= */}

        <section className="card">

          <h2>
            Before vs After AI Fix
          </h2>


          {!beforeFix ||
          !afterFix ? (

            <div className="empty-state">

              Apply the AI fix and run
              retesting to compare the
              original and corrected code.

            </div>

          ) : (

            <>

              <div className="comparison-table">

                <div className="comparison-row header-row">

                  <div>
                    Metric
                  </div>

                  <div>
                    Before Fix
                  </div>

                  <div>
                    After Fix
                  </div>

                  <div>
                    Change
                  </div>

                </div>


                <div className="comparison-row">

                  <div>
                    Detected Bugs
                  </div>

                  <div>
                    {beforeFix.bugs}
                  </div>

                  <div>
                    {afterFix.bugs}
                  </div>

                  <div
                    className={getDifferenceClass(
                      beforeFix.bugs,
                      afterFix.bugs,
                      true
                    )}
                  >

                    {difference(
                      beforeFix.bugs,
                      afterFix.bugs
                    )}

                  </div>

                </div>


                <div className="comparison-row">

                  <div>
                    Total Tests
                  </div>

                  <div>
                    {beforeFix.tests}
                  </div>

                  <div>
                    {afterFix.tests}
                  </div>

                  <div>

                    {difference(
                      beforeFix.tests,
                      afterFix.tests
                    )}

                  </div>

                </div>


                <div className="comparison-row">

                  <div>
                    Passed Tests
                  </div>

                  <div>
                    {beforeFix.passed}
                  </div>

                  <div>
                    {afterFix.passed}
                  </div>

                  <div
                    className={getDifferenceClass(
                      beforeFix.passed,
                      afterFix.passed
                    )}
                  >

                    {difference(
                      beforeFix.passed,
                      afterFix.passed
                    )}

                  </div>

                </div>


                <div className="comparison-row">

                  <div>
                    Failed Tests
                  </div>

                  <div>
                    {beforeFix.failed}
                  </div>

                  <div>
                    {afterFix.failed}
                  </div>

                  <div
                    className={getDifferenceClass(
                      beforeFix.failed,
                      afterFix.failed,
                      true
                    )}
                  >

                    {difference(
                      beforeFix.failed,
                      afterFix.failed
                    )}

                  </div>

                </div>


                <div className="comparison-row">

                  <div>
                    Pass Rate
                  </div>

                  <div>
                    {beforeFix.passRate}%
                  </div>

                  <div>
                    {afterFix.passRate}%
                  </div>

                  <div
                    className={getDifferenceClass(
                      beforeFix.passRate,
                      afterFix.passRate
                    )}
                  >

                    {difference(
                      beforeFix.passRate,
                      afterFix.passRate
                    ).toFixed(2)}
                    %

                  </div>

                </div>


                <div className="comparison-row">

                  <div>
                    Quality Score
                  </div>

                  <div>
                    {beforeFix.qualityScore}
                  </div>

                  <div>
                    {afterFix.qualityScore}
                  </div>

                  <div
                    className={getDifferenceClass(
                      beforeFix.qualityScore,
                      afterFix.qualityScore
                    )}
                  >

                    {difference(
                      beforeFix.qualityScore,
                      afterFix.qualityScore
                    ) > 0

                      ? `+${difference(
                          beforeFix.qualityScore,
                          afterFix.qualityScore
                        )}`

                      : difference(
                          beforeFix.qualityScore,
                          afterFix.qualityScore
                        )}

                  </div>

                </div>

              </div>


              <div className="improvement-box">

                <h3>
                  AI Fix Evaluation
                </h3>


                <p>
                  {getImprovementMessage()}
                </p>


                <div className="validation-status">

                  {afterFix.bugs <
                    beforeFix.bugs ||
                  afterFix.passRate >
                    beforeFix.passRate ||
                  afterFix.qualityScore >
                    beforeFix.qualityScore ? (

                    <>

                      <span>
                        ✓
                      </span>

                      AI fix validated successfully
                      through retesting.

                    </>

                  ) : (

                    <>

                      <span>
                        !
                      </span>

                      Review the remaining
                      results before accepting
                      the fix.

                    </>

                  )}

                </div>

              </div>

            </>

          )}

        </section>


        {/* =================================================
            TEST EXECUTION
        ================================================= */}

        <section className="card">

          <div className="section-header">

            <div>

              <h2>
                Test Execution Results
              </h2>

              <p>
                Review the execution status
                of generated tests.
              </p>

            </div>


            <div className="filter-buttons">

              <button
                className={
                  activeFilter === "ALL"
                    ? "filter active"
                    : "filter"
                }
                onClick={() =>
                  setActiveFilter("ALL")
                }
              >
                All
              </button>


              <button
                className={
                  activeFilter === "PASS"
                    ? "filter active"
                    : "filter"
                }
                onClick={() =>
                  setActiveFilter("PASS")
                }
              >
                Passed
              </button>


              <button
                className={
                  activeFilter === "FAIL"
                    ? "filter active"
                    : "filter"
                }
                onClick={() =>
                  setActiveFilter("FAIL")
                }
              >
                Failed
              </button>

            </div>

          </div>


          {!execution ? (

            <div className="empty-state">

              Test execution results will
              appear here.

            </div>

          ) : filteredResults.length === 0 ? (

            <div className="empty-state">

              No{" "}

              {activeFilter === "ALL"
                ? ""
                : activeFilter.toLowerCase()}

              {" "}test results found.

            </div>

          ) : (

            <div className="execution-list">

              {filteredResults.map(
                (result) => (

                  <div
                    className={`execution-item ${
                      result.status ===
                      "PASS"
                        ? "execution-pass"
                        : "execution-fail"
                    }`}
                    key={result.id}
                  >

                    <div>

                      <strong>
                        {result.id}
                      </strong>

                      <p>
                        {result.message}
                      </p>

                    </div>

                    <span>
                      {result.status}
                    </span>

                  </div>

                )
              )}

            </div>

          )}

        </section>


        {/* =================================================
            HISTORY
        ================================================= */}

        <section className="card">

          <div className="section-header">

            <div>

              <h2>
                Test History
              </h2>

              <p>
                Previous test execution
                records stored in MySQL.
              </p>

            </div>


            <button
              className="secondary-button"
              onClick={loadHistory}
              disabled={loading}
            >

              Refresh

            </button>

          </div>


          {historyError && (

            <div className="empty-state">

              ⚠️ {historyError}

            </div>

          )}


          {!historyError &&
          history.length === 0 ? (

            <div className="empty-state">

              No test history available.

            </div>

          ) : history.length > 0 ? (

            <div className="table-container">

              <table>

                <thead>

                  <tr>

                    <th>
                      ID
                    </th>

                    <th>
                      Bugs
                    </th>

                    <th>
                      Total Tests
                    </th>

                    <th>
                      Passed
                    </th>

                    <th>
                      Failed
                    </th>

                    <th>
                      Pass Rate
                    </th>

                    <th>
                      Date
                    </th>

                  </tr>

                </thead>


                <tbody>

                  {history.map(
                    (item) => (

                      <tr
                        key={item.id}
                      >

                        <td>
                          {item.id}
                        </td>

                        <td>
                          {item.bugs}
                        </td>

                        <td>
                          {item.total_tests}
                        </td>

                        <td>
                          {item.passed}
                        </td>

                        <td>
                          {item.failed}
                        </td>

                        <td>
                          {item.pass_rate}%
                        </td>

                        <td>

                          {item.created_at

                            ? new Date(
                                item.created_at
                              ).toLocaleString()

                            : "-"}

                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            </div>

          ) : null}

        </section>


        {/* =================================================
            FINAL STATUS
        ================================================= */}

        <section className="final-status">

          {execution ? (

            execution.failed === 0 ? (

              <>

                <span className="final-icon">
                  ✓
                </span>

                <div>

                  <h2>
                    All Tests Passed
                  </h2>

                  <p>
                    The analyzed code
                    successfully passed
                    all generated test cases.
                  </p>

                </div>
              </>

            ) : (

              <>

                <span className="final-icon">
                  !
                </span>

                <div>

                  <h2>
                    Testing Completed
                  </h2>

                  <p>
                    Some test cases failed.
                    Review the detected bugs
                    and AI recommendations.
                  </p>

                </div>

              </>

            )

          ) : (

            <>

              <span className="final-icon">
                🧪
              </span>

              <div>

                <h2>
                  Ready for Testing
                </h2>

                <p>
                  Enter Python code or upload
                  a Python file above to begin
                  software analysis.
                </p>

              </div>

            </>

          )}

        </section>

      </main>


      {/* =====================================================
          FOOTER
      ===================================================== */}

      <footer className="footer">

        <p>
          AI Software Testing Assistant
        </p>

        <span>
          React • Flask • Python • OpenAI • MySQL
        </span>

      </footer>

    </div>

  );

}


export default App;