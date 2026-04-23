const components = {
    chatHistory: [],

    Home() {
        return `
            <div style="text-align: center; margin-top: 4rem;">
                <h1 style="font-size: 3rem; margin-bottom: 1rem;">Travel the World with <span style="color: var(--accent-blue)">AI Intelligence</span></h1>
                <p style="font-size: 1.2rem; color: var(--text-secondary); margin-bottom: 3rem;">
                    Stop hunting for flights and guessing hidden costs. Ask our proprietary agent to build your itinerary instantly.
                </p>
                <div class="glassmorphism" style="max-width: 600px; margin: 0 auto; padding: 2rem; border-radius: 16px;">
                    <h2>Where do you want to go?</h2>
                    <br>
                    <button class="btn primary-btn" style="width: 100%; padding: 1rem; font-size: 1.1rem" onclick="router.navigate('agent')">
                        Chat with Owlie Agent
                    </button>
                </div>
            </div>
        `;
    },

    Destinations() {
        return `
            <div style="margin-top: 2rem;">
                <h1 style="margin-bottom: 2rem;">Popular Destinations</h1>
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 2rem;">
                    <!-- Mock Data -->
                    <div class="glassmorphism" style="padding: 1.5rem; border-radius: 16px;">
                        <h3>Tokyo, Japan</h3>
                        <p style="color: var(--text-secondary); margin-top: 1rem;">Experience the blend of ultra-modern and traditional.</p>
                        <button class="btn primary-btn" style="margin-top: 1.5rem;" onclick="router.navigate('agent')">Find Flights</button>
                    </div>
                    <div class="glassmorphism" style="padding: 1.5rem; border-radius: 16px;">
                        <h3>Paris, France</h3>
                        <p style="color: var(--text-secondary); margin-top: 1rem;">The city of light, romance, and incredible food.</p>
                        <button class="btn primary-btn" style="margin-top: 1.5rem;" onclick="router.navigate('agent')">Find Flights</button>
                    </div>
                </div>
            </div>
        `;
    },

    Placeholder(title) {
        return `
            <div style="text-align: center; margin-top: 5rem;">
                <h1 style="margin-bottom: 1rem;">${title} Dashboard</h1>
                <p style="color: var(--text-secondary);">This module is currently being wired up to the database. Try chatting with the Agent in the meantime!</p>
                <button class="btn primary-btn" style="margin-top: 2rem;" onclick="router.navigate('agent')">Go to Agent</button>
            </div>
        `;
    },

    AgentChat() {
        return `
            <div class="chat-container glassmorphism">
                <div class="chat-history" id="chat-box">
                    <div class="message agent">
                        Hello! I am Owlie, your AI travel architect. Tell me where you are flying from, your destination, and travel dates! 
                        I can also provide cost-of-living data for your destination.
                    </div>
                </div>
                <div class="chat-input-area">
                    <input type="text" id="chat-input" placeholder="E.g., Find me a flight from LHR to CDG on 2026-06-01..." onkeypress="if(event.key === 'Enter') components.sendMessage()">
                    <button class="btn primary-btn send-btn" onclick="components.sendMessage()">🚀</button>
                </div>
            </div>
        `;
    },

    AuthForm(type) {
        const isLogin = type === 'login';
        return `
            <div class="auth-container glassmorphism">
                <h2>${isLogin ? 'Welcome Back' : 'Create Account'}</h2>
                <div class="input-group">
                    <label>Email</label>
                    <input type="email" id="auth-email" placeholder="you@example.com">
                </div>
                <div class="input-group">
                    <label>Password</label>
                    <input type="password" id="auth-password" placeholder="••••••••">
                </div>
                <button class="btn primary-btn" style="width: 100%; margin-top: 1rem;" onclick="api.handleAuth('${type}')">
                    ${isLogin ? 'Sign In' : 'Sign Up'}
                </button>
                <p style="margin-top: 1.5rem; font-size: 0.9rem; color: var(--text-secondary)">
                    ${isLogin ? "Don't have an account?" : "Already have an account?"} 
                    <a href="#" style="color: var(--accent-blue)" onclick="router.navigate('${isLogin ? 'signup' : 'login'}')">
                        ${isLogin ? 'Sign Up' : 'Sign In'}
                    </a>
                </p>
            </div>
        `;
    },

    initChat() {
        // Clear history on fresh open if desired, or load from Supabase
        this.chatHistory = [];
    },

    appendMessage(content, sender) {
        const chatBox = document.getElementById('chat-box');
        if (!chatBox) return;

        const msgDiv = document.createElement('div');
        msgDiv.className = \`message \${sender}\`;
        
        // Simple Markdown parsing for flights (bolding and line breaks)
        let formattedContent = content.replace(/\\n/g, '<br>');
        formattedContent = formattedContent.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
        
        msgDiv.innerHTML = formattedContent;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    },

    async sendMessage() {
        const input = document.getElementById('chat-input');
        const text = input.value.trim();
        
        if (!text) return;
        
        // UI Update
        this.appendMessage(text, 'user');
        input.value = '';
        input.disabled = true;
        
        // Add loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message agent';
        loadingDiv.id = 'loading-indicator';
        loadingDiv.innerHTML = 'Thinking<span class="dots">...</span>';
        document.getElementById('chat-box').appendChild(loadingDiv);

        try {
            // Internal history state for tracking context
            this.chatHistory.push({"role": "user", "content": text});
            
            // Build the exact payload shape the FastAPI backend expects
            const payload = {
                "message": text,
                "conversation_history": this.chatHistory.slice(0, -1) // history excludes the current message
            };

            const response = await api.chat(payload);
            
            // Remove loading
            document.getElementById('loading-indicator').remove();
            
            if (response && response.response) {
                this.appendMessage(response.response, 'agent');
                this.chatHistory.push({"role": "assistant", "content": response.response});
            } else {
                this.appendMessage("I'm sorry, I couldn't process that request right now.", 'agent');
            }
        } catch (error) {
            document.getElementById('loading-indicator').remove();
            this.appendMessage("Connection to the AI Agent failed.", 'agent');
            util.showToast("Error connecting to backend");
        } finally {
            input.disabled = false;
            input.focus();
        }
    }
};
