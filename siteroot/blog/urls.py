from django.urls import path
from  .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('posts', PostsView.as_view(), name='posts'),
    path('login', AccountLoginView.as_view(), name='account-login'),
    path('logout', AccountLogoutView.as_view(), name='account-logout'),
    path('redirect', ProfileRedirectView.as_view(), name='profile-redirect'),
    path('<slug:username>', ProfileDetailView.as_view(), name='profile-detail'),
    path('<slug:username>/update', ProfileUpdateView.as_view(), name='profile-update'),
    path('create', AccountCreateView.as_view(), name='account-create'),
]