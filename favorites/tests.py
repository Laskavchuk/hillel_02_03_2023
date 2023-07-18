from django.urls import reverse

from products.models import Product


def test_favorites(client, product_factory, faker, login_client):
    url = reverse('favorites')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert '/en' + response.redirect_chain[0][0] == reverse('login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302
    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200
    product = product_factory()
    assert len(response.context['object_list']) != Product.objects.count()

    response = client.get(
        reverse('add_or_remove_favorite', args=(str(product.id),)), follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('products')
    assert response.redirect_chain[0][1] == 302

    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['object_list']) == Product.objects.count()

    response = client.get(
        reverse('add_or_remove_favorite', args=(str(product.id),)), follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('products')
    assert response.redirect_chain[0][1] == 302

    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['object_list']) != Product.objects.count()

