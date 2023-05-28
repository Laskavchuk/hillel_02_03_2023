from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from django.core.validators import URLValidator

from products.clients.parser import parser_client
from products.models import Product, Category
from project.celery import app


@app.task
def parse_products():
    products_list = parser_client.parse()
    if products_list:
        save_parser_result(products_list)


@app.task
def save_parser_result(products_list: list):
    for product_dict in products_list:
        image = product_dict.pop('image')
        category = product_dict.pop('category')
        sku = product_dict.pop('sku')
        product, created = Product.objects.update_or_create(
            sku=sku,
            defaults=product_dict
        )
        validate_url = URLValidator()
        try:
            validate_url(image)
        except ValidationError:
            ...
        else:
            image_data = parser_client.get_image(image)
            image = ImageFile(BytesIO(image_data.content), name=image)
            product.image = image
            product.save(update_fields=('image',))

        category, _ = Category.objects.get_or_create(
            name=category
        )
        product.categories.add(category)
