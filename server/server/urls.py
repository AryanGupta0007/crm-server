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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve
import os
    
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))    
    
urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path("admin/", admin.site.urls),
    path("api/auth/", include("auth_api.urls")),
    path("api/admin/", include("admin_api.urls")),
    path("api/ops/", include("ops_api.urls")),
    path("api/accounts/", include("accounts_api.urls")),
    path("api/gen/", include("gen_api.urls")),
    path("api/sales/", include("sales_api.urls")),
    path('silk/', include('silk.urls', namespace='silk'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(BASE_DIR, 'client_build/dist/assets'))
# Catch-all for SPA (must be last)
urlpatterns += [
    re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': os.path.join(os.path.dirname(BASE_DIR), 'client_build', 'dist', 'assets')}),
    re_path(r'^(?!api/|admin/|silk/|static/|media/).*$', TemplateView.as_view(template_name="index.html")),
]
