"""
Generator script to render crisp, publication-grade AI Agent Architecture diagrams:
1. simple_reflex_agent.png
2. model_based_agent.png
3. goal_based_agent.png
4. utility_based_agent.png
5. learning_agent.png
6. agent_environment_loop.png

Uses explicit polygon arrowheads so all vector arrows render perfectly across all SVG/PDF engines.
"""

import os
import math
# pyrefly: ignore [missing-import]
import pymupdf

OUTPUT_DIR = r"c:\Users\Simanta\Documents\vs studio\ai-exam-prep\images\pdf_diagrams"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_FAMILY = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

def arrow(x1, y1, x2, y2, color="#1e293b", width=2.5, head_len=11, head_w=6.5):
    """Draw a straight line with a filled polygon arrowhead at (x2, y2)."""
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    if length == 0:
        return ""
    ux = dx / length
    uy = dy / length
    
    # Perpendicular unit vector
    px = -uy
    py = ux
    
    # Base of arrow triangle
    bx = x2 - ux * head_len
    by = y2 - uy * head_len
    
    # Left and right wings
    lx = bx + px * head_w
    ly = by + py * head_w
    rx = bx - px * head_w
    ry = by - py * head_w
    
    # Shorten the line slightly so it ends at the base of the triangle
    line_svg = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
    head_svg = f'<polygon points="{x2:.1f},{y2:.1f} {lx:.1f},{ly:.1f} {rx:.1f},{ry:.1f}" fill="{color}"/>'
    return f"{line_svg}\n{head_svg}"

def arrow_to_point(x1, y1, x2, y2, angle_deg, color="#1e293b", head_len=11, head_w=6.5):
    """Draw arrowhead pointing at angle_deg."""
    rad = math.radians(angle_deg)
    ux = math.cos(rad)
    uy = math.sin(rad)
    px = -uy
    py = ux
    bx = x2 - ux * head_len
    by = y2 - uy * head_len
    lx = bx + px * head_w
    ly = by + py * head_w
    rx = bx - px * head_w
    ry = by - py * head_w
    return f'<polygon points="{x2:.1f},{y2:.1f} {lx:.1f},{ly:.1f} {rx:.1f},{ry:.1f}" fill="{color}"/>'

def build_simple_reflex_svg():
    return f"""<svg width="900" height="540" viewBox="0 0 900 540" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">
  <!-- Title -->
  <text x="450" y="44" font-family="{FONT_FAMILY}" font-size="25" font-weight="800" fill="#0f172a" text-anchor="middle" letter-spacing="-0.5">Simple Reflex Agent</text>
  <text x="450" y="68" font-family="{FONT_FAMILY}" font-size="13" font-weight="500" fill="#64748b" text-anchor="middle">Selects actions based solely on the current percept, ignoring percept history</text>

  <!-- Environment Container -->
  <rect x="740" y="90" width="130" height="420" rx="30" fill="#e2e8f0" stroke="#94a3b8" stroke-width="2.5"/>
  <text x="805" y="305" font-family="{FONT_FAMILY}" font-size="22" font-weight="800" fill="#334155" text-anchor="middle" transform="rotate(90, 805, 305)" letter-spacing="3">ENVIRONMENT</text>

  <!-- Agent Outer Box -->
  <rect x="30" y="90" width="665" height="420" rx="26" fill="#f8fafc" stroke="#64748b" stroke-width="2.5"/>
  <text x="60" y="480" font-family="{FONT_FAMILY}" font-size="28" font-weight="850" fill="#1e293b">Agent</text>

  <!-- Sensors Card -->
  <rect x="470" y="115" width="130" height="40" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="141" font-family="{FONT_FAMILY}" font-size="15" font-weight="700" fill="#0f172a" text-anchor="middle">Sensors</text>

  <!-- Arrow: Environment -> Sensors -->
  {arrow(740, 135, 605, 135, color="#1e293b", width=2.5)}

  <!-- Arrow: Sensors -> Box 1 -->
  {arrow(535, 155, 535, 195, color="#1e293b", width=2.5)}

  <!-- Box 1: What world is like now -->
  <rect x="420" y="195" width="230" height="60" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="231" font-family="{FONT_FAMILY}" font-size="15" font-weight="650" fill="#0f172a" text-anchor="middle">What the world is like now</text>

  <!-- Arrow: Box 1 -> Box 2 -->
  {arrow(535, 255, 535, 315, color="#1e293b", width=2.5)}

  <!-- Box 2: What action I should do now -->
  <rect x="420" y="315" width="230" height="60" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="351" font-family="{FONT_FAMILY}" font-size="15" font-weight="650" fill="#0f172a" text-anchor="middle">What action I should do now</text>

  <!-- Pill: Condition-action rules -->
  <rect x="80" y="320" width="230" height="50" rx="25" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <text x="195" y="351" font-family="{FONT_FAMILY}" font-size="14" font-weight="650" fill="#1e293b" text-anchor="middle">Condition–action rules</text>
  
  <!-- Arrow: Condition-action rules -> Box 2 -->
  {arrow(310, 345, 415, 345, color="#1e293b", width=2.5)}

  <!-- Actuators Card -->
  <rect x="470" y="415" width="130" height="40" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="441" font-family="{FONT_FAMILY}" font-size="15" font-weight="700" fill="#0f172a" text-anchor="middle">Actuators</text>

  <!-- Arrow: Box 2 -> Actuators -->
  {arrow(535, 375, 535, 410, color="#1e293b", width=2.5)}

  <!-- Arrow: Actuators -> Environment -->
  {arrow(605, 435, 735, 435, color="#1e293b", width=2.5)}
</svg>"""

def build_model_based_svg():
    return f"""<svg width="900" height="570" viewBox="0 0 900 570" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">
  <!-- Title -->
  <text x="450" y="44" font-family="{FONT_FAMILY}" font-size="25" font-weight="800" fill="#0f172a" text-anchor="middle" letter-spacing="-0.5">Model-Based Reflex Agent</text>
  <text x="450" y="68" font-family="{FONT_FAMILY}" font-size="13" font-weight="500" fill="#64748b" text-anchor="middle">Maintains internal state to track unperceived aspects of the current world</text>

  <!-- Environment Container -->
  <rect x="740" y="90" width="130" height="450" rx="30" fill="#e2e8f0" stroke="#94a3b8" stroke-width="2.5"/>
  <text x="805" y="320" font-family="{FONT_FAMILY}" font-size="22" font-weight="800" fill="#334155" text-anchor="middle" transform="rotate(90, 805, 320)" letter-spacing="3">ENVIRONMENT</text>

  <!-- Agent Outer Box -->
  <rect x="30" y="90" width="665" height="450" rx="26" fill="#f8fafc" stroke="#64748b" stroke-width="2.5"/>
  <text x="60" y="510" font-family="{FONT_FAMILY}" font-size="28" font-weight="850" fill="#1e293b">Agent</text>

  <!-- Sensors Card -->
  <rect x="470" y="110" width="130" height="38" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="135" font-family="{FONT_FAMILY}" font-size="15" font-weight="700" fill="#0f172a" text-anchor="middle">Sensors</text>

  <!-- Arrow: Environment -> Sensors -->
  {arrow(740, 129, 605, 129, color="#1e293b", width=2.5)}

  <!-- Arrow: Sensors -> Box 1 -->
  {arrow(535, 148, 535, 185, color="#1e293b", width=2.5)}

  <!-- Box 1: What world is like now -->
  <rect x="420" y="185" width="230" height="56" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="219" font-family="{FONT_FAMILY}" font-size="15" font-weight="650" fill="#0f172a" text-anchor="middle">What the world is like now</text>

  <!-- Feedback curve from Box 1 back to State -->
  <path d="M 450 185 C 410 120, 270 100, 220 125" fill="none" stroke="#1e293b" stroke-width="2" stroke-dasharray="5,4"/>
  {arrow_to_point(0, 0, 220, 125, 200, color="#1e293b")}

  <!-- Pills on Left -->
  <!-- Pill 1: State -->
  <rect x="90" y="125" width="130" height="40" rx="20" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <text x="155" y="150" font-family="{FONT_FAMILY}" font-size="14" font-weight="650" fill="#1e293b" text-anchor="middle">State</text>
  {arrow(220, 148, 415, 200, color="#1e293b", width=2)}

  <!-- Pill 2: How world evolves -->
  <rect x="60" y="185" width="220" height="40" rx="20" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <text x="170" y="210" font-family="{FONT_FAMILY}" font-size="13.5" font-weight="650" fill="#1e293b" text-anchor="middle">How the world evolves</text>
  {arrow(280, 205, 415, 212, color="#1e293b", width=2)}

  <!-- Pill 3: What my actions do -->
  <rect x="75" y="245" width="190" height="40" rx="20" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <text x="170" y="270" font-family="{FONT_FAMILY}" font-size="13.5" font-weight="650" fill="#1e293b" text-anchor="middle">What my actions do</text>
  {arrow(265, 260, 415, 225, color="#1e293b", width=2)}

  <!-- Box 2: What action I should do now -->
  <rect x="420" y="325" width="230" height="56" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="359" font-family="{FONT_FAMILY}" font-size="15" font-weight="650" fill="#0f172a" text-anchor="middle">What action I should do now</text>

  <!-- Arrow: Box 1 -> Box 2 -->
  {arrow(535, 241, 535, 320, color="#1e293b", width=2.5)}

  <!-- Pill 4: Condition-action rules -->
  <rect x="65" y="333" width="230" height="42" rx="21" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <text x="180" y="360" font-family="{FONT_FAMILY}" font-size="14" font-weight="650" fill="#1e293b" text-anchor="middle">Condition–action rules</text>
  {arrow(295, 354, 415, 354, color="#1e293b", width=2.5)}

  <!-- Actuators Card -->
  <rect x="470" y="430" width="130" height="38" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="455" font-family="{FONT_FAMILY}" font-size="15" font-weight="700" fill="#0f172a" text-anchor="middle">Actuators</text>

  <!-- Arrow: Box 2 -> Actuators -->
  {arrow(535, 381, 535, 425, color="#1e293b", width=2.5)}

  <!-- Arrow: Actuators -> Environment -->
  {arrow(605, 449, 735, 449, color="#1e293b", width=2.5)}
</svg>"""

def build_goal_based_svg():
    return f"""<svg width="900" height="630" viewBox="0 0 900 630" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">
  <!-- Title -->
  <text x="450" y="44" font-family="{FONT_FAMILY}" font-size="25" font-weight="800" fill="#0f172a" text-anchor="middle" letter-spacing="-0.5">Goal-Based Agent</text>
  <text x="450" y="68" font-family="{FONT_FAMILY}" font-size="13" font-weight="500" fill="#64748b" text-anchor="middle">Combines state knowledge with explicit goal descriptions to plan action sequences</text>

  <!-- Environment Container -->
  <rect x="740" y="90" width="130" height="510" rx="30" fill="#e2e8f0" stroke="#94a3b8" stroke-width="2.5"/>
  <text x="805" y="345" font-family="{FONT_FAMILY}" font-size="22" font-weight="800" fill="#334155" text-anchor="middle" transform="rotate(90, 805, 345)" letter-spacing="3">ENVIRONMENT</text>

  <!-- Agent Outer Box -->
  <rect x="30" y="90" width="665" height="510" rx="26" fill="#f8fafc" stroke="#64748b" stroke-width="2.5"/>
  <text x="60" y="565" font-family="{FONT_FAMILY}" font-size="28" font-weight="850" fill="#1e293b">Agent</text>

  <!-- Sensors Card -->
  <rect x="470" y="110" width="130" height="38" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="135" font-family="{FONT_FAMILY}" font-size="15" font-weight="700" fill="#0f172a" text-anchor="middle">Sensors</text>

  <!-- Arrow: Environment -> Sensors -->
  {arrow(740, 129, 605, 129, color="#1e293b", width=2.5)}

  <!-- Arrow: Sensors -> Box 1 -->
  {arrow(535, 148, 535, 178, color="#1e293b", width=2.5)}

  <!-- Box 1: What world is like now -->
  <rect x="420" y="178" width="230" height="54" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="211" font-family="{FONT_FAMILY}" font-size="15" font-weight="650" fill="#0f172a" text-anchor="middle">What the world is like now</text>

  <!-- Feedback curve to State -->
  <path d="M 450 178 C 410 115, 270 95, 215 115" fill="none" stroke="#1e293b" stroke-width="2" stroke-dasharray="5,4"/>
  {arrow_to_point(0, 0, 215, 115, 200, color="#1e293b")}

  <!-- Pills on Left -->
  <!-- Pill 1: State -->
  <rect x="95" y="115" width="120" height="38" rx="19" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <text x="155" y="139" font-family="{FONT_FAMILY}" font-size="13.5" font-weight="650" fill="#1e293b" text-anchor="middle">State</text>
  {arrow(215, 134, 415, 192, color="#1e293b", width=2)}

  <!-- Pill 2: How world evolves -->
  <rect x="60" y="170" width="210" height="38" rx="19" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <text x="165" y="194" font-family="{FONT_FAMILY}" font-size="13" font-weight="650" fill="#1e293b" text-anchor="middle">How the world evolves</text>
  {arrow(270, 185, 415, 200, color="#1e293b", width=2)}
  {arrow(270, 195, 415, 290, color="#1e293b", width=2)}

  <!-- Pill 3: What my actions do -->
  <rect x="70" y="225" width="190" height="38" rx="19" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <text x="165" y="249" font-family="{FONT_FAMILY}" font-size="13" font-weight="650" fill="#1e293b" text-anchor="middle">What my actions do</text>
  {arrow(260, 235, 415, 212, color="#1e293b", width=2)}
  {arrow(260, 250, 415, 305, color="#1e293b", width=2)}

  <!-- Box 2: What it will be like if I do action A -->
  <rect x="420" y="275" width="230" height="54" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="299" font-family="{FONT_FAMILY}" font-size="13.5" font-weight="650" fill="#0f172a" text-anchor="middle">What it will be like</text>
  <text x="535" y="318" font-family="{FONT_FAMILY}" font-size="13.5" font-weight="650" fill="#0f172a" text-anchor="middle">if I do action A</text>

  <!-- Arrow: Box 1 -> Box 2 -->
  {arrow(535, 232, 535, 270, color="#1e293b", width=2.5)}

  <!-- Box 3: What action I should do now -->
  <rect x="420" y="390" width="230" height="54" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="423" font-family="{FONT_FAMILY}" font-size="15" font-weight="650" fill="#0f172a" text-anchor="middle">What action I should do now</text>

  <!-- Arrow: Box 2 -> Box 3 -->
  {arrow(535, 329, 535, 385, color="#1e293b", width=2.5)}

  <!-- Pill 4: Goals -->
  <rect x="105" y="396" width="140" height="42" rx="21" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <text x="175" y="422" font-family="{FONT_FAMILY}" font-size="14" font-weight="650" fill="#1e293b" text-anchor="middle">Goals</text>
  {arrow(245, 417, 415, 417, color="#1e293b", width=2.5)}

  <!-- Actuators Card -->
  <rect x="470" y="495" width="130" height="38" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="520" font-family="{FONT_FAMILY}" font-size="15" font-weight="700" fill="#0f172a" text-anchor="middle">Actuators</text>

  <!-- Arrow: Box 3 -> Actuators -->
  {arrow(535, 444, 535, 490, color="#1e293b", width=2.5)}

  <!-- Arrow: Actuators -> Environment -->
  {arrow(605, 514, 735, 514, color="#1e293b", width=2.5)}
</svg>"""

def build_utility_based_svg():
    return f"""<svg width="900" height="690" viewBox="0 0 900 690" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">
  <!-- Title -->
  <text x="450" y="44" font-family="{FONT_FAMILY}" font-size="25" font-weight="800" fill="#0f172a" text-anchor="middle" letter-spacing="-0.5">Utility-Based Agent</text>
  <text x="450" y="68" font-family="{FONT_FAMILY}" font-size="13" font-weight="500" fill="#64748b" text-anchor="middle">Evaluates states using a real-valued utility function to balance conflicting goals</text>

  <!-- Environment Container -->
  <rect x="740" y="90" width="130" height="570" rx="30" fill="#e2e8f0" stroke="#94a3b8" stroke-width="2.5"/>
  <text x="805" y="375" font-family="{FONT_FAMILY}" font-size="22" font-weight="800" fill="#334155" text-anchor="middle" transform="rotate(90, 805, 375)" letter-spacing="3">ENVIRONMENT</text>

  <!-- Agent Outer Box -->
  <rect x="30" y="90" width="665" height="570" rx="26" fill="#f8fafc" stroke="#64748b" stroke-width="2.5"/>
  <text x="60" y="625" font-family="{FONT_FAMILY}" font-size="28" font-weight="850" fill="#1e293b">Agent</text>

  <!-- Sensors Card -->
  <rect x="470" y="110" width="130" height="38" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="135" font-family="{FONT_FAMILY}" font-size="15" font-weight="700" fill="#0f172a" text-anchor="middle">Sensors</text>

  <!-- Arrow: Environment -> Sensors -->
  {arrow(740, 129, 605, 129, color="#1e293b", width=2.5)}

  <!-- Arrow: Sensors -> Box 1 -->
  {arrow(535, 148, 535, 178, color="#1e293b", width=2.5)}

  <!-- Box 1: What world is like now -->
  <rect x="420" y="178" width="230" height="50" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="209" font-family="{FONT_FAMILY}" font-size="14.5" font-weight="650" fill="#0f172a" text-anchor="middle">What the world is like now</text>

  <!-- Feedback curve to State -->
  <path d="M 450 178 C 410 115, 270 95, 215 115" fill="none" stroke="#1e293b" stroke-width="2" stroke-dasharray="5,4"/>
  {arrow_to_point(0, 0, 215, 115, 200, color="#1e293b")}

  <!-- Pills on Left -->
  <!-- Pill 1: State -->
  <rect x="95" y="115" width="120" height="38" rx="19" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <text x="155" y="139" font-family="{FONT_FAMILY}" font-size="13.5" font-weight="650" fill="#1e293b" text-anchor="middle">State</text>
  {arrow(215, 134, 415, 192, color="#1e293b", width=2)}

  <!-- Pill 2: How world evolves -->
  <rect x="60" y="170" width="210" height="38" rx="19" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <text x="165" y="194" font-family="{FONT_FAMILY}" font-size="13" font-weight="650" fill="#1e293b" text-anchor="middle">How the world evolves</text>
  {arrow(270, 185, 415, 200, color="#1e293b", width=2)}
  {arrow(270, 195, 415, 280, color="#1e293b", width=2)}

  <!-- Pill 3: What my actions do -->
  <rect x="70" y="225" width="190" height="38" rx="19" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <text x="165" y="249" font-family="{FONT_FAMILY}" font-size="13" font-weight="650" fill="#1e293b" text-anchor="middle">What my actions do</text>
  {arrow(260, 235, 415, 212, color="#1e293b", width=2)}
  {arrow(260, 250, 415, 295, color="#1e293b", width=2)}

  <!-- Box 2: What it will be like if I do action A -->
  <rect x="420" y="265" width="230" height="52" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="288" font-family="{FONT_FAMILY}" font-size="13.5" font-weight="650" fill="#0f172a" text-anchor="middle">What it will be like</text>
  <text x="535" y="306" font-family="{FONT_FAMILY}" font-size="13.5" font-weight="650" fill="#0f172a" text-anchor="middle">if I do action A</text>
  {arrow(535, 228, 535, 260, color="#1e293b", width=2.5)}

  <!-- Box 3: How happy I will be in such a state -->
  <rect x="420" y="355" width="230" height="52" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="378" font-family="{FONT_FAMILY}" font-size="13.5" font-weight="650" fill="#0f172a" text-anchor="middle">How happy I will be</text>
  <text x="535" y="396" font-family="{FONT_FAMILY}" font-size="13.5" font-weight="650" fill="#0f172a" text-anchor="middle">in such a state</text>
  {arrow(535, 317, 535, 350, color="#1e293b", width=2.5)}

  <!-- Pill 4: Utility -->
  <rect x="100" y="360" width="140" height="42" rx="21" fill="#f1f5f9" stroke="#334155" stroke-width="2"/>
  <text x="170" y="386" font-family="{FONT_FAMILY}" font-size="14" font-weight="650" fill="#1e293b" text-anchor="middle">Utility</text>
  {arrow(240, 381, 415, 381, color="#1e293b", width=2.5)}

  <!-- Box 4: What action I should do now -->
  <rect x="420" y="445" width="230" height="52" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="477" font-family="{FONT_FAMILY}" font-size="14.5" font-weight="650" fill="#0f172a" text-anchor="middle">What action I should do now</text>
  {arrow(535, 407, 535, 440, color="#1e293b", width=2.5)}

  <!-- Actuators Card -->
  <rect x="470" y="550" width="130" height="38" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="535" y="575" font-family="{FONT_FAMILY}" font-size="15" font-weight="700" fill="#0f172a" text-anchor="middle">Actuators</text>

  <!-- Arrow: Box 4 -> Actuators -->
  {arrow(535, 497, 535, 545, color="#1e293b", width=2.5)}

  <!-- Arrow: Actuators -> Environment -->
  {arrow(605, 569, 735, 569, color="#1e293b", width=2.5)}
</svg>"""

def build_learning_agent_svg():
    return f"""<svg width="980" height="680" viewBox="0 0 980 680" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">
  <!-- Title -->
  <text x="490" y="44" font-family="{FONT_FAMILY}" font-size="26" font-weight="800" fill="#0f172a" text-anchor="middle" letter-spacing="-0.5">Learning Agent Architecture</text>
  <text x="490" y="68" font-family="{FONT_FAMILY}" font-size="13" font-weight="500" fill="#64748b" text-anchor="middle">Decouples learning mechanisms from the performance execution element (Russell &amp; Norvig)</text>

  <!-- Environment Container -->
  <rect x="805" y="88" width="140" height="555" rx="32" fill="#e2e8f0" stroke="#94a3b8" stroke-width="2.5"/>
  <text x="875" y="365" font-family="{FONT_FAMILY}" font-size="22" font-weight="800" fill="#334155" text-anchor="middle" transform="rotate(90, 875, 365)" letter-spacing="3">ENVIRONMENT</text>

  <!-- Agent Outer Box -->
  <rect x="35" y="88" width="730" height="555" rx="28" fill="#f8fafc" stroke="#64748b" stroke-width="2.5"/>
  <text x="65" y="615" font-family="{FONT_FAMILY}" font-size="28" font-weight="850" fill="#1e293b">Agent</text>

  <!-- Performance Standard (Top external input into Critic) -->
  <rect x="155" y="96" width="190" height="32" rx="8" fill="#fee2e2" stroke="#ef4444" stroke-width="1.8"/>
  <text x="250" y="117" font-family="{FONT_FAMILY}" font-size="12.5" font-weight="750" fill="#b91c1c" text-anchor="middle">Performance standard</text>
  {arrow(250, 128, 250, 155, color="#ef4444", width=2.5)}

  <!-- Sensors Card (aligned with Critic center y=179) -->
  <rect x="545" y="158" width="135" height="42" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="612" y="184" font-family="{FONT_FAMILY}" font-size="15" font-weight="700" fill="#0f172a" text-anchor="middle">Sensors</text>

  <!-- Arrow: Environment -> Sensors -->
  {arrow(805, 179, 685, 179, color="#1e293b", width=2.5)}

  <!-- Arrow: Sensors -> Critic -->
  {arrow(545, 179, 360, 179, color="#1e293b", width=2.5)}

  <!-- Branch from Sensors to Performance Element -->
  {arrow(612, 202, 612, 280, color="#1e293b", width=2.5)}

  <!-- 1. CRITIC BOX -->
  <rect x="145" y="155" width="210" height="48" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="250" y="185" font-family="{FONT_FAMILY}" font-size="16" font-weight="750" fill="#0f172a" text-anchor="middle">Critic</text>

  <!-- Arrow Critic -> Learning Element (Feedback) -->
  {arrow(250, 203, 250, 285, color="#7c3aed", width=2.5)}
  <rect x="150" y="232" width="90" height="24" rx="5" fill="#ede9fe" stroke="#c4b5fd" stroke-width="1"/>
  <text x="195" y="248" font-family="{FONT_FAMILY}" font-size="12.5" font-weight="750" fill="#6d28d9" text-anchor="middle">feedback</text>

  <!-- 2. LEARNING ELEMENT BOX with explanatory role tag -->
  <rect x="135" y="290" width="230" height="78" rx="10" fill="#ffffff" stroke="#6d28d9" stroke-width="2.5"/>
  <text x="250" y="322" font-family="{FONT_FAMILY}" font-size="16" font-weight="800" fill="#4c1d95" text-anchor="middle">Learning element</text>
  <!-- Role badge -->
  <rect x="145" y="334" width="210" height="22" rx="11" fill="#f5f3ff" stroke="#ddd6fe" stroke-width="1"/>
  <text x="250" y="349" font-family="{FONT_FAMILY}" font-size="10.5" font-weight="700" fill="#6d28d9" text-anchor="middle">★ Responsible for making improvements</text>

  <!-- 3. PERFORMANCE ELEMENT BOX with explanatory role tag -->
  <rect x="495" y="285" width="230" height="78" rx="10" fill="#ffffff" stroke="#0284c7" stroke-width="2.5"/>
  <text x="610" y="317" font-family="{FONT_FAMILY}" font-size="16" font-weight="800" fill="#0369a1" text-anchor="middle">Performance element</text>
  <!-- Role badge -->
  <rect x="505" y="329" width="210" height="22" rx="11" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1"/>
  <text x="610" y="344" font-family="{FONT_FAMILY}" font-size="10.5" font-weight="700" fill="#0284c7" text-anchor="middle">★ Selects external actions</text>

  <!-- Interaction between Learning Element and Performance Element -->
  <!-- changes: LE -> PE -->
  {arrow(365, 308, 490, 308, color="#7c3aed", width=2.5)}
  <rect x="395" y="290" width="70" height="22" rx="4" fill="#ede9fe" stroke="#c4b5fd" stroke-width="1"/>
  <text x="430" y="305" font-family="{FONT_FAMILY}" font-size="12" font-weight="750" fill="#6d28d9" text-anchor="middle">changes</text>

  <!-- knowledge: PE -> LE -->
  {arrow(495, 348, 370, 348, color="#0284c7", width=2.5)}
  <rect x="390" y="352" width="80" height="22" rx="4" fill="#e0f2fe" stroke="#bae6fd" stroke-width="1"/>
  <text x="430" y="367" font-family="{FONT_FAMILY}" font-size="12" font-weight="750" fill="#0369a1" text-anchor="middle">knowledge</text>

  <!-- 4. PROBLEM GENERATOR BOX with explanatory role tag -->
  <rect x="135" y="450" width="230" height="78" rx="10" fill="#ffffff" stroke="#059669" stroke-width="2.5"/>
  <text x="250" y="482" font-family="{FONT_FAMILY}" font-size="16" font-weight="800" fill="#065f46" text-anchor="middle">Problem generator</text>
  <!-- Role badge -->
  <rect x="145" y="494" width="210" height="22" rx="11" fill="#ecfdf5" stroke="#a7f3d0" stroke-width="1"/>
  <text x="250" y="509" font-family="{FONT_FAMILY}" font-size="10.5" font-weight="700" fill="#059669" text-anchor="middle">★ Suggests exploratory experiences</text>

  <!-- Arrow Learning element -> Problem generator (learning goals) -->
  {arrow(250, 368, 250, 445, color="#7c3aed", width=2.5)}
  <rect x="195" y="395" width="105" height="24" rx="4" fill="#ede9fe" stroke="#c4b5fd" stroke-width="1"/>
  <text x="247" y="411" font-family="{FONT_FAMILY}" font-size="12" font-weight="750" fill="#6d28d9" text-anchor="middle">learning goals</text>

  <!-- Arrow Problem generator -> Performance element (experiments) -->
  {arrow(365, 485, 555, 370, color="#059669", width=2.5)}
  <rect x="420" y="420" width="95" height="24" rx="4" fill="#d1fae5" stroke="#a7f3d0" stroke-width="1"/>
  <text x="467" y="436" font-family="{FONT_FAMILY}" font-size="12.5" font-weight="750" fill="#047857" text-anchor="middle">experiments</text>

  <!-- Effectors / Actuators Card -->
  <rect x="520" y="450" width="180" height="40" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="610" y="475" font-family="{FONT_FAMILY}" font-size="15" font-weight="700" fill="#0f172a" text-anchor="middle">Effectors / Actuators</text>

  <!-- Arrow: Performance element -> Effectors -->
  {arrow(610, 363, 610, 445, color="#1e293b", width=2.5)}

  <!-- Arrow: Effectors -> Environment -->
  {arrow(700, 470, 800, 470, color="#1e293b", width=2.5)}
</svg>"""

def build_agent_environment_loop_svg():
    return f"""<svg width="860" height="520" viewBox="0 0 860 520" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">
  <!-- Title -->
  <text x="430" y="42" font-family="{FONT_FAMILY}" font-size="24" font-weight="800" fill="#0f172a" text-anchor="middle" letter-spacing="-0.5">Intelligent Agent &amp; Environment Interaction Loop</text>
  <text x="430" y="65" font-family="{FONT_FAMILY}" font-size="13" font-weight="500" fill="#64748b" text-anchor="middle">The fundamental cyclic process: Sensing → Processing (f: P* → A) → Actuating</text>

  <!-- AGENT BOX (Top) -->
  <rect x="90" y="90" width="680" height="175" rx="20" fill="#f8fafc" stroke="#4f46e5" stroke-width="2.5"/>
  <text x="130" y="130" font-family="{FONT_FAMILY}" font-size="22" font-weight="800" fill="#3730a3">AGENT</text>

  <!-- Sensors inside Agent -->
  <rect x="130" y="155" width="135" height="50" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="197" y="186" font-family="{FONT_FAMILY}" font-size="15" font-weight="700" fill="#0f172a" text-anchor="middle">Sensors</text>

  <!-- Agent Program / Internal Architecture -->
  <rect x="330" y="145" width="200" height="70" rx="10" fill="#eef2ff" stroke="#6366f1" stroke-width="2"/>
  <text x="430" y="173" font-family="{FONT_FAMILY}" font-size="14" font-weight="750" fill="#312e81" text-anchor="middle">Agent Program</text>
  <text x="430" y="195" font-family="{FONT_FAMILY}" font-size="12" font-weight="600" fill="#4338ca" text-anchor="middle">Function: f : P* → A</text>

  <!-- Actuators inside Agent -->
  <rect x="595" y="155" width="135" height="50" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <text x="662" y="186" font-family="{FONT_FAMILY}" font-size="15" font-weight="700" fill="#0f172a" text-anchor="middle">Actuators</text>

  <!-- Internal arrows inside Agent -->
  {arrow(265, 180, 325, 180, color="#1e293b", width=2)}
  {arrow(530, 180, 590, 180, color="#1e293b", width=2)}

  <!-- ENVIRONMENT BOX (Bottom) -->
  <rect x="90" y="345" width="680" height="120" rx="20" fill="#e2e8f0" stroke="#64748b" stroke-width="2.5"/>
  <text x="430" y="410" font-family="{FONT_FAMILY}" font-size="22" font-weight="800" fill="#1e293b" text-anchor="middle" letter-spacing="2">ENVIRONMENT</text>
  <text x="430" y="435" font-family="{FONT_FAMILY}" font-size="12.5" font-weight="600" fill="#475569" text-anchor="middle">(Physical world, software domain, gridworld, network)</text>

  <!-- Left Loop Arrow: Percepts (Environment -> Sensors) -->
  {arrow(197, 345, 197, 210, color="#0284c7", width=3, head_len=14, head_w=8)}
  <rect x="120" y="260" width="130" height="34" rx="6" fill="#e0f2fe" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="185" y="282" font-family="{FONT_FAMILY}" font-size="13.5" font-weight="750" fill="#0369a1" text-anchor="middle">Percepts (P)</text>

  <!-- Right Loop Arrow: Actions (Actuators -> Environment) -->
  {arrow(662, 205, 662, 340, color="#7c3aed", width=3, head_len=14, head_w=8)}
  <rect x="610" y="260" width="130" height="34" rx="6" fill="#ede9fe" stroke="#a78bfa" stroke-width="1.5"/>
  <text x="675" y="282" font-family="{FONT_FAMILY}" font-size="13.5" font-weight="750" fill="#6d28d9" text-anchor="middle">Actions (A)</text>
</svg>"""

DIAGRAMS = {
    "simple_reflex_agent.png": build_simple_reflex_svg,
    "model_based_agent.png": build_model_based_svg,
    "goal_based_agent.png": build_goal_based_svg,
    "utility_based_agent.png": build_utility_based_svg,
    "learning_agent.png": build_learning_agent_svg,
    "agent_environment_loop.png": build_agent_environment_loop_svg,
}

def render_diagrams():
    for filename, builder in DIAGRAMS.items():
        svg_content = builder()
        
        # Save SVG file
        svg_filename = filename.replace('.png', '.svg')
        svg_path = os.path.join(OUTPUT_DIR, svg_filename)
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
            
        # Render high-res PNG (DPI=240)
        doc = pymupdf.open(stream=svg_content.encode('utf-8'), filetype='svg')
        page = doc[0]
        pix = page.get_pixmap(dpi=240)
        png_path = os.path.join(OUTPUT_DIR, filename)
        pix.save(png_path)
        print(f"Rendered {filename} ({pix.width}x{pix.height}) and {svg_filename}")

if __name__ == '__main__':
    render_diagrams()
