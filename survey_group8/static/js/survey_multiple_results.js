document.addEventListener('DOMContentLoaded', () => {
    const surveyId = getSurveyIdFromURL();
    fetchSurveyResults(surveyId);
});

function getSurveyIdFromURL() {
    const pathSegments = window.location.pathname.split('/');
    return pathSegments[pathSegments.length - 2];
}

function fetchSurveyResults(surveyId) {
    fetch(`/results/closed/${surveyId}/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(handleResponse)
    .then(data => {
        updateSurveyInfo(data);
        renderResults(data.organized_question_data, data.total_respondents_data);
    })
    .catch(handleError);
}

function handleResponse(response) {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
}

function updateSurveyInfo(data) {
    document.getElementById('survey-name').textContent = data.survey_name;
    document.getElementById('survey-description').textContent = data.survey_description;
}

function renderResults(organizedQuestionData, totalRespondentsData) {
    const resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = '';

    const table = createResultsTable(organizedQuestionData, totalRespondentsData);
    resultsContainer.appendChild(table);
}

function createResultsTable(organizedQuestionData, totalRespondentsData) {
    const table = document.createElement('table');
    table.style.width = '100%';
    table.style.borderCollapse = 'collapse';

    const headerRow = document.createElement('tr');
    headerRow.innerHTML = '<th style="border: 1px solid #ddd; padding: 8px;">Question</th><th style="border: 1px solid #ddd; padding: 8px;">Answer</th>';

    const versionsSet = new Set();
    for (const questionData of Object.values(organizedQuestionData)) {
        for (const answerInfo of Object.values(questionData.answers)) {
            for (const version of Object.keys(answerInfo.versions)) {
                versionsSet.add(version);
            }
        }
    }
    
    versionsSet.forEach(version => {
        const totalRespondents = totalRespondentsData.find(data => data[0] == version)?.[1] || 0;
        headerRow.innerHTML += `<th style="border: 1px solid #ddd; padding: 8px;">Publication ${version} (${totalRespondents} total responses)</th>`;
    });
    table.appendChild(headerRow);

    for (const [questionText, questionData] of Object.entries(organizedQuestionData)) {
        for (const [answerText, answerInfo] of Object.entries(questionData.answers)) {
            const row = document.createElement('tr');
            if (answerText === Object.keys(questionData.answers)[0]) {
                row.innerHTML = `<td style="border: 1px solid #ddd; padding: 8px;" rowspan="${Object.keys(questionData.answers).length}">${questionText}</td>`;
            }
            row.innerHTML += `<td style="border: 1px solid #ddd; padding: 8px;">${answerText}</td>`;

            versionsSet.forEach(version => {
                const resultData = answerInfo.versions[version];
                const cellContent = resultData ? `${resultData.count} responses (${resultData.percentage.toFixed(1)}%)` : '0 responses (0.0%)';
                row.innerHTML += `<td style="border: 1px solid #ddd; padding: 8px;">${cellContent}</td>`;
            });

            table.appendChild(row);
        }
    }

    return table;
}

function handleError(error) {
    console.error('There was a problem with the fetch operation:', error);
}
