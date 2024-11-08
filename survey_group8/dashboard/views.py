from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from core.models import Surveys, Questions, Answers, Results
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden,JsonResponse,HttpResponse
import json
from django import forms
from .forms  import AnswerForm

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
        #---MZ---
        surveytake=survey_take(request)
        return render(request, 'taker_dashboard.html',surveytake)  
    
    return render(request, 'home.html')


@user_passes_test(in_survey_creator_group)
def survey_create(request):
    if request.method == 'POST':
        print(request.body)
        try:
            data = json.loads(request.body) 
            name = data.get('name')
            description = data.get('description')
            user = request.user
            new_survey = Surveys.objects.create(
                name=name,
                description=description,
                user_id=user,
                republished=1,
                status='d'
            )

            questions = data.get('questions', {})
            for q_number, q_data in questions.items():
                question_text = q_data.get('question')
                question_type = q_data.get('type', 'Radio')

                question = Questions.objects.create(
                    survey_id=new_survey,
                    question=question_text,
                    type=question_type
                )

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
@login_required
def survey_edit(request, id):
    old_survey = get_object_or_404(Surveys, id=id)

    if request.method == 'POST':

        try:
            data = json.loads(request.body)
            name = data.get('name')
            description = data.get('description')

        
            old_survey.name = name
            old_survey.description = description
            old_survey.save()  


            Questions.objects.filter(survey_id=old_survey).delete()
            Answers.objects.filter(question_id__survey_id=old_survey).delete()

            questions = data.get('questions', {})
            for q_number, q_data in questions.items():
                if isinstance(q_data, dict): 
                    question_text = q_data.get('question')
                    question_type = q_data.get('type', 'Radio')

                    question = Questions.objects.create(
                        survey_id=old_survey,
                        question=question_text,
                        type=question_type
                    )

                    answers = q_data.get('answers', {})
                    for a_text in answers.values():
                        if a_text:
                            Answers.objects.create(
                                question_id=question,
                                answer=a_text
                            )
                else:
                    print(f"Unexpected format for question: {q_data}")
                    return JsonResponse({'status': 'error', 'message': 'Invalid question format'}, status=400)

            return JsonResponse({'status': 'success', 'message': 'Survey updated successfully'})
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

    questions = Questions.objects.filter(survey_id=old_survey)

    questions_data = []
    for question in questions:
        answers = Answers.objects.filter(question_id=question)
        answers_data = {answer.id: answer.answer for answer in answers}
        questions_data.append({
            'question': question,
            'answers': answers_data 
        })

    context = {
        'survey': old_survey,
        'questions_data': questions_data
    }
    return render(request, 'survey_edit.html', context)

#--- MZ ---
def survey_take(request):
    surveys = Surveys.objects.filter(status='p')
    surveys = {
        "surveys":surveys
    }
    return surveys

def qa_view(request, id):
    survey = Surveys.objects.prefetch_related('questions__answers').get(id=id, status='p')
    # republished_ver=survey.republished #直接在前端引用
    user=request.user
    questions = survey.questions.all()
    return render(request, 'qa.html', {'survey': survey, 'questions': questions,'user':user})

@login_required
def qa_submit(request):
    if request.method == 'POST':
        survey_id = request.POST.get('survey_id')
        user = request.user
        survey = get_object_or_404(Surveys, id=survey_id)
        republished_ver=survey.republished
        # 获取问题和答案，保存到 Result 表
        for question in survey.questions.all():
            selected_answers = request.POST.getlist(f'question_{question.id}')  # 获取选择的答案
            
            for answer_id in selected_answers:
                answer = get_object_or_404(Answers, id=answer_id)
                # 保存结果
                Results.objects.create(
                    survey_id=survey,
                    question_id=question,
                    answer_id=answer,
                    user_id=user,
                    republished_version=republished_ver
                )
        return render(request,'thankyou.html')
    return HttpResponse('Invalid request method.', status=405)

def thankyou(request):
    return render(request, 'thankyou.html')

    
