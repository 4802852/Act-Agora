from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('review/', views.ReviewListView.as_view(), name='reviews'),
    path('review/<int:pk>', views.review_detail_view, name='review-detail'),
    path('review/new', views.review_new, name='review-new'),
    path('review/<int:review_id>/update', views.review_update, name='review-update'),
    path('review/<int:review_id>/delete', views.review_delete, name='review-delete'),
]