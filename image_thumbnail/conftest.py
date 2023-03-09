import pytest
from django.test import Client
from images_api.models import (
    Tier,
    User,
    TierImage
)
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from mixer.backend.django import mixer


@pytest.fixture
def client():
    '''
    Testing client used to call request.
    '''
    client = Client()
    # client = Client(enforce_csrf_checks=True)
    return client


@pytest.fixture
def tier():
    return Tier.objects.create(
        name='Test Tier',
        link_to_original=True,
        thumbnail_height_sizes='300,400',
        expiring_links=True
    )


@pytest.fixture
def user(tier):
    '''
    Creating test client.
    '''
    user = User.objects.create_user(username='usertest', password='passwordtest')
    user.tier = tier
    user.save()
    return user


@pytest.fixture
def tier_image(tier):
    image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x04\x00\x00\x00\x9a' \
                 b'\x1e\xdd$\x00\x00\x00\rIDAT\x08\xd7c\xf8\xff\xff?\x03\x05\xfb\x01\xbf\xad\x08\t\x82\x8d \x00' \
                 b'\x00\x00\x00IEND\xaeB`\x82'
    image_file = SimpleUploadedFile('test_image.png', image_data, content_type='image/png')
    return TierImage.objects.create(upload_file=image_file, duration=3600, tier=tier)


@pytest.fixture
def image():
    '''
    Creating test image.
    '''
    image = User.objects.create_user(username='usertest', password='passwordtest')
    return image


@pytest.fixture
def file_data():
    with open('test_image_file/test_image.jpg', 'rb') as f:
        return {
            'upload_file': SimpleUploadedFile(f.name, f.read(), content_type='image/jpeg'),
            'duration': 600,
        }


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def tier_image():
    return mixer.blend('images_api.TierImage')


# @pytest.fixture
# def user_tier():
#     return mixer.blend('images_api.Tier')
#
#
# @pytest.fixture
# def tier_images(user_tier):
#     return [mixer.blend('images_api.TierImage', tier=user_tier) for _ in range(5)]
