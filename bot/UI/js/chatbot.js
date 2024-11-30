const chatInput = document.querySelector('.chat-input textarea');
const sendChatBtn = document.querySelector('#sendBTN');
const chatbox = document.querySelector(".chatbox");

// تابع ایجاد پیام جدید
const createChatItem = (message, className, lang = "en") => {
    const chatItem = document.createElement("li");
    chatItem.classList.add("chat", className);
    chatItem.innerHTML = `
        <p lang="${lang}">${message}</p>
        <span class="copy-btn" onclick="copyMessage(this)">📋</span>`;
    return chatItem;
};

// تشخیص زبان پیام
const detectLanguage = (text) => {
    const persianOrArabic = /[\u0600-\u06FF]/;
    return persianOrArabic.test(text) ? "fa" : "en";
};

// شبیه‌سازی پاسخ
const simulateResponse = () => {
    const responseMessage = "من اینجا هستم تا کمک کنم!";
    const lang = detectLanguage(responseMessage);
    setTimeout(() => {
        const incomingChatItem = createChatItem(responseMessage, "chat-incoming", lang);
        chatbox.appendChild(incomingChatItem);
        chatbox.scrollTo(0, chatbox.scrollHeight);
    }, 1000);
};

// ارسال پیام
const handleChat = () => {
    const userMessage = chatInput.value.trim();

    // بررسی محدودیت کاراکتر
    if (userMessage.length > 5000) {
        alert("پیام شما بیش از 5000 کاراکتر است و ارسال نمی‌شود!");
        return;
    }

    if (!userMessage) return;

    const lang = detectLanguage(userMessage);
    const outgoingChatItem = createChatItem(userMessage, "chat-outgoing", lang);
    chatbox.appendChild(outgoingChatItem);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    chatInput.value = "";

    simulateResponse();
};

// کپی پیام
const copyMessage = (button) => {
    const messageText = button.previousElementSibling.textContent;
    navigator.clipboard.writeText(messageText)
        .then(() => alert("پیام کپی شد!"))
        .catch((err) => alert("خطا در کپی کردن پیام!"));
};

sendChatBtn.addEventListener("click", handleChat);
chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        handleChat();
    }
});

const sidebarToggle = document.getElementById('sidebarToggle');
const dropdownContent = document.querySelector('.dropdown-content');

// نمایش/مخفی کردن dropdown
sidebarToggle.addEventListener('click', () => {
    dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
});

// مخفی کردن dropdown زمانی که روی هر گزینه کلیک می‌شود
const dropdownItems = document.querySelectorAll('.dropdown-item');
dropdownItems.forEach(item => {
    item.addEventListener('click', () => {
        dropdownContent.style.display = 'none';
        // در اینجا می‌توانید عملکرد هر گزینه را اضافه کنید
        alert(`${item.textContent} clicked!`);
    });
});

// مخفی کردن dropdown وقتی که کاربر در خارج از آن کلیک می‌کند
document.addEventListener('click', (event) => {
    if (!sidebarToggle.contains(event.target) && !dropdownContent.contains(event.target)) {
        dropdownContent.style.display = 'none';
    }
});