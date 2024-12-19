import { getUserChats, getAIResponse, deleteUserChats } from './api.js';

const chatInput = document.querySelector('.chat-input textarea');
const sendChatBtn = document.querySelector('#sendBTN');
const chatbox = document.querySelector(".chatbox");

// تابع ایجاد پیام جدید
const createChatItem = (message, className, lang = "en") => {
    const chatItem = document.createElement("li");
    chatItem.classList.add(className, "chat");
    chatItem.innerHTML = `
        <p lang="${lang}">${message}</p>
        <span class="copy-btn" onclick="copyMessage(this)"><i class="fas fa-copy"></i></span>`;
    chatItem.querySelector('.copy-btn').addEventListener('click', () => copyMessage(chatItem.querySelector('.copy-btn')));
    return chatItem;
};

// تشخیص زبان پیام
const detectLanguage = (text) => {
    const persianOrArabic = /[\u0600-\u06FF]/;
    return persianOrArabic.test(text) ? "fa" : "en";
};

// بارگذاری تاریخچه چت کاربر
const loadUserChats = async () => {
    const userChats = await getUserChats();
    if (userChats && userChats.length > 0) {
        userChats.forEach(chat => {
            const lang = detectLanguage(chat.message);
            const chatItem = createChatItem(chat.message, "chat-incoming", lang);
            chatbox.appendChild(chatItem);
        });
    } else {
        const initialMessage = createChatItem("سلام! چطور می‌توانم کمکتان کنم؟", "chat-incoming", "fa");
        chatbox.appendChild(initialMessage);
    }
    chatbox.scrollTo(0, chatbox.scrollHeight);
};

// ارسال پیام به سرور
const handleChat = async () => {
    const userMessage = chatInput.value.trim();

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

    // دریافت پاسخ از هوش مصنوعی
    const aiResponse = await getAIResponse(userMessage);
    const incomingChatItem = createChatItem(aiResponse, "chat-incoming", lang);
    chatbox.appendChild(incomingChatItem);
    chatbox.scrollTo(0, chatbox.scrollHeight);
};

// کپی پیام
const copyMessage = (button) => {
    const messageText = button.previousElementSibling.textContent;
    navigator.clipboard.writeText(messageText)
        .then(() => alert("پیام کپی شد!"))
        .catch((err) => alert("خطا در کپی کردن پیام!"));
};
/*
document.querySelectorAll('.copy-btn').forEach(button => {
    button.addEventListener('click', () => copyMessage(button));
});
*/
sendChatBtn.addEventListener("click", handleChat);
chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        handleChat();
    }
});

// پاک کردن چت
const clearChat = async () => {
    await deleteUserChats();
    chatbox.innerHTML = '';
    const initialMessage = createChatItem("سلام! چطور می‌توانم کمکتان کنم؟", "chat-incoming", "fa");
    chatbox.appendChild(initialMessage);
    alert("چت شما پاک شد!");
};

// اضافه کردن event listenerها
sendChatBtn.addEventListener("click", handleChat);
chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        handleChat();
    }
});

// منوی کناری
const sidebarToggle = document.getElementById('sidebarToggle');
const dropdownContent = document.querySelector('.dropdown-content');

// نمایش/مخفی کردن dropdown
sidebarToggle.addEventListener('click', () => {
    dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
});

// مخفی کردن dropdown زمانی که روی هر گزینه کلیک می‌شود
const dropdownItem = document.getElementById('clearchat');
dropdownItem.addEventListener('click', clearChat);

// مخفی کردن dropdown وقتی که کاربر در خارج از آن کلیک می‌کند
document.addEventListener('click', (event) => {
    if (!sidebarToggle.contains(event.target) && !dropdownContent.contains(event.target)) {
        dropdownContent.style.display = 'none';
    }
});

document.getElementById('accountmanagement').addEventListener('click', () => {
    window.location.href = 'AccountManagement.html';
});

document.getElementById('payment').addEventListener('click', () => {
    window.location.href = 'Payment.html';
});

document.getElementById('clearchat').addEventListener('click', clearChat);

// بارگذاری تاریخچه چت در ابتدای صفحه
loadUserChats();
