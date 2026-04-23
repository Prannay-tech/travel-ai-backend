const router = {
    routes: {},
    currentRoute: null,

    init() {
        // Listen to hash changes, default to 'home'
        window.addEventListener('hashchange', () => this.handleRouting());
        if (!window.location.hash) {
            window.location.hash = 'home';
        } else {
            this.handleRouting();
        }
    },

    navigate(path) {
        window.location.hash = path;
    },

    handleRouting() {
        const path = window.location.hash.substring(1) || 'home';
        this.currentRoute = path;
        this.renderView(path);
        this.updateNav(path);
    },

    renderView(path) {
        const container = document.getElementById('app-container');
        
        switch(path) {
            case 'home':
                container.innerHTML = components.Home();
                // If the user wants to test the bot here
                break;
            case 'agent':
                container.innerHTML = components.AgentChat();
                components.initChat();
                break;
            case 'login':
                container.innerHTML = components.AuthForm('login');
                break;
            case 'signup':
                container.innerHTML = components.AuthForm('signup');
                break;
            case 'reset-password':
                container.innerHTML = components.AuthForm('reset');
                break;
            case 'destinations':
                container.innerHTML = components.Destinations();
                break;
            case 'cities':
                container.innerHTML = components.Placeholder('Cities');
                break;
            case 'activities':
                container.innerHTML = components.Placeholder('Activities');
                break;
            case 'flights':
                container.innerHTML = components.Placeholder('Flights');
                break;
            case 'hotels':
                container.innerHTML = components.Placeholder('Hotels');
                break;
            default:
                container.innerHTML = components.Home();
        }
    },

    updateNav(path) {
        // Just simple logic to highlight active route if needed
    }
};

const util = {
    showToast(message) {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    router.init();
});
