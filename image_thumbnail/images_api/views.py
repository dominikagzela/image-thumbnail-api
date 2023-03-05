from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, ListView, CreateView, View
from .forms import LoginUserForm, TierImageForm
from django.contrib.auth import authenticate, login, logout
from .models import User, Tier, TierImage
from django.contrib.auth.mixins import LoginRequiredMixin


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


class LogoutView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class DashboardUserView(LoginRequiredMixin, ListView):
    template_name = 'dashboard_user.html'
    model = User


# class UploadImageView(FormView):
#     template_name = 'upload_image.html'
#     form_class = TierImageForm
#     success_url = reverse_lazy('image_links')
#
#     def form_valid(self, form):
#         tier_image = form.save(commit=False)
#         tier_image.tier = self.request.user
#         tier_image.save()
#         return super().form_valid(form)
#
#     def post(self, request, *args, **kwargs):
#         if "cancel" in request.POST:
#             return HttpResponseRedirect(self.success_url)
#         else:
#             return super(UploadImageView, self).post(request, *args, **kwargs)

class UploadImageView(LoginRequiredMixin, FormView):
    template_name = 'upload_image.html'
    form_class = TierImageForm
    success_url = reverse_lazy('image-links')

    # def get_form_kwargs(self):
    #     kwargs = super(UploadImageView, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user  # pass the logged-in user to the form
    #     return kwargs
    #
    # def form_valid(self, form):
    #     tier_image = TierImage(upload_file=self.request.FILES['upload_file'])
    #     tier_image.tier = self.request.user.tier
    #     if 'duration' in form.cleaned_data:
    #         tier_image.duration = form.cleaned_data['duration']
    #     tier_image.save()
    #     return super().form_valid(form)
    #
    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)
    #     ctx['tier_images'] = TierImage.objects.filter(tier=self.request.user.tier)
    #     return ctx

    def form_valid(self, form):
        # save the uploaded image and duration here
        tier_image = form.save(commit=False)
        tier_image.tier = self.request.user.tier
        tier_image.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


# class ImageLinksView(LoginRequiredMixin, ListView):
#     template_name = 'dashboard_user.html'
#     model = TierImage
#     context_object_name = 'images'
#
#     def get_queryset(self):
#         user = self.request.user
#         tier = user.tier
#         queryset = super().get_queryset().filter(tier=tier)
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         tier = user.tier
#
#         return context

