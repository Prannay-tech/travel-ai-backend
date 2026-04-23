// In a real deployed app, you'd load these from process.env or window.ENV.
// But for Vanilla JS client-side, we mock Supabase init here.
const SUPABASE_URL = 'https://replace-me.supabase.co';
const SUPABASE_ANON_KEY = 'replace-me';

// Initialize Supabase Client
// const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

const api = {
    async chat(payload) {
        // Calls our FastAPI backend directly
        const response = await fetch('/api/v1/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            if (response.status === 429) {
                throw new Error("Rate limit exceeded.");
            }
            throw new Error('API Error');
        }

        return await response.json();
    },

    async handleAuth(type) {
        const email = document.getElementById('auth-email').value;
        const password = document.getElementById('auth-password').value;

        if (!email || !password) {
            util.showToast("Please enter email and password");
            return;
        }

        // Mocking the Supabase integration since we are building vanilla
        try {
            /* 
            if (type === 'login') {
                const { user, error } = await supabase.auth.signInWithPassword({ email, password });
                if (error) throw error;
            } else {
                const { user, error } = await supabase.auth.signUp({ email, password });
                if (error) throw error;
            }
            */
            
            // Success Mock
            util.showToast(type === 'login' ? "Logged in successfully!" : "Account created!");
            
            // Adjust Navbar securely
            document.getElementById('auth-btn').textContent = "Sign Out";
            document.getElementById('auth-btn').onclick = () => {
                util.showToast("Signed Out");
                router.navigate('home');
                setTimeout(() => window.location.reload(), 1000);
            };

            // Navigate to agent
            setTimeout(() => router.navigate('agent'), 500);

        } catch (error) {
            util.showToast(error.message || "Authentication failed");
        }
    }
};
