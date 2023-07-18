from django.urls import reverse

from products.models import Product


def test_products_list(client, faker, product_factory):
    product = product_factory()
    url = reverse('products')
    response = client.get(url)
    assert response.status_code == 200

    assert len(response.context['products']) == Product.objects.count()

    response = client.get(reverse('product', args=(faker.uuid4(),)))
    assert response.status_code == 404

    response = client.get(reverse('product', args=(product.id,)))
    assert response.status_code == 200

    response = client.get(reverse('products_by_category', kwargs={'slug': faker.word()}))
    assert response.status_code == 404

    response = client.get(reverse('products_by_category', kwargs={'slug': product.categories.first()}))
    assert response.status_code == 200


def test_export_csv(client, faker, login_client):
    url = reverse('products_to_csv')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert '/en' + response.redirect_chain[0][0] == reverse(
        'login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302

    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200
