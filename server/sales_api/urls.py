from django.urls import path
from sales_api.views import LeadSaleView, LeadBoardScoreView, LeadView


urlpatterns = [
    path('leads/', LeadSaleView.as_view(), name="sales-leads"),
    path('boardScore/', LeadBoardScoreView.as_view(), name="sales-board_score"),
    path('lead/', LeadView.as_view(), name="lead-view")
]