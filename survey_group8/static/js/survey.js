let questionCount = 1; // Keep track of the number of questions

function addQuestion() {
    questionCount++;
    const questionsContainer = document.getElementById('questionsContainer');

    // Create a new question block
    const newQuestionBlock = document.createElement('div');
    newQuestionBlock.className = 'questionBlock';
    newQuestionBlock.id = `questionBlock${questionCount}`;

    newQuestionBlock.innerHTML = `
        <table border="1">
            <tr>
                <td>Question ${questionCount}</td>
                <td>
                    <input type="text" name="question_${questionCount}" placeholder="Enter Question">
                    <span class="error" id="questionError${questionCount}" style="color:red;"></span>
                </td>
            </tr>
            <tr>
                <td>Question Type</td>
                <td>
                    <label>
                        <input type="radio" name="type_${questionCount}" value="Radio" checked>
                        Radio Buttons
                    </label>
                    <label style="margin-left: 20px;">
                        <input type="radio" name="type_${questionCount}" value="Checkboxes">
                        Checkboxes
                    </label>
                </td>
            </tr>
            <tr>
                <td>Answer 1</td>
                <td>
                    <input type="text" name="answer_${questionCount}_1" placeholder="Enter Answer">
                    <span class="error" id="answerError${questionCount}_1" style="color:red;"></span>
                </td>
            </tr>
        </table>
        <button type="button" onclick="addAnswerField(${questionCount})">Add Another Answer</button>
    `;

    questionsContainer.appendChild(newQuestionBlock);
}

function addAnswerField(questionNumber) {
    const answerCount = document.querySelectorAll(`input[name^='answer_${questionNumber}']`).length + 1; // Count existing answers
    const questionBlock = document.getElementById(`questionBlock${questionNumber}`);

    const newAnswerField = document.createElement('tr');
    newAnswerField.innerHTML = `
        <td>Answer ${answerCount}</td>
        <td>
            <input type="text" name="answer_${questionNumber}_${answerCount}" placeholder="Enter Answer">
            <span class="error" id="answerError${questionNumber}_${answerCount}" style="color:red;"></span>
        </td>
    `;

    questionBlock.querySelector('table').appendChild(newAnswerField);
}
