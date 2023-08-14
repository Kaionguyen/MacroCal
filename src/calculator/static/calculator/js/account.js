var toLogin = document.getElementById('switch-to-login');
var toSignup = document.getElementById('switch-to-signup');
var heading = document.getElementById('dynamic-header');
var loginSection = document.getElementById('login-section');
var signupSection = document.getElementById('signup-section');
function showSection(sectionId) {
    if (sectionId === 'loginSection') {
        signupSection.style.display = 'none';
        heading.textContent = 'Sign In';
        loginSection.style.display = 'flex';
    }
    else {
        loginSection.style.display = 'none';
        heading.textContent = 'Sign Up';
        signupSection.style.display = 'inline';
    }
}
function handleSignupClick() {
    showSection('signupSection');
}
function handleLoginClick() {
    showSection('loginSection');
}
if (toLogin && toSignup && heading && loginSection && signupSection) {
    toSignup.addEventListener('click', handleSignupClick);
    toLogin.addEventListener('click', handleLoginClick);
}
