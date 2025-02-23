document.addEventListener('DOMContentLoaded', function () {
    // Fix for mobile viewport height
    function setViewportHeight() {
        let vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }

    // Set initial viewport height
    setViewportHeight();

    // Update viewport height on resize
    window.addEventListener('resize', () => {
        setViewportHeight();
    });

    // Form handling
    const signupForm = document.getElementById('signupForm');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const firstNameInput = document.getElementById('fname');
    const lastNameInput = document.getElementById('lname');
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    const roleInput = document.getElementById('role');

    // Handle form submission
    signupForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Basic validation
        if (passwordInput.value !== confirmPasswordInput.value) {
            alert('Passwords do not match!');
            return;
        }

        if (passwordInput.value.length < 8) {
            alert('Password must be at least 8 characters long!');
            return;
        }

        if (!roleInput.value) {
            alert('Please select a role.');
            return;
        }

        // Collect form data
        const userData = {
            email: emailInput.value,
            password: passwordInput.value,
            firstName: firstNameInput.value,
            lastName: lastNameInput.value,
            phone: phoneInput.value || '', // Optional phone input
            userRole: roleInput.value,
        };

        try {
            // Make API call to your backend Lambda function via API Gateway
            const response = await fetch('https://fgwxjjo7j9.execute-api.us-east-1.amazonaws.com/test/users', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData),
            });

            if (!response.ok) {
                const errorResponse = await response.json();
                throw new Error(errorResponse.message || 'Error signing up user.');
            }

            const result = await response.json();
            console.log('Sign-up successful:', result);

            alert(`Sign-up successful! Welcome, ${result.username}. Please check your email for verification.`);
            
            // Optional: Redirect to login page after successful sign-up
            //window.location.href = 'give login page path';
            
        } catch (error) {
            console.error('Error during sign-up:', error);
            alert(`Sign-up failed: ${error.message}`);
        }
    });

    // Handle Google Sign-In (if applicable)
    const googleSignInBtn = document.getElementById('googleSignIn');
    googleSignInBtn.addEventListener('click', function () {
        console.log('Google Sign-In clicked');
        // Add your Google Sign-In logic here
    });
    
    // Handle Login button redirect
    const loginBtn = document.querySelector('.top-login-btn');
    loginBtn.addEventListener('click', function () {
        console.log('Login clicked');
        window.location.href = 'login.html'; // Redirect to login page
    });
});
