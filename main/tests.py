from django.urls import reverse


def test_main_page(client, faker):
    url = reverse('main')
    response = client.get(url)
    assert response.status_code == 200

    url_contacts = reverse('contacts')
    response_contacts = client.get(url_contacts)
    assert response_contacts.status_code == 200


def test_contacts(client, faker):
    url = reverse('contacts')
    response = client.get(url)
    assert response.status_code == 200
    data = {
        'email': faker.email(),
        'text': faker.sentence()
    }
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('main')
    assert response.redirect_chain[0][1] == 302

    data['email'] = faker.word()
    data['text'] = str()
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    errors = response.context['form'].errors
    assert errors['email'] == ['Enter a valid email address.']
    assert errors['text'] == ['This field is required.']
