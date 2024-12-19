import { getUser } from './api/_api.js';

document.addEventListener("DOMContentLoaded", () => {
    const rowsPerPageSelect = document.getElementById('rowsPerPage');
    const prevPageButton = document.getElementById('prevPage');
    const nextPageButton = document.getElementById('nextPage');
    const backToChatBotButton = document.getElementById('backToChatBot');
    let currentPage = 1;
    let rowsPerPage = parseInt(rowsPerPageSelect.value);
    
    const subscriptionStatus = document.getElementById('subscriptionStatus');
    const transactionList = document.getElementById('transactionList');
    const API_URL = "http://127.0.0.1:8000/api/users/auth/get_user/";
    const token = localStorage.getItem("authToken");

    if (!token) {
        subscriptionStatus.textContent = "لطفاً وارد شوید.";
        subscriptionStatus.style.backgroundColor = "#f44336"; // قرمز
        return;
    }
    async function fetchUserData() {
        try {
            const userData = await getUser(token);
            updateSubscriptionStatus(userData);
            renderTransactions(userData.transactions);
        } catch (error) {
            console.error("Error fetching user data:", error);
            subscriptionStatus.textContent = "خطا در دریافت اطلاعات کاربر";
        }
    }
    function updateSubscriptionStatus(userData) {
        if (userData.ispremium && userData.last_transaction) {
            const { last_transaction } = userData;
            const paymentDate = new Date(last_transaction.date);
            const monthsPaid = last_transaction.months || 0;
            const expiryDate = new Date(paymentDate);
            expiryDate.setMonth(expiryDate.getMonth() + monthsPaid);

            subscriptionStatus.textContent = `اشتراک شما فعال است تا تاریخ ${expiryDate.toLocaleDateString("fa-IR")}`;
            subscriptionStatus.style.backgroundColor = "#4caf50"; // سبز
        } else {
            subscriptionStatus.textContent = "شما اشتراکی ندارید";
            subscriptionStatus.style.backgroundColor = "#f44336"; // قرمز
        }
    }
    function renderTransactions(transactions) {
        if (!transactions || transactions.length === 0) {
            transactionList.innerHTML = "<tr><td colspan='3'>تراکنشی یافت نشد</td></tr>";
            return;
        }

        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        const visibleTransactions = transactions.slice(start, end);

        transactionList.innerHTML = visibleTransactions
            .map((transaction, index) => `
                <tr>
                    <td>${start + index + 1}</td>
                    <td>${new Date(transaction.date).toLocaleDateString("fa-IR")}</td>
                    <td>${parseInt(transaction.amount).toLocaleString()} تومان</td>
                </tr>
            `)
            .join("");
    }
    
/*    // داده‌های نمونه
    const transactions = [
        { date: '1402/09/10', amount: '200,000' },
        { date: '1402/08/25', amount: '500,000' },
        ...Array.from({ length: 30 }, (_, i) => ({
            date: `1402/08/${25 - i}`,
            amount: `${(200 + i * 50).toLocaleString()}`
        }))
    ];
*/

    // مدیریت صفحه‌بندی
    function updatePagination() {
        prevPageButton.disabled = currentPage === 1;
        nextPageButton.disabled = currentPage * rowsPerPage >= transactions.length;
    }

    rowsPerPageSelect.addEventListener('change', () => {
        rowsPerPage = parseInt(rowsPerPageSelect.value);
        currentPage = 1;
        renderTransactions();
        updatePagination();
    });

    prevPageButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderTransactions();
            updatePagination();
        }
    });

    nextPageButton.addEventListener('click', () => {
        if (currentPage * rowsPerPage < transactions.length) {
            currentPage++;
            renderTransactions();
            updatePagination();
        }
    });

    // دکمه بازگشت
    backToChatBotButton.addEventListener('click', () => {
        window.location.href = '/ChatBot.html'; // لینک صفحه بازگشت
    });

    // بارگذاری اولیه
    fetchUserData();
});
