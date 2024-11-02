from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from core.models import Surveys, Questions, Answers, Results
from django.db.models import Max
from django.http import Http404

def survey_results_closed(request, id):
    return HttpResponse("Hello world!")

def survey_results_published(request, id):
    survey = Surveys.objects.get(id=id)

    if survey.status != 'p': # check if survey is in publish mode
        raise Http404("Survey not available.")
    
    if survey.user_id != request.user:
        raise Http404("You do not have permission to view these results.")
    
    questions = survey.questions.all()  

    max_republished = Surveys.objects.filter(pk=id).aggregate(Max('republished'))['republished__max'] #
   
    total_respondents = Results.objects.filter(survey_id=survey, republished_version=max_republished).values('user_id').distinct().count()

    question_data = []
    total_respondents = Results.objects.filter(survey_id=survey, republished_version=max_republished).count()

    if total_respondents > 0:
        results = Results.objects.filter(survey_id=survey, republished_version=max_republished)

        for question in questions:
            answers = Answers.objects.filter(question_id=question)

            answer_data = []
            for answer in answers:
                response_count = results.filter(answer_id=answer).count()
                percentage = (response_count / total_respondents * 100) if total_respondents > 0 else 0

                answer_data.append({
                    'answer_text': answer.answer,
                    'count': response_count,
                    'percentage': percentage,
                })

            question_data.append({
                'question_text': question.question,
                'answers': answer_data,
            })
    else:
        question_data.append({
            'question_text': "No responses yet",
            'answers': []
        })

    context = {
        'survey': survey,
        'question_data': question_data,
        'total_respondents': total_respondents,
    }

    return render(request, 'results.html', context)