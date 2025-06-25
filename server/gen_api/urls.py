from django.urls import path
from gen_api.views import (
    BatchView,
    UnderReviewLeads,
    CurrentUserView
)


urlpatterns = [
    path("batch/", BatchView.as_view(), name="batch"),
    path("under-review-leads/", UnderReviewLeads.as_view(), name="under_review_leads"),
    path("current-user/", CurrentUserView.as_view(), name="current-user")
]