import { signup } from './api/_api.js';
document.addEventListener("DOMContentLoaded", () => {
    const subscriptionStatus = document.getElementById('subscriptionStatus');
    const transactionList = document.getElementById('transactionList');
    const rowsPerPageSelect = document.getElementById('rowsPerPage');
    const prevPageButton = document.getElementById('prevPage');
    const nextPageButton = document.getElementById('nextPage');
    const backToChatBotButton = document.getElementById('backToChatBot');
    let currentPage = 1;
    let rowsPerPage = parseInt(rowsPerPageSelect.value);

    // داده‌های نمونه
    const transactions = [
        { date: '1402/09/10', amount: '200,000' },
        { date: '1402/08/25', amount: '500,000' },
        ...Array.from({ length: 30 }, (_, i) => ({
            date: `1402/08/${25 - i}`,
            amount: `${(200 + i * 50).toLocaleString()}`
        }))
    ];

    // مدیریت وضعیت اشتراک
    function updateSubscriptionStatus(hasSubscription, months) {
        if (hasSubscription) {
            subscriptionStatus.textContent = `اشتراک شما فعال است (${months} ماه)`;
            subscriptionStatus.style.backgroundColor = '#4caf50'; // سبز
        } else {
            subscriptionStatus.textContent = 'شما اشتراکی ندارید';
            subscriptionStatus.style.backgroundColor = '#f44336'; // قرمز
        }
    }

    // به‌روزرسانی شماره‌ها و نمایش تراکنش‌ها
    function renderTransactions() {
        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        const visibleTransactions = transactions.slice(start, end);
        transactionList.innerHTML = visibleTransactions
            .map((transaction, index) => `
                <tr>
                    <td>${start + index + 1}</td>
                    <td>${transaction.date}</td>
                    <td>${transaction.amount}</td>
                </tr>
            `)
            .join('');
    }

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
    renderTransactions();
    updatePagination();
    updateSubscriptionStatus(false, 0); // پیش‌فرض: بدون اشتراک
});
