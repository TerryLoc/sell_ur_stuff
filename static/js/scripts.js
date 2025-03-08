'use strict';

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

// Handle form submission with AJAX POST request to the server and show feedback modal
$(document).ready(function () {
  $('#saleForm').on('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    $.ajax({
      url: $(this).attr('action') || window.location.pathname,
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        showFeedbackModal(response.message, response.status);
        if (response.status === 'success') {
          setTimeout(
            () => (window.location.href = "{% url 'sales_list' %}"),
            1000
          ); // Redirect after modal
        }
      },
      error: function (xhr) {
        const response = xhr.responseJSON;
        showFeedbackModal(response.message, response.status);
      },
    });
  });
});
