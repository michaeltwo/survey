from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from core.models import Surveys, Questions, Answers, Results
from django.db.models import Max

def survey_results_published(request, id):
    survey = Surveys.objects.get(id=id)
    questions = survey.questions.all()  # Get all questions in the survey

    # Get the highest republished version for the survey
    latest_version = Results.objects.filter(survey_id=survey).aggregate(max_version=Max('republished_version'))['max_version']

    # Calculate the total number of unique respondents for the latest version
    total_respondents = Results.objects.filter(survey_id=survey, republished_version=latest_version).values('user_id').distinct().count()

    question_data = []
    for question in questions:
        answer_data = []
        
        # Count total responses for this question in the latest version
        total_responses = Results.objects.filter(question_id=question, republished_version=latest_version).count()

        for answer in question.answers.all():
            # Get the count of responses for this answer in the latest version
            count = Results.objects.filter(question_id=question, answer_id=answer, republished_version=latest_version).count()
            percentage = (count / total_responses * 100) if total_responses > 0 else 0
            answer_data.append({
                'answer_text': answer.answer,
                'count': count,
                'percentage': percentage,
            })

        question_data.append({
            'question_text': question.question,
            'answers': answer_data,
        })

    context = {
        'survey': survey,
        'question_data': question_data,
        'total_respondents': total_respondents,
        'latest_version': latest_version,
    }
    return render(request, 'results.html', context)