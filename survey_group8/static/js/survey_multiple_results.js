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
    for (const [questionText, questionData] of Object.entries(organizedQuestionData)) {
        const questionTable = createResultsTable(questionText, questionData, totalRespondentsData);
        resultsContainer.appendChild(questionTable);
    }
}

function createResultsTable(questionText, questionData, totalRespondentsData) {
    const table = document.createElement('table');
    table.style.width = '100%';
    table.style.borderCollapse = 'collapse';
    table.style.marginBottom = '20px'; 


    const headerRow = document.createElement('tr');
    headerRow.innerHTML = '<th style="border: 1px solid #ddd; padding: 8px;">Question</th><th style="border: 1px solid #ddd; padding: 8px;">Answer</th>';

    const versionsSet = new Set();
    for (const answerInfo of Object.values(questionData.answers)) {
        for (const version of Object.keys(answerInfo.versions)) {
            versionsSet.add(version);
        }
    }

    versionsSet.forEach(version => {
        const totalRespondents = totalRespondentsData.find(data => data[0] == version)?.[1] || 0;
        headerRow.innerHTML += `<th style="border: 1px solid #ddd; padding: 8px;">Publication ${version} (${totalRespondents} total responses)</th>`;
    });
    table.appendChild(headerRow);


    for (const [answerText, answerInfo] of Object.entries(questionData.answers)) {
        const row = document.createElement('tr');

   
        if (answerText === Object.keys(questionData.answers)[0]) {
            row.innerHTML += `<td style="border: 1px solid #ddd; padding: 8px;" rowspan="${Object.keys(questionData.answers).length}">${questionText}</td>`;
        }
        
        row.innerHTML += `<td style="border: 1px solid #ddd; padding: 8px;">${answerText}</td>`;

        versionsSet.forEach(version => {
            const resultData = answerInfo.versions[version];
            const cellContent = resultData ? `${resultData.count} responses (${resultData.percentage.toFixed(1)}%)` : '0 responses (0.0%)';
            row.innerHTML += `<td style="border: 1px solid #ddd; padding: 8px;">${cellContent}</td>`;
        });

        table.appendChild(row);
    }

    const canvasRow = document.createElement('tr');
    const canvasCell = document.createElement('td');
    canvasCell.colSpan = 1 + versionsSet.size; 
    const canvas = document.createElement('canvas');
    canvas.id = `chart-${questionText.replace(/\s+/g, '-')}`;
    canvasCell.appendChild(canvas);
    canvasRow.appendChild(canvasCell);
    table.appendChild(canvasRow);

    // Render the bar chart after a brief delay beacuse otherwise it wont find container
    setTimeout(() => {
        renderBarChart(canvas.id, questionData);
    }, 0);

    return table;
}

function renderBarChart(canvasId, questionData) {
    const labels = Object.keys(questionData.answers);
    const datasets = [];
    const totalRespondents = questionData.total_respondents;

    const versionsSet = new Set(Object.keys(totalRespondents));
    const colors = ['rgba(0, 123, 255, 0.6)', 'rgba(255, 99, 132, 0.6)', 'rgba(255, 206, 86, 0.6)', 'rgba(75, 192, 192, 0.6)', 'rgba(153, 102, 255, 0.6)'];

    versionsSet.forEach((version, index) => {
        const dataPercentages = labels.map(answer => {
            return questionData.answers[answer].versions[version]?.percentage || 0; 
        });

        datasets.push({
            label: `Publication ${version}`,
            data: dataPercentages,
            backgroundColor: colors[index % colors.length],
            borderColor: colors[index % colors.length].replace('0.6', '1'),
            borderWidth: 1
        });
    });

    const data = {
        labels: labels,
        datasets: datasets
    };

    const ctx = document.getElementById(canvasId)?.getContext('2d');
    if (!ctx) {
        console.error(`No canvas found with id: ${canvasId}`);
        return;
    }

    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100 
                }
            }
        }
    });
}


function handleError(error) {
    console.error('There was a problem with the fetch operation:', error);
}
