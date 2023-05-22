from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def test_login(client, faker):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200

    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert all(v == ['This field is required.']
               for v in response.context['form'].errors.values())
    data['username'] = faker.email()
    data['password'] = faker.word()

    response = client.post(url, data=data)
    assert response.status_code == 200

    assert response.context['form'].errors['__all__'] ==['Please enter a correct email address or phone and password. Note that both fields may be case-sensitive. ']

    password = faker.word()
    user, _ = User.objects.get_or_create(
        email=faker.email(),
        phone=faker.phone_number(),
        is_phone_valid=True
    )
    user.set_password(password)
    user.save()

    data['username'] = user.email
    data['password'] = password

    response = client.post(url, data=data, follow=True)
    assert response.redirect_chain[0][0] == reverse('main')
    assert response.redirect_chain[0][1] == 302

    data['username'] = user.phone
    data['password'] = password

    response = client.post(url, data=data, follow=True)
    assert response.redirect_chain[0][0] == reverse('main')
    assert response.redirect_chain[0][1] == 302


def test_registration(client, faker):
    url = reverse('registration')
    response = client.get(url)
    assert response.status_code == 200

    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert all(v == ['This field is required.']
               for v in response.context['form'].errors.values())

    user, _ = User.objects.get_or_create(
        email=faker.email(),
    )
    password = faker.word()
    data = {
        'email': user.email,
        'password1': password,
        'password2': faker.word(),
        'phone': ''
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    errors = response.context['form'].errors
    assert errors['email'] == ['Email already exist.']
    assert errors['password2'] == ['The two password fields didn’t match.']

    data['email'] = faker.email()
    data['password2'] = password
    response = client.post(url, data=data)
    assert response.status_code == 200
    errors = response.context['form'].errors
    assert errors['password2'] == ['This password is too short. It must contain at least 8 characters.']

    password = faker.password()
    data['password1'] = password
    data['password2'] = password
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('main')
    assert response.redirect_chain[0][1] == 302

    data['email'] = faker.email()
    data['password1'] = password
    data['password2'] = password
    data['phone'] = faker.word()
    response = client.post(url, data=data, follow=True)
    errors = response.context['form'].errors
    assert errors['phone'] == ['Invalid phone number']

    data['password1'] = password
    data['password2'] = password
    data['phone'] = faker.random_int(min=1, max=100)
    response = client.post(url, data=data, follow=True)
    errors = response.context['form'].errors
    assert errors['phone'] == ['Invalid phone number']

    data['password1'] = password
    data['password2'] = password
    data['phone'] = faker.random_int(min=10**100, max=90**100)
    response = client.post(url, data=data, follow=True)
    errors = response.context['form'].errors
    assert errors['phone'] == ['Invalid phone number']

    data['password1'] = password
    data['password2'] = password
    data['phone'] = faker.phone_number()
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('phone_validation')
    assert response.redirect_chain[0][1] == 302


def test_phone_validation(client, faker, login_client):
    url = reverse('phone_validation')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert '/en' + response.redirect_chain[0][0] == reverse(
        'login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302

    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200

    data = {
        'code': str()
    }

    response = client.post(url, data=data, follow=True)
    errors = response.context['form'].errors
    assert errors['code'] == ['This field is required.']

    data['code'] = faker.random_number(digits=4)
    response = client.post(url, data=data, follow=True)
    errors = response.context['form'].errors
    assert errors['code'] == ['Confirmation code has expired. We sent you a new code']
