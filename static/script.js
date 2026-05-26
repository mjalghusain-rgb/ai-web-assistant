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


    document.querySelectorAll(
        "pre code"
    ).forEach((el) => {

        hljs.highlightElement(el);
    });
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



/* =========================
   QUIZ SYSTEM
========================= */

const quizQuestions = [

{
    question:
    "What does chmod do in Linux?",

    options: [
        "Change permissions",
        "Delete files",
        "Restart Docker",
        "Monitor RAM"
    ],

    correct:
    "Change permissions"
},

{
    question:
    "Which command shows current directory?",

    options: [
        "pwd",
        "mkdir",
        "ls",
        "chmod"
    ],

    correct:
    "pwd"
},

{
    question:
    "What is Docker mainly used for?",

    options: [
        "Containers",
        "Databases only",
        "Monitoring",
        "Text editing"
    ],

    correct:
    "Containers"
}

];


let currentQuestion = 0;

let selectedAnswer = null;

let quizScore = 0;



function showQuiz() {

    document.getElementById(
        "quiz-modal"
    ).style.display = "block";

    currentQuestion = 0;

    quizScore = 0;

    loadQuestion();
}


function closeQuiz() {

    document.getElementById(
        "quiz-modal"
    ).style.display = "none";
}


function loadQuestion() {

    selectedAnswer = null;

    let q =
        quizQuestions[currentQuestion];

    document.getElementById(
        "quiz-question"
    ).innerHTML = `

    <strong>
    Question ${currentQuestion + 1}
    / ${quizQuestions.length}
    </strong>

    <br><br>

    ${q.question}
    `;


    let optionsHTML = "";

    q.options.forEach(option => {

        optionsHTML += `

        <button
        class="quiz-option"
        onclick="selectAnswer(this)">

            ${option}

        </button>
        `;
    });

    document.getElementById(
        "quiz-options"
    ).innerHTML = optionsHTML;
}


function selectAnswer(button) {

    document.querySelectorAll(
        ".quiz-option"
    ).forEach(btn => {

        btn.style.background =
            "rgba(255,255,255,0.04)";
    });

    button.style.background =
        "linear-gradient(to right,#2563eb,#7c3aed)";

    selectedAnswer =
        button.innerText;
}


function nextQuestion() {

    if (!selectedAnswer) {

        alert(
            "Please select an answer."
        );

        return;
    }

    let q =
        quizQuestions[currentQuestion];

    if (selectedAnswer === q.correct) {

        quizScore++;
    }

    currentQuestion++;

    if (
        currentQuestion >=
        quizQuestions.length
    ) {

        let level = "Beginner";

        if (quizScore >= 2) {
            level = "Intermediate";
        }

        if (quizScore === 3) {
            level = "Advanced";
        }

        document.getElementById(
            "quiz-question"
        ).innerHTML = `

        🎉 Assessment Completed!
        `;

        document.getElementById(
            "quiz-options"
        ).innerHTML = `

        <h3>
        Score:
        ${quizScore}
        / ${quizQuestions.length}
        </h3>

        <br>

        <h2>
        Level:
        ${level}
        </h2>
        `;

        return;
    }

    loadQuestion();
}



/* =========================
   AI INTERVIEW SYSTEM
========================= */

let interviewStep = 0;

let interviewRole = "";


const interviewQuestions = {

    "DevOps Engineer": [

        "Tell me about yourself.",

        "What is Docker?",

        "Explain CI/CD.",

        "What is Nginx?"
    ],

    "Linux Administrator": [

        "What does chmod do?",

        "Explain systemctl.",

        "How do you monitor Linux performance?"
    ],

    "AWS Cloud Engineer": [

        "What is EC2?",

        "What is an S3 bucket?",

        "Explain IAM."
    ]
};


function showInterview() {

    document.getElementById(
        "interview-modal"
    ).style.display = "block";
}


function closeInterview() {

    document.getElementById(
        "interview-modal"
    ).style.display = "none";
}


function startInterview() {

    interviewRole =
        document.getElementById(
            "job-role"
        ).value;

    interviewStep = 0;

    loadInterviewQuestion();
}


function loadInterviewQuestion() {

    let questions =
        interviewQuestions[interviewRole];

    if (
        interviewStep >=
        questions.length
    ) {

        document.getElementById(
            "interview-content"
        ).innerHTML = `

        <h2>
        🎉 Interview Completed
        </h2>

        <br>

        <p>
        Great job completing the interview.
        </p>
        `;

        return;
    }

    document.getElementById(
        "interview-content"
    ).innerHTML = `

    <h3>
    ${interviewRole}
    Interview
    </h3>

    <br>

    <strong>
    Question ${interviewStep + 1}
    </strong>

    <br><br>

    <p>
    ${questions[interviewStep]}
    </p>

    <br>

    <textarea
    id="interview-answer"
    placeholder="Type your answer here..."></textarea>

    <br><br>

    <button onclick="submitInterviewAnswer()">

        Submit Answer

    </button>
    `;
}


async function submitInterviewAnswer() {

    let answer =
        document.getElementById(
            "interview-answer"
        ).value;

    if (answer.trim() === "") {

        alert(
            "Please write an answer."
        );

        return;
    }

    let questions =
        interviewQuestions[interviewRole];

    let currentQ =
        questions[interviewStep];


    document.getElementById(
        "interview-content"
    ).innerHTML += `

    <br><br>

    <div class="message ai">

        <div class="typing">

            <span></span>
            <span></span>
            <span></span>

        </div>

    </div>
    `;


    const response = await fetch(
        "/evaluate-interview",
        {

            method: "POST",

            headers: {
                "Content-Type":
                "application/json"
            },

            body: JSON.stringify({

                question: currentQ,

                answer: answer
            })
        }
    );


    const data =
        await response.json();


    document.getElementById(
        "interview-content"
    ).innerHTML = `

    <h3>
    AI Feedback
    </h3>

    <br>

    <div class="message ai">

        ${marked.parse(data.feedback)}

    </div>

    <br>

    <button onclick="continueInterview()">

        Next Question

    </button>
    `;
}
function continueInterview() {

    interviewStep++;

    loadInterviewQuestion();
}
