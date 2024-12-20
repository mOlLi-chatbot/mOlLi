import { signup } from './api/_api.js';

document.getElementById("signupForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const email = document.getElementById("email").value.trim();
    const terms = document.getElementById("terms").checked;
    const errorMessage = document.getElementById("errorMessage");
    const loadingElement = document.getElementById("loading");

    errorMessage.textContent = ""; // Clear previous errors

    // Validating required fields
    if (!email || !username || !password || !confirmPassword || !terms) {
        errorMessage.textContent = "لطفاً تمامی فیلدهای ضروری را پر کنید.";
        return;
    }

    // Validating password length
    if (password.length < 8) {
        errorMessage.textContent = "رمز عبور باید حداقل 8 کاراکتر باشد.";
        return;
    }

    // Validating password match
    if (password !== confirmPassword) {
        errorMessage.textContent = "رمز عبور و تکرار آن یکسان نیستند.";
        return;
    }

    // Validating email format if provided
    if (email && !/\S+@\S+\.\S+/.test(email)) {
        errorMessage.textContent = "ایمیل وارد شده صحیح نیست.";
        return;
    }

    // Validating terms checkbox
    if (!terms) {
        errorMessage.textContent = "باید قوانین و حقوق سایت را بپذیرید.";
        return;
    }

    // نمایش لودینگ
    loadingElement.style.display = 'block';

    // ارسال داده‌ها به API
    const data = { username, email, password };

    try {
        const response = await signup(data);

        if (response.token) {
            alert("ثبت نام با موفقیت انجام شد!");
            localStorage.setItem("authToken", response.token); // ذخیره توکن
            window.location.href = "ChatBot.html"; // هدایت به صفحه چت
        } else {
            errorMessage.textContent = "ثبت نام ناموفق: " + (response.message || "خطای ناشناخته");
        }
    } catch (error) {
        console.error("Error during signup:", error);
        errorMessage.textContent = "خطا در ارتباط با سرور: " + error.message;
    } finally {
        // مخفی کردن لودینگ
        loadingElement.style.display = 'none';
    }

    // فرم فقط در صورتی ریست می‌شود که ثبت‌نام موفقیت‌آمیز باشد
    if (errorMessage.textContent === "") {
        document.getElementById("signupForm").reset();
    }
});
