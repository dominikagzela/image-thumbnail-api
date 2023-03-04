from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, ListView, CreateView
from .forms import LoginUserForm
from django.contrib.auth import authenticate, login, logout
from .models import User


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('dashboard-user')

    def form_valid(self, form):
        cd = form.cleaned_data
        username = cd['username']
        password = cd['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)


class LogoutView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class DashboardUserView(ListView):
    '''
    The view shows the dashboard for the client with the menu available.
    '''
    template_name = 'dashboard_user.html'
    queryset = User.objects.filter(id=1)


class UploadImageView(CreateView):
    pass