from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from .forms import UserRegisterForm, UserUpdateForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserPost, Comment, Friend, Profile
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse_lazy


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            username = username.upper()
            messages.success(request, f'Account created for @{username} !!')
            return redirect('/login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/signup.html', {'title': 'Signup', 'form': form})


@login_required
def profile(request):
    post = UserPost.objects.filter(username=request.user).order_by('-datetime')
    friend = Friend.objects.get(current_user=request.user)
    friend = friend.users.all().count
    following_people = friend
    title = str(request.user)
    title = title.upper()
    post = {
        'post': post,
        'following_people': following_people,
        'other_title': title,
    }
    return render(request, 'users/profile.html', post)


@login_required
def update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, request.FILES, instance=request.user.oser)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account detail updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.oser)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/update.html', context)


class PostDetailView(DetailView):
    model = UserPost


class PostCreateView(LoginRequiredMixin, CreateView):
    model = UserPost
    fields = ['content', 'Image', 'tags']

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['comment']

    def form_valid(self, form):
        form.instance.username = self.request.user
        pk = self.kwargs
        pk = pk['pk']
        post = UserPost.objects.get(id=pk)
        form.instance.post = post
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserPost
    fields = ['content', 'Image', 'tags']

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.username:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserPost
    success_url = '/accounts/profile/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.username:
            return True
        return False


def explore(request):
    post = UserPost.objects.annotate(like_count=Count('likes')).order_by('-like_count')
    post = {
        'post': post,
        'title': 'Explore'
    }
    return render(request, 'kopdesign/explore.html', post)


@login_required
def user_profile(request, username):
    try:
        if username == str(User.objects.get(username=username)):
            username = User.objects.get(username=username)
            post = UserPost.objects.filter(username=username).order_by('-datetime')
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()
            friends = friends.exclude(id=request.user.id)
            if username == request.user:
                is_user = True
            else:
                is_user = False
            context = {
                'username': username,
                'post': post,
                'friends': friends,
                'title': username,
                'is_user': is_user,
                'following': following,
            }
            return render(request, 'users/profile_visit.html', context)
    except User.DoesNotExist:
        return render(request, 'users/notfound.html')


def comments(request, pk):
    comm = Comment.objects.filter(post=pk).order_by('-datetime')
    post = UserPost.objects.get(id=pk)
    can_edit = None
    if post.username == request.user:
        can_edit = True
    else:
        can_edit = False
    total_likes = UserPost.total_likes(post)
    total_likes_you = int(total_likes - 1)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    comm = {
        'comm': comm,
        'post': post,
        'pk': pk,
        'is_liked': is_liked,
        'total_likes': total_likes,
        'total_likes_you': total_likes_you,
        'title': 'Post {}'.format(post.id),
        'can_edit': can_edit,
            }
    return render(request, 'users/comments.html', comm)


@login_required
def members(request):
    users = User.objects.all()
    users = users.exclude(id=request.user.id)
    pro = Profile.objects.all()
    friend = Friend.objects.get(current_user=request.user)
    friends = friend.users.all()
    friends = friends.exclude(id=request.user.id)
    context = {
        'users': users,
        'friends': friends,
        'pro': pro,
        'title': 'FindPeople',
    }
    return render(request, 'kopdesign/members.html', context)


@login_required
def add_friend(request, pk, operation):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
        return redirect('/find-people')
    if operation == 'remove':
        Friend.lose_friend(request.user, friend)
        return redirect('/following')


@login_required
def following(request):
    friend = Friend.objects.get(current_user=request.user)
    friends = friend.users.all()
    friends = friends.exclude(id=request.user.id)
    context = {
        'friends': friends,
        'title': 'Following'
    }
    return render(request, 'kopdesign/following.html', context)


@login_required
def home(request):
    friend = Friend.objects.get(current_user=request.user)
    friends = friend.users.all()
    friends = friends.exclude(id=request.user.id)
    post = UserPost.objects.filter(username__in=friends).order_by('-datetime')

    context = {
        'post': post,
        'other_title': 'Home'
    }
    return render(request, 'kopdesign/home.html', context)


def like_post(request, pk):
    post = get_object_or_404(UserPost, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect('/post/{}/'.format(pk))


class EditComment(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['comment']

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.username:
            return True
        return False


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy("comments")

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.username:
            return True
        return False
