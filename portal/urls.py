from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.PortalIndexTemplateView.as_view(), name='portal_index'),
    path('dashboard/', views.DashboardTemplateView.as_view(), name='dashboard_index'),
    path('create-roles/', views.CreateRulesRedirectView.as_view(), name='create_roles'),
]
