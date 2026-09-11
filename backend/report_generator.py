from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Preformatted
)
from reportlab.lib import colors
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm


def safe_text(value):
    """Convert values into safe PDF text."""

    if value is None:
        return ""

    return str(value)


def generate_report(data, filename):

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=24,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        fontSize=11,
        leading=15,
        spaceAfter=20
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=10,
        spaceAfter=10
    )

    normal_style = ParagraphStyle(
        "NormalReport",
        parent=styles["Normal"],
        fontSize=9,
        leading=13
    )

    code_style = ParagraphStyle(
        "Code",
        fontName="Courier",
        fontSize=7,
        leading=9
    )

    story = []

    # =====================================================
    # GET DATA
    # =====================================================
    source_code = data.get("code") or ""

    bugs = data.get("bugs") or []

    test_cases = data.get("test_cases") or []

    ai_test_cases = data.get("ai_test_cases") or ""

    ai_analysis = data.get("ai_analysis") or []

    fixed_code = data.get("fixed_code") or ""

    execution = data.get("execution") or {}

    before_fix = data.get("before_fix") or {}

    after_fix = data.get("after_fix") or {}

    # =====================================================
    # EXECUTION DATA
    # =====================================================

    total_tests = execution.get(
        "total",
        0
    )

    passed = execution.get(
        "passed",
        0
    )

    failed = execution.get(
        "failed",
        0
    )

    pass_rate = execution.get(
        "pass_percentage",
        0
    )

    quality_score = data.get(
        "quality_score",
        0
    )

    # =====================================================
    # TITLE
    # =====================================================

    story.append(
        Paragraph(
            "AI Software Testing Assistant",
            title_style
        )
    )

    story.append(
        Paragraph(
            "AI-Based Software Bug Detection & "
            "Test Case Generation System",
            subtitle_style
        )
    )

    story.append(
        Paragraph(
            "Software Testing Analysis Report",
            section_style
        )
    )

    story.append(
        Paragraph(
            "This report summarizes static bug detection, "
            "automatically generated test cases, test execution, "
            "AI-assisted analysis, and code improvement results.",
            normal_style
        )
    )

    story.append(
        Spacer(1, 15)
    )

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    story.append(
        Paragraph(
            "1. Testing Summary",
            section_style
        )
    )

    summary = [
        ["Metric", "Result"],
        [
            "Detected Bugs",
            str(len(bugs))
        ],
        [
            "Generated Test Cases",
            str(len(test_cases))
        ],
        [
            "Executed Tests",
            str(total_tests)
        ],
        [
            "Passed Tests",
            str(passed)
        ],
        [
            "Failed Tests",
            str(failed)
        ],
        [
            "Pass Rate",
            f"{pass_rate}%"
        ],
        [
            "Quality Score",
            f"{quality_score}/100"
        ]
    ]

    summary_table = Table(
        summary,
        colWidths=[230, 120]
    )

    summary_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.7,
                colors.black
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "FONTNAME",
                (0, 1),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "ALIGN",
                (1, 1),
                (1, -1),
                "CENTER"
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            )
        ])
    )

    story.append(summary_table)

    # =====================================================
    # SOURCE CODE
    # =====================================================

    story.append(
        Paragraph(
            "2. Source Python Code",
            section_style
        )
    )

    if source_code:

        story.append(
            Preformatted(
                safe_text(source_code),
                code_style
            )
        )

    else:

        story.append(
            Paragraph(
                "Source code was not provided.",
                normal_style
            )
        )

    story.append(
        Spacer(1, 15)
    )

    # =====================================================
    # BUG DETECTION
    # =====================================================

    story.append(
        Paragraph(
            "3. Detected Bugs",
            section_style
        )
    )

    if bugs:

        bug_data = [
            [
                "Type",
                "Severity",
                "Line",
                "Message"
            ]
        ]

        for bug in bugs:

            bug_data.append([
                safe_text(
                    bug.get("type")
                ),
                safe_text(
                    bug.get("severity")
                ),
                safe_text(
                    bug.get("line")
                ),
                safe_text(
                    bug.get("message")
                )
            ])

        bug_table = Table(
            bug_data,
            colWidths=[
                90,
                55,
                35,
                190
            ],
            repeatRows=1
        )

        bug_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    colors.black
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                )
            ])
        )

        story.append(
            bug_table
        )

    else:

        story.append(
            Paragraph(
                "No static bugs were detected.",
                normal_style
            )
        )

    # =====================================================
    # GENERATED TEST CASES
    # =====================================================

    story.append(
        Paragraph(
            "4. Generated Test Cases",
            section_style
        )
    )

    if test_cases:

        test_data = [
            [
                "ID",
                "Description",
                "Input",
                "Expected"
            ]
        ]

        for test in test_cases:

            expected = (
                test.get(
                    "expected_exception",
                    "Execution Success"
                )
            )

            test_data.append([
                safe_text(
                    test.get("id")
                ),
                safe_text(
                    test.get("description")
                ),
                safe_text(
                    test.get("input")
                ),
                safe_text(
                    expected
                )
            ])

        test_table = Table(
            test_data,
            colWidths=[
                40,
                150,
                120,
                60
            ],
            repeatRows=1
        )

        test_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    colors.black
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                )
            ])
        )

        story.append(
            test_table
        )

    else:

        story.append(
            Paragraph(
                "No generated test cases available.",
                normal_style
            )
        )

    # =====================================================
    # TEST EXECUTION
    # =====================================================

    story.append(
        Paragraph(
            "5. Test Execution Results",
            section_style
        )
    )

    results = execution.get(
        "results",
        []
    )

    if results:

        result_data = [
            [
                "ID",
                "Status",
                "Message"
            ]
        ]

        for result in results:

            result_data.append([
                safe_text(
                    result.get("id")
                ),
                safe_text(
                    result.get("status")
                ),
                safe_text(
                    result.get("message")
                )
            ])

        result_table = Table(
            result_data,
            colWidths=[
                45,
                55,
                270
            ],
            repeatRows=1
        )

        result_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    colors.black
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                )
            ])
        )

        story.append(
            result_table
        )

    else:

        story.append(
            Paragraph(
                "No execution results available.",
                normal_style
            )
        )

    # =====================================================
    # AI ANALYSIS
    # =====================================================

    story.append(
        PageBreak()
    )

    story.append(
        Paragraph(
            "6. AI-Powered Analysis",
            section_style
        )
    )

    if ai_analysis:

        for analysis in ai_analysis:

            title = safe_text(
                analysis.get(
                    "title",
                    "AI Analysis"
                )
            )

            summary_text = safe_text(
                analysis.get(
                    "summary",
                    ""
                )
            )

            explanation = safe_text(
                analysis.get(
                    "explanation",
                    ""
                )
            )

            suggestion = safe_text(
                analysis.get(
                    "suggestion",
                    ""
                )
            )

            story.append(
                Paragraph(
                    title,
                    styles["Heading3"]
                )
            )

            if summary_text:

                story.append(
                    Paragraph(
                        f"<b>Summary:</b> "
                        f"{summary_text}",
                        normal_style
                    )
                )

            if explanation:

                story.append(
                    Paragraph(
                        "<b>Analysis:</b>",
                        normal_style
                    )
                )

                # Split long AI response into paragraphs
                for paragraph in explanation.split("\n"):

                    paragraph = paragraph.strip()

                    if paragraph:

                        story.append(
                            Paragraph(
                                safe_text(
                                    paragraph
                                ).replace(
                                    "&",
                                    "&amp;"
                                ),
                                normal_style
                            )
                        )

                        story.append(
                            Spacer(1, 4)
                        )

            if suggestion:

                story.append(
                    Paragraph(
                        f"<b>Recommendation:</b> "
                        f"{suggestion}",
                        normal_style
                    )
                )

            story.append(
                Spacer(1, 12)
            )

    else:

        story.append(
            Paragraph(
                "AI analysis was not available.",
                normal_style
            )
        )

    # =====================================================
    # AI GENERATED TEST CASES
    # =====================================================

    story.append(
        Paragraph(
            "7. AI-Generated Test Cases",
            section_style
        )
    )

    if ai_test_cases:

        story.append(
            Preformatted(
                safe_text(
                    ai_test_cases
                ),
                code_style
            )
        )

    else:

        story.append(
            Paragraph(
                "AI-generated test cases were not available.",
                normal_style
            )
        )

    # =====================================================
    # AI FIXED CODE
    # =====================================================

    story.append(
        PageBreak()
    )

    story.append(
        Paragraph(
            "8. AI Suggested Fixed Code",
            section_style
        )
    )

    if fixed_code:

        story.append(
            Preformatted(
                safe_text(
                    fixed_code
                ),
                code_style
            )
        )

    else:

        story.append(
            Paragraph(
                "No AI fixed code was generated.",
                normal_style
            )
        )

    # =====================================================
    # BEFORE VS AFTER
    # =====================================================

    story.append(
        Paragraph(
            "9. Before vs After AI Fix",
            section_style
        )
    )

    if before_fix or after_fix:

        comparison = [
            [
                "Metric",
                "Before Fix",
                "After Fix"
            ],
            [
                "Bugs",
                safe_text(
                    before_fix.get(
                        "bugs",
                        "-"
                    )
                ),
                safe_text(
                    after_fix.get(
                        "bugs",
                        "-"
                    )
                )
            ],
            [
                "Tests",
                safe_text(
                    before_fix.get(
                        "tests",
                        "-"
                    )
                ),
                safe_text(
                    after_fix.get(
                        "tests",
                        "-"
                    )
                )
            ],
            [
                "Passed",
                safe_text(
                    before_fix.get(
                        "passed",
                        "-"
                    )
                ),
                safe_text(
                    after_fix.get(
                        "passed",
                        "-"
                    )
                )
            ],
            [
                "Failed",
                safe_text(
                    before_fix.get(
                        "failed",
                        "-"
                    )
                ),
                safe_text(
                    after_fix.get(
                        "failed",
                        "-"
                    )
                )
            ],
            [
                "Pass Rate",
                safe_text(
                    before_fix.get(
                        "passRate",
                        "-"
                    )
                ) + "%",
                safe_text(
                    after_fix.get(
                        "passRate",
                        "-"
                    )
                ) + "%"
            ],
            [
                "Quality Score",
                safe_text(
                    before_fix.get(
                        "qualityScore",
                        "-"
                    )
                ),
                safe_text(
                    after_fix.get(
                        "qualityScore",
                        "-"
                    )
                )
            ]
        ]

        comparison_table = Table(
            comparison,
            colWidths=[
                150,
                120,
                120
            ]
        )

        comparison_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    colors.black
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (0, -1),
                    "Helvetica-Bold"
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "CENTER"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ])
        )

        story.append(
            comparison_table
        )

    else:

        story.append(
            Paragraph(
                "Before/after comparison is available "
                "after applying and retesting an AI fix.",
                normal_style
            )
        )

    # =====================================================
    # FINAL CONCLUSION
    # =====================================================

    story.append(
        Paragraph(
            "10. Final Assessment",
            section_style
        )
    )

    if quality_score >= 90:

        conclusion = (
            "The analyzed code achieved a high quality score. "
            "Only minor or no static issues were identified."
        )

    elif quality_score >= 70:

        conclusion = (
            "The analyzed code has moderate quality. "
            "Some issues should be reviewed and tested further."
        )

    elif quality_score >= 40:

        conclusion = (
            "The analyzed code requires improvement. "
            "Several potential issues were detected."
        )

    else:

        conclusion = (
            "The analyzed code requires significant improvement. "
            "High-priority issues should be addressed before deployment."
        )

    story.append(
        Paragraph(
            conclusion,
            normal_style
        )
    )

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            "Generated by AI Software Testing Assistant",
            normal_style
        )
    )

    story.append(
        Paragraph(
            "React • Flask • Python • OpenAI • MySQL",
            normal_style
        )
    )

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(
        story
    )

    return filename
