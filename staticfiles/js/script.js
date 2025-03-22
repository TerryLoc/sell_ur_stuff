// This is for the password toggle in the login form
document.addEventListener('DOMContentLoaded', function () {
  const togglePassword = document.getElementById('togglePassword');
  const passwordInput = document.getElementById('id_password');

  togglePassword.addEventListener('click', function () {
    // Toggle password visibility
    const type =
      passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);

    // Toggle icon
    const iconClass = type === 'password' ? 'bi-eye' : 'bi-eye-slash';
    togglePassword.innerHTML = `<i class="${iconClass}"></i>`;
  });
});

// This is for the password toggle in the registration form
document
  .getElementById('togglePassword')
  .addEventListener('click', function () {
    const password = document.getElementById('id_password1');
    const type =
      password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    this.querySelector('i').classList.toggle('bi-eye');
    this.querySelector('i').classList.toggle('bi-eye-slash');
  });
