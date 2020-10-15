from django.urls import path
from django.views.generic.base import RedirectView
from . import views
from . import transactions

app_name = 'accounts'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('sign-up/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('report-issue/', views.report_view, name='report'),
    path('profile/edit/', views.profile_editview, name='profile-edit'),
    path('users/', views.userList, name='users'),
    path('password-change/', views.password_change, name='passwordChange'),
    path('save-money/', transactions.savemoney_view, name='savemoney'),
    path('transaction-hisotry/', transactions.transaction_history, name='history'),
    path('withdraw-money/', transactions.withdrawmoney_view, name='withdrawmoney'),
    path('transfer-money/', transactions.transmoney_view, name='transfermoney'),
    path('transfer-money/verify/', transactions.transverify_view, name='transverify'),
    path('transfer-money/complete/', transactions.transcomplete_view, name='transcomplete'),
]
