from django.urls import path
from admin_api.views import (
    LeadSheetView,
    SaleView,
    DownloadDatabaseFile,
    EmployeeView,
    BatchView,
    DashboardStatsView,
    ResetAllotLeads,
    ClosedSalesView
    )
urlpatterns = [
    path('leads/', LeadSheetView.as_view(), name="upload_lead_sheet"),
    path('sales/', SaleView.as_view(), name="sales"),
    path('download-db/', DownloadDatabaseFile.as_view(), name='download-db'),
    path('closed-sales/', ClosedSalesView.as_view(), name="closed_sales"),
    path('employee/', EmployeeView.as_view(), name="employee_view"),
    path('batch/', BatchView.as_view(), name="batches"),
    path('dashboard-stats/', DashboardStatsView.as_view(), name='dash-stats'),
    path('reset-allot-leads/', ResetAllotLeads.as_view(), name='reset_allot_leads')
]