const API_BASE_URL = "http://127.0.0.1:8000";
const headers = {
    "Authorization": "Bearer YOUR_TOKEN_HERE",
    "Content-Type": "application/json"
};

// ثبت‌ نام
async function signup(data) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/users/auth/signup/`, {
            method: "POST",
            headers: headers,
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || "خطای ناشناخته");
        }

        return await response.json();
    } catch (error) {
        console.error("Signup API error:", error);
        throw error;
    }
}

// ورود
async function signin(username, password) {
    const url = `${API_BASE_URL}/api/users/auth/login/`;

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: headers,
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || "خطای ناشناخته");
        }
        localStorage.setItem("authToken", data.token);
        return await response.json();
    } catch (error) {
        console.error("Login API error:", error);
        throw error;
    }
}


// گرفتن اطلاعات یک کاربر خاص
async function getUser(token) {
    const response = await fetch(`${API_BASE_URL}/api/users/auth/get_user/`, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    if (!response.ok) {
        throw new Error("خطا در دریافت اطلاعات کاربر");
    }

    return await response.json();
}

// بروزرسانی وضعیت پریمیوم کاربر
async function updatePremiumStatus(id, isPremium) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/users/users/${id}/update_premium_status/`, {
            method: "PATCH",
            headers: headers,
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
        const response = await fetch(`${API_BASE_URL}/api/users/users/${id}/`, {
            method: "DELETE",
            headers: headers,
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

// دریافت تاریخچه چت کاربر
const getUserChats = async () => {
    const date = new Date().toISOString();
    const response = await fetch(`${API_BASE_URL}/api/users/get_user_chats/`, {
        method: "GET",
        headers: headers,
        body: JSON.stringify({ date })
    });

    if (response.ok) {
        const data = await response.json();
        return data.chats || [];
    }
    return [];
};

// ارسال پیام به هوش مصنوعی و دریافت پاسخ
const getAIResponse = async (userMessage) => {
    const response = await fetch(`${API_BASE_URL}/api/chat/aichat/get_ai_response/`, {
        method: "GET",
        headers: headers,
        body: JSON.stringify({ user_message: userMessage })
    });

    if (response.ok) {
        const data = await response.json();
        return data.response || "متاسفم، پاسخ مناسبی یافت نشد.";
    }
    return "خطا در دریافت پاسخ از هوش مصنوعی.";
};

// پاک کردن تاریخچه چت کاربر
const deleteUserChats = async () => {
    const username = "amirjafari"; // باید به نام کاربری واقعی تغییر دهید
    const response = await fetch(`${API_BASE_URL}/api/chat/aichat/delete_user_chats/`, {
        method: "DELETE",
        headers: headers,
        body: JSON.stringify({ username })
    });

    if (!response.ok) {
        alert("خطا در پاک کردن تاریخچه چت.");
    }
};

export { signup, signin, getUser, updatePremiumStatus, deleteUser, getUserChats, getAIResponse, deleteUserChats };