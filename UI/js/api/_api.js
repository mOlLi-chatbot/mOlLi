const API_BASE_URL = "http://127.0.0.1:8000";

// ثبت‌ نام
async function signup(data) {
    const response = await fetch(`${API_BASE_URL}/auth/signup/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return await response.json();
}

// ورود
async function login(data) {
    const response = await fetch(`${API_BASE_URL}/auth/login/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return await response.json();
}

// گرفتن اطلاعات یک کاربر خاص
async function getUser(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/${id}/`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                // "Authorization": "Bearer " + token
            },
        });
        if (!response.ok) {
            throw new Error(`Failed to fetch user: ${response.statusText}`);
        }
        return await response.json(); // برمی‌گرداند اطلاعات کاربر
    } catch (error) {
        console.error("Error fetching user:", error);
        throw error; // خطا را به تابع فراخوانی می‌فرستد
    }
}

// بروزرسانی وضعیت پریمیوم کاربر
async function updatePremiumStatus(id, isPremium) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/${id}/update_premium_status/`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ is_premium: isPremium }),
        });
        if (!response.ok) {
            throw new Error(`Failed to update premium status: ${response.statusText}`);
        }
        return await response.json(); // برمی‌گرداند اطلاعات بروزرسانی شده
    } catch (error) {
        console.error("Error updating premium status:", error);
        throw error; // خطا را به تابع فراخوانی می‌فرستد
    }
}

// حذف (غیرفعال کردن) کاربر
async function deleteUser(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/${id}/`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
        });
        if (!response.ok) {
            throw new Error(`Failed to delete user: ${response.statusText}`);
        }
        return await response.json(); // برمی‌گرداند نتیجه حذف
    } catch (error) {
        console.error("Error deleting user:", error);
        throw error; // خطا را به تابع فراخوانی می‌فرستد
    }
}


export { signup, login, getUser, updatePremiumStatus, deleteUser };