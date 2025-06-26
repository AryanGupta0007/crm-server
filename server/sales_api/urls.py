from django.urls import path
from sales_api.views import LeadView


urlpatterns = [
    path('leads/', LeadView.as_view(), name="sales-leads"),
]