"""
update_index_icons.py
Updates index.html to add the deep-dive link icon to every topic across all sections
and in the glossary cards.
"""

import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add CSS for .topic-dive-btn
css_addition = """
/* ========== TOPIC DEEP-DIVE BADGES & BUTTONS ========== */
.topic-dive-btn{
  display:inline-flex;
  align-items:center;
  gap:.3rem;
  padding:.18rem .52rem;
  border-radius:6px;
  font-size:.72rem;
  font-weight:600;
  color:var(--cyan);
  background:rgba(0,206,201,.1);
  border:1px solid rgba(0,206,201,.28);
  text-decoration:none!important;
  transition:all .2s ease;
  vertical-align:middle;
  margin-left:.45rem;
  white-space:nowrap;
  cursor:pointer;
  line-height:1.2;
}
.topic-dive-btn:hover{
  background:rgba(0,206,201,.25);
  color:#fff;
  border-color:var(--cyan);
  transform:translateY(-1px);
  box-shadow:0 2px 10px rgba(0,206,201,.35);
}
.topic-dive-btn svg{
  width:11px;
  height:11px;
  fill:currentColor;
  flex-shrink:0;
}
"""

if ".topic-dive-btn" not in content:
    content = content.replace("/* ========== TIMELINE ========== */", css_addition + "\n/* ========== TIMELINE ========== */")

# 2. Add Navbar link for Topic Deep-Dives
nav_target = '<a href="AI_Exam_Complete_Explainer_Guide.pdf" target="_blank" style="color:var(--gold);font-weight:700;display:inline-flex;align-items:center;gap:.3rem">📥 Explainer PDF</a>'
nav_replacement = '<a href="topic.html" target="_blank" style="color:var(--cyan);font-weight:700;display:inline-flex;align-items:center;gap:.3rem">📚 Deep-Dives ↗</a>\n    ' + nav_target

if 'href="topic.html"' not in content:
    content = content.replace(nav_target, nav_replacement)

# 3. Add Hero button for Topic Deep-Dives
hero_target = '<button class="btn btn-outline" onclick="document.getElementById(\'quiz\').scrollIntoView({behavior:\'smooth\'})">🎯 Take 20Q Exam Quiz</button>'
hero_replacement = hero_target + '\n      <a href="topic.html" target="_blank" class="btn btn-outline" style="border-color:var(--cyan);color:var(--cyan)">📖 38 Topic Deep-Dives ↗</a>'

if '📖 38 Topic Deep-Dives ↗' not in content:
    content = content.replace(hero_target, hero_replacement)

# 4. Updates on specific section headers and titles
replacements = [
    # Foundations & Timeline
    (
        '<div class="def-title">💡 Core Definition: Four Dimensions of AI</div>',
        '<div class="def-title">💡 Core Definition: Four Dimensions of AI <a href="topic.html?topic=foundations_ai" target="_blank" class="topic-dive-btn" title="Open complete deep-dive explainer">📖 Deep Dive ↗</a></div>'
    ),
    (
        '<div class="diagram-title">Sense, Reason, Act Model</div>',
        '<div class="diagram-title">Sense, Reason, Act Model <a href="topic.html?topic=foundations_ai" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></div>'
    ),
    (
        '<div class="diagram-title">Four Approaches to AI Matrix</div>',
        '<div class="diagram-title">Four Approaches to AI Matrix <a href="topic.html?topic=foundations_ai" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></div>'
    ),
    (
        '<div class="diagram-title">The Turing Test Setup (1950)</div>',
        '<div class="diagram-title">The Turing Test Setup (1950) <a href="topic.html?topic=turing_test" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></div>'
    ),
    (
        '<div class="tl-year">1943 – Gestation of AI</div>',
        '<div class="tl-year">1943 – Gestation of AI <a href="topic.html?topic=ai_history" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></div>'
    ),
    (
        '<div class="tl-year">1956 – The Birth of AI</div>',
        '<div class="tl-year">1956 – The Birth of AI <a href="topic.html?topic=ai_history" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></div>'
    ),
    (
        '<div class="tl-year">1966–1973 – Dose of Reality</div>',
        '<div class="tl-year">1966–1973 – Dose of Reality <a href="topic.html?topic=ai_history" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></div>'
    ),

    # Agents & PEAS
    (
        '<h2>🤖 Intelligent Agents & The PEAS Framework</h2>',
        '<h2>🤖 Intelligent Agents & The PEAS Framework <a href="topic.html?topic=peas" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h2>'
    ),
    (
        '<div class="def-title">📐 Formal Definition: Intelligent Agent & Rationality</div>',
        '<div class="def-title">📐 Formal Definition: Intelligent Agent & Rationality <a href="topic.html?topic=rationality" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></div>'
    ),
    (
        '<h4 style="color:var(--text-bright)">🖼️ The Fundamental Agent-Environment Interaction Loop</h4>',
        '<h4 style="color:var(--text-bright)">🖼️ The Fundamental Agent-Environment Interaction Loop <a href="topic.html?topic=agent_concept" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4><span class="icon">⚡</span> 1. Simple Reflex Agent</h4>',
        '<h4><span class="icon">⚡</span> 1. Simple Reflex Agent <a href="topic.html?topic=simple_reflex" target="_blank" class="topic-dive-btn" onclick="event.stopPropagation()">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4><span class="icon">🧠</span> 2. Model-Based Reflex Agent</h4>',
        '<h4><span class="icon">🧠</span> 2. Model-Based Reflex Agent <a href="topic.html?topic=model_based" target="_blank" class="topic-dive-btn" onclick="event.stopPropagation()">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4><span class="icon">🎯</span> 3. Goal-Based Agent</h4>',
        '<h4><span class="icon">🎯</span> 3. Goal-Based Agent <a href="topic.html?topic=goal_based" target="_blank" class="topic-dive-btn" onclick="event.stopPropagation()">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4><span class="icon">⭐</span> 4. Utility-Based Agent</h4>',
        '<h4><span class="icon">⭐</span> 4. Utility-Based Agent <a href="topic.html?topic=utility_based" target="_blank" class="topic-dive-btn" onclick="event.stopPropagation()">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4><span class="icon">📚</span> 5. Learning Agent</h4>',
        '<h4><span class="icon">📚</span> 5. Learning Agent <a href="topic.html?topic=learning_agent" target="_blank" class="topic-dive-btn" onclick="event.stopPropagation()">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h3 style="margin-bottom:.5rem">📋 PEAS Framework — Standard Exam Case Studies</h3>',
        '<h3 style="margin-bottom:.5rem">📋 PEAS Framework — Standard Exam Case Studies <a href="topic.html?topic=peas" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h3>'
    ),
    (
        '<h3 style="margin-bottom:.5rem">🌍 The 7 Environment Dimensions (Properties)</h3>',
        '<h3 style="margin-bottom:.5rem">🌍 The 7 Environment Dimensions (Properties) <a href="topic.html?topic=environments" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h3>'
    ),

    # Search & Heuristics
    (
        '<div class="def-title">📐 Key Concept: Heuristic Functions & Optimality</div>',
        '<div class="def-title">📐 Key Concept: Heuristic Functions & Optimality <a href="topic.html?topic=heuristics" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></div>'
    ),
    (
        '<h4 style="font-size:.95rem;color:var(--text-bright)">Search Tree Simulation</h4>',
        '<h4 style="font-size:.95rem;color:var(--text-bright)">Search Tree Simulation <a href="topic.html?topic=astar_search" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4>🟢 Greedy Best-First Search</h4>',
        '<h4>🟢 Greedy Best-First Search <a href="topic.html?topic=greedy_search" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4>⭐ A* Search (The Benchmark)</h4>',
        '<h4>⭐ A* Search (The Benchmark) <a href="topic.html?topic=astar_search" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4>💰 Uniform Cost Search (Dijkstra\'s)</h4>',
        '<h4>💰 Uniform Cost Search (Dijkstra\'s) <a href="topic.html?topic=ucs_search" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<div class="diagram-title">Romania Map & Heuristics</div>',
        '<div class="diagram-title">Romania Map & Heuristics <a href="topic.html?topic=romania_problem" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></div>'
    ),
    (
        '<div class="diagram-title">A* Optimality Contour Proof</div>',
        '<div class="diagram-title">A* Optimality Contour Proof <a href="topic.html?topic=admissibility" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></div>'
    ),
    (
        '<div class="diagram-title">Consistency Triangle Inequality</div>',
        '<div class="diagram-title">Consistency Triangle Inequality <a href="topic.html?topic=consistency" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></div>'
    ),

    # Memory Bounded Search
    (
        '<div class="def-title">⚠️ The $A^*$ Memory Crisis</div>',
        '<div class="def-title">⚠️ The $A^*$ Memory Crisis <a href="topic.html?topic=memory_bounded" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></div>'
    ),
    (
        '<h4>💥 Standard A* Search</h4>',
        '<h4>💥 Standard A* Search <a href="topic.html?topic=memory_bounded" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4>⚡ IDA* (Iterative Deepening A*)</h4>',
        '<h4>⚡ IDA* (Iterative Deepening A*) <a href="topic.html?topic=ida_star" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4>🔄 RBFS (Recursive Best-First)</h4>',
        '<h4>🔄 RBFS (Recursive Best-First) <a href="topic.html?topic=rbfs" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4>🧠 SMA* (Simplified Memory-Bounded)</h4>',
        '<h4>🧠 SMA* (Simplified Memory-Bounded) <a href="topic.html?topic=sma_star" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),

    # Knowledge Representation
    (
        '<div class="def-title">💡 The DIKW Hierarchy & KR Properties</div>',
        '<div class="def-title">💡 The DIKW Hierarchy & KR Properties <a href="topic.html?topic=dikw" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></div>'
    ),
    (
        '<h4>📊 1. Relational Knowledge</h4>',
        '<h4>📊 1. Relational Knowledge <a href="topic.html?topic=knowledge_types" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4>🕸️ 2. Inheritable Knowledge (Semantic Nets & Frames)</h4>',
        '<h4>🕸️ 2. Inheritable Knowledge (Semantic Nets & Frames) <a href="topic.html?topic=semantic_nets" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4>🧮 3. Inferential Knowledge (Predicate Logic)</h4>',
        '<h4>🧮 3. Inferential Knowledge (Predicate Logic) <a href="topic.html?topic=quant_rules" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4>⚙️ 4. Procedural Knowledge (Production Systems)</h4>',
        '<h4>⚙️ 4. Procedural Knowledge (Production Systems) <a href="topic.html?topic=forward_chaining" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4 style="color:var(--cyan)">⏩ Forward Chaining (Data-Driven)</h4>',
        '<h4 style="color:var(--cyan)">⏩ Forward Chaining (Data-Driven) <a href="topic.html?topic=forward_chaining" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4 style="color:var(--pink)">⏪ Backward Chaining (Goal-Driven)</h4>',
        '<h4 style="color:var(--pink)">⏪ Backward Chaining (Goal-Driven) <a href="topic.html?topic=backward_chaining" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h3 style="margin-bottom:.4rem">💻 Logic Programming & Prolog Essentials</h3>',
        '<h3 style="margin-bottom:.4rem">💻 Logic Programming & Prolog Essentials <a href="topic.html?topic=prolog" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h3>'
    ),

    # Logic & Formulas
    (
        '<h2>🃏 Interactive Logic & Inference Rules</h2>',
        '<h2>🃏 Interactive Logic & Inference Rules <a href="topic.html?topic=prop_rules" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h2>'
    ),
    (
        '<h4>⚡ De Morgan\'s Laws</h4>',
        '<h4>⚡ De Morgan\'s Laws <a href="topic.html?topic=de_morgan_equivalences" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    ),
    (
        '<h4 style="margin-bottom:.6rem;color:var(--gold)">📊 The 16 Binary Propositional Truth Functions</h4>',
        '<h4 style="margin-bottom:.6rem;color:var(--gold)">📊 The 16 Binary Propositional Truth Functions <a href="topic.html?topic=wff_truth" target="_blank" class="topic-dive-btn">📖 Deep Dive ↗</a></h4>'
    )
]

for old, new in replacements:
    content = content.replace(old, new)

# 5. Update renderGlossary to include the Deep Dive link on each glossary card
old_render = """    filtered.forEach(item=>{
    const card = document.createElement('div');
    card.className = 'glossary-card';
    card.innerHTML = `
      <div class="glossary-head">
        <div class="glossary-term">${item.term}</div>
        <span class="glossary-tag badge ${item.badge}">${item.cat}</span>
      </div>
      <div class="glossary-def">${item.def}</div>
      <div class="glossary-formula">${item.formula}</div>
      ${item.eg ? `<div class="glossary-eg">💡 ${item.eg}</div>` : ''}
    `;
    grid.appendChild(card);
  });"""

new_render = """    const topicMap = {
      "Artificial Intelligence (AI)": "foundations_ai",
      "Rationality vs. Omniscience": "rationality",
      "DIKW Hierarchy": "dikw",
      "Turing Test (1950)": "turing_test",
      "Dartmouth Workshop (1956)": "ai_history",
      "AI Winter": "ai_history",
      "Agent & Architecture": "agent_concept",
      "Agent Function vs. Program": "agent_concept",
      "PEAS Framework": "peas",
      "Simple Reflex Agent": "simple_reflex",
      "Model-Based Reflex Agent": "model_based",
      "Goal-Based Agent": "goal_based",
      "Utility-Based Agent": "utility_based",
      "Learning Agent": "learning_agent",
      "Episodic vs. Sequential": "environments",
      "Search Problem Formulation": "search_formulation",
      "Heuristic Function h(n)": "heuristics",
      "Admissibility": "admissibility",
      "Consistency (Monotonicity)": "consistency",
      "Greedy Best-First Search": "greedy_search",
      "A* Search Algorithm": "astar_search",
      "Uniform Cost Search (UCS)": "ucs_search",
      "IDA* (Iterative Deepening A*)": "ida_star",
      "RBFS (Recursive Best-First Search)": "rbfs",
      "SMA* (Simplified Memory-Bounded A*)": "sma_star",
      "Thrashing": "thrashing",
      "Tacit vs. Explicit Knowledge": "knowledge_types",
      "Declarative vs. Procedural": "knowledge_types",
      "Semantic Networks": "semantic_nets",
      "Frames & Slots": "frames",
      "Forward Chaining": "forward_chaining",
      "Backward Chaining": "backward_chaining",
      "Conflict Resolution Strategies": "conflict_resolution",
      "Kowalski's Equation (Prolog)": "prolog",
      "Well-Formed Formula (WFF)": "wff_truth",
      "Tautology, Contradiction, Contingency": "wff_truth",
      "Resolution Principle": "resolution_principle",
      "Deduction Theorem": "proof_techniques",
      "Proof by Contradiction (Reductio)": "proof_techniques"
    };

    filtered.forEach(item=>{
      const card = document.createElement('div');
      card.className = 'glossary-card';
      const topicId = topicMap[item.term] || 'foundations_ai';
      card.innerHTML = `
        <div class="glossary-head">
          <div class="glossary-term">
            ${item.term}
            <a href="topic.html?topic=${topicId}" target="_blank" class="topic-dive-btn" title="Open complete deep-dive explainer for ${item.term}">
              <svg viewBox="0 0 24 24"><path d="M19 19H5V5h7V3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2v-7h-2v7zM14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z"/></svg> Deep Dive ↗
            </a>
          </div>
          <span class="glossary-tag badge ${item.badge}">${item.cat}</span>
        </div>
        <div class="glossary-def">${item.def}</div>
        <div class="glossary-formula">${item.formula}</div>
        ${item.eg ? `<div class="glossary-eg">💡 ${item.eg}</div>` : ''}
      `;
      grid.appendChild(card);
    });"""

if old_render in content:
    content = content.replace(old_render, new_render)
else:
    print("Warning: old_render exact string match not found, checking with regex.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated index.html successfully with deep-dive topic icons!")
