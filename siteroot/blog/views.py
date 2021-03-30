from django.views.generic.base import TemplateView
from .models import Post, Profile
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from .forms import LoginForm, AccountCreateForm, ProfileUpdateForm, AccountPasswordChangeForm, PostCreateForm
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from .decorators import anonymous_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect

@method_decorator(anonymous_required, name='dispatch')
class IndexView(TemplateView):
    ''' Display index page '''
    template_name = f'index.html'


class PostsView(ListView):
    ''' Display all posts '''
    model = Post
    template_name = f'posts_list.html'
    context_object_name = 'posts'


@method_decorator(anonymous_required, name='dispatch')
class AccountCreateView(SuccessMessageMixin, CreateView):
    ''' Display the account creation form '''
    form_class = AccountCreateForm
    template_name = f'create.html'
    success_url = reverse_lazy(settings.LOGIN_URL)


class AccountDeleteView(DeleteView):
    ''' Display deletion confirmation page '''
    model = get_user_model()
    template_name = f'account-confirm-delete.html'
    success_url = reverse_lazy(settings.INDEX_URL)

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class UsernameUpdateView(SuccessMessageMixin, UpdateView):
    ''' Display the username change form '''
    model = get_user_model()
    fields = ['username']
    template_name = f'account-username-update.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def get_object(self):
        return self.request.user


class PasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    ''' Display the password change form '''
    form_class = AccountPasswordChangeForm
    template_name = f'password-change.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)


class AccountLoginView(LoginView):
    ''' Display the login form '''
    form_class = LoginForm
    template_name = f'login.html'
    redirect_authenticated_user = True


class AccountLogoutView(LogoutView):
    ''' Logout '''
    pass


class ProfileRedirectView(RedirectView):
    ''' Redirect user to his profile '''
    def get_redirect_url(self, *args, **kwargs):
        return reverse(
            'profile-detail', args=[self.request.user.username]
        )


class ProfileDetailView(DetailView):
    ''' Display profile information '''
    model=Profile
    template_name = f'profile.html'

    def get_object(self):
        return self.request.user.profile



class ProfilePostsView(SuccessMessageMixin, CreateView, ListView):
    ''' Display user posts '''
    model = Post
    template_name = f'profile-posts.html'
    form_class=PostCreateForm
    context_object_name = 'posts'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user.id).order_by('created_date')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ProfilePostsView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile-posts', args=[self.request.user.username])


class ProfileUpdateView(SuccessMessageMixin, UpdateView):
    ''' Display the profile update form '''
    model = Profile
    form_class = ProfileUpdateForm
    template_name = f'profile-update.html'
    success_url = reverse_lazy('profile-redirect')

    def get_object(self):
        return self.request.user.profile


class EmailUpdateView(SuccessMessageMixin, UpdateView):
    ''' Display the email update form '''
    model = get_user_model()
    fields = ['email']
    template_name = f'email-update.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def get_object(self):
        return self.request.user


def delete_post(request, post_id=None):
    ''' Post deletion function '''
    post_to_delete = Post.objects.get(id=post_id)

    if post_to_delete.author == request.user:
        post_to_delete.delete()
    return HttpResponseRedirect(reverse('profile-posts', args=[request.user.username]))


