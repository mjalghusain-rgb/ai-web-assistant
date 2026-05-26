const input =
document.getElementById(
    "user-input"
);

const chatBox =
document.getElementById(
    "chat-box"
);

const recordBtn =
document.getElementById(
    "record-btn"
);

const documentInput =
document.getElementById(
    "document-input"
);



/* =========================================
   GLOBALS
========================================= */

let currentMode = "general";

let voiceEnabled = true;

let mediaRecorder;

let audioChunks = [];



/* =========================================
   ENTER SEND
========================================= */

input.addEventListener(
    "keypress",
    function(event){

        if(event.key === "Enter"){

            sendMessage();
        }
    }
);



/* =========================================
   SET AI MODE
========================================= */

function setMode(mode){

    currentMode = mode;

    addMessage(

        "ai",

        `⚡ AI mode switched to:
        <strong>${mode}</strong>`
    );
}



/* =========================================
   VOICE TOGGLE
========================================= */

function toggleVoice(){

    voiceEnabled = !voiceEnabled;

    const button =
    document.querySelector(
        ".voice-toggle"
    );


    if(voiceEnabled){

        button.innerHTML =
        "🔊 Voice ON";

        button.style.background =
        "#22c55e";

    }else{

        window.speechSynthesis.cancel();

        button.innerHTML =
        "🔇 Voice OFF";

        button.style.background =
        "#ef4444";
    }
}



/* =========================================
   ADD MESSAGE
========================================= */

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



/* =========================================
   LOADING
========================================= */

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

        Thinking...

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



/* =========================================
   SEND MESSAGE
========================================= */

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

                    message:userMessage,

                    mode:currentMode
                })
            }
        );


        const data =
        await response.json();

        removeLoading();


        const aiHtml = `

        <div class="markdown-body">

            ${marked.parse(data.response)}

        </div>

        `;


        addMessage(
            "ai",
            aiHtml
        );


        if(voiceEnabled){

            speakText(
                data.response
            );
        }


        highlightCode();


    }catch(error){

        removeLoading();

        addMessage(

            "ai",

            "⚠️ Server connection failed."
        );
    }
}



/* =========================================
   SPEAK TEXT
========================================= */

function speakText(text){

    if(!voiceEnabled){

        return;
    }

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



/* =========================================
   WHISPER RECORDING
========================================= */

if(recordBtn){

    recordBtn.addEventListener(

        "click",

        async ()=>{

            if(
                recordBtn.innerText
                ===
                "🎤"
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
                    "⏹";


                }catch(error){

                    alert(
                        "Microphone denied."
                    );
                }

            }else{

                mediaRecorder.stop();


                mediaRecorder.onstop =
                async ()=>{

                    recordBtn.innerText =
                    "⌛";


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
                        "🎤";


                        sendMessage();


                    }catch(error){

                        alert(
                            "Voice transcription failed."
                        );

                        recordBtn.innerText =
                        "🎤";
                    }
                };
            }
        }
    );
}



/* =========================================
   DOCUMENT UPLOAD
========================================= */

async function uploadDocument(){

    const file =
    documentInput.files[0];

    if(!file){

        alert(
            "Select a document first."
        );

        return;
    }


    const formData =
    new FormData();

    formData.append(
        "document",
        file
    );


    try{

        const response =
        await fetch(
            "/upload-document",
            {

                method:"POST",

                body:formData
            }
        );


        const data =
        await response.json();


        addMessage(

            "ai",

            `📁 Document uploaded:
            <strong>${data.filename}</strong>`
        );


    }catch(error){

        alert(
            "Upload failed."
        );
    }
}



/* =========================================
   QUICK PROMPTS
========================================= */

function showResumePrompt(){

    input.value = `
Create a professional ATS-friendly DevOps resume.
`;

    sendMessage();
}



function showRecommendations(){

    input.value = `
Recommend technologies and learning paths for DevOps.
`;

    sendMessage();
}



function showDockerHelp(){

    setMode("coding");

    input.value = `
Help me create a professional Docker setup.
`;

    sendMessage();
}



function showTerraformHelp(){

    setMode("coding");

    input.value = `
Generate Terraform infrastructure example.
`;

    sendMessage();
}



function showCodingPrompt(){

    setMode("coding");

    input.value = `
Help me with programming and debugging.
`;

    sendMessage();
}



function showTranslationPrompt(){

    setMode("language");

    input.value = `
Translate this text professionally:
`;

    input.focus();
}



function showGrammarPrompt(){

    setMode("language");

    input.value = `
Correct grammar for:
`;

    input.focus();
}



function showEmailPrompt(){

    setMode("language");

    input.value = `
Write a professional email about:
`;

    input.focus();
}



function showCareerAdvice(){

    input.value = `
Give me professional IT career advice.
`;

    sendMessage();
}



function showLearningPath(){

    input.value = `
Create a DevOps learning roadmap.
`;

    sendMessage();
}



function showImagePrompt(){

    input.value = `
Generate a professional AI image for:
`;

    input.focus();
}



/* =========================================
   SCROLL
========================================= */

function scrollToBottom(){

    chatBox.scrollTop =
    chatBox.scrollHeight;
}



/* =========================================
   HIGHLIGHT CODE
========================================= */

function highlightCode(){

    document
    .querySelectorAll(
        "pre code"
    )
    .forEach((el)=>{

        hljs.highlightElement(el);
    });
}
