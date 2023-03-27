from django.urls import path
from posts import views

urlpatterns = [
    path('posts/', views.AllPostsListView.as_view()),
    path('posts/post/', views.PostListView.as_view()),
    path('posts/post/<int:pk>/', views.PostDetailView.as_view()),
    path('posts/pokebuild/', views.PokeBuildListView.as_view()),
    path('posts/pokebuild/<int:pk>/', views.PokeBuildDetailView.as_view()),

]
