from django.urls import path
from .views import AccessRuleView, OrdersView

urlpatterns = [
    path('rules/', AccessRuleView.as_view(), name='access_rules'),
    path('orders/', OrdersView.as_view(), name='orders'),
]
