document.addEventListener("DOMContentLoaded", () => {
    const loginButton = document.querySelector(".login-container button");
    const usernameInput = document.querySelector(".login-container input[type='text']");
    const passwordInput = document.querySelector(".login-container input[type='password']");

    let messageContainer = document.querySelector(".message-container");
    if (!messageContainer) {
        messageContainer = document.createElement("div");
        messageContainer.className = "message-container";
        document.body.appendChild(messageContainer);
    }

    const displayMessage = (message, isError = false) => {
        messageContainer.textContent = message;
        messageContainer.style.padding = "10px";
        messageContainer.style.marginBottom = "10px";
        messageContainer.style.borderRadius = "4px";
        messageContainer.style.textAlign = "center";
        messageContainer.style.fontFamily = "Arial, sans-serif";
        messageContainer.style.fontSize = "14px";
        messageContainer.style.color = isError ? "#a94442" : "#3c763d";
        messageContainer.style.backgroundColor = isError ? "#f2dede" : "#dff0d8";
        messageContainer.style.border = isError ? "1px solid #ebccd1" : "1px solid #d6e9c6";
        messageContainer.style.display = "block";

        // Автоматическое скрытие сообщения через 3 секунды
        setTimeout(() => {
            messageContainer.style.display = "none";
        }, 3000);
    };

    const setButtonState = (isDisabled) => {
        loginButton.disabled = isDisabled;
        if (isDisabled) {
            loginButton.innerHTML = '<span class="spinner"></span> Processing...';
        } else {
            loginButton.innerHTML = 'Login';
        }
    };

    const spinnerStyle = document.createElement("style");
    spinnerStyle.innerHTML = `
        .spinner {
            border: 2px solid #f3f3f3;
            border-top: 2px solid #3498db;
            border-radius: 50%;
            width: 14px;
            height: 14px;
            display: inline-block;
            animation: spin 1s linear infinite;
            vertical-align: middle;
            margin-right: 5px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .message-container {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            min-width: 300px;
        }
    `;
    document.head.appendChild(spinnerStyle);

    loginButton.addEventListener("click", async () => {
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        if (!username || !password) {
            displayMessage("Please enter your username and password.", true);
            return;
        }
        if (password.length < 6) {
            displayMessage("Password must be at least 6 characters long.", true);
            return;
        }

        setButtonState(true);

        try {
            const response = await fetch("/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (!response.ok) {
                displayMessage(`Login failed: ${data.message || "Unknown error"}`, true);
                return;
            }

            
            displayMessage("Login successful!");
            console.log("Login successful:", data);

            localStorage.setItem("token", data.token);
            window.location.href = "/main"; 

        } catch (error) {
            console.error("Error during login:", error);
            displayMessage("An error occurred while trying to login. Please try again later.", true);
        } finally {
            setButtonState(false);
        }
    });
});
