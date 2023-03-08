import pytest
from .models import (
    Tier,
    User,
    TierImage
)

from django.urls import reverse_lazy, reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import os


@pytest.mark.django_db
def test_login_user(client, user):
    '''
    The test of user login with valid credentials
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
def test_upload_image(client, user):
    '''
    Test that the upload image view requires authentication and saves a new TierImage object.
    '''
    response = client.get('/upload_image/')

    assert response.status_code == 302
    assert response.url == '/accounts/login/?next=/upload_image/'

    client.force_login(user)

    test_image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
    with open(test_image_path, 'rb') as f:
        test_image_data = f.read()
    test_image = SimpleUploadedFile('test_image.jpg', test_image_data, content_type='image/jpeg')

    response = client.post(reverse('upload_image'), {'image_file': test_image})

    # image_file = SimpleUploadedFile('test_image.jpg', b'test_image_content')
    # response = client.post('/upload_image/', {
    #     'upload_file': image_file,
    #     'duration': 600,
    #     'tier': user
    # }, follow=True)

    # Expect a redirection response to the success URL
    assert response.status_code == 200
    assert 'upload_image.html' in [t.name for t in response.templates]

    # Check that a new TierImage object was created with the correct data
    uploaded_image_id = client.session.get('uploaded_image_id')
    assert uploaded_image_id is not None

    uploaded_image = TierImage.objects.get(id=uploaded_image_id)
    assert uploaded_image.user == user
    assert uploaded_image.tier == user.tier
    assert uploaded_image.image_file.read() == test_image.read()
    # assert uploaded_image.image_file.read() == b'test_image_content'
    # assert uploaded_image.duration == 600
