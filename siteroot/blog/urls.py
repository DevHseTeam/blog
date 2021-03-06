from django.urls import path
from  .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('posts', PostsView.as_view(), name='posts'),
    path('create', AccountCreateView.as_view(), name='account-create'),
    path('login', AccountLoginView.as_view(), name='account-login'),
    path('logout', AccountLogoutView.as_view(), name='account-logout'),
    path('delete', AccountDeleteView.as_view(), name='account-delete'),
    path('username/update', UsernameUpdateView.as_view(), name='account-username-update'),
    path('password/change', PasswordChangeView.as_view(), name='account-password-change'),
    path('email/update', EmailUpdateView.as_view(), name='account-email-update'),
    path('redirect', ProfileRedirectView.as_view(), name='profile-redirect'),
    path('<slug:username>', ProfileDetailView.as_view(), name='profile-detail'),
    path('<slug:username>/update', ProfileUpdateView.as_view(), name='profile-update'),
    path('<slug:username>/posts',ProfilePostsView.as_view(), name='profile-posts'),
    path('delete/<post_id>',delete_post,name='delete')
]