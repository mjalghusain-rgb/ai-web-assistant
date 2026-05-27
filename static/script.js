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

const projectViewer =
document.getElementById(
    "project-file-viewer"
);



/* =========================================
   GLOBALS
========================================= */

let currentMode = "general";

let voiceEnabled = true;

let mediaRecorder;

let audioChunks = [];



/* =========================================
   PROJECT FILES
========================================= */

const projectFiles = {

    "app.py": `from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)
`,



    "Dockerfile": `FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python","app.py"]
`,



    "docker-compose.yml": `version: "3"

services:

  web:
    build: .
    ports:
      - "5000:5000"
`,



    "nginx.conf": `server {

    listen 80;

    location / {

        proxy_pass http://web:5000;
    }
}
`,



    "requirements.txt": `flask
gunicorn
openai
`
};



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
   NOTIFICATIONS
========================================= */

function showNotification(message){

    const notification =
    document.createElement("div");

    notification.classList.add(
        "notification-popup"
    );

    notification.innerHTML = `

        🔔 ${message}

    `;


    document.body.appendChild(
        notification
    );


    setTimeout(()=>{

        notification.style.opacity = "0";

    },2500);


    setTimeout(()=>{

        notification.remove();

    },3000);
}



/* =========================================
   SET AI MODE
========================================= */

function setMode(mode){

    currentMode = mode;

    showNotification(
        `AI mode:
        ${mode}`
    );
}



/* =========================================
   VOICE TOGGLE
========================================= */

function toggleVoice(){

    voiceEnabled = !voiceEnabled;

    const button =
    document.querySelector(
        ".voice-btn"
    );


    if(voiceEnabled){

        button.innerHTML =
        "🔊 Voice ON";

        button.style.background =
        "#22c55e";

        showNotification(
            "Voice enabled"
        );

    }else{

        window.speechSynthesis.cancel();

        button.innerHTML =
        "🔇 Voice OFF";

        button.style.background =
        "#ef4444";

        showNotification(
            "Voice disabled"
        );
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

    div.classList.add(
        "fade-in"
    );


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
   TYPING
========================================= */

function showTyping(){

    const div =
    document.createElement("div");

    div.classList.add(
        "message",
        "ai"
    );

    div.id = "typing-message";

    div.innerHTML = `

        <strong>

            DevOps AI

        </strong>

        <br><br>

        <span class="typing-dots">

            ● ● ●

        </span>

    `;

    chatBox.appendChild(div);

    scrollToBottom();
}



function removeTyping(){

    const typing =
    document.getElementById(
        "typing-message"
    );

    if(typing){

        typing.remove();
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

    showTyping();


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

        removeTyping();


        const aiHtml = `

        <div class="markdown-body">

            ${marked.parse(data.response)}

        </div>

        `;


        addMessage(
            "ai",
            aiHtml
        );


        extractAndDisplayCode(
            data.response
        );


        if(voiceEnabled){

            speakText(
                data.response
            );
        }


        highlightCode();


    }catch(error){

        removeTyping();

        addMessage(

            "ai",

            "⚠️ Server connection failed."
        );
    }
}



/* =========================================
   AGENTS
========================================= */

function runAgent(agentName){

    showNotification(
        `${agentName} started`
    );


    let response = "";


    if(agentName === "DevOps Agent"){

        response = `

# DevOps Agent Report

## Suggested Stack

- Docker
- Docker Compose
- Nginx
- Flask
- Gunicorn

## Recommended Steps

1. Create Dockerfile
2. Configure docker-compose
3. Configure nginx reverse proxy
4. Add SSL
5. Deploy with CI/CD

`;

        updateCodePlayground(`docker compose up -d`);

    }



    if(agentName === "Security Agent"){

        response = `

# Security Agent Report

## Security Recommendations

- Enable HTTPS
- Use fail2ban
- Add firewall rules
- Secure Docker containers
- Hide server headers

`;

        updateCodePlayground(`ufw allow 80
ufw allow 443`);

    }



    if(agentName === "Deployment Agent"){

        response = `

# Deployment Agent Report

## Deployment Plan

- Build Docker image
- Configure Nginx
- Deploy containers
- Configure SSL
- Monitor logs

`;

        updateCodePlayground(`docker build -t app .`);

    }



    if(agentName === "Infrastructure Agent"){

        response = `

# Infrastructure Agent Report

## Suggested Infrastructure

- AWS EC2
- Nginx reverse proxy
- Docker Swarm
- Cloudflare DNS
- Prometheus Monitoring

`;

        updateCodePlayground(`terraform init`);

    }


    addMessage(
        "ai",
        marked.parse(response)
    );
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

    window.speechSynthesis
    .speak(speech);
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


        showNotification(
            "Document uploaded"
        );


    }catch(error){

        alert(
            "Upload failed."
        );
    }
}



/* =========================================
   MODALS
========================================= */

function openModal(modalId){

    document.getElementById(
        modalId
    ).style.display = "flex";
}



function closeModal(modalId){

    document.getElementById(
        modalId
    ).style.display = "none";
}



/* =========================================
   TOOL BUTTONS
========================================= */

function showCodingPrompt(){

    openModal(
        "coding-modal"
    );
}



function showTranslationPrompt(){

    openModal(
        "translation-modal"
    );
}



function showGrammarPrompt(){

    openModal(
        "translation-modal"
    );
}



function showEmailPrompt(){

    openModal(
        "email-modal"
    );
}



function showImagePrompt(){

    openModal(
        "image-modal"
    );
}



/* =========================================
   CODING MODAL
========================================= */

function submitCodingModal(){

    const prompt =
    document.getElementById(
        "coding-prompt"
    ).value;


    closeModal(
        "coding-modal"
    );


    setMode("coding");

    input.value = prompt;

    sendMessage();
}



/* =========================================
   TRANSLATION MODAL
========================================= */

function submitTranslationModal(){

    const text =
    document.getElementById(
        "translation-text"
    ).value;

    const language =
    document.getElementById(
        "translation-language"
    ).value;


    closeModal(
        "translation-modal"
    );


    setMode("language");

    input.value = `

Translate this to ${language}:

${text}

`;

    sendMessage();
}



/* =========================================
   EMAIL MODAL
========================================= */

function submitEmailModal(){

    const request =
    document.getElementById(
        "email-request"
    ).value;


    closeModal(
        "email-modal"
    );


    setMode("language");

    input.value = `

Write a professional email about:

${request}

`;

    sendMessage();
}



/* =========================================
   IMAGE GENERATION
========================================= */

async function submitImageModal(){

    const prompt =
    document.getElementById(
        "image-prompt"
    ).value;


    closeModal(
        "image-modal"
    );


    showNotification(
        "Generating AI image..."
    );


    try{

        const response =
        await fetch(
            "/generate-image",
            {

                method:"POST",

                headers:{
                    "Content-Type":
                    "application/json"
                },

                body:JSON.stringify({

                    prompt:prompt
                })
            }
        );


        const data =
        await response.json();


        if(data.image_url){

            addGeneratedImage(

                data.image_url,

                prompt
            );


            showNotification(
                "AI image generated"
            );

        }else{

            showNotification(
                "Image generation failed"
            );
        }

    }catch(error){

        showNotification(
            "Server error"
        );
    }
}



/* =========================================
   IMAGE GALLERY
========================================= */

function addGeneratedImage(

    imageUrl,

    prompt
){

    const gallery =
    document.getElementById(
        "generated-images"
    );


    const card =
    document.createElement("div");

    card.classList.add(
        "generated-image-card"
    );

    card.classList.add(
        "fade-in"
    );


    card.innerHTML = `

        <img src="${imageUrl}">

        <div class="image-card-footer">

            <p>

                ${prompt}

            </p>

            <button onclick="downloadImage('${imageUrl}')">

                Download

            </button>

        </div>

    `;


    gallery.prepend(card);
}



function downloadImage(url){

    const link =
    document.createElement("a");

    link.href = url;

    link.download = "ai-image.png";

    link.click();
}



/* =========================================
   CODE EXTRACTION
========================================= */

function extractAndDisplayCode(text){

    const codeMatch =
    text.match(/```([\s\S]*?)```/);


    if(codeMatch){

        const code =
        codeMatch[1];

        updateCodePlayground(code);
    }
}



/* =========================================
   UPDATE PLAYGROUND
========================================= */

function updateCodePlayground(code){

    const block =
    document.querySelector(
        "#generated-code-block code"
    );


    block.textContent = code;


    hljs.highlightElement(
        block
    );


    showNotification(
        "Code added to playground"
    );
}



/* =========================================
   COPY CODE
========================================= */

function copyGeneratedCode(){

    const code =
    document.querySelector(
        "#generated-code-block code"
    ).innerText;


    navigator.clipboard.writeText(
        code
    );


    showNotification(
        "Code copied"
    );
}



/* =========================================
   PROJECT FILES
========================================= */

document.querySelectorAll(
    ".file-item"
)
.forEach(item=>{

    item.addEventListener(

        "click",

        ()=>{

            document
            .querySelectorAll(
                ".file-item"
            )
            .forEach(file=>{

                file.classList.remove(
                    "active-file"
                );
            });


            item.classList.add(
                "active-file"
            );


            const filename =
            item.innerText
            .replace("🐍","")
            .replace("🐳","")
            .replace("⚙","")
            .replace("🌐","")
            .replace("📦","")
            .trim();


            if(projectFiles[filename]){

                projectViewer.innerText =
                projectFiles[filename];
            }


            showNotification(
                `${filename} opened`
            );
        }
    );
});



/* =========================================
   DRAG & DROP
========================================= */

const dropZone =
document.getElementById(
    "drop-zone"
);



if(dropZone){

    dropZone.addEventListener(

        "dragover",

        (event)=>{

            event.preventDefault();

            dropZone.classList.add(
                "dragover"
            );
        }
    );



    dropZone.addEventListener(

        "dragleave",

        ()=>{

            dropZone.classList.remove(
                "dragover"
            );
        }
    );



    dropZone.addEventListener(

        "drop",

        (event)=>{

            event.preventDefault();

            dropZone.classList.remove(
                "dragover"
            );


            const files =
            event.dataTransfer.files;


            if(files.length > 0){

                documentInput.files =
                files;

                showNotification(
                    "File added successfully"
                );
            }
        }
    );
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



/* =========================================
   SCROLL
========================================= */

function scrollToBottom(){

    chatBox.scrollTop =
    chatBox.scrollHeight;
}



/* =========================================
   ESC CLOSE MODALS
========================================= */

document.addEventListener(

    "keydown",

    (event)=>{

        if(event.key === "Escape"){

            document
            .querySelectorAll(
                ".modal"
            )
            .forEach(modal=>{

                modal.style.display =
                "none";
            });
        }
    }
);



/* =========================================
   AUTO FOCUS
========================================= */

window.addEventListener(

    "load",

    ()=>{

        input.focus();


        projectViewer.innerText =
        projectFiles["app.py"];
    }
);


/* =========================================
   NOTIFICATIONS
========================================= */

async function toggleNotifications(){

    const dropdown =
    document.getElementById(
        "notifications-dropdown"
    );


    if(
        dropdown.style.display ===
        "block"
    ){

        dropdown.style.display =
        "none";

        return;
    }


    dropdown.style.display =
    "block";


    try{

        const response =
        await fetch(
            "/notifications"
        );


        const data =
        await response.json();


        const container =
        document.getElementById(
            "notifications-list"
        );


        if(data.length === 0){

            container.innerHTML = `

                <p>

                    No notifications

                </p>

            `;

            return;
        }


        let html = "";


        data.forEach(notification=>{

            html += `

                <div class="notification-item">

                    <strong>

                        ${notification.title}

                    </strong>

                    <p>

                        ${notification.message}

                    </p>

                </div>

            `;
        });


        container.innerHTML =
        html;


    }catch(error){

        console.log(error);
    }
}
