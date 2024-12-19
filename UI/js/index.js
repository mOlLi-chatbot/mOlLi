import { signup } from './api/_api.js';

// Redirect buttons
document.getElementById("signIn").addEventListener("click", function () {
    window.location.href = "signIn.html";
});

document.getElementById("signUp").addEventListener("click", function () {
    window.location.href = "signUp.html";
});
