document.getElementById('logoutBTN').addEventListener('click', function () {
    // Redirect to the Index page on logout
    const confirmLogOut = confirm("آیا مطمئن هستید که می‌خواهید از حساب خود خارج شوید؟");
    
    if (confirmLogOut) {
        // Redirect to the Index page after account deletion confirmation
        alert("از حساب خود خارج شدید.");
        window.location.href = 'index.html';
    }
    window.location.href = 'index.html';
});

document.getElementById('deleteAccountBTN').addEventListener('click', function () {
    // Show a confirmation prompt for account deletion
    const confirmDelete = confirm("آیا مطمئن هستید که می‌خواهید حساب خود را پاک کنید؟ این عملیات غیرقابل بازگشت است.");
    
    if (confirmDelete) {
        // Redirect to the Index page after account deletion confirmation
        alert("حساب شما پاک شد.");
        window.location.href = 'index.html';
    }
});

document.getElementById('changePasswordBTN').addEventListener('click', function () {
    // Redirect to the ChangePassword page
    window.location.href = 'ChangePassword.html';
});
