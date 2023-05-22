from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, RedirectView

from orders.mixins import GetCurrentOrderMixin
from orders.model_forms import CartForm, CartActionForm
from django.utils.translation import gettext_lazy as _


class CartView(GetCurrentOrderMixin, FormView):
    form_class = CartForm
    template_name = 'orders/cart.html'
    success_url = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('cart')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context.update({
            'order': order,
            'order_items': order.order_items.all()
        })
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.get_object()})
        return kwargs

    def form_valid(self, form):
        is_discount_changed = form.cleaned_data.get(
            'discount') != self.get_object().discount
        form.save()
        if is_discount_changed:
            messages.success(self.request, _('Discount updated successfully'))
        messages.success(self.request, _('Recalculate succeeded'))
        return super().form_valid(form)


class CartActionView(GetCurrentOrderMixin, RedirectView):
    url = reverse_lazy('products')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = CartActionForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.action(kwargs.get('action'))
            if kwargs.get('action') == 'add':
                messages.success(self.request, _('Product added!'))
            elif kwargs.get('action') == 'remove':
                messages.success(self.request, _('Product removed!'))
            elif kwargs.get('action') == 'clear':
                messages.success(self.request, _('Cart is clear!'))
            elif kwargs.get('action') == 'pay':
                messages.success(self.request, _('Pay succeeded'))
            else:
                messages.error(self.request, _('ERROR'))
        return self.get(request, *args, **kwargs)

