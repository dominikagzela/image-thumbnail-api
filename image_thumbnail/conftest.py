import pytest
from django.test import Client
from images_api.models import (
    Tier,
    User,
    TierImage
)

@pytest.fixture
def client():
    '''
    Testing client used to call request.
    '''
    client = Client()
    # client = Client(enforce_csrf_checks=True)
    return client


@pytest.fixture
def user():
    '''
    Creating test client.
    '''
    user = User.objects.create_user(username='usertest', password='passwordtest')
    return user


@pytest.fixture
def image():
    '''
    Creating test image.
    '''
    image = User.objects.create_user(username='usertest', password='passwordtest')
    return image

# @pytest.fixture
# def exercise():
#     '''
#     Creating test exercise.
#     '''
#     exercise = Exercises.objects.create(
#         name='test exercise',
#         description='description of test exercise',
#         url='https://www.youtube.com/watch?v=LYX6nlECcro&list=PLOLrQ9Pn6caw3ilqDR8_qezp76QuEOlHY',
#     )
#     return exercise
#
#
# @pytest.fixture
# def tip():
#     '''
#     Creating test practical tip.
#     '''
#     tip = PracticalTips.objects.create(tip='testowy')
#     return tip


@pytest.fixture
def macro_elements(user):
    '''
    Creating test macro elements for client.
    '''
    macros = MacroElements.objects.create(
        calories=1950,
        protein=60,
        fat=30,
        carb=300,
        user=user
    )
    return macros


# @pytest.fixture
# def users():
#     '''
#     Creating several test clients.
#     '''
#     user1 = User.objects.create(
#         first_name='Dorota',
#         username='userd',
#         password='passd'
#     )
#     user2 = User.objects.create(
#         first_name='Anna',
#         username='usera',
#         password='passa'
#     )
#     user3 = User.objects.create(
#         first_name='Magdalena',
#         username='userm',
#         password='passm'
#     )
#     return user1, user2, user3
