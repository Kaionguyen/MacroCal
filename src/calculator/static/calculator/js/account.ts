const toLogin = document.getElementById("switch-to-login") as HTMLElement;
const toSignup = document.getElementById("switch-to-signup") as HTMLElement;
const heading = document.getElementById("dynamic-header") as HTMLElement;
const loginSection = document.getElementById("login-section") as HTMLElement;
const signupSection = document.getElementById("signup-section") as HTMLElement;

function showSection(sectionId: string) {
  if (sectionId === "loginSection") {
    signupSection.style.display = "none";
    heading.textContent = "Sign In";
    loginSection.style.display = "flex";
  } else {
    loginSection.style.display = "none";
    heading.textContent = "Sign Up";
    signupSection.style.display = "flex";
  }
}

function handleSignupClick() {
  showSection("signupSection");
}

function handleLoginClick() {
  showSection("loginSection");
}

if (toLogin && toSignup && heading && loginSection && signupSection) {
  toSignup.addEventListener("click", handleSignupClick);
  toLogin.addEventListener("click", handleLoginClick);
}
