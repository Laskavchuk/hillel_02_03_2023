from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from favorites.models import Favorite
from products.models import Product
from django.utils.translation import gettext_lazy as _


class FavoriteView(ListView):
    model = Favorite
    template_name = 'favorites/favorites_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related(
            'product', 'user'
        )
        return queryset


class FavoriteAddOrRemoveView(DetailView):
    model = Product

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        favorite, created = Favorite.objects.get_or_create(
            product=product,
            user=user
        )
        if not created:
            favorite.delete()
            messages.success(self.request, _('Product removed!'))
        else:
            messages.success(self.request, _('Product added!'))
        return HttpResponseRedirect(reverse_lazy('products'))