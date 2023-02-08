from django.urls import path
from profiles import views


urlpatterns = [
    path('profiles/', views.TrainerProfileList.as_view()),
    path('profiles/<int:pk>', views.TrainerProfileDetail.as_view()),
]
