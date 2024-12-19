import { signin } from './api/_api.js';

document.getElementById("signinForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    // گرفتن مقادیر فرم
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // اعتبارسنجی فرم
    if (!username || !password) {
        alert("لطفاً تمامی فیلدها را پر کنید.");
        return;
    }

    // ارسال درخواست به API
    try {
        const response = await signin(username, password);
        alert("ورود موفقیت‌آمیز بود!");
        console.log("Response data:", response);
        if (response.token)
        window.location.href = "ChatBot.html";
    } catch (error) {
        alert("ورود ناموفق: " + error.message);
    }
});

// مدیریت فراموشی رمز عبور
document.getElementById("forgotPassword").addEventListener("click", function () {
    window.location.href = "ForgotPassword.html";
});