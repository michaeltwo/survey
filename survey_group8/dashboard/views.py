from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

#@login_required
def home(request):
    # Check if the user is in the 'Survey Creator' group
    if request.user.groups.filter(name='Creator').exists():
        return render(request, 'creator_dashboard.html')  # Template for creators
    elif request.user.groups.filter(name='Taker').exists():
        return render(request, 'taker_dashboard.html')  # Template for takers
    else:
        return render(request, 'home.html')  