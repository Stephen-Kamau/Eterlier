from django.urls import path
from accounts import views
# from django.conf.urls import url

urlpatterns = [
    path('',views.index_page),
    path('signup',views.user_registration),
    path('verify',views.user_verification),
    path('resend_otp',views.resend_otp),
    path('login',views.user_login),
    path('password_reset',views.password_reset),
    path('password_reset_change',views.password_reset_change),
]
