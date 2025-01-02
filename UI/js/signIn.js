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

    // اعتبارسنجی پسورد (حداقل 6 کاراکتر)
    if (password.length < 6) {
        alert("پسورد باید حداقل 6 کاراکتر باشد.");
        return;
    }

    // نمایش وضعیت لودینگ
    const loadingElement = document.getElementById('loading');
    loadingElement.style.display = 'flex'; // نمایش وضعیت لودینگ

    // ارسال درخواست به API
    try {
        const response = await signin(username, password);
        alert("ورود موفقیت‌آمیز بود!");
        console.log("Response data:", response);

        if (response.token) {
            localStorage.setItem('authToken', response.token); // ذخیره توکن در localStorage
            window.location.href = "ChatBot.html"; // هدایت به صفحه چت بات
        }
    } catch (error) {
        // مدیریت خطاهای مختلف
        console.error("Login Error:", error); // نمایش خطا در کنسول

        // بررسی خطای شبکه (اگر اتصال به سرور مشکل داشته باشد)
        if (error.message.includes("NetworkError")) {
            alert("مشکل در اتصال به سرور. لطفاً دوباره تلاش کنید.");
        }
        // بررسی خطاهای مربوط به اعتبارسنجی یا سایر خطاها
        else if (error.message.includes("403")) {
            alert("نام کاربری یا رمز عبور اشتباه است.");
        }
        else {
            alert("ورود ناموفق: " + error.message); // نمایش خطای عمومی
        }
    } finally {
        // مخفی کردن وضعیت لودینگ
        loadingElement.style.display = 'none';
    }
});

// مدیریت فراموشی رمز عبور
document.getElementById("forgotPassword").addEventListener("click", function () {
    window.location.href = "ForgotPassword.html";
});
