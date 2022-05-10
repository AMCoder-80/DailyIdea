from django.urls import path
from . import views

app_name='idea'

urlpatterns = [
    path('create/', views.create_idea, name='main_idea'),
    path('', views.index, name='test'),
    path('idea/', views.idea, name='table'),
    path('categories/', views.CategoryList.as_view(), name="cat_views"),
    path('categories/create/', views.CreateCategory.as_view(), name="create_cat"),
    path('idea/<int:pk>/', views.IdeaDetail.as_view(), name='detail'),
    path('idea/<str:status>/', views.idea),
    path('status/change/<str:state>/<int:pk>/', views.change_status),
    path('cat/change/<int:id>/<int:pk>/', views.change_cat),
    path('content/change/<str:content>/<str:user>/<int:pk>/', views.change_content),
    path('save_req/', views.save_req),
]