from django.urls import path
from . import views

app_name='idea'

urlpatterns = [
    path('', views.idea, name='main_idea'),
    path('index/', views.test, name='test'),
    path('table/', views.test_table, name='table'),
    path('table/<int:pk>/', views.IdeaDetail.as_view(), name='detail'),
    path('table/<str:status>/', views.test_table),
    path('status/change/<str:state>/<int:pk>/', views.change_status),
    path('cat/change/<int:id>/<int:pk>/', views.change_cat)
]