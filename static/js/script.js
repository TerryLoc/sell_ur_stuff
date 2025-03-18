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
