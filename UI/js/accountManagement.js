import { signup } from './api/_api.js';

// Function to handle logout
function handleLogout() {
    const confirmLogOut = confirm("آیا مطمئن هستید که می‌خواهید از حساب خود خارج شوید؟");
    if (confirmLogOut) {
        alert("از حساب خود خارج شدید.");
        window.location.href = 'index.html';
    }
}
document.getElementById('logoutBTN').addEventListener('click', handleLogout);

// Function to handle account deletion
function handleAccountDeletion() {
    const confirmDelete = confirm("آیا مطمئن هستید که می‌خواهید حساب خود را پاک کنید؟ این عملیات غیرقابل بازگشت است.");
    if (confirmDelete) {
        alert("حساب شما پاک شد.");
        window.location.href = 'index.html';
    }
}
document.getElementById('deleteAccountBTN').addEventListener('click', handleAccountDeletion);

// Redirect to the ChangePassword page
function redirectToChangePassword() {
    window.location.href = 'ChangePassword.html';
}
document.getElementById('changePasswordBTN').addEventListener('click', redirectToChangePassword);
