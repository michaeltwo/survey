from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm  

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save()
        user_type = form.cleaned_data.get('user_type')

        if user_type == 'Taker':
            group = Group.objects.get(name='Taker')
        elif user_type == 'Creator':
            group = Group.objects.get(name='Creator')
        else:
            group = None

        if group:
            user.groups.add(group)

        login(self.request, user) 
        return super().form_valid(form)
