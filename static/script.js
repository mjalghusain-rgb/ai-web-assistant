const input =
document.getElementById("user-input");

const recordBtn =
document.getElementById("record-btn");

let mediaRecorder;

let audioChunks = [];



/* =========================
   SEND MESSAGE
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

        AI is thinking...

    </div>
    `;

    const response =
    await fetch("/chat", {

        method: "POST",

        headers: {
            "Content-Type":
            "application/json"
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

    chatBox.innerHTML += `

    <div class="message ai">

        <strong>
        DevOps AI
        </strong>

        <br><br>

        <div id="latest-ai-response">

            ${marked.parse(data.response)}

        </div>

        <br>

        <button onclick="downloadCVPDF()">

            📄 Download PDF

        </button>

    </div>
    `;

    speakText(data.response);

    chatBox.scrollTop =
    chatBox.scrollHeight;
}



/* =========================
   DOWNLOAD PDF
========================= */

async function downloadCVPDF() {

    const cvText =
    document.getElementById(
        "latest-ai-response"
    ).innerText;

    const response =
    await fetch(
        "/generate-cv-pdf",
        {

            method: "POST",

            headers: {
                "Content-Type":
                "application/json"
            },

            body: JSON.stringify({

                cv_text: cvText
            })
        }
    );

    const blob =
    await response.blob();

    const url =
    window.URL.createObjectURL(blob);

    const a =
    document.createElement("a");

    a.href = url;

    a.download = "AI_CV.pdf";

    document.body.appendChild(a);

    a.click();

    a.remove();
}



/* =========================
   VOICE RECORDING
========================= */

recordBtn.addEventListener(
"click",
async () => {

    if (
        recordBtn.innerText ===
        "🎤 Start Recording"
    ) {

        const stream =
        await navigator.mediaDevices
        .getUserMedia({

            audio: true
        });

        mediaRecorder =
        new MediaRecorder(stream);

        mediaRecorder.start();

        audioChunks = [];

        mediaRecorder.ondataavailable =
        event => {

            audioChunks.push(
                event.data
            );
        };

        recordBtn.innerText =
        "⏹ Stop Recording";

    } else {

        mediaRecorder.stop();

        mediaRecorder.onstop =
        async () => {

            const audioBlob =
            new Blob(audioChunks, {

                type: "audio/webm"
            });

            const formData =
            new FormData();

            formData.append(
                "audio",
                audioBlob,
                "recording.webm"
            );

            recordBtn.innerText =
            "⌛ Processing";

            const response =
            await fetch(
                "/transcribe",
                {

                    method: "POST",

                    body: formData
                }
            );

            const data =
            await response.json();

            input.value =
            data.text;

            recordBtn.innerText =
            "🎤 Start Recording";

            sendMessage();
        };
    }
});



/* =========================
   AI VOICE RESPONSE
========================= */

function speakText(text) {

    const speech =
    new SpeechSynthesisUtterance();

    speech.text = text;

    speech.lang = "en-US";

    window.speechSynthesis
    .speak(speech);
}



/* =========================
   QUICK TOOLS
========================= */

function setPrompt(text) {

    document.getElementById(
        "user-input"
    ).value = text;
}



/* =========================
   QUIZ PLACEHOLDER
========================= */

function showQuiz() {

    alert(
    "Quiz system coming soon."
    );
}



/* =========================
   INTERVIEW PLACEHOLDER
========================= */

function showInterview() {

    alert(
    "AI Interview system ready soon."
    );
}



/* =========================
   CV BUILDER
========================= */

function showCVBuilder() {

    const prompt = `
Create a professional ATS-friendly DevOps resume template.
`;

    document.getElementById(
        "user-input"
    ).value = prompt;

    sendMessage();
}
