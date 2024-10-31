from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from core.models import Surveys
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
        name = request.POST['name']
        description = request.POST['description']
        stock_quantity = request.POST['stock']
        price = request.POST['price']
        created_at = timezone.now()
        updated_at = timezone.now()
        user = request.user
        version = 1
        new_product = Product.objects.create(name=name, version=version, description=description, stock_quantity=stock_quantity, price=price, user=user, created_at=created_at,updated_at=updated_at)
        Log.objects.create(version=version,name=name,description=description,stock_quantity=stock_quantity,price=price,timestamp=updated_at,modified_by_id=user.id,product_id=new_product.id, instruction='create')
        return redirect('product_list')
    return render(request, 'new_survey.html')