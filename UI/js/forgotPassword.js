import { signup } from './api/_api.js';

document.getElementById('forgotPasswordForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const contact = document.getElementById('contact').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // بررسی تطابق رمز عبور جدید و تکرار آن
    if (newPassword !== confirmPassword) {
        alert("رمز عبور جدید و تکرار آن یکسان نیستند.");
        return;
    }

    // بررسی طول رمز عبور جدید (حداقل 8 رقم)
    if (newPassword.length < 8) {
        alert("رمز عبور جدید باید حداقل 8 رقم باشد.");
        return;
    }

    // نمایش باکس وارد کردن کد ارسال شده
    document.getElementById('verificationBox').style.display = '    block';

    // شروع تایمر 2 دقیقه‌ای
    startTimer();
});

// تایمر شمارش معکوس 2 دقیقه‌ای
let timer;
let timeLeft = 120; // 2 دقیقه به ثانیه

function startTimer() {
    const timerElement = document.getElementById('timer');
    timer = setInterval(function () {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.innerText = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
        timeLeft--;

        if (timeLeft < 0) {
            clearInterval(timer);
            document.getElementById('resendCode').style.display = 'block';
        }
    }, 1000);
}

// تایید کد وارد شده
document.getElementById('verifyCodeBTN').addEventListener('click', function () {
    const verificationCode = document.getElementById('verificationCode').value;

    // فرض می‌کنیم که کد صحیح "1234" است (برای تست)
    if (verificationCode === "1234") {
        alert("رمز عبور با موفقیت تغییر یافت.");
        window.location.href = 'sign-in.html'; // هدایت به صفحه ورود
    } else {
        alert("کد وارد شده صحیح نیست.");
    }
});

// ارسال مجدد کد
document.getElementById('resendCode').addEventListener('click', function () {
    alert("کد جدید ارسال شد.");
    timeLeft = 120; // بازنشانی تایمر به 2 دقیقه
    document.getElementById('resendCode').style.display = 'none';
    startTimer(); // شروع مجدد تایمر
});
