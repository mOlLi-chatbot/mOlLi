const API_BASE_URL = "http://127.0.0.1:8000";

// تابع برای دریافت هدرها (شامل Authorization با استفاده از توکن ذخیره‌شده)
const getHeaders = () => ({
    'Authorization': `Bearer ${localStorage.getItem('authToken')}`, // دریافت توکن از localStorage و اضافه کردن به هدر
    'Content-Type': 'application/json', // نوع محتوا به صورت JSON
});

// ثبت‌نام
async function signup(data) {
    return await apiRequest(`${API_BASE_URL}/api/users/auth/signup/`, "POST", data); // ارسال درخواست POST برای ثبت‌نام
}

// ورود (لاگین)
async function signin(username, password) {
    // ارسال درخواست POST برای ورود
    const data = await apiRequest(`${API_BASE_URL}/api/users/auth/login/`, "POST", { username, password });
    // ذخیره توکن دریافتی از سرور در localStorage
    localStorage.setItem("authToken", data.token);
    return data; // بازگشت اطلاعات دریافتی از سرور
}

// گرفتن اطلاعات یک کاربر خاص
async function getUser() {
    // ارسال درخواست GET برای دریافت اطلاعات کاربر
    return await apiRequest(`${API_BASE_URL}/api/users/auth/get_user/`, "GET");
}

// بروزرسانی وضعیت پریمیوم کاربر
async function updatePremiumStatus(id, isPremium) {
    // ارسال درخواست PATCH برای بروزرسانی وضعیت پریمیوم کاربر
    return await apiRequest(`${API_BASE_URL}/api/users/users/${id}/update_premium_status/`, "PATCH", { isPremium });
}

// حذف (غیرفعال کردن) کاربر
async function deleteUser() {
    // ارسال درخواست DELETE برای حذف یا غیرفعال کردن کاربر
    return await apiRequest(`${API_BASE_URL}/api/users/users/`, "DELETE");
}

// دریافت تاریخچه چت کاربر
async function getUserChats() {
    const date = new Date().toISOString(); // دریافت تاریخ و زمان جاری به فرمت ISO
    // ارسال درخواست GET برای دریافت تاریخچه چت‌های کاربر
    return await apiRequest(`${API_BASE_URL}/api/users/get_user_chats/?date=${encodeURIComponent(date)}`, "GET");
}

// ارسال پیام به هوش مصنوعی و دریافت پاسخ
async function getAIResponse(userMessage) {
    if (userMessage.length > 5000) {
        // بررسی طول پیام، اگر بیشتر از 5000 کاراکتر باشد خطا می‌دهد
        throw new Error("پیام شما بیش از حد طولانی است.");
    }
    // ارسال درخواست GET برای ارسال پیام به هوش مصنوعی و دریافت پاسخ
    return await apiRequest(`${API_BASE_URL}/api/chat/aichat/get_ai_response/?user_message=${encodeURIComponent(userMessage)}`, "GET");
}

// پاک کردن تاریخچه چت کاربر
async function deleteUserChats() {
    // ارسال درخواست DELETE برای پاک کردن تاریخچه چت‌های کاربر
    return await apiRequest(`${API_BASE_URL}/api/chat/aichat/delete_user_chats/`, "DELETE");
}

// تابع عمومی برای ارسال درخواست به API
async function apiRequest(url, method, body = null) {
    const headers = getHeaders(); // دریافت هدرها
    const options = { method, headers }; // تنظیمات درخواست با متد و هدرها
    if (body) options.body = JSON.stringify(body); // اگر بدنه‌ای وجود داشت، آن را به فرمت JSON تبدیل می‌کنیم
    
    // ارسال درخواست با استفاده از fetch API
    const response = await fetch(url, options);
    if (!response.ok) {
        // در صورت بروز خطا در درخواست، خطا را لاگ کرده و خطای مناسب را پرتاب می‌کنیم
        const errorData = await response.json();
        console.error("API Request Error:", errorData);
        throw new Error(errorData.message || "خطای ناشناخته");
    }
    // اگر درخواست موفق بود، داده‌های پاسخ را برمی‌گردانیم
    return await response.json();
}

// صادرات توابع برای استفاده در دیگر فایل‌ها
export { signup, signin, getUser, updatePremiumStatus, deleteUser, getUserChats, getAIResponse, deleteUserChats };
