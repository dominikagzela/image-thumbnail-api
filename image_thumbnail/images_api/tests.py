import pytest
from .models import (TierImage)
from django.urls import reverse_lazy
from .views import ImageLinksView


@pytest.mark.django_db
def test_login_user(client, user):
    '''
    The test of user login with valid credentials.
    '''
    username = 'usertest'
    password = 'passwordtest'

    response = client.post(reverse_lazy('login'), {
        'username': username,
        'password': password,
    })

    assert response.status_code == 302
    assert response.url == reverse_lazy('dashboard-user')


@pytest.mark.django_db
def test_logout_user(client, user):
    '''
    The test of user logout.
    '''

    client.login(username='usertest', password='passwordtest')
    response = client.get('/logout/')

    assert response.status_code == 302
    assert response.url == reverse_lazy('login')
    assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_dashboard_user(client, user):
    '''
    The test of displaying dashboard user.
    '''
    response = client.get('/dashboard_user/')

    assert response.status_code == 302
    assert response.url == '/accounts/login/?next=/dashboard_user/'

    client.force_login(user)
    response = client.get('/dashboard_user/')

    assert response.status_code == 200
    assert 'dashboard_user.html' in [t.name for t in response.templates]
    assert 'user_list' in response.context
    assert user in response.context['user_list']


@pytest.mark.django_db
def test_upload_image(client, user, file_data):
    """
    The test of uploading image by user.
    """
    client.force_login(user)
    url = reverse_lazy('upload-image')
    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url, data=file_data, follow=True)
    assert response.status_code == 200

    uploaded_image = TierImage.objects.last()
    assert uploaded_image.tier == user.tier

    assert uploaded_image.upload_file.storage.exists(uploaded_image.upload_file.name)
    assert uploaded_image.duration == 600


@pytest.mark.django_db
def test_upload_image_view(client, user, file_data):
    """
    The test of uploading an image via the image upload view.
    """
    client.force_login(user)
    url = reverse_lazy('upload-image')
    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url, data=file_data, follow=True)
    assert response.status_code == 200

    uploaded_image = TierImage.objects.last()
    assert uploaded_image.tier == user.tier

    assert uploaded_image.upload_file.storage.exists(uploaded_image.upload_file.name)
    assert uploaded_image.duration == 600


@pytest.mark.django_db
def test_upload_image_view_form_validity(client, user):
    """
    The test of form validity of the image upload view.
    """
    client.force_login(user)
    url = reverse_lazy('upload-image')
    response = client.get(url)
    assert response


@pytest.mark.django_db
def test_image_links_view_unauthenticated_user(client):
    """
    The test of accessing the image links view as an unauthenticated user.
    """
    url = reverse_lazy('image-links')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/accounts/login/?next=/image_links/'


@pytest.mark.django_db
def test_image_links_view(factory, tier_image, user):
    """
    The test of accessing the image links view as an authenticated user
    and checks that the correct data is displayed in the context.
    """
    request = factory.get(reverse_lazy('image-links'))
    request.user = user
    request.session = {'uploaded_image_id': tier_image.id}

    response = ImageLinksView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['tier_name'] == user.tier.name
    assert response.context_data['image_id'] == tier_image.id
    assert response.context_data['original_link'] == f'http://127.0.0.1:8001{tier_image.upload_file.url}'
    assert 'thumbnail_links' in response.context_data

    if tier_image.duration is not None:
        assert response.context_data['expiring_link'] is not None
