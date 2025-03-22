// Main initialization - everything wrapped in one DOMContentLoaded
document.addEventListener('DOMContentLoaded', function () {
  // Password toggle for login form
  const togglePassword = document.getElementById('togglePassword');
  const passwordInput = document.getElementById('id_password');

  if (togglePassword && passwordInput) {
    togglePassword.addEventListener('click', function () {
      // Toggle password visibility
      const type =
        passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
      passwordInput.setAttribute('type', type);

      // Toggle icon
      const iconClass = type === 'password' ? 'bi-eye' : 'bi-eye-slash';
      togglePassword.innerHTML = `<i class="${iconClass}"></i>`;
    });
  }

  // Password toggle for registration form
  const togglePasswordReg = document.getElementById('togglePassword');
  const passwordReg = document.getElementById('id_password1');

  if (togglePasswordReg && passwordReg) {
    togglePasswordReg.addEventListener('click', function () {
      const type =
        passwordReg.getAttribute('type') === 'password' ? 'text' : 'password';
      passwordReg.setAttribute('type', type);
      this.querySelector('i').classList.toggle('bi-eye');
      this.querySelector('i').classList.toggle('bi-eye-slash');
    });
  }

  // Newsletter form handling
  const newsletterSection = document.getElementById('newsletter');
  const newsletterForm = document.getElementById('newsletter-form');

  if (newsletterForm) {
    // Add hidden field on form submission
    newsletterForm.addEventListener('submit', function () {
      if (!document.getElementById('is_newsletter_submit')) {
        const hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = 'is_newsletter_submit';
        hiddenField.id = 'is_newsletter_submit';
        hiddenField.value = 'true';
        this.appendChild(hiddenField);
      }
    });
  }

  // Handle URL fragment for newsletter section
  if (newsletterSection) {
    // Check if we need to scroll to the newsletter section
    const hasFormErrors = document.querySelector('.error-message') !== null;
    const hasUrlFragment = window.location.hash === '#newsletter';

    if (hasFormErrors || hasUrlFragment) {
      // Use setTimeout to ensure this happens after the page loads
      setTimeout(function () {
        newsletterSection.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }

    // If we have success message and the hash fragment, clear the form
    if (hasUrlFragment && document.querySelector('.alert-success')) {
      if (newsletterForm) newsletterForm.reset();
    }
  }
});
