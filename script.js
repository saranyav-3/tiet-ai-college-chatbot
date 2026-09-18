// =========================================================
// CHATBOT SCRIPT
// =========================================================

const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");


// =========================================================
// SEND MESSAGE
// =========================================================

function sendMessage() {

    const message = input.value.trim();

    if (message === "") {
        return;
    }

    // Show user message
    addUserMessage(message);

    // Clear input
    input.value = "";

    // Show typing message
    const typing = document.createElement("div");
    typing.className = "bot-message";
    typing.id = "typing";

    typing.innerHTML = `
        <div class="message-title">
            🤖 AI Assistant
        </div>
        Typing... ⏳
    `;

    chatBox.appendChild(typing);
    chatBox.scrollTop = chatBox.scrollHeight;


    // Send to Flask
    fetch("/chat", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message
        })

    })

    .then(response => response.json())

    .then(data => {

        // Remove typing
        const typingElement =
            document.getElementById("typing");

        if (typingElement) {
            typingElement.remove();
        }

        // Show bot response
        addBotMessage(data.response);

    })

    .catch(error => {

        const typingElement =
            document.getElementById("typing");

        if (typingElement) {
            typingElement.remove();
        }

        addBotMessage(
            "Sorry 😔 Something went wrong. Please try again."
        );

        console.error(error);

    });

}


// =========================================================
// USER MESSAGE
// =========================================================

function addUserMessage(message) {

    const div = document.createElement("div");

    div.className = "user-message";

    div.innerHTML = `
        <div class="message-title">
            👤 You
        </div>
        ${escapeHtml(message)}
    `;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
}


// =========================================================
// BOT MESSAGE
// =========================================================

function addBotMessage(message) {

    const div = document.createElement("div");

    div.className = "bot-message";

    div.innerHTML = `
        <div class="message-title">
            🤖 AI Assistant
        </div>
        ${escapeHtml(message)}
    `;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
}


// =========================================================
// QUICK QUESTION
// =========================================================

function quickMessage(message) {

    input.value = message;

    sendMessage();
}


// =========================================================
// ENTER KEY
// =========================================================

input.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {

        event.preventDefault();

        sendMessage();
    }

});


// =========================================================
// VOICE INPUT
// =========================================================

function startVoice() {

    if (
        !("webkitSpeechRecognition" in window) &&
        !("SpeechRecognition" in window)
    ) {

        alert(
            "Voice input is not supported in this browser."
        );

        return;
    }


    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    const recognition =
        new SpeechRecognition();


    recognition.lang = "en-IN";

    recognition.continuous = false;

    recognition.interimResults = false;


    recognition.start();


    recognition.onstart = function() {

        console.log("Voice recognition started");

    };


    recognition.onresult = function(event) {

        const text =
            event.results[0][0].transcript;

        input.value = text;

    };


    recognition.onerror = function(event) {

        console.log(
            "Voice error:",
            event.error
        );

    };

}


// =========================================================
// SECURITY
// =========================================================

function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}