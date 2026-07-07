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

        alert("✅ API Key Saved");

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

        alert("Please paste an incoming email.");
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

            body: JSON.stringify({

                email: email,

                tone: tone,

                additional_instruction: instruction,

                api_key: apiKey

            })

        });

        if (!response.ok) {

            throw new Error(`HTTP ${response.status}`);

        }

        const data = await response.json();

        if (data.success && data.reply) {

            replyBox.value = data.reply;

        } else {

            replyBox.value = data.error;

        }

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

        alert("Nothing to copy.");
        return;

    }

    try {

        await navigator.clipboard.writeText(reply);

        copyBtn.innerHTML = "✅ Copied!";

        setTimeout(() => {

            copyBtn.innerHTML = "📋 Copy";

        }, 1800);

    }

    catch (error) {

        alert("Copy failed.");

    }

});