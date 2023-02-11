from django.urls import path
from likes import views

urlpatterns = [
    path('likes/', views.LikeListView.as_view()),
    path('likes/<int:pk>/', views.LikeDetailView.as_view()),
]