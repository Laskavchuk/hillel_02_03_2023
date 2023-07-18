from django.contrib.auth import get_user_model
from django.urls import reverse
from feedbacks.models import Feedback

User = get_user_model()


def test_feedbacks_list(client, faker, login_client):
    client, user = login_client()
    for _ in range(5):
        Feedback.objects.create(
            user=user,
            text=faker.text(),
            rating=faker.random_int(min=1, max=5)
        )
    url = reverse('feedbacks')
    response = client.get(url)
    assert response.status_code == 200
    assert b'Leave your feedback' in response.content
    assert len(response.context['feedback_list']) == Feedback.objects.count()


def test_create_feedback(client, faker, login_client):
    url = reverse('feedback_create')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert '/en' + response.redirect_chain[0][0] == reverse(
        'login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302

    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200

    data = {
        'user': str(user.id),
        'text': faker.sentences(),
        'rating': str()
    }

    assert not Feedback.objects.exists()
    data['rating'] = faker.random_int(min=6, max=10)
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    errors = response.context['form'].errors
    assert errors['rating'] == [
        'Ensure this value is less than or equal to 5.']

    assert not Feedback.objects.exists()
    data['rating'] = faker.random_int(min=1, max=5)
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert Feedback.objects.exists()
    assert response.redirect_chain[0][0] == reverse('feedbacks')
    assert response.redirect_chain[0][1] == 302
