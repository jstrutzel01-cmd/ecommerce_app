from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

class SignUp(CreateView):
    template_name = "registration/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")