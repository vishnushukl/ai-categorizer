from django.urls import path
from .views import CategorizeView, HealthView

urlpatterns = [
    path('categorize/', CategorizeView.as_view(), name='categorize'),
    path('health/', HealthView.as_view(), name='health'),
]
