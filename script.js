const startButton = document.getElementById('start-quiz');
const quizContainer = document.getElementById('quiz-container');

// Fetch quiz data from Cosmos DB
async function fetchQuizzes() {
    try {
        const response = await fetch('/api/quizzes');
        if (!response.ok) {
            throw new Error('Failed to fetch quizzes');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching quizzes:', error);
        return [];
    }
}

// Initialize quizzes when the page loads
window.onload = async () => {
    const quizzes = await fetchQuizzes();
    startButton.addEventListener('click', () => startQuiz(quizzes));
};

function startQuiz(quizzes) {
    quizContainer.innerHTML = '';
    quizzes.forEach((quiz, index) => {
        const quizElement = document.createElement('div');
        quizElement.className = 'quiz';
        quizElement.innerHTML = `
            <h2>${quiz.title}</h2>
            <button onclick="showQuiz(${index})">Take Quiz</button>
        `;
        quizContainer.appendChild(quizElement);
    });
}

function showQuiz(index) {
    const quiz = quizzes[index];
    let quizHTML = `<h2>${quiz.title}</h2>`;
    quiz.questions.forEach((question, qIndex) => {
        quizHTML += `<div class="question">
            <p>${question.question}</p>
            ${question.choices.map(choice => `
                <button onclick="checkAnswer(${index}, ${qIndex}, '${choice}')">${choice}</button>
            `).join('')}
        </div>`;
    });
    quizContainer.innerHTML = quizHTML;
}

function checkAnswer(quizIndex, questionIndex, selectedAnswer) {
    const quiz = quizzes[quizIndex];
    const question = quiz.questions[questionIndex];
    if (selectedAnswer === question.answer) {
        alert('Correct!');
    } else {
        alert('Wrong answer.');
    }
}
