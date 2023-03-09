from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, ListView
from .forms import LoginUserForm, TierImageForm
from django.contrib.auth import authenticate, login, logout
from .models import User, TierImage

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import datetime
from easy_thumbnails.files import get_thumbnailer
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect
from django.core import signing
from django.conf import settings


class LoginView(FormView):
    """
    The view that allows the user to log in and redirects user to the dashboard page.
    """
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
    """
    The view that allows the user to log out and redirects to the login view.
    """
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class DashboardUserView(LoginRequiredMixin, ListView):
    """
    The view shows the dashboard for the user with the menu available.
    """
    template_name = 'dashboard_user.html'
    model = User


class UploadImageView(LoginRequiredMixin, FormView):
    """
    The view allows the user to upload an image and redirects to the Image Links view.
    """
    template_name = 'upload_image.html'
    form_class = TierImageForm
    success_url = reverse_lazy('image-links')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.tier = self.request.user.tier
        form.save()

        self.request.session['uploaded_image_id'] = form.instance.id
        return redirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ImageLinksView(LoginRequiredMixin, ListView):
    """
    The view shows the user a list of links (depending on account tier:
    original link, expiring link, thumbnail links).
    """
    template_name = 'image_links.html'
    model = TierImage

    def get_queryset(self):
        uploaded_image_id = self.request.session.get('uploaded_image_id')
        if uploaded_image_id:
            try:
                return TierImage.objects.filter(id=uploaded_image_id)
            except ObjectDoesNotExist:
                raise Http404('The requested image does not exist')
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_tier = self.request.user.tier
        context['tier_name'] = user_tier.name

        try:
            uploaded_image = self.get_queryset().get()
        except ObjectDoesNotExist:
            raise Exception('There is no uploaded image')

        context['image_id'] = uploaded_image.id
        original_link = 'http://127.0.0.1:8000' + uploaded_image.upload_file.url

        if user_tier.link_to_original:
            context['original_link'] = original_link

        if user_tier.expiring_links and uploaded_image.duration is not None:
            expiration_time = timezone.now() + timezone.timedelta(seconds=int(uploaded_image.duration))
            # expiration_timestamp = int(expiration_time.timestamp())
            # token = signing.dumps({'url': uploaded_image.upload_file.url, 'expires': expiration_timestamp},
            #                       key=settings.SECRET_KEY)
            # expiring_link = original_link + '?token=' + token
            context['expiring_link'] = expiration_time

        try:
            thumbnail_sizes_in_list = user_tier.thumbnail_height_sizes.split(',')
        except (ValueError, TypeError):
            raise Exception('Invalid thumbnail sizes')

        original_width = uploaded_image.upload_file.width
        original_height = uploaded_image.upload_file.height
        aspect_ratio = original_width / original_height

        thumbnailer = get_thumbnailer(uploaded_image.upload_file)

        thumbnail_links = {}
        for size in thumbnail_sizes_in_list:
            height = int(size)
            new_width = height * aspect_ratio
            thumbnail_options = {'size': (new_width, height)}
            final_thumbnail = thumbnailer.get_thumbnail(thumbnail_options)

            thumbnail_link = final_thumbnail.url
            thumbnail_links[f'{height}'] = 'http://127.0.0.1:8000' + thumbnail_link

        context['thumbnail_links'] = thumbnail_links

        return context


class AllUserImagesListView(LoginRequiredMixin, ListView):
    """
    The view shows the user a list of his uploaded images.
    """
    template_name = 'images_list.html'

    def get_queryset(self):
        try:
            user_tier = self.request.user.tier
        except ObjectDoesNotExist:
            raise Http404('The requested tier does not exist')
        return TierImage.objects.filter(tier=user_tier)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['all_user_images'] = ctx['object_list']
        return ctx
