const input = document.getElementById("user-input");


/* =========================
   ENTER KEY
========================= */

input.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {

        sendMessage();
    }
});


/* =========================
   MAIN CHAT
========================= */

async function sendMessage() {

    let chatBox =
        document.getElementById("chat-box");

    let userMessage =
        input.value;

    if (userMessage.trim() === "") {
        return;
    }

    chatBox.innerHTML += `
        <div class="message user">

            <strong>You</strong>

            <br><br>

            ${userMessage}

        </div>
    `;

    input.value = "";

    chatBox.innerHTML += `
        <div class="message ai" id="loading">

            <div class="typing">

                <span></span>
                <span></span>
                <span></span>

            </div>

        </div>
    `;

    chatBox.scrollTop =
        chatBox.scrollHeight;


    const response = await fetch("/chat", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: userMessage
        })
    });


    const data =
        await response.json();

    document
        .getElementById("loading")
        .remove();


    const renderedMarkdown =
        marked.parse(data.response);


    chatBox.innerHTML += `
        <div class="message ai">

            <strong>
                DevOps AI
            </strong>

            <button class="copy-btn"
            onclick="copyText(this)">
                Copy
            </button>

            <br><br>

            <div class="markdown-body">

                ${renderedMarkdown}

            </div>

        </div>
    `;

    chatBox.scrollTop =
        chatBox.scrollHeight;


    speakText(data.response);


    document.querySelectorAll(
        "pre code"
    ).forEach((el) => {

        hljs.highlightElement(el);
    });
}



/* =========================
   VOICE RECOGNITION
========================= */

function startVoiceRecognition() {

    const recognition =
        new (
            window.SpeechRecognition ||
            window.webkitSpeechRecognition
        )();

    recognition.lang = "en-US";

    recognition.start();

    document.getElementById(
        "voice-btn"
    ).innerText = "🎙️";


    recognition.onresult = function(event) {

        const transcript =
            event.results[0][0].transcript;

        document.getElementById(
            "user-input"
        ).value = transcript;

        document.getElementById(
            "voice-btn"
        ).innerText = "🎤";

        sendMessage();
    };


    recognition.onerror = function() {

        document.getElementById(
            "voice-btn"
        ).innerText = "🎤";

        alert(
            "Voice recognition failed."
        );
    };
}



/* =========================
   AI VOICE RESPONSE
========================= */

function speakText(text) {

    const speech =
        new SpeechSynthesisUtterance();

    speech.text = text;

    speech.lang = "en-US";

    speech.rate = 1;

    speech.pitch = 1;

    window.speechSynthesis.speak(
        speech
    );
}



/* =========================
   COPY BUTTON
========================= */

function copyText(button) {

    const text =
        button.parentElement.innerText;

    navigator.clipboard.writeText(text);

    button.innerText = "Copied!";

    setTimeout(() => {

        button.innerText = "Copy";

    }, 2000);
}



/* =========================
   QUICK TOOLS
========================= */

function quickAsk(text) {

    document.getElementById(
        "user-input"
    ).value = text;

    sendMessage();
}


function setPrompt(text) {

    document.getElementById(
        "user-input"
    ).value = text;
}



/* =========================
   ERROR ANALYZER
========================= */

function analyzeError() {

    let errorText =
        document.getElementById(
            "error-input"
        ).value;

    if (errorText.trim() === "") {
        return;
    }

    document.getElementById(
        "user-input"
    ).value =
        `Analyze this error:\n\n${errorText}`;

    sendMessage();
}



/* =========================
   CV BUILDER
========================= */

function showCVBuilder() {

    document.getElementById(
        "cv-builder"
    ).style.display = "block";

    document.getElementById(
        "chat-box"
    ).scrollIntoView({
        behavior: "smooth"
    });
}


async function generateCV() {

    let name =
        document.getElementById(
            "cv-name"
        ).value;

    let skills =
        document.getElementById(
            "cv-skills"
        ).value;

    let experience =
        document.getElementById(
            "cv-experience"
        ).value;

    let education =
        document.getElementById(
            "cv-education"
        ).value;


    let prompt = `
Create a professional ATS-friendly resume.

Name:
${name}

Skills:
${skills}

Experience:
${experience}

Education:
${education}
`;


    document.getElementById(
        "user-input"
    ).value = prompt;

    sendMessage();
}
