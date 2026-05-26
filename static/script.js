const input =
document.getElementById("user-input");

const chatBox =
document.getElementById("chat-box");

const recordBtn =
document.getElementById("record-btn");


let mediaRecorder;

let audioChunks = [];



/* ==================================================
   ENTER KEY SEND
================================================== */

input.addEventListener(
    "keypress",
    function(event){

        if(event.key === "Enter"){

            sendMessage();
        }
    }
);



/* ==================================================
   ADD MESSAGE
================================================== */

function addMessage(
    sender,
    message
){

    const div =
    document.createElement("div");

    div.classList.add(
        "message"
    );

    div.classList.add(sender);


    div.innerHTML = `

        <strong>

            ${
                sender === "user"
                ? "You"
                : "DevOps AI"
            }

        </strong>

        <br><br>

        ${message}

    `;


    chatBox.appendChild(div);

    scrollToBottom();
}



/* ==================================================
   LOADING MESSAGE
================================================== */

function showLoading(){

    const div =
    document.createElement("div");

    div.classList.add(
        "message",
        "ai"
    );

    div.id = "loading-message";

    div.innerHTML = `

        <strong>
            DevOps AI
        </strong>

        <br><br>

        <div class="typing">

            Thinking...

        </div>
    `;

    chatBox.appendChild(div);

    scrollToBottom();
}



function removeLoading(){

    const loading =
    document.getElementById(
        "loading-message"
    );

    if(loading){

        loading.remove();
    }
}



/* ==================================================
   SEND MESSAGE
================================================== */

async function sendMessage(){

    const userMessage =
    input.value.trim();

    if(userMessage === ""){

        return;
    }


    addMessage(
        "user",
        userMessage
    );

    input.value = "";

    showLoading();


    try{

        const response =
        await fetch(
            "/chat",
            {

                method:"POST",

                headers:{
                    "Content-Type":
                    "application/json"
                },

                body:JSON.stringify({

                    message:userMessage
                })
            }
        );


        const data =
        await response.json();

        removeLoading();


        const aiHtml =
        `

        <div class="markdown-body">

            ${marked.parse(data.response)}

        </div>

        <br>

        <button onclick="downloadCVPDF()">

            📄 Download PDF

        </button>

        `;


        addMessage(
            "ai",
            aiHtml
        );


        speakText(
            data.response
        );


        highlightCode();


    }catch(error){

        removeLoading();

        addMessage(
            "ai",
            "⚠️ Error communicating with server."
        );
    }
}



/* ==================================================
   SPEAK AI RESPONSE
================================================== */

function speakText(text){

    const speech =
    new SpeechSynthesisUtterance();

    speech.text = text;

    speech.lang = "en-US";

    speech.rate = 1;

    speech.pitch = 1;

    speech.volume = 1;

    window.speechSynthesis
    .speak(speech);
}



/* ==================================================
   WHISPER RECORDING
================================================== */

if(recordBtn){

    recordBtn.addEventListener(
        "click",
        async ()=>{

            if(
                recordBtn.innerText
                ===
                "🎤 Start Recording"
            ){

                try{

                    const stream =
                    await navigator
                    .mediaDevices
                    .getUserMedia({

                        audio:true
                    });


                    mediaRecorder =
                    new MediaRecorder(
                        stream
                    );


                    mediaRecorder.start();

                    audioChunks = [];


                    mediaRecorder
                    .ondataavailable =
                    event=>{

                        audioChunks.push(
                            event.data
                        );
                    };


                    recordBtn.innerText =
                    "⏹ Stop Recording";


                }catch(error){

                    alert(
                        "Microphone access denied."
                    );
                }

            }else{

                mediaRecorder.stop();


                mediaRecorder.onstop =
                async ()=>{

                    recordBtn.innerText =
                    "⌛ Processing";


                    const audioBlob =
                    new Blob(
                        audioChunks,
                        {
                            type:"audio/webm"
                        }
                    );


                    const formData =
                    new FormData();


                    formData.append(

                        "audio",

                        audioBlob,

                        "recording.webm"
                    );


                    try{

                        const response =
                        await fetch(
                            "/transcribe",
                            {

                                method:"POST",

                                body:formData
                            }
                        );


                        const data =
                        await response.json();


                        input.value =
                        data.text;


                        recordBtn.innerText =
                        "🎤 Start Recording";


                        sendMessage();


                    }catch(error){

                        alert(
                            "Whisper transcription failed."
                        );

                        recordBtn.innerText =
                        "🎤 Start Recording";
                    }
                };
            }
        }
    );
}



/* ==================================================
   PDF DOWNLOAD
================================================== */

async function downloadCVPDF(){

    const messages =
    document.querySelectorAll(
        ".message.ai"
    );


    if(messages.length === 0){

        return;
    }


    const latestMessage =
    messages[
        messages.length - 1
    ];


    const cvText =
    latestMessage.innerText;


    try{

        const response =
        await fetch(
            "/generate-cv-pdf",
            {

                method:"POST",

                headers:{
                    "Content-Type":
                    "application/json"
                },

                body:JSON.stringify({

                    cv_text:cvText
                })
            }
        );


        const blob =
        await response.blob();


        const url =
        window.URL
        .createObjectURL(blob);


        const a =
        document.createElement("a");


        a.href = url;

        a.download = "AI_CV.pdf";


        document.body.appendChild(a);

        a.click();

        a.remove();


    }catch(error){

        alert(
            "PDF generation failed."
        );
    }
}



/* ==================================================
   QUICK PROMPTS
================================================== */

function setPrompt(text){

    input.value = text;

    input.focus();
}



/* ==================================================
   QUICK ASK
================================================== */

function quickAsk(text){

    input.value = text;

    sendMessage();
}



/* ==================================================
   SHOW CV BUILDER
================================================== */

function showCVBuilder(){

    const prompt = `

Create a professional ATS-friendly DevOps resume template with:

- Summary
- Skills
- Experience
- Certifications
- Education
- Projects

`;

    input.value = prompt;

    sendMessage();
}



/* ==================================================
   SHOW INTERVIEW
================================================== */

function showInterview(){

    const prompt = `

Start a professional DevOps interview simulation.

Ask one question at a time.

`;

    input.value = prompt;

    sendMessage();
}



/* ==================================================
   SHOW QUIZ
================================================== */

function showQuiz(){

    const prompt = `

Create a 10-question DevOps multiple-choice quiz.

Show:
- Question
- 4 choices
- Correct answer

`;

    input.value = prompt;

    sendMessage();
}



/* ==================================================
   AUTO SCROLL
================================================== */

function scrollToBottom(){

    chatBox.scrollTop =
    chatBox.scrollHeight;
}



/* ==================================================
   HIGHLIGHT CODE
================================================== */

function highlightCode(){

    document
    .querySelectorAll(
        "pre code"
    )
    .forEach((el)=>{

        hljs.highlightElement(el);
    });
}
