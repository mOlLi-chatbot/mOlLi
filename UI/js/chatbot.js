import { getUserChats, getAIResponse, deleteUserChats } from './api.js';

const chatInput = document.querySelector('.chat-input textarea');
const sendChatBtn = document.querySelector('#sendBTN');
const chatbox = document.querySelector(".chatbox");

// تابع ایجاد پیام جدید
const createChatItem = (message, className, lang = "en") => {
    // ایجاد عنصر <li> جدید برای نمایش پیام
    const chatItem = document.createElement("li");
    chatItem.classList.add(className, "chat");
    chatItem.innerHTML = `
        <p lang="${lang}">${message}</p>
        <span class="copy-btn"><i class="fas fa-copy"></i></span>`;
    
    // افزودن event listener برای دکمه کپی پیام
    chatItem.querySelector('.copy-btn').addEventListener('click', () => copyMessage(chatItem));
    return chatItem; // بازگشت به عنصر ایجاد شده
};

// تشخیص زبان پیام (فارسی یا انگلیسی)
const detectLanguage = (text) => {
    const persianOrArabic = /[\u0600-\u06FF]/;
    // اگر متن شامل حروف فارسی یا عربی باشد، زبان فارسی (fa) تشخیص داده می‌شود
    return persianOrArabic.test(text) ? "fa" : "en";
};

// بارگذاری تاریخچه چت کاربر
const loadUserChats = async () => {
    try {
        const userChats = await getUserChats(); // دریافت تاریخچه چت از سرور
        if (userChats.length > 0) {
            // اگر تاریخچه چت وجود داشت، پیام‌ها را بارگذاری می‌کنیم
            userChats.forEach(chat => {
                const lang = detectLanguage(chat.message); // تشخیص زبان پیام
                const chatItem = createChatItem(chat.message, "chat-incoming", lang); // ایجاد پیام
                chatbox.appendChild(chatItem); // افزودن پیام به لیست چت
            });
        } else {
            // اگر هیچ چتی وجود نداشت، پیام خوشامدگویی نمایش داده می‌شود
            const initialMessage = createChatItem("سلام! چطور می‌توانم کمکتان کنم؟", "chat-incoming", "fa");
            chatbox.appendChild(initialMessage); // نمایش پیام خوشامدگویی
        }
        chatbox.scrollTo(0, chatbox.scrollHeight); // اسکرول خودکار به پایین
    } catch (error) {
        // در صورت بروز خطا در بارگذاری تاریخچه چت، پیغام خطا نمایش داده می‌شود
        console.error("Error loading user chats:", error);
        const errorMessage = createChatItem("خطا در بارگذاری چت. لطفاً بعداً تلاش کنید.", "chat-incoming", "fa");
        chatbox.appendChild(errorMessage);
    }
};

// ارسال پیام به سرور
const handleChat = async () => {
    const userMessage = chatInput.value.trim(); // دریافت پیام کاربر

    if (!userMessage) {
        // اگر پیام خالی باشد، هشدار نمایش داده می‌شود
        alert("پیام نمی‌تواند خالی باشد!");
        return;
    }

    const lang = detectLanguage(userMessage); // تشخیص زبان پیام
    const outgoingChatItem = createChatItem(userMessage, "chat-outgoing", lang); // ایجاد پیام ارسال‌شده
    chatbox.appendChild(outgoingChatItem); // افزودن پیام ارسال‌شده به چت
    chatbox.scrollTo(0, chatbox.scrollHeight); // اسکرول خودکار به پایین
    chatInput.value = ""; // پاک کردن ورودی پیام

    try {
        const aiResponse = await getAIResponse(userMessage); // دریافت پاسخ از هوش مصنوعی
        const incomingChatItem = createChatItem(aiResponse, "chat-incoming", lang); // ایجاد پیام پاسخ از هوش مصنوعی
        chatbox.appendChild(incomingChatItem); // افزودن پاسخ به چت
    } catch (error) {
        // در صورت بروز خطا در دریافت پاسخ از هوش مصنوعی، پیغام خطا نمایش داده می‌شود
        console.error("Error getting AI response:", error);
        const errorMessage = createChatItem("خطا در دریافت پاسخ. لطفاً دوباره تلاش کنید.", "chat-incoming", "fa");
        chatbox.appendChild(errorMessage);
    }
    chatbox.scrollTo(0, chatbox.scrollHeight); // اسکرول خودکار به پایین
};

// کپی پیام
const copyMessage = (chatItem) => {
    const messageText = chatItem.querySelector("p").textContent; // استخراج متن پیام
    if (navigator.clipboard) {
        // بررسی پشتیبانی مرورگر از قابلیت کپی به کلیپ‌بورد
        navigator.clipboard.writeText(messageText)
            .then(() => alert("پیام کپی شد!")) // نمایش پیام موفقیت‌آمیز
            .catch(() => alert("خطا در کپی کردن پیام!")); // در صورت بروز خطا
    } else {
        alert("مرورگر شما از قابلیت کپی پشتیبانی نمی‌کند."); // اگر مرورگر از کپی پشتیبانی نمی‌کند
    }
};

// افزودن event listener برای دکمه ارسال پیام
sendChatBtn.addEventListener("click", handleChat);

// افزودن event listener برای ارسال پیام با کلید Enter
chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        e.preventDefault(); // جلوگیری از ارسال فرم با Enter
        handleChat(); // فراخوانی تابع ارسال پیام
    }
});

// پاک کردن چت
const clearChat = async () => {
    try {
        await deleteUserChats(); // حذف تاریخچه چت از سرور
        chatbox.innerHTML = ''; // پاک کردن محتوای چت باکس
        const initialMessage = createChatItem("سلام! چطور می‌توانم کمکتان کنم؟", "chat-incoming", "fa");
        chatbox.appendChild(initialMessage); // نمایش پیام خوشامدگویی پس از پاکسازی
        alert("چت شما پاک شد!"); // نمایش پیغام تایید
    } catch (error) {
        console.error("Error clearing chat:", error);
        alert("خطا در پاک کردن تاریخچه چت."); // در صورت بروز خطا در پاکسازی
    }
};

// بارگذاری تاریخچه چت در ابتدای صفحه
loadUserChats();
