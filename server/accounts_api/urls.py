from django.urls import path
from accounts_api.views import LeadView

urlpatterns = [
    path('lead/', LeadView.as_view(), name="account_view" )
]