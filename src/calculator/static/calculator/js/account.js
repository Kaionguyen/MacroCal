const toLogin = document.getElementById('switch-to-login');
const toSignup = document.getElementById('switch-to-signup');
const heading = document.getElementById('dynamic-header');
const loginSection = document.getElementById('login-section');
const signupSection = document.getElementById('signup-section');

function showSection(sectionId) {
  if (sectionId === 'loginSection') {
    signupSection.style.display = 'none';
    heading.textContent = 'Sign In';
    loginSection.style.display = 'flex';
  } else {
    loginSection.style.display = 'none';
    heading.textContent = 'Sign Up';
    signupSection.style.display = 'inline';
  }
}

toSignup.addEventListener('click', function() {
  showSection('signupSection');
});

toLogin.addEventListener('click', function() {
  showSection('loginSection');
});

