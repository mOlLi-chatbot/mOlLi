import { signup } from './api/_api.js';

document.getElementById('changePasswordForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    const correctCurrentPassword = "11111111";  // رمز عبور فعلی (برای تست از یک مقدار ثابت استفاده می‌شود)

    // بررسی رمز عبور فعلی
    if (currentPassword !== correctCurrentPassword) {
        alert("رمز عبور فعلی اشتباه وارد شده است.");
        return;
    }

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

    // تایید تغییر رمز عبور
    const confirmChange = confirm("آیا مطمئن هستید که می‌خواهید رمز عبور خود را تغییر دهید؟");
    if (confirmChange) {
        alert("رمز عبور شما تغییر کرد.");
        window.location.href = 'chatbot.html';  // هدایت به صفحه چت‌بات پس از تایید تغییر رمز عبور
    }
});
