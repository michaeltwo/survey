from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from core.models import Surveys

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