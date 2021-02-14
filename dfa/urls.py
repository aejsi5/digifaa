"""dfa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from dfa_App import views
from dfa_App import emails

urlpatterns = [
    path('/', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/login.html'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('search/', views.VehicleSearch.as_view(), name='search'),
    path('search_V2/', views.VehicleSearch_V2.as_view(), name='search_v2'),
    path('stammdaten/', views.Administration.as_view(), name='master_data'),
    path('produktverbesserung/', views.RecallDetail.as_view(), name='recall_detail'),
    path('tis/', views.tis, name='tech_inf'),
    path('home/', views.index , name='home'),
    path('samples/vehicle/', views.sample_vehicle_csv, name='vehicle_csv'),
    path('api/v1/vehicle_recall/<pk>', views.Vehicle_Recall_Api.as_view()),
    path('api/v1/note/new', views.Note_Api.as_view()),
    path('api/v1/note/<pk>', views.Note_Api.as_view()),
    path('api/v1/vehiclelist/', views.VehicleList.as_view()),
    path('api/v1/vehicle/<pk>', views.VehicleAPI.as_view()),
    path('api/v1/recalllist/', views.RecallListAPI.as_view()),
    path('api/v1/recall/<pk>', views.RecallAPI.as_view()),
    path('api/v1/workshoplist/', views.WorkshopList.as_view()),
    path('api/v1/workshop/<pk>', views.WorkshopAPI.as_view()),
    path('api/v1/vehiclelist_per_recall/<pk>', views.VehicleRecallList.as_view()),
    path('api/v1/constraint/<pk>', views.Recall_Constraint_Api.as_view()),
    path('api/v1/recalldoc/<pk>', views.RecallDocsAPI.as_view()),
    path('api/v1/recalldoc/', views.RecallDocsAPI.as_view()),
    path('api/v1/recalldoclist/', views.RecallDocsListAPI.as_view()),
    path('api/v1/run_rules/<pk>', views.run_RuleManager, name='run_rules'),
    path('api/v1/update_all/', views.update_all, name='update_all'),
    path('start_email/', emails.start_tech_mail_listener, name='start_tech'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

