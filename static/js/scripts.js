function showFeedbackModal(message, type) {
  // Set message and styling based on type (success, error, warning, info)
  const modalBody = document.getElementById('feedbackMessage');
  modalBody.innerHTML = message;
  modalBody.className =
    'modal-body alert alert-' +
    (type === 'error'
      ? 'danger'
      : type === 'success'
      ? 'success'
      : type === 'warning'
      ? 'warning'
      : 'info');

  // Show the modal
  const feedbackModal = new bootstrap.Modal(
    document.getElementById('feedbackModal')
  );
  feedbackModal.show();
}
