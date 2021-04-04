from django.urls import path
from . import views


# index, trainer list
urlpatterns = [
    path('', views.index, name='index'),
    path('trainers/', views.TrainerListView.as_view(), name='trainers'),
    path('trainer/<int:pk>', views.trainer_detail_view, name='trainer-detail'),
    path('lectures/', views.LectureListView.as_view(), name='lectures'),
    path('lecture/<int:pk>', views.LectureDetailView.as_view(), name='lecture-detail'),
]

urlpatterns += [
    path('aboutus/', views.aboutus, name='aboutus'),
]

# my class
urlpatterns += [
    path('traineelectures/', views.LecturesByUserListView.as_view(), name='trainee-lectures'),
    path('trainerlectures/', views.LecturesByTrainerListView.as_view(), name='trainer-lectures'),
]

# Register, modify, delete trainer
urlpatterns += [
    path('trainer/new/', views.trainer_new, name='trainer-new'),
    path('trainer/<int:trainer_id>/update/', views.trainer_update, name='trainer-update'),
    path('trainer/<int:trainer_id>/delete/', views.trainer_delete, name='trainer-delete')
]

# Search
urlpatterns += [
    path('search/', views.trainer_search, name='search'),
]

urlpatterns += [
    path('accounts/mypage/mylist/', views.trainer_mylist, name='trainer-mylist'),
]