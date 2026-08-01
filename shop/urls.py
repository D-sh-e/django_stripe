from django.urls import path
from shop import views

app_name = 'shop'
urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('buy/<int:id>', views.BuyView.as_view(), name='buy'),
    path('item/<int:id>', views.ItemView.as_view(), name='item'),
    path('payment-intent/<int:id>/', views.PaymentIntentView.as_view(), name='payment_intent'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
]
