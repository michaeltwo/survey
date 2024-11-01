from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from core.models import Surveys, Questions, Answers, Results
from django.contrib.auth.decorators import user_passes_test

def in_survey_taker_group(user):
    return user.groups.filter(name='Taker').exists()

def in_survey_creator_group(user):
    return user.groups.filter(name='Creator').exists()


def categorize_surveys(surveys):
    draft_surveys = []
    published_surveys = []
    closed_surveys = []

    for survey in surveys:
        if survey.status == 'd':
            draft_surveys.append(survey.name)
        elif survey.status == 'p':
            published_surveys.append(survey.name)
        elif survey.status == 'c':
            closed_surveys.append(survey.name)

    return draft_surveys, published_surveys, closed_surveys

def home(request):
    if request.user.groups.filter(name='Creator').exists():
        survey_all = Surveys.objects.select_related('user_id').all().order_by('id')
        draft_surveys, published_surveys, closed_surveys = categorize_surveys(survey_all)
    
        survey_context = {
            'draft_surveys': draft_surveys,
            'published_surveys': published_surveys,
            'closed_surveys': closed_surveys,
        }
        return render(request, 'creator_dashboard.html', survey_context)
    
    elif request.user.groups.filter(name='Taker').exists():
        return render(request, 'taker_dashboard.html')  
    
    return render(request, 'home.html')


@user_passes_test(in_survey_creator_group)
def survey_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        user = request.user  
        
        new_survey = Surveys.objects.create(
            name=name,
            description=description,
            user_id=user,
            republished=0,  
            status='d'  
        )

        
        question_number = 1
        while True:
            question_key = f'question_{question_number}'
            question_text = request.POST.get(question_key)
            
            if not question_text:
                break  

            question_type = request.POST.get(f'type_{question_number}', 'Radio')  
            question = Questions.objects.create(
                survey_id=new_survey,
                question=question_text,
                type=question_type
            )

            answer_number = 1
            while True:
                answer_key = f'answer_{question_number}_{answer_number}'
                answer_text = request.POST.get(answer_key)

                if not answer_text:
                    break  

                Answers.objects.create(
                    question_id=question,
                    answer=answer_text
                )
                answer_number += 1

            question_number += 1

        return redirect('home')

    return render(request, 'new_survey.html')