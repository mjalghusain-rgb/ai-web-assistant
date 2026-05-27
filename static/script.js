/* =========================================
   CHAT
========================================= */

async function sendMessage(){

    const input =
    document.getElementById(
        "user-input"
    );

    const chatBox =
    document.getElementById(
        "chat-box"
    );

    const message =
    input.value.trim();


    if(!message){

        return;
    }


    chatBox.innerHTML += `

        <div class="message user">

            <strong>

                You

            </strong>

            <br><br>

            ${message}

        </div>

    `;


    input.value = "";


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

                    message:message
                })
            }
        );


        const data =
        await response.json();


        chatBox.innerHTML += `

            <div class="message ai">

                <strong>

                    🚀 DevOps AI

                </strong>

                <br><br>

                ${marked.parse(
                    data.response
                )}

            </div>

        `;


        document.getElementById(
            "generated-code-block"
        ).innerText =
        data.response;


        hljs.highlightAll();


        chatBox.scrollTop =
        chatBox.scrollHeight;


    }catch(error){

        console.log(error);
    }
}





/* =========================================
   ENTER SEND
========================================= */

document.addEventListener(
    "DOMContentLoaded",
    ()=>{

        document.getElementById(
            "user-input"
        ).addEventListener(
            "keypress",
            function(event){

                if(
                    event.key === "Enter"
                ){

                    sendMessage();
                }
            }
        );
    }
);





/* =========================================
   NOTIFICATIONS
========================================= */

function toggleNotifications(){

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

    }else{

        dropdown.style.display =
        "block";
    }
}





/* =========================================
   PROFILE MENU
========================================= */

function toggleProfileMenu(){

    const menu =
    document.getElementById(
        "profile-dropdown"
    );


    if(
        menu.style.display ===
        "block"
    ){

        menu.style.display =
        "none";

    }else{

        menu.style.display =
        "block";
    }
}





/* =========================================
   QUICK TOOLS
========================================= */

function showCodingPrompt(){

    document.getElementById(
        "user-input"
    ).value =
    "Generate a Python DevOps automation script";
}



function showTranslationPrompt(){

    document.getElementById(
        "user-input"
    ).value =
    "Translate this text professionally";
}



function showGrammarPrompt(){

    document.getElementById(
        "user-input"
    ).value =
    "Fix grammar and improve this text";
}



function showEmailPrompt(){

    document.getElementById(
        "user-input"
    ).value =
    "Generate a professional email";
}



function generateDiagramIdea(){

    document.getElementById(
        "user-input"
    ).value =
    "Generate a cloud architecture diagram idea";
}





/* =========================================
   AI IMAGES
========================================= */

async function showImagePrompt(){

    const promptText =
    prompt(
        "Describe the image"
    );


    if(!promptText){

        return;
    }


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

                    prompt:promptText
                })
            }
        );


        const data =
        await response.json();


        const gallery =
        document.getElementById(
            "generated-images"
        );


        gallery.innerHTML += `

            <img
            src="${data.image_url}"
            class="generated-image">

        `;


    }catch(error){

        console.log(error);
    }
}





/* =========================================
   DOCUMENT UPLOAD
========================================= */

async function uploadDocument(){

    const fileInput =
    document.getElementById(
        "document-input"
    );


    if(
        fileInput.files.length === 0
    ){

        alert(
            "Select a file first"
        );

        return;
    }


    const formData =
    new FormData();

    formData.append(

        "document",

        fileInput.files[0]
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


        alert(

            "Uploaded: " +
            data.filename
        );


    }catch(error){

        console.log(error);
    }
}





/* =========================================
   COPY CODE
========================================= */

function copyGeneratedCode(){

    const code =
    document.getElementById(
        "generated-code-block"
    ).innerText;


    navigator.clipboard.writeText(
        code
    );


    alert(
        "Code copied"
    );
}





/* =========================================
   VOICE
========================================= */

function toggleVoice(){

    alert(
        "Voice system enabled"
    );
}





/* =========================================
   WORKSPACE TABS
========================================= */

const workspaceTabs =
document.querySelectorAll(
    ".workspace-tabs button"
);


workspaceTabs.forEach(tab=>{

    tab.addEventListener(
        "click",
        ()=>{

            workspaceTabs.forEach(t=>{

                t.classList.remove(
                    "active-tab"
                );
            });


            tab.classList.add(
                "active-tab"
            );
        }
    );
});





/* =========================================
   SIDEBAR PROMPTS
========================================= */

function loadPresetChat(type){

    const input =
    document.getElementById(
        "user-input"
    );


    if(type === "docker"){

        input.value =
        "Help me deploy Docker containers";
    }


    if(type === "kubernetes"){

        input.value =
        "Fix Kubernetes deployment issues";
    }


    if(type === "terraform"){

        input.value =
        "Generate Terraform infrastructure";
    }


    if(type === "resume"){

        input.value =
        "Improve my DevOps resume";
    }


    if(type === "aws"){

        input.value =
        "Design AWS cloud architecture";
    }
}
