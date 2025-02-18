document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const remember = document.getElementById('remember').checked;
        
        // Log form data (for demonstration)
        console.log({
            email: email,
            password: password,
            rememberMe: remember
        });
        
        // Here you would typically:
        // 1. Validate the input
        // 2. Make an API call to your backend
        // 3. Handle the response (success/error)
    });
});