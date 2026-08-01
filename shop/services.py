from django.conf import settings
import stripe
from django.urls import reverse


stripe.api_key = settings.STRIPE_SECRET_KEY




def checkout_session_item(item, request):
      try:
        session = stripe.checkout.Session.create(
        success_url = request.build_absolute_uri(reverse('shop:success')),
        cancel_url = request.build_absolute_uri(reverse('shop:cancel')),
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": item.name,
                        },
                        "unit_amount": int(item.price * 100),
                    },
                    "quantity": 1,
                }
            ],
            metadata={
                "item_id": item.id,
            },
        )
        return {'id': session.id, 'url': session.url}
      except Exception as e:
          raise e



def payment_intent_item(item):
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(item.price * 100),
            currency="usd",
            automatic_payment_methods={'enabled': True},
            metadata={
                'item_id': item.id,
                'item_name': item.name,
            },
            description=f"Payment for {item.name}",
        )
        return intent.client_secret
    except Exception as e:
        raise e

