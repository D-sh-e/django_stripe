from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
import stripe
from shop.services import checkout_session_item, payment_intent_item
from shop.models import Item



class MainView(TemplateView):
    """Страница Main"""
    template_name = "shop/main.html"
    model = Item
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item =Item.objects.all()
        context['items'] = item
        return context

class ItemView(TemplateView):
    """Страница item"""
    template_name = "shop/item.html"
    model = Item
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = get_object_or_404(Item, pk=self.kwargs['id'])
        context['stripe_public_key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['item'] = item
        return context


class BuyView(View):
    """Страница buy"""
    model = Item
    def get(self, request, id):
        item = get_object_or_404(Item, pk=id)
        try:
            session_data  = checkout_session_item(item, request)
            return JsonResponse({'id': session_data['id'], 'url': session_data['url']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    

class PaymentIntentView(TemplateView):
    """Payment intent"""
    template_name = "shop/payment_intent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = get_object_or_404(Item, pk=self.kwargs['id'])
        client_secret = payment_intent_item(item)
        context['item'] = item
        context['client_secret'] = client_secret
        context['stripe_public_key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['price_cents'] = int(item.price * 100)
        return context
    


class SuccessView(TemplateView):
    template_name = "shop/success.html"

class CancelView(TemplateView):
    template_name = "shop/cancel.html"