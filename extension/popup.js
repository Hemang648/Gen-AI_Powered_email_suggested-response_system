const generateBtn = document.getElementById("generateBtn");
const copyBtn = document.getElementById("copyBtn");

const emailInput = document.getElementById("email");
const toneInput = document.getElementById("tone");
const instructionInput = document.getElementById("instruction");
const replyBox = document.getElementById("reply");

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

generateBtn.addEventListener("click", async () => {

    const email = emailInput.value.trim();
    const tone = toneInput.value;
    const instruction = instructionInput.value.trim();

    if (!email) {

        alert("Please paste an incoming email.");
        emailInput.focus();
        return;

    }

    setLoading(true);

    try {

        const response = await fetch("http://127.0.0.1:8000/generate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                email: email,

                tone: tone,

                additional_instruction: instruction

            })

        });

        if (!response.ok) {

            throw new Error(`Server Error (${response.status})`);

        }

        const data = await response.json();

        if (data.reply) {

            replyBox.value = data.reply;

        } else {

            replyBox.value = "No reply generated.";

        }

    }

    catch (error) {

        console.error(error);

        replyBox.value =
            "❌ Unable to connect to the AI server.\n\n" +
            "Make sure:\n" +
            "• FastAPI is running\n" +
            "• Internet is available\n" +
            "• Gemini API key is valid";

    }

    finally {

        setLoading(false);

    }

});

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

    catch (err) {

        alert("Copy failed.");

    }

});