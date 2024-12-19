import { signup } from './api/_api.js';

document.getElementById("signinForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (email && password) {
        alert("ورود موفقیت‌آمیز بود!");
        window.location.href = "ChatBot.html";
    } else {
        alert("لطفاً تمامی فیلدها را پر کنید.");
    }
});

document.getElementById("forgotPassword").addEventListener("click", function () {
    window.location.href = "ForgotPassword.html";
});