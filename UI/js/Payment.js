import { getUser } from './api/_api.js';

document.addEventListener("DOMContentLoaded", () => {
    const rowsPerPageSelect = document.getElementById('rowsPerPage');
    const prevPageButton = document.getElementById('prevPage');
    const nextPageButton = document.getElementById('nextPage');
    const backToChatBotButton = document.getElementById('backToChatBot');
    
    let currentPage = 1;
    let rowsPerPage = parseInt(rowsPerPageSelect.value); // تعداد ردیف‌ها در هر صفحه
    
    const subscriptionStatus = document.getElementById('subscriptionStatus');
    const transactionList = document.getElementById('transactionList');
    
    // گرفتن توکن از localStorage
    const token = localStorage.getItem("authToken");
    if (!token) {
        subscriptionStatus.textContent = "لطفاً وارد شوید.";
        subscriptionStatus.style.backgroundColor = "#f44336"; // قرمز
        return; // اگر توکن موجود نباشد، از اینجا خارج می‌شویم
    }

    // تابع برای بارگذاری داده‌های کاربر از API
    async function fetchUserData() {
        try {
            const userData = await getUser(); // فراخوانی تابع getUser بدون نیاز به ارسال توکن
            updateSubscriptionStatus(userData); // بروزرسانی وضعیت اشتراک
            if (userData.transactions && userData.transactions.length > 0) {
                renderTransactions(userData.transactions); // رندر تراکنش‌ها
                updatePagination(userData.transactions); // بروزرسانی صفحه‌بندی
            } else {
                transactionList.innerHTML = "<tr><td colspan='3'>تراکنشی یافت نشد</td></tr>"; // اگر تراکنش‌ها نباشند
            }
        } catch (error) {
            console.error("Error fetching user data:", error); // چاپ خطا در کنسول
            subscriptionStatus.textContent = "خطا در دریافت اطلاعات کاربر"; // نمایش پیام خطا به کاربر
            subscriptionStatus.style.backgroundColor = "#f44336"; // رنگ قرمز برای خطا
        }
    }

    // بروزرسانی وضعیت اشتراک
    function updateSubscriptionStatus(userData) {
        if (userData.ispremium && userData.last_transaction) {
            const { last_transaction } = userData;
            const paymentDate = new Date(last_transaction.date); // تبدیل تاریخ تراکنش به شیء Date
            const monthsPaid = last_transaction.months || 0;
            const expiryDate = new Date(paymentDate);
            expiryDate.setMonth(expiryDate.getMonth() + monthsPaid); // محاسبه تاریخ انقضا اشتراک

            subscriptionStatus.textContent = `اشتراک شما فعال است تا تاریخ ${expiryDate.toLocaleDateString("fa-IR")}`; // نمایش تاریخ انقضا
            subscriptionStatus.style.backgroundColor = "#4caf50"; // رنگ سبز برای اشتراک فعال
        } else {
            subscriptionStatus.textContent = "شما اشتراکی ندارید"; // در صورتی که اشتراکی نباشد
            subscriptionStatus.style.backgroundColor = "#f44336"; // رنگ قرمز برای اشتراک غیرفعال
        }
    }

    // رندر تراکنش‌ها
    function renderTransactions(transactions) {
        if (!transactions || transactions.length === 0) {
            transactionList.innerHTML = "<tr><td colspan='3'>تراکنشی یافت نشد</td></tr>";
            return; // اگر تراکنش‌ها موجود نیستند، پیامی برای کاربر نمایش می‌دهیم
        }

        const start = (currentPage - 1) * rowsPerPage; // شروع از صفحه جاری
        const end = start + rowsPerPage; // پایان صفحه جاری
        const visibleTransactions = transactions.slice(start, end); // برش دادن تراکنش‌ها برای نمایش صفحه جاری

        transactionList.innerHTML = visibleTransactions
            .map((transaction, index) => `
                <tr>
                    <td>${start + index + 1}</td>
                    <td>${new Date(transaction.date).toLocaleDateString("fa-IR")}</td>
                    <td>${parseInt(transaction.amount).toLocaleString()} تومان</td>
                </tr>
            `)
            .join(""); // نمایش تراکنش‌ها
    }

    // بروزرسانی صفحه‌بندی
    function updatePagination(transactions) {
        prevPageButton.disabled = currentPage === 1; // دکمه قبلی غیرفعال در صفحه اول
        nextPageButton.disabled = currentPage * rowsPerPage >= transactions.length; // دکمه بعدی غیرفعال در آخرین صفحه
    }

    // مدیریت تغییرات در تعداد ردیف‌ها در هر صفحه
    rowsPerPageSelect.addEventListener('change', () => {
        rowsPerPage = parseInt(rowsPerPageSelect.value); // به روز رسانی تعداد ردیف‌ها
        currentPage = 1; // صفحه به اول باز می‌گردد
        fetchUserData(); // بارگذاری مجدد داده‌ها
    });

    // مدیریت صفحه قبلی
    prevPageButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--; // کاهش شماره صفحه
            fetchUserData(); // بارگذاری مجدد داده‌ها
        }
    });

    // مدیریت صفحه بعدی
    nextPageButton.addEventListener('click', () => {
        fetchUserData(); // بارگذاری مجدد داده‌ها
    });

    // دکمه بازگشت به صفحه چت
    backToChatBotButton.addEventListener('click', () => {
        window.location.href = '/ChatBot.html'; // لینک صفحه بازگشت
    });

    // بارگذاری اولیه داده‌ها هنگام بارگذاری صفحه
    fetchUserData();
});
