"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
    
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("auth_api.urls")),
    path("api/admin/", include("admin_api.urls")),
    path("api/ops/", include("ops_api.urls")),
    path("api/accounts/", include("accounts_api.urls")),
    path("api/gen/", include("gen_api.urls")),
    path("api/sales/", include("sales_api.urls"))
]
