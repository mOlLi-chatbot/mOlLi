import { signup } from './api/_api.js';

document.getElementById("signupForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    //const phone = document.getElementById("phone").value.trim();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const email = document.getElementById("email").value.trim();
    const terms = document.getElementById("terms").checked;
    const errorMessage = document.getElementById("errorMessage");

    errorMessage.textContent = ""; // Clear previous errors

    // Validating required fields
    if (!email || !username || !password || !confirmPassword) {
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

    // Validating birthDate in Jalali format
    /*const currentYearJalali = moment().jYear();
    const enteredDate = moment(birthDate, "jYYYY/jMM/jDD", true);
    if (!enteredDate.isValid()) {
        errorMessage.textContent = "تاریخ تولد باید به فرمت شمسی (مثال: 1400/05/10) باشد.";
        return;
    }
    const enteredYear = enteredDate.jYear();
    if (enteredYear < 1300 || enteredYear > currentYearJalali) {
        errorMessage.textContent = `تاریخ تولد باید بین سال 1300 تا ${currentYearJalali} باشد.`;
        return;
    }
*/
    //api
    const data = { username, email, password };
    try {
        const response = await signup(data);

        if (response.id) {
            alert("ثبت نام با موفقیت انجام شد!");
            console.log("Response:", response);
        } else {
            alert("Signup failed: " + JSON.stringify(response));
        }
    } catch (error) {
        console.error("Error during signup:", error);
        alert("An error occurred. Please try again.");
    }

    // Redirect to chatbot page on successful validation
    window.location.href = "chatbot.html";
    document.getElementById("signupForm").reset();
});
