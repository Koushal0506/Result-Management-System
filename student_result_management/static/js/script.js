/**
 * Student Result Management System
 * Basic JavaScript utilities for form validation and user interactions.
 */

// Validate registration form inputs before submission
function validateRegisterForm(form) {
    const password = form.password.value;
    const confirmPassword = form.confirm_password.value;

    if (password.length < 6) {
        alert("Password must be at least 6 characters long.");
        form.password.focus();
        return false;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match. Please re-enter.");
        form.confirm_password.focus();
        return false;
    }

    return true;
}

// Auto-dismiss alerts after 6 seconds
document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll(".student-alert");
    alerts.forEach(function (alertElement) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alertElement);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 6000);
    });
});

