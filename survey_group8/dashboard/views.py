from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from core.models import Surveys, Questions, Answers, Results
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden,JsonResponse
import json


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
        try:
            data = json.loads(request.body) 
            name = data.get('name')
            description = data.get('description')
            user = request.user

            # Create a new survey instance
            new_survey = Surveys.objects.create(
                name=name,
                description=description,
                user_id=user,
                republished=0,
                status='d'
            )

            # Process each question in the JSON data
            questions = data.get('questions', {})
            for q_number, q_data in questions.items():
                question_text = q_data.get('question')
                question_type = q_data.get('type', 'Radio')

                # Create a question instance
                question = Questions.objects.create(
                    survey_id=new_survey,
                    question=question_text,
                    type=question_type
                )

                # Process each answer for the question
                answers = q_data.get('answers', {})
                for a_text in answers.values():
                    if a_text:
                        Answers.objects.create(
                            question_id=question,
                            answer=a_text
                        )

            return JsonResponse({'status': 'success', 'message': 'Survey created successfully'})
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

    return render(request, 'new_survey.html')

@login_required
def survey_delete(request, id):
    delete_survey = Surveys.objects.get(id=id)
    delete_survey.delete()
    return redirect('home')

@login_required
def survey_publish(request, id):
    publish_survey = get_object_or_404(Surveys, id=id)

    if publish_survey.user_id != request.user:
        return HttpResponseForbidden("You do not have permission to publish this survey.")
    publish_survey.status = 'p' 
    publish_survey.save()  
    return redirect('home')  

@login_required
def survey_close(request, id):
    close_survey = get_object_or_404(Surveys, id=id)

    if close_survey.user_id != request.user:
        return HttpResponseForbidden("You do not have permission to close this survey.")
    
    close_survey.status = 'c' 
    close_survey.save()  
    return redirect('home') 

@login_required
def survey_draft(request, id):
    draft_survey = get_object_or_404(Surveys, id=id)

    if draft_survey.user_id != request.user:
        return HttpResponseForbidden("You do not have permission to draft this survey.")
    
    draft_survey.status = 'd' 
    draft_survey.save()  
    return redirect('home') 

@login_required
def survey_republish(request, id):
    repubish_survey = get_object_or_404(Surveys, id=id)

    if repubish_survey.user_id != request.user:
        return HttpResponseForbidden("You do not have permission to republish this survey.")
    
    repubish_survey.status = 'p' 
    repubish_survey.republished += 1
    repubish_survey.save()  
    return redirect('home')

@login_required
def survey_edit(request, id):
    return render(request, 'survey_edit.html')
