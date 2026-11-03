
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Login credentials
INBUILT_USER_NAME = "admin"
INBUILT_USER_PASSWORD = "admin123"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Login</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', sans-serif;
        }

        body {
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #0f172a, #312e81, #6d28d9);
            padding: 20px;
            overflow-x: hidden;
        }

        .background-circle {
            position: fixed;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            filter: blur(2px);
            opacity: 0.4;
            animation: float 6s ease-in-out infinite;
        }

        .circle-one {
            background: #a78bfa;
            top: -100px;
            left: -80px;
        }

        .circle-two {
            background: #22d3ee;
            bottom: -120px;
            right: -60px;
            animation-delay: 2s;
        }

        .login-container {
            width: 100%;
            max-width: 900px;
            min-height: 520px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            background: rgba(255, 255, 255, 0.10);
            border: 1px solid rgba(255, 255, 255, 0.22);
            border-radius: 25px;
            overflow: hidden;
            backdrop-filter: blur(20px);
            box-shadow: 0 25px 70px rgba(0, 0, 0, 0.3);
            position: relative;
            z-index: 1;
        }

        .welcome-panel {
            padding: 45px 35px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white;
            background: rgba(255, 255, 255, 0.04);
        }

        .illustration {
            width: 210px;
            height: 210px;
            border-radius: 50%;
            background: linear-gradient(145deg, #a78bfa, #22d3ee);
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 95px;
            margin-bottom: 30px;
            box-shadow: 0 0 50px rgba(167, 139, 250, 0.35);
            animation: float 4s ease-in-out infinite;
        }

        .welcome-panel h1 {
            font-size: 30px;
            margin-bottom: 12px;
        }

        .welcome-panel p {
            color: #ddd6fe;
            line-height: 1.7;
            max-width: 300px;
        }

        .form-panel {
            padding: 55px 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            color: white;
        }

        .form-panel h2 {
            font-size: 32px;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #c4b5fd;
            margin-bottom: 32px;
        }

        .input-group {
            margin-bottom: 22px;
        }

        .input-group label {
            display: block;
            margin-bottom: 9px;
            font-size: 14px;
            color: #f3f0ff;
        }

        .input-box {
            display: flex;
            align-items: center;
            border: 1px solid rgba(255, 255, 255, 0.25);
            background: rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 0 14px;
            transition: 0.3s;
        }

        .input-box:focus-within {
            border-color: #a78bfa;
            box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15);
        }

        .input-box span {
            font-size: 19px;
            margin-right: 10px;
        }

        .input-box input {
            width: 100%;
            padding: 15px 0;
            background: transparent;
            border: none;
            outline: none;
            color: white;
            font-size: 15px;
        }

        .input-box input::placeholder {
            color: #c4b5fd;
        }

        .toggle-password {
            cursor: pointer;
            font-size: 13px !important;
            margin: 0 !important;
            color: #c4b5fd;
            user-select: none;
        }

        .login-btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 12px;
            color: white;
            background: linear-gradient(90deg, #7c3aed, #4f46e5);
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
            margin-top: 5px;
        }

        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4);
        }

        .message {
            padding: 12px;
            margin-bottom: 20px;
            border-radius: 9px;
            text-align: center;
            font-size: 14px;
        }

        .success {
            background: rgba(34, 197, 94, 0.15);
            color: #86efac;
            border: 1px solid #22c55e;
        }

        .error {
            background: rgba(239, 68, 68, 0.15);
            color: #fca5a5;
            border: 1px solid #ef4444;
        }

        .footer {
            text-align: center;
            margin-top: 25px;
            font-size: 12px;
            color: #c4b5fd;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }

        @media (max-width: 700px) {
            .login-container {
                max-width: 430px;
                grid-template-columns: 1fr;
            }

            .welcome-panel {
                padding: 30px 20px 20px;
            }

            .illustration {
                width: 110px;
                height: 110px;
                font-size: 55px;
                margin-bottom: 20px;
            }

            .welcome-panel h1 {
                font-size: 24px;
            }

            .form-panel {
                padding: 30px 25px 40px;
            }
        }
    </style>
</head>

<body>

    <div class="background-circle circle-one"></div>
    <div class="background-circle circle-two"></div>

    <div class="login-container">

        <div class="welcome-panel">
            <div class="illustration">🔐</div>
            <h1>Welcome Back!</h1>
            <p>
                Your secure space awaits.
                Sign in to continue your journey.
            </p>
        </div>

        <div class="form-panel">
            <h2>Sign In</h2>
            <p class="subtitle">Enter your credentials to continue.</p>

            {% if message %}
                <div class="message {{ status }}">
                    {{ message }}
                </div>
            {% endif %}

            <form method="POST" action="/">
                <div class="input-group">
                    <label for="username">Username</label>
                    <div class="input-box">
                        <span>👤</span>
                        <input
                            type="text"
                            id="username"
                            name="username"
                            placeholder="Enter your username"
                            autocomplete="username"
                            required>
                    </div>
                </div>

                <div class="input-group">
                    <label for="password">Password</label>
                    <div class="input-box">
                        <span>🔑</span>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            placeholder="Enter your password"
                            autocomplete="current-password"
                            required>
                        <span class="toggle-password"
                              onclick="togglePassword()">Show</span>
                    </div>
                </div>

                <button type="submit" class="login-btn">
                    Login →
                </button>
            </form>

            <div class="footer">
                © 2026 Secure Login System
            </div>
        </div>

    </div>

    <script>
        function togglePassword() {
            const password = document.getElementById("password");
            const toggle = document.querySelector(".toggle-password");

            if (password.type === "password") {
                password.type = "text";
                toggle.textContent = "Hide";
            } else {
                password.type = "password";
                toggle.textContent = "Show";
            }
        }
    </script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    status = ""

    if request.method == "POST":
        user_name = request.form.get("username", "").strip()
        user_password = request.form.get("password", "")

        if (user_name == INBUILT_USER_NAME and
                user_password == INBUILT_USER_PASSWORD):
            message = "Login successful! Welcome, admin."
            status = "success"
        else:
            message = "Invalid username or password."
            status = "error"

    return render_template_string(
        HTML_PAGE, message=message, status=status
    )

if __name__ == "__main__":
    app.run(debug=True)
