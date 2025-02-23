document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginStatus = document.createElement('div');
    loginStatus.id = 'loginStatus';
    document.body.appendChild(loginStatus);

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const remember = document.getElementById('remember').checked;

        try {
            // Keep your existing endpoint URL
            const response = await fetch('https://fgwxjjo7j9.execute-api.us-east-1.amazonaws.com/test/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password, remember })
            });

            const data = await response.json();

            if (data.success) {
                // Store tokens if needed
                if (data.idToken) {
                    localStorage.setItem('idToken', data.idToken);
                }
                if (data.accessToken) {
                    localStorage.setItem('accessToken', data.accessToken);
                }
                if (data.refreshToken) {
                    localStorage.setItem('refreshToken', data.refreshToken);
                }
                
                document.getElementById('loginStatus').innerText = 'Successfully Logged In';
                document.getElementById('loginStatus').style.color = 'green';
                
                // Optional: Redirect to dashboard
                // window.location.href = 'dashboard.html';
            } else {
                document.getElementById('loginStatus').innerText = 'Login Failed: ' + data.message;
                document.getElementById('loginStatus').style.color = 'red';
            }
        } catch (error) {
            document.getElementById('loginStatus').innerText = 'Error logging in: ' + error.message;
            document.getElementById('loginStatus').style.color = 'red';
        }
    });
    
    // Handle signup link if it exists
    const signupLink = document.querySelector('.signup-link');
    if (signupLink) {
        signupLink.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = 'signup.html';
        });
    }
});