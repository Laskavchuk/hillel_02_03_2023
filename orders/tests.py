from django.urls import reverse

from orders.models import Order


def test_cart(client, login_client, product_factory, faker):
    url = reverse('cart')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert '/en' + response.redirect_chain[0][0] == reverse('login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302

    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200
    assert not response.context['order_items']
    order = response.context['order']
    assert order
    assert not order.order_items.exists()

    product = product_factory()
    data = {
        'product_id': faker.uuid4()
    }
    response = client.post(reverse('cart_action', args=('add',)), data=data,
                           follow=True)
    assert response.status_code == 200
    assert not order.order_items.exists()

    data['product_id'] = str(product.id)
    response = client.post(reverse('cart_action', args=('add',)), data=data,
                           follow=True)
    assert response.status_code == 200
    order_item = order.order_items.first()
    assert order_item.product == product
    assert order_item.quantity == 1
    assert order_item.price == product.price

    data = {
        'item_1': str(order_item.id),
        'quantity_1': 5
    }

    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    order_item.refresh_from_db()
    assert order_item.quantity == data['quantity_1']

    client.post(reverse('cart_action', args=('clear',)), data={}, follow=True)
    assert not order.order_items.exists()

    response = client.post(reverse('cart_action', args=('remove',)), data=data,
                           follow=True)
    assert response.status_code == 200
    assert not order.order_items.exists()

    response = client.post(reverse('cart_action', args=('pay',)), data=data,
                           follow=True)
    assert response.status_code == 200
    assert not order.order_items.exists()
