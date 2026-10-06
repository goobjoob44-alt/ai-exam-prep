/**
 * AI Exam Tutor & Problem Solver Widget
 * Powers interactive AI tutoring for Assam Don Bosco University (ADBU) CSE AI Exam Prep.
 * Supports Google Gemini 2.0 Flash with direct Google AI Studio sign-in link,
 * local storage key persistence, and built-in offline syllabus fallback.
 */

(function () {
  const STORAGE_KEY = 'adbu_ai_gemini_key';
  const CHAT_STORAGE_KEY = 'adbu_ai_chat_history';

  // Offline Syllabus Knowledge Base for instant testing
  const OFFLINE_KB = {
    peas: "### PEAS Framework Breakdown\n\nPEAS stands for **Performance Measure (P)**, **Environment (E)**, **Actuators (A)**, and **Sensors (S)**.\n\n- **Autonomous Taxi Example:**\n  - **P:** Safety, travel speed, legal compliance, comfort, maximum profit.\n  - **E:** Urban roads, highway traffic, pedestrians, weather, customers.\n  - **A:** Steering wheel, accelerator, brakes, horn, turn signals, display.\n  - **S:** Cameras, LiDAR, radar, GPS, speedometer, accelerometer.\n\n*Golden Rule:* Always specify Performance in terms of environmental outcomes, not the agent's internal actions!",
    astar: "### A* Search: Admissibility vs Consistency\n\n- **Evaluation Function:** $f(n) = g(n) + h(n)$\n  - $g(n)$: Exact path cost from start to $n$.\n  - $h(n)$: Estimated heuristic cost from $n$ to goal.\n\n- **Admissibility (Tree Search Optimality):**\n  $$0 \\le h(n) \\le h^*(n)$$\n  $h(n)$ never overestimates the true remaining cost to the goal.\n\n- **Consistency / Monotonicity (Graph Search Optimality):**\n  $$h(n) \\le c(n, a, n') + h(n')$$\n  Satisfies the triangle inequality. Every consistent heuristic is admissible, but not every admissible heuristic is consistent!",
    alphabeta: "### Alpha-Beta Pruning Core Essentials\n\nAlpha-Beta pruning preserves the exact same minimax decision while pruning branches that cannot influence the final outcome:\n\n- **$\\alpha$ (Alpha):** The best (highest-value) choice found so far along the path for the **MAX** player. Initialized to $-\\infty$.\n- **$\\beta$ (Beta):** The best (lowest-value) choice found so far along the path for the **MIN** player. Initialized to $+\\infty$.\n\n- **Pruning Condition:** Prune when $\\alpha \\ge \\beta$.\n- **Best-case Time Complexity:** $O(b^{d/2})$ with perfect move ordering (effectively doubles the search depth achievable)!",
    resolution: "### Resolution Refutation in First-Order Logic\n\nResolution is a complete, sound theorem-proving technique based on **Proof by Contradiction**:\n\n1. Given knowledge base $KB$ and target query $\\alpha$.\n2. Convert all sentences in $KB$ and $\\neg \\alpha$ into **Conjunctive Normal Form (CNF)**.\n3. Repeatedly select two clauses with complementary literals (e.g. $P(x)$ and $\\neg P(A)$), compute the Most General Unifier (MGU), and generate their **resolvent**.\n4. If the **empty clause $\\square$** (Falsehood) is derived, the assumption $\\neg \\alpha$ is refuted, proving $KB \\models \\alpha$!",
    viva: "### Top 5 High-Yield ADBU AI Viva Questions\n\n1. **Q:** Why is Depth-First Search not guaranteed to be complete in infinite state spaces?\n   *Ans:* DFS can traverse an infinite path or get trapped in cycles without backtracking.\n2. **Q:** Can an admissible heuristic overestimate the cost?\n   *Ans:* No. By definition, $h(n) \\le h^*(n)$.\n3. **Q:** What is the difference between a Model-Based Reflex agent and a Goal-Based agent?\n   *Ans:* A model-based reflex agent only knows the current world state; a goal-based agent plans future action sequences to satisfy an explicit target state.\n4. **Q:** What is the role of Skolemization in First-Order Logic?\n   *Ans:* To eliminate existential quantifiers $(\\exists)$ by replacing the quantified variable with a fresh Skolem constant or Skolem function of universally quantified variables.\n5. **Q:** When does Breadth-First Search guarantee optimal solutions?\n   *Ans:* When all step costs are equal (uniform step cost $c = 1$)."
  };

  class AiExamTutor {
    constructor() {
      this.apiKey = localStorage.getItem(STORAGE_KEY) || '';
      this.isOfflineMode = false;
      this.isOpen = false;
      this.isGenerating = false;
      this.chatHistory = this.loadChatHistory();

      this.initUI();
      this.updateStatus();
      this.renderHistory();
    }

    loadChatHistory() {
      try {
        const stored = sessionStorage.getItem(CHAT_STORAGE_KEY);
        if (stored) return JSON.parse(stored);
      } catch (e) {}
      return [
        {
          role: 'model',
          text: "👋 **Hello! I am your AI Exam Prep Tutor** for the Assam Don Bosco University (ADBU) CSE Artificial Intelligence course.\n\nI can explain algorithms, solve search problems step-by-step, review viva questions, or convert logic formulas to CNF. How can I help you today?"
        }
      ];
    }

    saveChatHistory() {
      try {
        sessionStorage.setItem(CHAT_STORAGE_KEY, JSON.stringify(this.chatHistory));
      } catch (e) {}
    }

    initUI() {
      // Create FAB
      const fab = document.createElement('button');
      fab.id = 'aiTutorFab';
      fab.className = 'ai-fab';
      fab.setAttribute('aria-label', 'Open AI Exam Tutor');
      fab.innerHTML = `
        <span class="ai-fab-icon">✨</span>
        <span>AI Exam Tutor</span>
        <span class="ai-fab-badge">Gemini</span>
      `;
      fab.onclick = () => this.toggleDrawer();
      document.body.appendChild(fab);

      // Create Overlay
      const overlay = document.createElement('div');
      overlay.id = 'aiTutorOverlay';
      overlay.className = 'ai-drawer-overlay';
      overlay.onclick = () => this.toggleDrawer(false);
      document.body.appendChild(overlay);

      // Create Drawer
      const drawer = document.createElement('div');
      drawer.id = 'aiTutorDrawer';
      drawer.className = 'ai-drawer';
      drawer.innerHTML = `
        <!-- Header -->
        <div class="ai-header">
          <div class="ai-header-info">
            <div class="ai-avatar">🧠</div>
            <div>
              <div class="ai-header-title">ADBU AI Exam Tutor</div>
              <div class="ai-header-status">
                <span class="ai-status-dot" id="aiStatusDot"></span>
                <span id="aiStatusText">Initializing...</span>
              </div>
            </div>
          </div>
          <div class="ai-header-tools">
            <button class="ai-icon-btn" id="aiConfigToggleBtn" title="API Key Settings">⚙️</button>
            <button class="ai-icon-btn" id="aiClearChatBtn" title="Clear Conversation">🗑️</button>
            <button class="ai-icon-btn" id="aiCloseBtn" title="Close Drawer">✕</button>
          </div>
        </div>

        <!-- API Key Auth Card -->
        <div id="aiAuthCard" class="ai-auth-card" style="${this.apiKey ? 'display:none;' : 'display:block;'}">
          <div class="ai-auth-badge">🔑 Free Google Gemini Integration</div>
          <div class="ai-auth-title">Connect Your AI Exam Assistant</div>
          <div class="ai-auth-desc">
            Get unlimited step-by-step problem solving powered by Google Gemini 2.0 Flash. Sign in with Google to get your free API key in 10 seconds:
          </div>
          <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" class="ai-google-btn">
            <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
            <span>1. Sign In to Google AI Studio & Get Free Key ↗</span>
          </a>
          <div class="ai-key-input-row">
            <input type="password" id="aiKeyInput" class="ai-key-input" placeholder="2. Paste API key (AIzaSy...)" value="${this.apiKey}" />
            <button id="aiSaveKeyBtn" class="ai-save-btn">Save</button>
          </div>
          <div class="ai-auth-footer">
            <span>🔒 Stored locally in your browser</span>
            <button id="aiOfflineBtn" class="ai-text-btn">Try Offline Demo Mode</button>
          </div>
        </div>

        <!-- Messages Pane -->
        <div id="aiMessagesPane" class="ai-messages-pane"></div>

        <!-- Prompt Suggestions Chips -->
        <div class="ai-chips-container">
          <button class="ai-prompt-chip" data-prompt="Predict 5 high-yield viva questions for ADBU AI exam">🎓 Viva Questions</button>
          <button class="ai-prompt-chip" data-prompt="Explain A* admissibility vs consistency with Romanian map example">🔍 A* Heuristics</button>
          <button class="ai-prompt-chip" data-prompt="Give PEAS specification for an Autonomous Drone Delivery agent">🚕 PEAS Spec</button>
          <button class="ai-prompt-chip" data-prompt="How does Alpha-Beta pruning reduce minimax time complexity?">🌲 Alpha-Beta</button>
          <button class="ai-prompt-chip" data-prompt="Explain Resolution Refutation in First-Order Logic with an example">📐 FOL Resolution</button>
        </div>

        <!-- Input Bar -->
        <div class="ai-input-box">
          <textarea id="aiInputText" class="ai-textarea" rows="1" placeholder="Ask any AI concept, viva question, or derivation..."></textarea>
          <button id="aiSendBtn" class="ai-send-btn" aria-label="Send">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg>
          </button>
        </div>
      `;
      document.body.appendChild(drawer);

      // Event listeners
      document.getElementById('aiCloseBtn').onclick = () => this.toggleDrawer(false);
      document.getElementById('aiConfigToggleBtn').onclick = () => this.toggleConfig();
      document.getElementById('aiClearChatBtn').onclick = () => this.clearChat();
      document.getElementById('aiSaveKeyBtn').onclick = () => this.saveKey();
      document.getElementById('aiOfflineBtn').onclick = () => this.enableOfflineMode();
      document.getElementById('aiSendBtn').onclick = () => this.sendMessage();

      const input = document.getElementById('aiInputText');
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendMessage();
        }
      });
      input.addEventListener('input', () => {
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 120) + 'px';
      });

      // Quick Chips
      drawer.querySelectorAll('.ai-prompt-chip').forEach((btn) => {
        btn.onclick = () => {
          const prompt = btn.getAttribute('data-prompt');
          document.getElementById('aiInputText').value = prompt;
          this.sendMessage();
        };
      });
    }

    toggleDrawer(show) {
      this.isOpen = show !== undefined ? show : !this.isOpen;
      const drawer = document.getElementById('aiTutorDrawer');
      const overlay = document.getElementById('aiTutorOverlay');
      if (this.isOpen) {
        drawer.classList.add('active');
        overlay.classList.add('active');
        document.getElementById('aiInputText').focus();
        this.scrollToBottom();
      } else {
        drawer.classList.remove('active');
        overlay.classList.remove('active');
      }
    }

    toggleConfig() {
      const card = document.getElementById('aiAuthCard');
      card.style.display = card.style.display === 'none' ? 'block' : 'none';
    }

    updateStatus() {
      const dot = document.getElementById('aiStatusDot');
      const text = document.getElementById('aiStatusText');
      if (this.apiKey) {
        dot.style.background = '#00cec9';
        dot.style.boxShadow = '0 0 8px #00cec9';
        text.innerText = 'Gemini 2.0 Flash Connected';
        text.style.color = '#00cec9';
      } else if (this.isOfflineMode) {
        dot.style.background = '#fdcb6e';
        dot.style.boxShadow = '0 0 8px #fdcb6e';
        text.innerText = 'Offline Syllabus Mode';
        text.style.color = '#fdcb6e';
      } else {
        dot.style.background = '#fd79a8';
        dot.style.boxShadow = '0 0 8px #fd79a8';
        text.innerText = 'Key Required (Free Setup)';
        text.style.color = '#fd79a8';
      }
    }

    saveKey() {
      const input = document.getElementById('aiKeyInput');
      const val = input.value.trim();
      if (!val) {
        alert('Please paste a valid Google Gemini API key.');
        return;
      }
      this.apiKey = val;
      this.isOfflineMode = false;
      localStorage.setItem(STORAGE_KEY, val);
      document.getElementById('aiAuthCard').style.display = 'none';
      this.updateStatus();
      this.addBotMessage('✅ **Google Gemini connected successfully!** Ask me anything from your syllabus.');
    }

    enableOfflineMode() {
      this.isOfflineMode = true;
      document.getElementById('aiAuthCard').style.display = 'none';
      this.updateStatus();
      this.addBotMessage('⚡ **Running in Offline Syllabus Mode!** You can explore core exam questions. To unlock arbitrary questions, add your free Gemini key via ⚙️.');
    }

    clearChat() {
      if (!confirm('Clear all conversation history?')) return;
      this.chatHistory = [
        {
          role: 'model',
          text: "Chat cleared. What topic or exam question would you like to review?"
        }
      ];
      this.saveChatHistory();
      this.renderHistory();
    }

    formatMarkdown(text) {
      if (!text) return '';
      let out = text;

      // Tables
      out = out.replace(/(?:^|\n)(\|.+?\|\n\|[-:\s|]+\|\n(?:\|.+?\|\n?)+)/g, function (match) {
        const lines = match.trim().split('\n');
        if (lines.length < 2) return match;
        const headerCols = lines[0].split('|').map((s) => s.trim()).filter((s, i, arr) => (i > 0 && i < arr.length - 1) || s !== '');
        let html = '<div style="overflow-x:auto;margin:8px 0;"><table style="width:100%;border-collapse:collapse;font-size:0.76rem;"><thead><tr>';
        headerCols.forEach((col) => {
          html += `<th style="padding:6px 10px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.1);color:#fff;">${col}</th>`;
        });
        html += '</tr></thead><tbody>';
        for (let r = 2; r < lines.length; r++) {
          const cols = lines[r].split('|').map((s) => s.trim()).filter((s, i, arr) => (i > 0 && i < arr.length - 1) || s !== '');
          if (cols.length === 0) continue;
          html += '<tr>';
          cols.forEach((col) => {
            html += `<td style="padding:5px 10px;border:1px solid rgba(255,255,255,0.08);">${col}</td>`;
          });
          html += '</tr>';
        }
        html += '</tbody></table></div>';
        return '\n' + html + '\n';
      });

      // Code blocks
      out = out.replace(/```([a-z]*)\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>');
      out = out.replace(/`([^`]+)`/g, '<code>$1</code>');

      // Bold & Italics
      out = out.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      out = out.replace(/\*(.*?)\*/g, '<em>$1</em>');

      // Lists
      out = out.replace(/^\s*-\s+(.*)$/gm, '<li>$1</li>');
      out = out.replace(/(<li>.*<\/li>)/s, '<ul style="margin:6px 0;padding-left:18px;">$1</ul>');

      // Headers
      out = out.replace(/^### (.*)$/gm, '<h4 style="color:#00cec9;margin:8px 0 4px;font-size:0.92rem;">$1</h4>');
      out = out.replace(/^## (.*)$/gm, '<h3 style="color:#ffffff;margin:10px 0 6px;font-size:1rem;">$1</h3>');

      // Paragraph newlines
      out = out.replace(/\n\n/g, '<div style="height:6px"></div>');

      return out;
    }

    renderHistory() {
      const pane = document.getElementById('aiMessagesPane');
      pane.innerHTML = '';
      this.chatHistory.forEach((msg) => {
        this.appendMessageDOM(msg.role, msg.text);
      });
      this.scrollToBottom();
      this.renderMath();
    }

    appendMessageDOM(role, text) {
      const pane = document.getElementById('aiMessagesPane');
      const div = document.createElement('div');
      div.className = `ai-msg ${role === 'user' ? 'user' : 'bot'}`;
      div.innerHTML = `
        <div class="ai-msg-avatar">${role === 'user' ? '👤' : '🧠'}</div>
        <div class="ai-msg-content">${this.formatMarkdown(text)}</div>
      `;
      pane.appendChild(div);
    }

    addUserMessage(text) {
      this.chatHistory.push({ role: 'user', text });
      this.saveChatHistory();
      this.appendMessageDOM('user', text);
      this.scrollToBottom();
    }

    addBotMessage(text) {
      this.chatHistory.push({ role: 'model', text });
      this.saveChatHistory();
      this.appendMessageDOM('bot', text);
      this.scrollToBottom();
      this.renderMath();
    }

    showTyping() {
      const pane = document.getElementById('aiMessagesPane');
      const indicator = document.createElement('div');
      indicator.id = 'aiTypingIndicator';
      indicator.className = 'ai-typing-indicator';
      indicator.innerHTML = `
        <span class="ai-dot"></span>
        <span class="ai-dot"></span>
        <span class="ai-dot"></span>
      `;
      pane.appendChild(indicator);
      this.scrollToBottom();
    }

    removeTyping() {
      const el = document.getElementById('aiTypingIndicator');
      if (el) el.remove();
    }

    scrollToBottom() {
      const pane = document.getElementById('aiMessagesPane');
      if (pane) {
        pane.scrollTop = pane.scrollHeight;
      }
    }

    renderMath() {
      if (window.renderMathInElement) {
        const pane = document.getElementById('aiMessagesPane');
        try {
          window.renderMathInElement(pane, {
            delimiters: [
              { left: '$$', right: '$$', display: true },
              { left: '$', right: '$', display: false }
            ],
            throwOnError: false
          });
        } catch (e) {}
      }
    }

    async sendMessage() {
      const input = document.getElementById('aiInputText');
      const text = input.value.trim();
      if (!text || this.isGenerating) return;

      input.value = '';
      input.style.height = 'auto';
      this.addUserMessage(text);

      if (!this.apiKey && !this.isOfflineMode) {
        document.getElementById('aiAuthCard').style.display = 'block';
        this.addBotMessage("⚠️ **Please connect your free Google Gemini API key** above to continue, or click **'Try Offline Demo Mode'**.");
        return;
      }

      this.isGenerating = true;
      document.getElementById('aiSendBtn').disabled = true;
      this.showTyping();

      try {
        if (this.isOfflineMode || !this.apiKey) {
          await new Promise((r) => setTimeout(r, 600)); // natural typing delay
          const reply = this.getOfflineAnswer(text);
          this.removeTyping();
          this.addBotMessage(reply);
        } else {
          const reply = await this.callGeminiAPI(text);
          this.removeTyping();
          this.addBotMessage(reply);
        }
      } catch (err) {
        this.removeTyping();
        this.addBotMessage(`❌ **Error:** ${err.message || 'Failed to reach Gemini API. Please check your API key or network connection.'}`);
      } finally {
        this.isGenerating = false;
        document.getElementById('aiSendBtn').disabled = false;
      }
    }

    getOfflineAnswer(query) {
      const q = query.toLowerCase();
      if (q.includes('peas') || q.includes('taxi') || q.includes('agent spec')) {
        return OFFLINE_KB.peas;
      } else if (q.includes('a*') || q.includes('admissib') || q.includes('consist')) {
        return OFFLINE_KB.astar;
      } else if (q.includes('alpha') || q.includes('beta') || q.includes('pruning') || q.includes('minimax')) {
        return OFFLINE_KB.alphabeta;
      } else if (q.includes('resolution') || q.includes('cnf') || q.includes('fol') || q.includes('first-order')) {
        return OFFLINE_KB.resolution;
      } else if (q.includes('viva') || q.includes('question') || q.includes('important')) {
        return OFFLINE_KB.viva;
      } else {
        return `### 💡 Offline Syllabus Answer\n\nI found related concepts in your Assam Don Bosco University course syllabus!\n\n- **Tip:** In your exam, always structure answers with:\n  1. **Formal Definition & Notation** (e.g. states, cost functions, knowledge representations).\n  2. **Step-by-Step Algorithm or Formulation** (e.g. pseudo-code or truth table).\n  3. **Complexity Analysis** (Time & Space complexity in $O(\\cdot)$ notation).\n  4. **Concrete Real-World Example** (e.g. Romania travel problem or vacuum world).\n\n*To ask custom, arbitrary questions on any topic, add your free Google Gemini API key by clicking the ⚙️ icon above.*`;
      }
    }

    async callGeminiAPI(userQuery) {
      const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${encodeURIComponent(this.apiKey)}`;

      const systemPrompt = `You are the official Artificial Intelligence Course Professor & Exam Assistant for Assam Don Bosco University (ADBU) B.Tech CSE students.
The course covers:
1. Unit 1: AI Foundations, History, Rationality, Turing Test.
2. Unit 2: Intelligent Agents & PEAS Framework, 5 Agent Architectures, 7 Environment Types.
3. Unit 3: Uninformed Search (BFS, DFS, DLS, IDDFS, UCS, Bidirectional) and Informed Heuristic Search (Greedy Best-First, A* with Admissibility & Consistency, Romania Map).
4. Unit 4: Adversarial Search (Game Theory, Minimax Algorithm, Alpha-Beta Pruning, Horizon Effect).
5. Unit 5: Knowledge Representation & Memory (DIKW Pyramid, Declarative vs Procedural, Semantic Networks, Frames, Conceptual Dependency, Scripts).
6. Unit 6: Propositional & First-Order Logic (Truth tables, CNF conversion, Resolution Refutation, Quantifiers, Unification, Horn Clauses, Prolog).

Style Guidelines:
- Give concise, clear, and mathematically precise explanations.
- Use LaTeX math delimiters ($...$ for inline, $$...$$ for display).
- Include practical exam tips, viva pitfalls, and step-by-step numerical/algorithmic traces when asked.
- Format with clean Markdown headings, bullet points, and tables.`;

      // Build contents array from recent chat history (up to last 10 messages)
      const recent = this.chatHistory.slice(-8).map((m) => ({
        role: m.role === 'user' ? 'user' : 'model',
        parts: [{ text: m.text }]
      }));

      // Add the new user query
      recent.push({
        role: 'user',
        parts: [{ text: userQuery }]
      });

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          system_instruction: {
            parts: [{ text: systemPrompt }]
          },
          contents: recent,
          generationConfig: {
            temperature: 0.7,
            maxOutputTokens: 2048
          }
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error?.message || `HTTP ${response.status}: Failed to generate response.`);
      }

      const data = await response.json();
      const candidate = data.candidates?.[0];
      const text = candidate?.content?.parts?.[0]?.text;
      if (!text) {
        throw new Error('Gemini API returned an empty response.');
      }
      return text;
    }
  }

  // Initialize once DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new AiExamTutor());
  } else {
    new AiExamTutor();
  }
})();
