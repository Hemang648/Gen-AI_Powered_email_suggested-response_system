// ===============================
// Configuration
// ===============================

// Change this after deployment
const API_URL = "https://gen-ai-powered-email-suggested-response.onrender.com/generate";
// Example:
// const API_URL = "https://your-app.up.railway.app/generate";


// ===============================
// DOM Elements
// ===============================

const apiKeyInput = document.getElementById("apiKey");
const saveBtn = document.getElementById("saveKey");

const generateBtn = document.getElementById("generateBtn");
const copyBtn = document.getElementById("copyBtn");

const emailInput = document.getElementById("email");
const toneInput = document.getElementById("tone");
const instructionInput = document.getElementById("instruction");
const replyBox = document.getElementById("reply");

const toast = document.getElementById("toast");
const toastMessage = document.getElementById("toastMessage");

function showToast(message, type = "success") {

    toastMessage.textContent = message;

    toast.className = `toast show ${type}`;

    setTimeout(() => {

        toast.className = "toast";

    }, 2500);

}
// ===============================
// DOCUMENTS and password
// ===============================

const lengthInput=document.getElementById("length");

const togglePassword=document.getElementById("togglePassword");

const eyeOpen = document.getElementById("eyeOpen");
const eyeClosed = document.getElementById("eyeClosed");

// ===============================
// Load Saved API Key
// ===============================
console.log("chrome =", chrome);
console.log("chrome.storage =", chrome.storage);
console.log("chrome.storage.local =", chrome.storage?.local);
chrome.storage.local.get(["geminiKey"], (result) => {

    if (result.geminiKey) {

        apiKeyInput.value = result.geminiKey;

    }

});


// ===============================
// Save API Key
// ===============================

saveBtn.addEventListener("click", () => {

    const key = apiKeyInput.value.trim();

    if (!key) {

        alert("Please enter a Gemini API key.");
        return;

    }

    chrome.storage.local.set({

        geminiKey: key

    }, () => {

        showToast("API Key Saved");

    });

});


// ===============================
// Loading State
// ===============================

function setLoading(isLoading) {

    if (isLoading) {

        generateBtn.disabled = true;
        generateBtn.innerHTML = "⏳ Generating...";
        replyBox.value = "";

    } else {

        generateBtn.disabled = false;
        generateBtn.innerHTML = "✨ Generate Reply";

    }

}


// ===============================
// Generate Reply
// ===============================

generateBtn.addEventListener("click", async () => {

    const email = emailInput.value.trim();
    const tone = toneInput.value;
    const instruction = instructionInput.value.trim();
    const apiKey = apiKeyInput.value.trim();

    if (!email) {

        showToast("Please paste an email","error");
        emailInput.focus();
        return;

    }

    setLoading(true);

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body:JSON.stringify({

                    email,

                    tone,

                    length:lengthInput.value,

                    additional_instruction:instruction,

                    api_key:apiKey

                })

        });

        const data = await response.json();

if (!response.ok || !data.success) {

    replyBox.value = "❌ " + (data.error || "Unknown error");

    showToast(data.error || "Request failed", "error");

    return;

}

replyBox.value = data.reply;

    }

    catch (error) {

        console.error(error);

        replyBox.value =
`❌ Unable to generate reply.

Possible reasons:

• Backend server is not running
• Wrong API URL
• Invalid Gemini API Key
• Internet connection issue`;

    }

    finally {

        setLoading(false);

    }

});


// ===============================
// Copy Reply
// ===============================

copyBtn.addEventListener("click", async () => {

    const reply = replyBox.value.trim();

    if (!reply) {

        showToast("Nothing to copy","error");
        return;

    }

    try {

        await navigator.clipboard.writeText(reply);

        showToast("Reply copied");

        setTimeout(() => {

            copyBtn.innerHTML = "📋 Copy";

        }, 1800);

    }

    catch (error) {

        showToast("Copy failed","error");

    }

});

// ===============================
// SHOW / HIDE BOTTON
// ===============================

togglePassword.addEventListener("click", () => {

    const hidden = apiKeyInput.type === "password";

    apiKeyInput.type = hidden ? "text" : "password";

    eyeOpen.style.display = hidden ? "none" : "block";
    eyeClosed.style.display = hidden ? "block" : "none";

});