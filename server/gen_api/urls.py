from django.urls import path
from gen_api.views import (
    BatchView,
    UnderReviewLeads,
    CurrentUserView,
    ProofView,
    TotalPagesView
)


urlpatterns = [
    path("total-pages/", TotalPagesView.as_view(), name="total_pages"),
    path("lead/<int:pk>/download-image/", ProofView.as_view(), name="proof"),
    path("batch/", BatchView.as_view(), name="batch"),
    path("under-review-leads/<int:page>/", UnderReviewLeads.as_view(), name="under_review_leads"),
    path("current-user/", CurrentUserView.as_view(), name="current-user")
]