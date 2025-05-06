"""
URL configuration for h4ev project.

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

from onadata.views import GetFormsByUsernameView, GetFormSubmissionsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/onadata/user/<str:username>/forms', GetFormsByUsernameView.as_view(), name='get_forms_by_username'),
    path('api/onadata/form/<str:form_id>/', GetFormSubmissionsView.as_view(), name='get_form_submissions')
]
