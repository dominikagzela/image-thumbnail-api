from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, ListView, CreateView, DetailView
from .forms import LoginUserForm, TierImageForm
from django.contrib.auth import authenticate, login, logout
from .models import User, Tier, TierImage
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime, timedelta
from django.utils import timezone
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from easy_thumbnails.files import get_thumbnailer


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

    # def form_valid(self, form):
    #     # save the uploaded image and duration here
    #     tier_image = form.save(commit=False)
    #     tier_image.tier = self.request.user.tier
    #     tier_image.save()
    #     return super().form_valid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.tier = self.request.user.tier

        self.request.session['uploaded_image_id'] = form.save().id
        messages.success(self.request, 'Image uploaded successfully!')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ImageLinksView(SuccessMessageMixin, DetailView):
    template_name = 'image_links.html'
    model = TierImage

    # context_object_name = 'images'

    def get_object(self):
        uploaded_image_id = self.request.session.get('uploaded_image_id', None)
        if uploaded_image_id:
            return TierImage.objects.get(id=uploaded_image_id)
        # return super().get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_tier = self.request.user.tier
        context['tier_name'] = user_tier.name

        uploaded_image_id = self.request.session.get('uploaded_image_id', None)
        if uploaded_image_id is None:
            raise Exception('There is no uploaded image')
        uploaded_image = TierImage.objects.get(id=uploaded_image_id)
        if uploaded_image_id:
            context['image_id'] = uploaded_image_id

        if user_tier.link_to_original:
            context['original_link'] = 'http://127.0.0.1:8000' + uploaded_image.upload_file.url

        if user_tier.expiring_links:
            expiration_time = timezone.now() + timezone.timedelta(seconds=int(uploaded_image.duration))
            context['expiring_link'] = expiration_time

        sizes = user_tier.thumbnail_height_sizes.split(',')

        original_width = uploaded_image.upload_file.width
        original_height = uploaded_image.upload_file.height
        aspect_ratio = original_width / original_height

        thumbnailer = get_thumbnailer(uploaded_image.upload_file)

        thumbnail_links = {}
        for size in sizes:
            height = int(size)
            new_width = height * aspect_ratio
            thumbnail_options = {'size': (new_width, height)}
            thumbnail = thumbnailer.get_thumbnail(thumbnail_options)

            thumbnail_link = thumbnail.url
            thumbnail_links[f'{height}'] = 'http://127.0.0.1:8000' + thumbnail_link
        context['thumbnail_links'] = thumbnail_links

        return context
