from django.contrib import admin
from django.utils.safestring import mark_safe
from products.models import Product, Category


def render_image(obj):
    if obj.image:
        img_html = '<img src="{url}" width="{width}" height="{height}" />' \
            .format(url=obj.image.url,
                    width=64,
                    height=64
                    )
        return mark_safe(img_html)
    return None


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (render_image, 'name', 'price', 'is_active')
    filter_horizontal = ('categories', 'products')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (render_image, 'name',)


