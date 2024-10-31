from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from .models import UserProfile

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save()  # Save the user
        UserProfile.objects.create(user=user, user_type=form.cleaned_data['user_type'])
        return super().form_valid(form)
