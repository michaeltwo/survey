let qId = 0;

function addQuestion() {
    qId++;
    const qContainer = document.getElementById('questionsContainer');
    const qBlock = document.createElement('div');
    qBlock.className = 'questionBlock';
    qBlock.id = `qBlock_${qId}`;
    qBlock.innerHTML = `
        <table border="1">
            <tr>
                <td>Question</td>
                <td>
                    <input type="text" name="question_${qId}" placeholder="Enter Question">
                    <span class="error" id="qError${qId}" style="color:red;"></span>
                </td>
            </tr>
            <tr>
                <td>Question Type</td>
                <td>
                    <label>
                        <input type="radio" name="type_${qId}" value="Radio" checked>
                        Radio Buttons
                    </label>
                    <label style="margin-left: 20px;">
                        <input type="radio" name="type_${qId}" value="Checkboxes">
                        Checkboxes
                    </label>
                </td>
            </tr>
            <tbody id="aContainer_${qId}">
                <tr id="aField_${qId}_1">
                    <td>Answer</td>
                    <td>
                        <input type="text" name="answer_${qId}_1" placeholder="Enter Answer">
                        <button type="button" onclick="removeAnswer(${qId}, 1)">Remove Answer</button>
                        <span class="error" id="aError${qId}_1" style="color:red;"></span>
                    </td>
                </tr>
            </tbody>
        </table>
        <button type="button" onclick="addAnswerField(${qId})">Add Another Answer</button>
        <button type="button" onclick="removeQuestion(${qId})" id="removeQBtn${qId}" style="display: inline;">Remove Question</button>
    `;
    qContainer.appendChild(qBlock);
}

function removeQuestion(id) {
    const block = document.getElementById(`qBlock_${id}`);
    if (block) block.remove();
}

function addAnswerField(qId) {
    const aContainer = document.getElementById(`aContainer_${qId}`);
    const aCount = aContainer.querySelectorAll("tr[id^='aField_']").length + 1;
    const aRow = document.createElement('tr');
    aRow.id = `aField_${qId}_${aCount}`;
    aRow.innerHTML = `
        <td>Answer</td>
        <td>
            <input type="text" name="answer_${qId}_${aCount}" placeholder="Enter Answer">
            <button type="button" onclick="removeAnswer(${qId}, ${aCount})">Remove Answer</button>
            <span class="error" id="aError${qId}_${aCount}" style="color:red;"></span>
        </td>
    `;
    aContainer.appendChild(aRow);
}

function removeAnswer(qId, aId) {
    const aField = document.getElementById(`aField_${qId}_${aId}`);
    if (aField) aField.remove();
}
