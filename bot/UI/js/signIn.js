document.getElementById("signinForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const emailOrPhone = document.getElementById("emailOrPhone").value;
    const password = document.getElementById("password").value;

    if (emailOrPhone && password) {
        alert("ورود موفقیت‌آمیز بود!");
        window.location.href = "ChatBot.html";
    } else {
        alert("لطفاً تمامی فیلدها را پر کنید.");
    }
});

document.getElementById("forgotPassword").addEventListener("click", function () {
    window.location.href = "ForgotPassword.html";
});