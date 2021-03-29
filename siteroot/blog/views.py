from django.views.generic.base import TemplateView
from .models import Post, Profile
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from .forms import LoginForm, AccountCreateForm, ProfileUpdateForm, AccountPasswordChangeForm
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from .decorators import anonymous_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import get_user_model


class IndexView(TemplateView): #ok
    template_name = f'index.html'


class PostsView(ListView): #ok
    model = Post
    template_name = f'posts_list.html'
    context_object_name = 'posts'


@method_decorator(anonymous_required, name='dispatch')
class AccountCreateView(SuccessMessageMixin, CreateView):

    form_class = AccountCreateForm
    template_name = f'create.html'
    success_url = reverse_lazy(settings.LOGIN_URL)
    success_message = 'Пользователь был успешно создан.'


class AccountDeleteView(DeleteView): #ok

    model = get_user_model()
    template_name = f'account-confirm-delete.html'
    success_url = reverse_lazy(settings.INDEX_URL)

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class UsernameUpdateView(SuccessMessageMixin, UpdateView):

    model = get_user_model()
    fields = ['username']
    template_name = f'account-username-update.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    success_message = 'Имя пользователя было успешно изменено.'

    def get_object(self):
        return self.request.user


class PasswordChangeView(SuccessMessageMixin, PasswordChangeView):

    form_class = AccountPasswordChangeForm
    template_name = f'password-change.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    success_message = 'Пароль был успешно изменён.'


class AccountLoginView(LoginView): #ok
    form_class = LoginForm
    template_name = f'login.html'
    redirect_authenticated_user = True


class AccountLogoutView(LogoutView): #ok
    pass  # Consistency :)


class ProfileRedirectView(RedirectView): #ok
    ''' Redirect user to his profile. '''

    def get_redirect_url(self, *args, **kwargs):
        return reverse(
            'profile-detail', args=[self.request.user.username]
        )


class ProfileDetailView(DetailView):
    ''' Display profile information. '''

    template_name = f'profile.html'

    def get_object(self):
        return None


class ProfilePostsView(ListView):
    template_name = f'profile-posts.html'
    model=Post
    context_object_name = 'posts'
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user.id).order_by('created_date')


class ProfileUpdateView(SuccessMessageMixin, UpdateView): #ok

    model = Profile
    form_class = ProfileUpdateForm
    template_name = f'profile-update.html'
    success_url = reverse_lazy('profile-redirect')
    success_message = 'Профиль был успешно обновлён.'

    def get_object(self):
        return self.request.user.profile


class EmailUpdateView(SuccessMessageMixin, UpdateView):

    model = get_user_model()
    fields = ['email']
    template_name = f'email-update.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    success_message = 'Адрес электронной почты был успешно изменён.'

    def get_object(self):
        return self.request.user





