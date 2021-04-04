from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('accounts/agreement/', views.AgreementView.as_view(), name='agreement'),
    path('accounts/signup_t/', views.TrainerRegisterView.as_view(), name='signup_t'),
    path('accounts/signup/', views.TraineeRegisterView.as_view(), name='signup'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/mypage/', views.mypage, name='mypage'),
    path('accounts/recovery/id/', views.RecoveryIdView.as_view(), name='recovery_id'),
    path('accounts/recovery/id/find/', views.ajax_find_id_view, name='ajax_id'),
    path('accounts/mypage/password_change/', views.password_edit_view, name='password_change'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/profile/update/', views.profile_update_view, name='profile_update'),
    path('accounts/delete/', views.profile_delete_view, name='profile_delete'),
    path('accounts/registerauth/', views.register_success, name='register_success'),
    path('accounts/activate/<str:uid64>/<str:token>/', views.activate, name='activate'),
    path('accounts/recovery/pw/', views.RecoveryPwView.as_view(), name='recovery_pw'),
    path('accounts/recovery/pw/find/', views.ajax_find_pw_view, name='ajax_pw'),
    path('accounts/recovery/pw/auth/', views.auth_confirm_view, name='recovery_auth'),
    path('accounts/recovery/pw/reset/', views.auth_pw_reset_view, name='recovery_pw_reset'),
]
