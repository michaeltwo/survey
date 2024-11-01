let questionCount = 1; // Track the number of questions

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
            <tbody id="answersContainer_${questionCount}">
                <tr>
                    <td>Answer 1</td>
                    <td>
                        <input type="text" name="answer_${questionCount}_1" placeholder="Enter Answer">
                        <span class="error" id="answerError${questionCount}_1" style="color:red;"></span>
                    </td>
                </tr>
            </tbody>
        </table>
        <button type="button" onclick="addAnswerField(${questionCount})">Add Another Answer</button>
        <button type="button" onclick="removeQuestion(${questionCount})" id="removeQuestionBtn${questionCount}" style="display: none;">Remove Question</button>
    `;

    questionsContainer.appendChild(newQuestionBlock);

    // Update visibility of "Remove Question" buttons
    updateQuestionButtons();
}

function removeQuestion(questionId) {
    const questionBlock = document.getElementById(`questionBlock${questionId}`);
    questionBlock.remove();
    questionCount--;

    // Update visibility of "Remove Question" buttons
    updateQuestionButtons();
}

function updateQuestionButtons() {
    const questionBlocks = document.querySelectorAll('.questionBlock');
    questionBlocks.forEach((block) => {
        const removeButton = block.querySelector('button[id^="removeQuestionBtn"]');
        if (removeButton) {
            removeButton.style.display = questionBlocks.length > 1 ? 'inline' : 'none';
        }
    });
}

function addAnswerField(questionNumber) {
    const answersContainer = document.getElementById(`answersContainer_${questionNumber}`);
    const answerCount = answersContainer.querySelectorAll("input[type='text']").length + 1;

    const newAnswerRow = document.createElement('tr');
    newAnswerRow.id = `answerField_${questionNumber}_${answerCount}`;
    newAnswerRow.innerHTML = `
        <td>Answer ${answerCount}</td>
        <td>
            <input type="text" name="answer_${questionNumber}_${answerCount}" placeholder="Enter Answer">
            <button type="button" onclick="removeAnswer(${questionNumber}, ${answerCount})">Remove Answer</button>
            <span class="error" id="answerError${questionNumber}_${answerCount}" style="color:red;"></span>
        </td>
    `;
    answersContainer.appendChild(newAnswerRow);

    // Update visibility of "Remove Answer" buttons
    updateAnswerButtons(questionNumber);
}

function removeAnswer(questionNumber, answerId) {
    const answerField = document.getElementById(`answerField_${questionNumber}_${answerId}`);
    answerField.remove();

    // Update visibility of "Remove Answer" buttons
    updateAnswerButtons(questionNumber);
}

function updateAnswerButtons(questionNumber) {
    const answersContainer = document.getElementById(`answersContainer_${questionNumber}`);
    const answerFields = answersContainer.querySelectorAll("tr[id^='answerField_']");
    answerFields.forEach((answerField) => {
        const removeButton = answerField.querySelector('button');
        if (removeButton) {
            removeButton.style.display = answerFields.length > 1 ? 'inline' : 'none';
        }
    });
}

// Initialize by hiding the remove buttons if there is only one question
document.addEventListener('DOMContentLoaded', updateQuestionButtons);
