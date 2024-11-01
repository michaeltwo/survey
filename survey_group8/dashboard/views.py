from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from core.models import Surveys, Questions, Answers, Results
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def in_survey_taker_group(user):
    return user.groups.filter(name='Taker').exists()

def in_survey_creator_group(user):
    return user.groups.filter(name='Creator').exists()


def categorize_surveys(surveys):
    draft_surveys = []
    published_surveys = []
    closed_surveys = []

    for survey in surveys:
        survey_data = {"name": survey.name, "id": survey.id}
        if survey.status == 'd':
            draft_surveys.append(survey_data)
        elif survey.status == 'p':
            published_surveys.append(survey_data)
        elif survey.status == 'c':
            closed_surveys.append(survey_data)

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

def survey_delete(request, id):
    delete_survey = Surveys.objects.get(id=id)
    delete_survey.delete()
    return redirect('home')

def survey_publish(request, id):
    publish_survey = get_object_or_404(Surveys, id=id)

    if publish_survey.user_id != request.user:
        return HttpResponseForbidden("You do not have permission to publish this survey.")

    # Proceed to publish the survey
    publish_survey.status = 'p' 
    publish_survey.save()  
    return redirect('home')  