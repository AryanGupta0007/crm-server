from django.urls import path
from ops_api.views import LeadView
urlpatterns = [
    path('lead/', LeadView.as_view(), name="lead-ops")
]