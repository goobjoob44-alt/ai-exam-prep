import os
import sys
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress headers and footers on cover page
        
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#4a3b82"))
        self.drawString(54, 800, "ARTIFICIAL INTELLIGENCE — COMPLETE EXAM REVISION & EXPLAINER GUIDE")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#888888"))
        self.drawRightString(540, 800, "ADBU B.Tech CSE (CS701)")
        
        self.setStrokeColor(colors.HexColor("#dcdcf0"))
        self.setLineWidth(0.7)
        self.line(54, 794, 540, 794)
        
        # Footer
        self.line(54, 45, 540, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))
        self.drawString(54, 32, "Course Notes by Prof. Alok Choudhury & Prof. R.C. Chakraborty")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(540, 32, page_str)
        self.restoreState()

def get_scaled_image(img_path, max_width=470, max_height=250):
    if not os.path.exists(img_path):
        return None
    try:
        with PILImage.open(img_path) as pil_img:
            w, h = pil_img.size
            aspect = h / w
            target_w = min(max_width, w)
            target_h = target_w * aspect
            if target_h > max_height:
                target_h = max_height
                target_w = target_h / aspect
            return Image(img_path, width=target_w, height=target_h)
    except Exception as e:
        print(f"Error loading image {img_path}: {e}")
        return None

def build_pdf(filename="AI_Exam_Complete_Explainer_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    c_primary = colors.HexColor("#16163e")
    c_secondary = colors.HexColor("#4a3b82")
    c_accent = colors.HexColor("#008080")
    c_gold = colors.HexColor("#b8860b")
    c_dark = colors.HexColor("#222222")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=c_primary,
        alignment=1,
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        alignment=1,
        spaceAfter=25
    )
    
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_primary,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=c_accent,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=c_dark,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    formula_style = ParagraphStyle(
        'FormulaText',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#004d4d")
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1a1a2e")
    )

    caption_style = ParagraphStyle(
        'CaptionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#555555"),
        alignment=1,
        spaceBefore=3,
        spaceAfter=10
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=c_secondary
    )

    story = []

    def make_callout(text, title="KEY EXAM DEFINITION & TAKEAWAY", border_color="#6c5ce7", bg_color="#f5f4fc"):
        content = [
            Paragraph(f"<b><font color='{border_color}'>{title}</font></b>", callout_style),
            Spacer(1, 3),
            Paragraph(text, callout_style)
        ]
        t = Table([[content]], colWidths=[495])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LINELEFT', (0,0), (0,0), 3.5, colors.HexColor(border_color)),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#dcdcf0")),
        ]))
        return t

    def add_diagram(filename, caption, source_ref, max_w=470, max_h=230):
        img_path = os.path.join("images/pdf_diagrams", filename)
        img = get_scaled_image(img_path, max_w, max_h)
        res = []
        if img:
            res.append(Spacer(1, 4))
            res.append(img)
            res.append(Paragraph(f"<b>Figure:</b> {caption} — <i>[Source: {source_ref}]</i>", caption_style))
        return res

    # ==================== COVER / TITLE ====================
    story.append(Spacer(1, 20))
    story.append(Paragraph("ARTIFICIAL INTELLIGENCE", title_style))
    story.append(Paragraph("Complete Exam Revision Guide & Detailed Syllabus Explainer", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_secondary, spaceBefore=0, spaceAfter=15))

    meta_table_data = [
        [Paragraph("<b>Course Code:</b> CS701 (B.Tech CSE)", body_style), Paragraph("<b>Department:</b> Computer Science & Engineering", body_style)],
        [Paragraph("<b>University:</b> Assam Don Bosco University (ADBU)", body_style), Paragraph("<b>Instructor / Source:</b> Prof. Alok Choudhury & Prof. R.C. Chakraborty", body_style)],
        [Paragraph("<b>Coverage:</b> All 8 Lecture Modules & PDFs", body_style), Paragraph("<b>Includes:</b> 36 Core Definitions, 24 Official Diagrams, Proofs & 20Q Quiz", body_style)]
    ]
    meta_table = Table(meta_table_data, colWidths=[245, 250])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8f8fc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#dcdce8")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e8e8f2")),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # Executive Overview
    story.append(make_callout(
        "This master document provides a consolidated, in-depth mathematical and conceptual explanation of the entire Artificial Intelligence curriculum. "
        "It integrates official textbook diagrams, formal algorithms, complexity analyses, the PEAS agent matrix, heuristic search principles, logic proof techniques, "
        "and a fully resolved 20-question exam readiness test.",
        "EXAM REVISION GUIDE EXECUTIVE SUMMARY", "#16163e", "#f0f2fa"
    ))
    story.append(Spacer(1, 15))

    # Table of Contents
    toc_data = [
        [Paragraph("<b>Section</b>", table_header_style), Paragraph("<b>Topic & Lecture Focus</b>", table_header_style), Paragraph("<b>Primary Course Reference</b>", table_header_style)],
        [Paragraph("<b>Module 1</b>", table_cell_bold), Paragraph("Foundations, DIKW Hierarchy & 8 Eras of AI History", table_cell_style), Paragraph("1_Introduction_Agent.pdf", table_cell_style)],
        [Paragraph("<b>Module 2</b>", table_cell_bold), Paragraph("Intelligent Agents, PEAS Framework & 5 Architectures", table_cell_style), Paragraph("2_Agent Architecture and environment.pdf", table_cell_style)],
        [Paragraph("<b>Module 3</b>", table_cell_bold), Paragraph("Problem Solving & Informed Search (Greedy, A*, Consistency)", table_cell_style), Paragraph("4_ Informed Search Algorithms.pdf", table_cell_style)],
        [Paragraph("<b>Module 4</b>", table_cell_bold), Paragraph("Memory-Bounded Heuristic Search (IDA*, RBFS, SMA*)", table_cell_style), Paragraph("5_Memory Bounded Search.pdf", table_cell_style)],
        [Paragraph("<b>Module 5</b>", table_cell_bold), Paragraph("Knowledge Representation, Production Systems & Prolog", table_cell_style), Paragraph("1_Knowledge_Representations.pdf", table_cell_style)],
        [Paragraph("<b>Module 6</b>", table_cell_bold), Paragraph("Formal Logic, Rules of Inference & 8 Proof Methods", table_cell_style), Paragraph("4_Logic.pdf & 2_Rules-of-inference.pdf", table_cell_style)],
        [Paragraph("<b>Module 7</b>", table_cell_bold), Paragraph("Master AI Glossary (36 High-Yield Exam Definitions)", table_cell_style), Paragraph("Consolidated Course Glossary", table_cell_style)],
        [Paragraph("<b>Module 8</b>", table_cell_bold), Paragraph("20-Question Comprehensive Exam Simulation & Answer Key", table_cell_style), Paragraph("Exam Readiness Assessment", table_cell_style)]
    ]
    toc_t = Table(toc_data, colWidths=[65, 270, 160])
    toc_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dcdce8")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f9f9fd")]),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(toc_t)

    story.append(PageBreak())

    # ==================== MODULE 1 ====================
    story.append(Paragraph("Module 1: Foundations, DIKW Pyramid & History of AI", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "Artificial Intelligence is defined through two foundational paradigms: the scientific pursuit of understanding and modeling cognitive processes, "
        "and the engineering endeavor of constructing rational computational agents capable of sensing, deliberating, and acting.", body_style
    ))

    story.append(make_callout(
        "<b>The 4 Perspectives of AI (Russell & Norvig):</b><br/>"
        "• <b>Thinking Humanly:</b> Cognitive science approach; empirical modeling of the human mind.<br/>"
        "• <b>Acting Humanly:</b> Turing Test approach (1950); passing behavioral benchmarks in NLP, reasoning, knowledge, and ML.<br/>"
        "• <b>Thinking Rationally:</b> Laws of Thought approach; rigorous deductive inference via formal syllogisms and logic.<br/>"
        "• <b>Acting Rationally:</b> Rational Agent approach; selecting actions that maximize expected performance given available percepts.",
        "THE FOUR DIMENSIONS OF ARTIFICIAL INTELLIGENCE", "#008080", "#eef9f9"
    ))
    story.append(Spacer(1, 8))

    story.extend(add_diagram("ai_four_approaches.png", "The Four Approaches to AI Matrix", "PDF 1, Slide 10", max_h=190))
    story.extend(add_diagram("ai_sense_reason_act.png", "Sense, Reason, Act Framework Loop", "PDF 1, Slide 7", max_h=190))

    story.append(Paragraph("The DIKW Hierarchy", h2_style))
    story.append(Paragraph(
        "A foundational model in knowledge systems conceptualizing the progressive enrichment of human and computational cognition:<br/>"
        "1. <b>Data:</b> Disconnected, unorganized raw symbols, numbers, and facts without contextual framing.<br/>"
        "2. <b>Information:</b> Structured data enriched with relational context and meaning (answers <i>who, what, where</i>).<br/>"
        "3. <b>Knowledge:</b> Understanding of patterns, associations, rules, and procedures; encapsulated as <i>'knowing that'</i> (declarative) and <i>'knowing how'</i> (procedural).<br/>"
        "4. <b>Wisdom / Intelligence:</b> Evaluating principles and rationale (answers <i>why</i>).", body_style
    ))

    story.extend(add_diagram("turing_test_setup.png", "Alan Turing's 1950 Imitation Game (Turing Test) Setup", "PDF 1, Slide 11", max_h=180))

    story.append(Paragraph("Key Historical Eras & Milestones in AI", h2_style))
    history_bullets = [
        "<b>1943–1955 (Gestation):</b> McCulloch & Pitts propose the first mathematical model of artificial neurons. Alan Turing publishes <i>'Computing Machinery and Intelligence'</i>.",
        "<b>1956 (Birth of AI):</b> Dartmouth College Workshop. John McCarthy, Marvin Minsky, Claude Shannon, and Nathaniel Rochester officially coin the term <i>'Artificial Intelligence'</i>.",
        "<b>1952–1969 (Early Enthusiasm):</b> Newell & Simon build the Logic Theorist and General Problem Solver (GPS). Arthur Samuel constructs self-learning checkers programs.",
        "<b>1966–1973 (Reality Check & AI Winter I):</b> Early microworlds fail against combinatorial explosion. Minsky & Papert's <i>Perceptrons</i> book proves single-layer neural nets cannot solve XOR.",
        "<b>1969–1979 (Knowledge-Based / Expert Systems):</b> The shift toward domain-specific knowledge. DENDRAL analyzes molecular mass spectra; MYCIN diagnoses bacterial infections (~600 rules).",
        "<b>1980–1988 (Commercialization & Fifth Generation):</b> Commercial expert systems boom (DEC XCON saves millions). Japan invests in the massive Fifth Generation Project (Prolog).",
        "<b>1986–Present (Neural Renaissance):</b> Rumelhart, Hinton, and Williams popularize Backpropagation for multi-layer perceptrons, overcoming the XOR limitation.",
        "<b>2012–Present (Deep Learning & Foundation Models):</b> AlexNet wins ImageNet (2012); AlphaGo beats world champions (2016); Transformers and Large Language Models achieve general reasoning milestones."
    ]
    for b in history_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))

    story.append(PageBreak())

    # ==================== MODULE 2 ====================
    story.append(Paragraph("Module 2: Intelligent Agents & The PEAS Framework", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "An <b>Agent</b> is formally defined as an entity that perceives its environment through <b>Sensors</b> and acts upon it via <b>Actuators</b>. "
        "The mathematical relation is encapsulated by: <b>Agent = Architecture + Program</b>. The abstract mathematical mapping from complete percept histories "
        "to actions is the <b>Agent Function</b> $f: P^* \\to A$.", body_style
    ))

    story.append(make_callout(
        "<b>Rationality vs. Omniscience:</b><br/>"
        "A <b>Rational Agent</b> chooses an action expected to maximize its performance measure, based on: "
        "(1) Percept sequence to date, (2) Built-in domain knowledge, and (3) Actions available.<br/>"
        "<i>Critical Exam Distinction:</i> Rationality is NOT omniscience. Omniscience implies knowing the actual outcome in advance, which is impossible in real-world stochastic environments.",
        "RATIONAL AGENT PRINCIPLE", "#b8860b", "#fdfcf0"
    ))
    story.append(Spacer(1, 6))

    story.extend(add_diagram("agent_environment_loop.png", "Official Agent-Environment Interaction Model", "PDF 2, Slide 6", max_h=200))

    story.append(Paragraph("The PEAS Specification Matrix", h2_style))
    story.append(Paragraph(
        "Before designing an agent, the task environment must be rigorously specified using the PEAS framework: "
        "<b>Performance measure</b> (P), <b>Environment</b> (E), <b>Actuators</b> (A), and <b>Sensors</b> (S).", body_style
    ))

    peas_rows = [
        [Paragraph("<b>Agent</b>", table_header_style), Paragraph("<b>Performance Measure (P)</b>", table_header_style), Paragraph("<b>Environment (E)</b>", table_header_style), Paragraph("<b>Actuators (A)</b>", table_header_style), Paragraph("<b>Sensors (S)</b>", table_header_style)],
        [Paragraph("<b>Autonomous Taxi</b>", table_cell_bold), Paragraph("Safety, speed, legal compliance, comfort, profit", table_cell_style), Paragraph("Roads, traffic, pedestrians, weather", table_cell_style), Paragraph("Steering, accelerator, brakes, horn, turn signal", table_cell_style), Paragraph("Cameras, LiDAR, radar, GPS, speedometer", table_cell_style)],
        [Paragraph("<b>Medical Diagnostician</b>", table_cell_bold), Paragraph("Healthy patient, minimized cost, diagnostic accuracy", table_cell_style), Paragraph("Patient, clinical staff, laboratory", table_cell_style), Paragraph("Prescriptions, test orders, screen reports", table_cell_style), Paragraph("Keyboard entry of symptoms, vitals, lab data", table_cell_style)],
        [Paragraph("<b>Satellite Image Analysis</b>", table_cell_bold), Paragraph("Image classification accuracy, discovery rate", table_cell_style), Paragraph("Downlink telemetry, orbit paths, cloud cover", table_cell_style), Paragraph("Antenna repointing, alert dispatches", table_cell_style), Paragraph("Multi-spectral optical & infrared sensors", table_cell_style)],
        [Paragraph("<b>Part-Picking Robot</b>", table_cell_bold), Paragraph("Sorting percentage, sorting speed, zero damage", table_cell_style), Paragraph("Conveyor belt with mixed parts, bins", table_cell_style), Paragraph("Jointed robotic arm, suction gripper, motor", table_cell_style), Paragraph("Stereo cameras, grip pressure sensors", table_cell_style)],
        [Paragraph("<b>Smart Vacuum Cleaner</b>", table_cell_bold), Paragraph("Cleanliness score, battery life, room coverage", table_cell_style), Paragraph("Floors, carpet, obstacles, stairs, pets", table_cell_style), Paragraph("Drive wheels, brushes, suction motor", table_cell_style), Paragraph("Infrared cliff sensor, bump switch, dirt sensor", table_cell_style)]
    ]
    peas_t = Table(peas_rows, colWidths=[75, 110, 105, 105, 100])
    peas_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dcdce8")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f9f9fd")]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(peas_t)
    story.append(Spacer(1, 10))

    story.append(Paragraph("The 7 Environment Dimensions (Properties)", h2_style))
    env_data = [
        [Paragraph("<b>Dimension</b>", table_header_style), Paragraph("<b>Contrasting Extremes</b>", table_header_style), Paragraph("<b>Formal Definition & Exam Example</b>", table_header_style)],
        [Paragraph("<b>1. Observability</b>", table_cell_bold), Paragraph("Fully vs. Partially", table_cell_style), Paragraph("<b>Fully:</b> Complete state access (Chess). <b>Partially:</b> Sensor noise or blind spots require internal world model (Poker, Driving).", table_cell_style)],
        [Paragraph("<b>2. Determinism</b>", table_cell_bold), Paragraph("Deterministic vs. Stochastic", table_cell_style), Paragraph("<b>Deterministic:</b> Next state strictly fixed by state + action (Chess). <b>Stochastic:</b> Probabilities/noise exist (Backgammon, Driving).", table_cell_style)],
        [Paragraph("<b>3. Episodic</b>", table_cell_bold), Paragraph("Episodic vs. Sequential", table_cell_style), Paragraph("<b>Episodic:</b> Current action has no effect on future episodes (Defect inspection). <b>Sequential:</b> Actions cascade into future (Chess, Driving).", table_cell_style)],
        [Paragraph("<b>4. Dynamism</b>", table_cell_bold), Paragraph("Static vs. Dynamic vs. Semi", table_cell_style), Paragraph("<b>Static:</b> World doesn't change during deliberation (Crosswords). <b>Dynamic:</b> Changes constantly (Driving). <b>Semi:</b> Score decays with time (Timed Chess).", table_cell_style)],
        [Paragraph("<b>5. Continuity</b>", table_cell_bold), Paragraph("Discrete vs. Continuous", table_cell_style), Paragraph("<b>Discrete:</b> Countable finite states and actions (Chess). <b>Continuous:</b> Real-valued continuous coordinates, speed, angles (Driving).", table_cell_style)],
        [Paragraph("<b>6. Agent Count</b>", table_cell_bold), Paragraph("Single vs. Multi-Agent", table_cell_style), Paragraph("<b>Single:</b> Solo puzzle solving (Solitaire). <b>Multi-Agent:</b> Competitive (zero-sum, Chess) or Cooperative (fleet navigation).", table_cell_style)],
        [Paragraph("<b>7. Known Physics</b>", table_cell_bold), Paragraph("Known vs. Unknown", table_cell_style), Paragraph("<b>Known:</b> Environment rules are given upfront. <b>Unknown:</b> Agent must explore and discover transition physics first.", table_cell_style)]
    ]
    env_t = Table(env_data, colWidths=[90, 110, 295])
    env_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_accent),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dcdce8")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f9f9fd")]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(env_t)

    story.append(PageBreak())

    # ==================== AGENT ARCHITECTURES ====================
    story.append(Paragraph("The 5 Agent Architectures & Schematics", h2_style))
    story.append(Paragraph(
        "There are five fundamental agent program architectures ranging from simple condition-action lookup to full adaptive learning:", body_style
    ))

    story.append(Paragraph("1. Simple Reflex Agent", h3_style))
    story.append(Paragraph(
        "Selects actions based exclusively on the current percept, completely ignoring percept history. "
        "Operates via direct condition-action rules: <code>IF condition THEN action</code>. "
        "Fails completely in partially observable environments, frequently getting trapped in infinite loops.", body_style
    ))
    story.extend(add_diagram("simple_reflex_agent.png", "Simple Reflex Agent Architecture", "PDF 2, Slide 11", max_h=175))

    story.append(Paragraph("2. Model-Based Reflex Agent", h3_style))
    story.append(Paragraph(
        "Overcomes partial observability by maintaining an <b>internal state</b>. It relies on two types of knowledge: "
        "(1) <i>Transition Model:</i> how the world evolves independently of the agent, and "
        "(2) <i>Sensor Model:</i> how the agent's actions alter the world.", body_style
    ))
    story.extend(add_diagram("model_based_agent.png", "Model-Based Reflex Agent Architecture", "PDF 2, Slide 13", max_h=175))

    story.append(Paragraph("3. Goal-Based Agent", h3_style))
    story.append(Paragraph(
        "Combines internal state knowledge with explicit <b>goal descriptions</b> indicating desirable situations. "
        "Employs Search and Planning algorithms to compute a sequence of actions that achieves the goal.", body_style
    ))
    story.extend(add_diagram("goal_based_agent.png", "Goal-Based Agent Architecture", "PDF 2, Slide 15", max_h=175))

    story.append(Paragraph("4. Utility-Based Agent", h3_style))
    story.append(Paragraph(
        "Goals alone provide only a binary pass/fail assessment. A <b>utility function</b> $U(s)$ maps world states to real numbers, "
        "scoring degrees of happiness or preference. Allows the agent to make rational trade-offs between competing goals (e.g., speed vs. safety).", body_style
    ))
    story.extend(add_diagram("utility_based_agent.png", "Utility-Based Agent Architecture", "PDF 2, Slide 17", max_h=175))

    story.append(Paragraph("5. Learning Agent", h3_style))
    story.append(Paragraph(
        "Separated into four distinct functional modules:<br/>"
        "• <b>Learning Element:</b> Responsible for making improvements based on past experiences.<br/>"
        "• <b>Performance Element:</b> Responsible for selecting external actions (equivalent to previous agents).<br/>"
        "• <b>Critic:</b> Evaluates the agent's behavior against an external performance standard.<br/>"
        "• <b>Problem Generator:</b> Suggests exploratory actions leading to new, informative experiences (exploration vs. exploitation).", body_style
    ))
    story.extend(add_diagram("learning_agent.png", "Learning Agent Architecture", "PDF 2, Slide 19", max_h=175))

    story.append(PageBreak())

    # ==================== MODULE 3 ====================
    story.append(Paragraph("Module 3: Problem Solving & Informed / Heuristic Search", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "A search problem is formally formulated by 5 components: (1) <b>Initial State</b> $s_0$, (2) <b>Actions</b> $A(s)$, "
        "(3) <b>Transition Model</b> $\\text{Result}(s, a)$, (4) <b>Goal Test</b> $G(s)$, and (5) <b>Path Cost</b> $c(s, a, s')$. "
        "Search algorithms are evaluated along 4 metrics: <b>Completeness</b>, <b>Time Complexity</b>, <b>Space Complexity</b>, and <b>Optimality</b>.", body_style
    ))

    story.append(make_callout(
        "<b>Heuristic Function & Mathematical Guarantees:</b><br/>"
        "• A <b>Heuristic</b> $h(n)$ estimates the cost of the cheapest path from node $n$ to the goal (derived via problem relaxations).<br/>"
        "• <b>Admissibility:</b> $0 \\le h(n) \\le h^*(n)$ (never overestimates true cost). Guarantees optimality in $A^*$ tree search.<br/>"
        "• <b>Consistency (Monotonicity):</b> $h(n) \\le c(n, a, n') + h(n')$ (triangle inequality). Guarantees optimality in $A^*$ graph search.<br/>"
        "• <i>Theorem:</i> <b>Consistency $\\implies$ Admissibility</b>, but admissibility does NOT always imply consistency!",
        "HEURISTIC PROPERTIES & OPTIMALITY CRITERIA", "#008080", "#eef9f9"
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Comparison of Search Cost Evaluation Functions", h2_style))
    search_fns = [
        [Paragraph("<b>Algorithm</b>", table_header_style), Paragraph("<b>Evaluation Function</b>", table_header_style), Paragraph("<b>Completeness</b>", table_header_style), Paragraph("<b>Optimality</b>", table_header_style), Paragraph("<b>Complexity / Flaw</b>", table_header_style)],
        [Paragraph("<b>Uniform Cost (UCS)</b>", table_cell_bold), Paragraph("<code>f(n) = g(n)</code>", table_cell_style), Paragraph("Yes (step cost ≥ ε)", table_cell_style), Paragraph("Yes", table_cell_style), Paragraph("Expands circular contours in all directions; slow.", table_cell_style)],
        [Paragraph("<b>Greedy Best-First</b>", table_cell_bold), Paragraph("<code>f(n) = h(n)</code>", table_cell_style), Paragraph("No (can loop in graph)", table_cell_style), Paragraph("No", table_cell_style), Paragraph("Chases heuristic; gets fooled by deceptive paths.", table_cell_style)],
        [Paragraph("<b>A* Search</b>", table_cell_bold), Paragraph("<code>f(n) = g(n) + h(n)</code>", table_cell_style), Paragraph("Yes", table_cell_style), Paragraph("Yes (if admissible)", table_cell_style), Paragraph("Memory explosion: Space complexity is O(b^d).", table_cell_style)]
    ]
    search_t = Table(search_fns, colWidths=[95, 105, 80, 80, 135])
    search_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dcdce8")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f9f9fd")]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(search_t)
    story.append(Spacer(1, 8))

    story.extend(add_diagram("romania_map_costs.png", "The Romania Route Benchmark Problem Map", "PDF 4, Slide 17", max_h=190))
    story.extend(add_diagram("greedy_search_tree.png", "Greedy Best-First Search on Romania Tree", "PDF 4, Slide 22", max_h=190))
    story.extend(add_diagram("astar_search_tree.png", "A* Search on Romania Tree", "PDF 4, Slide 30", max_h=190))
    story.extend(add_diagram("astar_optimality_contours.png", "A* Optimality Proof via Concentric f-Cost Contours", "PDF 4, Slide 33", max_h=190))
    story.extend(add_diagram("heuristic_consistency_triangle.png", "Consistency / Monotonicity Triangle Inequality", "PDF 4, Slide 34", max_h=190))

    story.append(PageBreak())

    # ==================== MODULE 4 ====================
    story.append(Paragraph("Module 4: Memory-Bounded Heuristic Search", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "While $A^*$ search is optimally efficient in terms of expanded nodes, its space complexity is exponential: $O(b^d)$. "
        "Every generated state must be preserved in either the Open or Closed list. For a problem with branching factor $b=10$ and depth $d=10$, "
        "$A^*$ generates over $10^{10}$ nodes, demanding over 100 Gigabytes of RAM and exhausting physical memory within minutes. "
        "Memory-bounded algorithms resolve this space bottleneck.", body_style
    ))

    story.append(make_callout(
        "<b>Core Memory-Bounded Algorithms:</b><br/>"
        "• <b>IDA* (Iterative Deepening A*):</b> Uses depth-first search bounded by an $f$-cost limit rather than depth. Requires only linear space $O(b \\cdot d)$.<br/>"
        "• <b>RBFS (Recursive Best-First Search):</b> Mimics best-first search in linear memory $O(b \\cdot d)$. Keeps track of the best alternative $f$-cost at each ancestor node.<br/>"
        "• <b>SMA* (Simplified Memory-Bounded A*):</b> Utilizes all allocated memory buffer $M$. When memory is full, it evicts the <i>shallowest, highest $f$-cost</i> leaf node and stores its backed-up value in its parent.",
        "MEMORY-BOUNDED PARADIGMS", "#b8860b", "#fdfcf0"
    ))
    story.append(Spacer(1, 8))

    story.extend(add_diagram("ida_star_contours.png", "IDA* Contour Search Iterations & f-Limit Thresholds", "PDF 5, Slide 4", max_h=190))
    story.extend(add_diagram("rbfs_search_tree.png", "RBFS Search Progression on Romania with Backed-Up Values", "PDF 5, Slide 8", max_h=190))

    story.append(Paragraph("SMA* Progression & Eviction Mechanics", h2_style))
    story.append(Paragraph(
        "SMA* operates by expanding the newest best leaf. When memory buffer $M$ is exhausted:<br/>"
        "1. It finds the shallowest node with the highest $f$-value (the worst leaf) and removes it from memory.<br/>"
        "2. It backs up the forgotten leaf's $f$-cost into its parent node.<br/>"
        "3. If all other alternative branches prove worse, the parent node can regenerate the forgotten child.<br/>"
        "• <b>Completeness:</b> Guaranteed if memory buffer $M \\ge d$ (shallowest goal depth fits in memory).<br/>"
        "• <b>Optimality:</b> Guaranteed if memory buffer $M \\ge d^*$ (optimal path fits in memory).", body_style
    ))

    story.extend(add_diagram("sma_star_stage1.png", "SMA* Stage 1: Filling Allocated Memory Buffer M", "PDF 5, Slide 11", max_h=180))
    story.extend(add_diagram("sma_star_stage2.png", "SMA* Stage 2: Evicting Worst Leaf & Backing Up Value", "PDF 5, Slide 13", max_h=180))
    story.extend(add_diagram("sma_star_stage3.png", "SMA* Stage 3: Regenerating Leaf Node from Parent Backup", "PDF 5, Slide 15", max_h=180))

    story.append(Paragraph("Memory-Bounded Complexity Matrix", h3_style))
    mem_table_data = [
        [Paragraph("<b>Algorithm</b>", table_header_style), Paragraph("<b>Time Complexity</b>", table_header_style), Paragraph("<b>Space Complexity</b>", table_header_style), Paragraph("<b>Completeness</b>", table_header_style), Paragraph("<b>Optimality</b>", table_header_style)],
        [Paragraph("<b>A* Search</b>", table_cell_bold), Paragraph("O(b^d)", table_cell_style), Paragraph("O(b^d) [Exponential]", table_cell_style), Paragraph("Yes", table_cell_style), Paragraph("Yes (admissible h)", table_cell_style)],
        [Paragraph("<b>IDA*</b>", table_cell_bold), Paragraph("O(b^d) [worse with fine costs]", table_cell_style), Paragraph("O(b · d) [Linear]", table_cell_style), Paragraph("Yes", table_cell_style), Paragraph("Yes", table_cell_style)],
        [Paragraph("<b>RBFS</b>", table_cell_bold), Paragraph("O(b^d) [can thrash]", table_cell_style), Paragraph("O(b · d) [Linear]", table_cell_style), Paragraph("Yes", table_cell_style), Paragraph("Yes", table_cell_style)],
        [Paragraph("<b>SMA*</b>", table_cell_bold), Paragraph("O(b^d)", table_cell_style), Paragraph("O(M) [Exact buffer cap]", table_cell_style), Paragraph("If M ≥ d", table_cell_style), Paragraph("If M ≥ d*", table_cell_style)]
    ]
    mem_t = Table(mem_table_data, colWidths=[90, 115, 110, 85, 95])
    mem_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dcdce8")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f9f9fd")]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(mem_t)

    story.append(PageBreak())

    # ==================== MODULE 5 ====================
    story.append(Paragraph("Module 5: Knowledge Representation & Production Systems", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "A Knowledge Representation (KR) system must satisfy 4 primary criteria: "
        "<b>Representational Adequacy</b> (capturing all domain concepts), "
        "<b>Inferential Adequacy</b> (manipulating structures to derive new facts), "
        "<b>Inferential Efficiency</b> (focusing reasoning in fruitful directions), and "
        "<b>Acquisitional Efficiency</b> (ease of integrating new knowledge).", body_style
    ))

    story.append(make_callout(
        "<b>Knowledge Schemes & Typology:</b><br/>"
        "• <b>Declarative ('Knowing That'):</b> Static facts, relationships, and axioms (e.g. Prolog facts, SQL tables).<br/>"
        "• <b>Procedural ('Knowing How'):</b> Step-by-step algorithms, control instructions, and rules of execution.<br/>"
        "• <b>Inheritable Knowledge:</b> Graphical structures (Semantic Nets & Frames) where properties propagate down <code>IsA</code> hierarchies.<br/>"
        "• <b>Production Systems:</b> Composed of <i>Working Memory</i> (facts), <i>Rule Base</i> (IF-THEN rules), and an <i>Inference Engine</i>.",
        "KNOWLEDGE REPRESENTATION SCHEMES", "#008080", "#eef9f9"
    ))
    story.append(Spacer(1, 6))

    story.extend(add_diagram("dikw_knowledge_model.png", "The DIKW Knowledge Model (Bellinger 1980)", "PDF KR, Slide 5", max_h=210))
    story.extend(add_diagram("semantic_net_inheritable.png", "Inheritable Semantic Network Hierarchy", "PDF KR, Slide 17", max_h=210))
    story.extend(add_diagram("production_rule_architecture.png", "Production System Architecture (Working Memory + Rules + Engine)", "PDF KR, Slide 71", max_h=210))

    story.append(Paragraph("Forward Chaining vs. Backward Chaining", h2_style))
    story.append(Paragraph(
        "• <b>Forward Chaining (Data-Driven):</b> Starts with known facts in Working Memory, checks rule conditions, fires matching rules, "
        "and asserts new facts into memory until a goal is proven. Uses <i>Conflict Resolution</i> strategies:<br/>"
        "  - <b>Refractory:</b> A rule cannot fire twice on the identical piece of data (prevents infinite loops).<br/>"
        "  - <b>Recency:</b> Prefers rules matching newly generated facts (time-tags).<br/>"
        "  - <b>Specificity:</b> Prefers rules having more detailed condition clauses.<br/>"
        "• <b>Backward Chaining (Goal-Driven):</b> Starts with a hypothesis (goal), finds rules concluding it, and recursively sets unproven premises as new sub-goals.", body_style
    ))

    story.extend(add_diagram("forward_vs_backward_chaining.png", "Forward vs. Backward Chaining Comparison Table", "PDF KR, Slide 77", max_h=210))
    story.extend(add_diagram("forward_backward_representation.png", "Facts ↔ Representation Mapping", "PDF KR, Slide 13", max_h=200))

    story.append(Paragraph("Logic Programming & Prolog Fundamentals", h2_style))
    story.append(Paragraph(
        "Based on Robert Kowalski's landmark formulation: <b>Algorithm = Logic + Control</b>.<br/>"
        "• <b>Facts (Unit Clauses):</b> <code>parent(tom, bob).</code>, <code>female(pam).</code> (end with period).<br/>"
        "• <b>Rules (Horn Clauses):</b> <code>grandparent(X, Z) :- parent(X, Y), parent(Y, Z).</code> ('Head is true IF Body is true').<br/>"
        "• <b>Queries:</b> <code>?- grandparent(tom, Who).</code> unifies variables (capitalized) using SLD resolution and depth-first backtracking.", body_style
    ))

    story.append(PageBreak())

    # ==================== MODULE 6 ====================
    story.append(Paragraph("Module 6: Logic, Rules of Inference & Proof Methods", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "Propositional logic studies declarative statements with boolean truth values. Compound statements are formed with connectives "
        "$\\neg, \\land, \\lor, \\to, \\leftrightarrow$. A <b>Tautology</b> is always true; a <b>Contradiction</b> is always false; a <b>Contingency</b> varies. "
        "Entailment $\\alpha \\models \\beta$ means in every model where $\\alpha$ is true, $\\beta$ is also true.", body_style
    ))

    story.append(Paragraph("The 8 Propositional Rules of Inference", h2_style))
    prop_rules_data = [
        [Paragraph("<b>Rule of Inference</b>", table_header_style), Paragraph("<b>Premises & Derivation</b>", table_header_style), Paragraph("<b>Formal Name & Plain English Meaning</b>", table_header_style)],
        [Paragraph("<b>Modus Ponens</b>", table_cell_bold), Paragraph("<code>p, p → q ⊢ q</code>", table_cell_style), Paragraph("Affirming antecedent: If p is true, and p implies q, then q must be true.", table_cell_style)],
        [Paragraph("<b>Modus Tollens</b>", table_cell_bold), Paragraph("<code>¬q, p → q ⊢ ¬p</code>", table_cell_style), Paragraph("Denying consequent: If p implies q, and q is false, then p must be false.", table_cell_style)],
        [Paragraph("<b>Hypothetical Syllogism</b>", table_cell_bold), Paragraph("<code>p → q, q → r ⊢ p → r</code>", table_cell_style), Paragraph("Transitivity: If p implies q, and q implies r, then p implies r.", table_cell_style)],
        [Paragraph("<b>Disjunctive Syllogism</b>", table_cell_bold), Paragraph("<code>p ∨ q, ¬p ⊢ q</code>", table_cell_style), Paragraph("Elimination: If p or q is true, and p is false, then q must be true.", table_cell_style)],
        [Paragraph("<b>Addition</b>", table_cell_bold), Paragraph("<code>p ⊢ p ∨ q</code>", table_cell_style), Paragraph("Disjunction introduction: If p is true, then p OR anything else is true.", table_cell_style)],
        [Paragraph("<b>Simplification</b>", table_cell_bold), Paragraph("<code>p ∧ q ⊢ p</code>", table_cell_style), Paragraph("Conjunction elimination: If both p and q are true, then p alone is true.", table_cell_style)],
        [Paragraph("<b>Conjunction</b>", table_cell_bold), Paragraph("<code>p, q ⊢ p ∧ q</code>", table_cell_style), Paragraph("Conjunction introduction: If p is true and q is true, both are true together.", table_cell_style)],
        [Paragraph("<b>Resolution</b>", table_cell_bold), Paragraph("<code>p ∨ q, ¬p ∨ r ⊢ q ∨ r</code>", table_cell_style), Paragraph("Resolvent derivation: Key automated theorem proving & Prolog rule.", table_cell_style)]
    ]
    prop_t = Table(prop_rules_data, colWidths=[105, 120, 270])
    prop_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dcdce8")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f9f9fd")]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(prop_t)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Quantifier Rules of Inference", h2_style))
    story.append(Paragraph(
        "• <b>Universal Instantiation (UI):</b> $\\forall x P(x) \\vdash P(c)$ for any arbitrary constant $c$.<br/>"
        "• <b>Universal Generalization (UG):</b> $P(c)$ for an arbitrary element $c \\vdash \\forall x P(x)$.<br/>"
        "• <b>Existential Instantiation (EI):</b> $\\exists x P(x) \\vdash P(c)$ for some newly introduced specific element $c$.<br/>"
        "• <b>Existential Generalization (EG):</b> $P(c)$ for a known witness $c \\vdash \\exists x P(x)$.<br/>"
        "• <b>Universal Modus Ponens:</b> $\\forall x (P(x) \\to Q(x)), P(a) \\vdash Q(a)$.", body_style
    ))

    story.append(Paragraph("The 8 Mathematical Proof Techniques", h2_style))
    proof_data = [
        [Paragraph("<b>Proof Method</b>", table_header_style), Paragraph("<b>Mechanism / Logical Blueprint</b>", table_header_style), Paragraph("<b>Standard Exam Application</b>", table_header_style)],
        [Paragraph("<b>1. Direct Proof</b>", table_cell_bold), Paragraph("Assume $p$ is true $\\to$ deduce $q$ via axioms and definitions.", table_cell_style), Paragraph("If $n$ is odd, $n^2$ is odd: $(2k+1)^2 = 4k^2+4k+1 = 2(2k^2+2k)+1$.", table_cell_style)],
        [Paragraph("<b>2. Contraposition</b>", table_cell_bold), Paragraph("To prove $p \\to q$, prove logically equivalent $\\neg q \\to \\neg p$.", table_cell_style), Paragraph("If $3n+2$ is odd, then $n$ is odd: assume $n=2k$ is even $\\implies 6k+2$ is even.", table_cell_style)],
        [Paragraph("<b>3. Contradiction</b>", table_cell_bold), Paragraph("Assume $\\neg p$ is true $\\to$ derive an impossible contradiction $F$.", table_cell_style), Paragraph("Proving $\\sqrt{2}$ is irrational, or that the set of prime numbers is infinite.", table_cell_style)],
        [Paragraph("<b>4. Proof by Cases</b>", table_cell_bold), Paragraph("Break domain into exhaustive cases: $(p_1 \\lor \\dots \\lor p_n) \\to q$.", table_cell_style), Paragraph("Proving $|xy| = |x||y|$ by evaluating positive, negative, and zero cases.", table_cell_style)],
        [Paragraph("<b>5. Constructive</b>", table_cell_bold), Paragraph("Find an explicit concrete witness $c$ satisfying $P(c)$.", table_cell_style), Paragraph("Taxicab number: $1729 = 10^3 + 9^3 = 12^3 + 1^3$.", table_cell_style)],
        [Paragraph("<b>6. Non-Constructive</b>", table_cell_bold), Paragraph("Prove existence of witness via contradiction without producing it.", table_cell_style), Paragraph("Proving irrational numbers $a, b$ exist such that $a^b$ is rational.", table_cell_style)],
        [Paragraph("<b>7. Counterexample</b>", table_cell_bold), Paragraph("Disprove a universal claim $\\forall x P(x)$ by finding one witness $c$ with $\\neg P(c)$.", table_cell_style), Paragraph("Refuting 'all primes are odd' by naming the even prime $2$.", table_cell_style)],
        [Paragraph("<b>8. Uniqueness Proof</b>", table_cell_bold), Paragraph("Prove existence $P(x)$, then assume $P(y) \\implies y = x$.", table_cell_style), Paragraph("Proving a linear equation $ax + b = 0$ ($a \\ne 0$) has exactly one root.", table_cell_style)]
    ]
    proof_t = Table(proof_data, colWidths=[105, 175, 215])
    proof_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_accent),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dcdce8")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f9f9fd")]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(proof_t)
    story.append(Spacer(1, 8))

    story.extend(add_diagram("logic_equivalences_table.png", "Official Table of Logical Equivalences Cheat Sheet", "PDF 3, Formula Sheet", max_h=210))
    story.extend(add_diagram("rules_of_inference_p1.png", "Official Rules of Inference Derivations (Page 1)", "PDF 2, Page 1", max_h=210))
    story.extend(add_diagram("rules_of_inference_p2.png", "Official Rules of Inference Derivations (Page 2)", "PDF 2, Page 2", max_h=210))

    story.append(PageBreak())

    # ==================== MODULE 7 ====================
    story.append(Paragraph("Module 7: Master AI Glossary (36 Key Definitions)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "A curated, alphabetical lexicon of all 36 critical exam definitions spanning all 8 syllabus topics:", body_style
    ))

    glossary_data_table = [
        [Paragraph("<b>Term</b>", table_header_style), Paragraph("<b>Category</b>", table_header_style), Paragraph("<b>Official Definition & Exam Takeaway</b>", table_header_style), Paragraph("<b>Mathematical Formula / Notation</b>", table_header_style)]
    ]

    glossary_items = [
        ("A* Search Algorithm", "Search", "Informed search evaluating f(n) = g(n) + h(n), balancing accumulated cost with heuristic estimate. Optimal if admissible/consistent.", "f(n) = g(n) + h(n)"),
        ("Admissibility", "Search", "A heuristic property meaning h(n) never overestimates the true cost to reach the goal: 0 ≤ h(n) ≤ h*(n). Guarantees tree A* optimality.", "0 ≤ h(n) ≤ h*(n)"),
        ("Agent Function", "Agents", "The abstract mathematical mapping f: P* → A from complete percept histories to external actions executed via actuators.", "f : P* → A"),
        ("AI Winter", "History", "Periods of severe funding freezes in AI (1974-1980, 1987-1993) caused by over-promising and combinatorial explosion bottlenecks.", "Over-promising → Funding freeze"),
        ("Artificial Intelligence", "Foundations", "Computational engineering and science devoted to constructing rational agents capable of perceiving, reasoning, and acting.", "AI = Cognitive Science + Agent Engineering"),
        ("Backward Chaining", "KR", "Goal-driven reasoning: starts from a query hypothesis, finds matching rules, and recursively verifies sub-goals (used in MYCIN and Prolog).", "Goal → Match Conclusions → Sub-goals"),
        ("Consistency", "Search", "Triangle inequality for heuristics: h(n) ≤ c(n,a,n') + h(n'). Guarantees graph A* optimality and monotonic f-cost progression.", "h(n) ≤ c(n,a,n') + h(n')"),
        ("Contradiction", "Logic", "A compound logical formula that evaluates to False under every possible truth assignment.", "P ∧ ¬P ≡ 0 (False)"),
        ("Dartmouth Workshop", "History", "1956 summer workshop organized by McCarthy, Minsky, Shannon, Rochester where 'Artificial Intelligence' was officially coined.", "Birth of AI discipline (1956)"),
        ("Declarative Knowledge", "KR", "Knowledge representing 'knowing that' — static assertions, facts, axioms, and relationships without execution control.", "Declarative = 'Knowing That'"),
        ("Deduction Theorem", "Logic", "Metalogical theorem establishing that premise P derives statement Q if and only if P → Q is a logical tautology.", "P ⊢ Q ⟺ ⊢ (P → Q)"),
        ("DIKW Pyramid", "Foundations", "Cognitive hierarchy: Data (raw symbols) → Information (context) → Knowledge (actionable rules) → Wisdom (evaluative principles).", "Data → Info → Knowledge → Wisdom"),
        ("Episodic Environment", "Agents", "An environment where the agent's experience is split into independent atomic episodes; current choices do not impact future episodes.", "Episode i independent of Episode i+1"),
        ("Forward Chaining", "KR", "Data-driven reasoning: starts with working memory facts, matches rule conditions, fires rules, and asserts conclusions until goal is found.", "Facts → Match Premises → Fire Rules"),
        ("Frames & Slots", "KR", "Minsky's data structure for stereotypical situations, comprising named Slots (attributes) filled with Fillers and default values.", "Frame = { Slot: Value, Demon }"),
        ("Goal-Based Agent", "Agents", "Agent architecture combining internal state with explicit goal representations, employing search and planning to reach goals.", "State + Goal Formulation → Action"),
        ("Greedy Best-First", "Search", "Heuristic search algorithm expanding the node with lowest heuristic value f(n) = h(n). Incomplete and non-optimal.", "f(n) = h(n)"),
        ("Heuristic Function", "Search", "An informed estimate of the cheapest path cost from node n to the nearest goal, derived from problem relaxations.", "h(n) ≈ h*(n) [True cost]"),
        ("IDA*", "Memory", "Iterative Deepening A*: adapts IDDFS by using f-cost cutoffs instead of depth. Uses linear space O(b·d).", "Space: O(b · d) | f-limit cutoff"),
        ("Kowalski's Equation", "KR", "Theoretical foundation of logic programming: an algorithm consists of a logic component and a control execution component.", "Algorithm = Logic + Control"),
        ("Learning Agent", "Agents", "Modular agent architecture split into 4 elements: Learning Element, Performance Element, Critic, and Problem Generator.", "Learning + Performance + Critic + Explorer"),
        ("Model-Based Agent", "Agents", "Reflex agent maintaining an internal state estimating unobserved aspects of the world to overcome partial observability.", "State + Percept + Model → New State"),
        ("Modus Ponens", "Logic", "Propositional inference rule: from premises p and p → q, deduce conclusion q.", "p, p → q ⊢ q"),
        ("Modus Tollens", "Logic", "Propositional inference rule: from premises ¬q and p → q, deduce conclusion ¬p.", "¬q, p → q ⊢ ¬p"),
        ("PEAS Framework", "Agents", "Task environment specification: Performance measure (P), Environment (E), Actuators (A), and Sensors (S).", "P = Perf, E = Env, A = Act, S = Sens"),
        ("Procedural Knowledge", "KR", "Knowledge representing 'knowing how' — step-by-step algorithms, instructions, and executable recipes.", "Procedural = 'Knowing How'"),
        ("Production System", "KR", "Knowledge architecture composed of Working Memory (facts), Rule Base (IF-THEN), and Inference Engine (match-resolve-act).", "Working Memory + Rules + Engine"),
        ("Rationality", "Foundations", "Selecting actions expected to maximize performance given percept sequence to date and built-in knowledge. Distinct from omniscience.", "Max E[U] given Percepts P*"),
        ("RBFS", "Memory", "Recursive Best-First Search: linear space O(b·d) search keeping track of the best alternative f-cost at each ancestor.", "Space: O(b · d) | Tracks alternative f"),
        ("Refractory Strategy", "KR", "Conflict resolution rule: prevents the same rule from firing twice on the identical piece of working memory data.", "Prevents infinite loops"),
        ("Resolution Principle", "Logic", "Automated theorem proving rule: from clauses (p ∨ q) and (¬p ∨ r), derive the resolvent (q ∨ r).", "(p ∨ q) ∧ (¬p ∨ r) ⊢ (q ∨ r)"),
        ("Semantic Network", "KR", "Knowledge graph where nodes represent concepts and directed edges represent relationships, primarily IsA and Instance links.", "Nodes = Concepts | Edges = IsA / Instance"),
        ("Simple Reflex Agent", "Agents", "Agent selecting actions based exclusively on current percept using condition-action rules. Has no memory of past percepts.", "condition → action"),
        ("SMA*", "Memory", "Simplified Memory-Bounded A*: uses all memory buffer M. Drops worst leaf and backs up its value to parent when full.", "Space: O(M) | Complete if M ≥ d"),
        ("Tautology", "Logic", "A compound logical formula that evaluates to True under all possible truth interpretations.", "P ∨ ¬P ≡ 1 (True)"),
        ("Thrashing", "Memory", "Phenomenon in RBFS where the algorithm repeatedly switches between competing branches, recalculating forgotten subtrees.", "Frequent backtracking + re-exploration")
    ]

    for term, cat, defn, form in glossary_items:
        glossary_data_table.append([
            Paragraph(f"<b>{term}</b>", table_cell_bold),
            Paragraph(cat, table_cell_style),
            Paragraph(defn, table_cell_style),
            Paragraph(form, formula_style)
        ])

    glossary_t = Table(glossary_data_table, colWidths=[105, 65, 215, 110])
    glossary_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dcdce8")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f9f9fd")]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(glossary_t)

    story.append(PageBreak())

    # ==================== MODULE 8 ====================
    story.append(Paragraph("Module 8: 20-Question Comprehensive Exam Simulation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "A rigorous self-assessment test covering all syllabus topics with marked answer keys and detailed pedagogical rationales:", body_style
    ))

    quiz_questions = [
        ("1. Who coined the term 'Artificial Intelligence' at the 1956 Dartmouth Workshop?",
         ["A. Alan Turing", "B. John McCarthy (CORRECT)", "C. Marvin Minsky", "D. Claude Shannon"],
         "John McCarthy coined 'Artificial Intelligence' in his 1955 proposal for the 1956 Dartmouth College workshop."),
        ("2. In the PEAS framework, what does the acronym stand for?",
         ["A. Program, Environment, Algorithm, Sensors", "B. Performance, Environment, Actuators, Sensors (CORRECT)", "C. Process, Environment, Architecture, Storage", "D. Percept, Execution, Action, Strategy"],
         "PEAS = Performance measure, Environment, Actuators, Sensors."),
        ("3. What is the evaluation function for the A* search algorithm?",
         ["A. f(n) = h(n)", "B. f(n) = g(n)", "C. f(n) = g(n) + h(n) (CORRECT)", "D. f(n) = g(n) × h(n)"],
         "A* combines the exact path cost from start g(n) with the heuristic estimate to the goal h(n)."),
        ("4. An admissible heuristic h(n) is formally defined as one that...",
         ["A. Always overestimates true cost", "B. Never overestimates true cost: 0 ≤ h(n) ≤ h*(n) (CORRECT)", "C. Equals 0 for all nodes", "D. Is strictly greater than true cost"],
         "Admissibility means h(n) is an optimistic estimate that never overestimates the true cost h*(n) to the goal."),
        ("5. Which inference rule derives 'q' from premises 'p' and 'p → q'?",
         ["A. Modus Tollens", "B. Modus Ponens (CORRECT)", "C. Resolution", "D. Hypothetical Syllogism"],
         "Modus Ponens (affirming the antecedent): If p is true and p implies q, then q must be true."),
        ("6. Which search algorithm utilizes strictly linear space O(b·d)?",
         ["A. Standard A* Search", "B. Iterative Deepening A* (IDA*) (CORRECT)", "C. Breadth-First Search (BFS)", "D. SMA* with unbounded memory"],
         "IDA* runs a sequence of depth-first searches bounded by f-cost cutoffs, requiring only linear space O(b·d)."),
        ("7. In a fully observable environment, an intelligent agent...",
         ["A. Requires internal memory to infer unseen objects", "B. Has complete state access at all times through sensors (CORRECT)", "C. Must continuously learn rules", "D. Has noise in every step"],
         "Full observability gives complete, noiseless access to the current state, so no internal world model is required."),
        ("8. Forward chaining is characterized as being...",
         ["A. Data-driven, reasoning forward from facts to conclusions (CORRECT)", "B. Goal-driven, reasoning backward from hypothesis", "C. Exclusively probabilistic", "D. Unable to resolve conflicts"],
         "Forward chaining starts with known facts in working memory and triggers rules forward to derive new facts."),
        ("9. According to De Morgan's Laws, what is the logical equivalence of ¬(p ∧ q)?",
         ["A. ¬p ∧ ¬q", "B. ¬p ∨ ¬q (CORRECT)", "C. p ∨ q", "D. ¬p → ¬q"],
         "¬(p ∧ q) ≡ ¬p ∨ ¬q — the negation flips the conjunction into a disjunction."),
        ("10. When memory is full in SMA*, which node does the algorithm drop?",
         ["A. The root node", "B. The deepest node", "C. The shallowest, highest f-cost (worst) leaf node (CORRECT)", "D. A randomly selected node"],
         "SMA* discards the shallowest, highest f-cost leaf node and backs up its value to the parent node."),
        ("11. In Prolog, how is a rule formally structured?",
         ["A. Head :- Body. (CORRECT)", "B. Body -> Head.", "C. IF Condition THEN Action.", "D. ?- Query."],
         "Prolog rules are Horn clauses written as 'Head :- Body.', meaning Head is true IF Body is true."),
        ("12. What is the contrapositive of the conditional statement (p → q)?",
         ["A. q → p", "B. ¬p → ¬q", "C. ¬q → ¬p (CORRECT)", "D. ¬p ∨ q"],
         "The contrapositive of (p → q) is (¬q → ¬p), and both are strictly logically equivalent."),
        ("13. Which environment dimension means current actions do not impact future decisions?",
         ["A. Deterministic", "B. Static", "C. Episodic (CORRECT)", "D. Discrete"],
         "In episodic environments, each interaction is independent; the agent's current action has no bearing on future episodes."),
        ("14. What does Consistency (Monotonicity) in heuristics require?",
         ["A. h(n) = 0 for all nodes", "B. h(n) ≤ c(n,a,n') + h(n') [Triangle inequality] (CORRECT)", "C. h(n) > h*(n)", "D. f(n) = g(n)"],
         "Consistency requires h(n) ≤ c(n,a,n') + h(n'), guaranteeing that f-values along any path never decrease."),
        ("15. What type of knowledge is described as 'knowing how' to execute procedures?",
         ["A. Declarative Knowledge", "B. Procedural Knowledge (CORRECT)", "C. Relational Knowledge", "D. Inferential Knowledge"],
         "Procedural knowledge ('knowing how') represents step-by-step algorithms, instructions, and executable rules."),
        ("16. Which conflict resolution strategy avoids firing the same rule twice on identical data?",
         ["A. Recency", "B. Specificity", "C. Refractory (CORRECT)", "D. Priority"],
         "Refractory ensures that a rule cannot fire more than once on the exact same data, preventing infinite loops."),
        ("17. Greedy Best-First Search prioritizes nodes using which evaluation function?",
         ["A. f(n) = g(n)", "B. f(n) = h(n) (CORRECT)", "C. f(n) = g(n) + h(n)", "D. f(n) = c(s,a,s')"],
         "Greedy Best-First search expands the node that looks closest to the goal based solely on the heuristic h(n)."),
        ("18. How many components comprise a Learning Agent architecture?",
         ["A. 2 components", "B. 3 components", "C. 4 components (Learning, Performance, Critic, Explorer) (CORRECT)", "D. 5 components"],
         "A Learning Agent consists of 4 parts: Learning Element, Performance Element, Critic, and Problem Generator."),
        ("19. The Resolution Refutation principle proves a statement S by...",
         ["A. Assuming S is true and verifying it", "B. Negating S and deriving a contradiction (empty clause □) (CORRECT)", "C. Converting S directly to DNF", "D. Using forward chaining only"],
         "Resolution refutation assumes ¬S and applies resolution until the empty clause □ (contradiction) is derived."),
        ("20. Robert Kowalski summarized logic programming with which famous equation?",
         ["A. AI = Architecture + Program", "B. Algorithm = Logic + Control (CORRECT)", "C. Search = Cost + Heuristic", "D. Knowledge = Information + Rules"],
         "Kowalski's famous formula states: Algorithm = Logic + Control.")
    ]

    for q_text, opts, explanation in quiz_questions:
        q_content = [
            Paragraph(f"<b>{q_text}</b>", h3_style),
            Spacer(1, 2)
        ]
        for opt in opts:
            is_correct = "(CORRECT)" in opt
            opt_clean = opt.replace(" (CORRECT)", "")
            if is_correct:
                q_content.append(Paragraph(f"<b><font color='#008080'>✓ {opt_clean}</font></b>", bullet_style))
            else:
                q_content.append(Paragraph(f"• {opt_clean}", bullet_style))
        q_content.append(Spacer(1, 2))
        q_content.append(Paragraph(f"<b>Rationale:</b> {explanation}", caption_style))
        
        q_box = Table([[q_content]], colWidths=[495])
        q_box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8f8fc")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#dcdce8")),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(q_box)
        story.append(Spacer(1, 6))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {filename}")

if __name__ == '__main__':
    build_pdf()
