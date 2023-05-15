from products.models import Category


def slug_categories(request) -> dict:
    slugs = Category.objects.values('slug', 'name')
    return {'category_slugs': slugs,
            'is_home': request.path == f'/{ request.LANGUAGE_CODE}/'}