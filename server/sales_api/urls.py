from django.urls import path
from sales_api.views import LeadSaleView, LeadBoardScoreView, LeadView, TotalPagesView, GetLeadsView


urlpatterns = [
    path('leads/', LeadSaleView.as_view(), name="sales-leads"),
    path('boardScore/', LeadBoardScoreView.as_view(), name="sales-board_score"),
    path('lead/', LeadView.as_view(), name="lead-view"),
    path("total-pages/", TotalPagesView.as_view(), name="total_pages"),
    path("get-leads/<int:page>/", GetLeadsView.as_view(), name="get_sales_leads_view")   
]