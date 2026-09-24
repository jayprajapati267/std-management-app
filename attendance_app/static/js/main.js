// Auto-dismiss flash alerts after 4 seconds.
document.addEventListener("DOMContentLoaded", function () {
    var alerts = document.querySelectorAll(".alert");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 4000);
    });
});
