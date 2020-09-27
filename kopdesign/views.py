from django.shortcuts import render, get_object_or_404
from .models import HomePosts
from users.models import UserPost, User
from django.views.generic import DetailView, CreateView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib import messages


def homepage(request):
    context = {
        'posts': HomePosts.objects.all(),
    }
    return render(request, 'kopdesign/index.html', context)


class PostDetailView(DetailView):
    model = HomePosts


class PostCreateView(CreateView):
    model = HomePosts
    fields = ['content', 'linkToImg', 'url']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def about(request):
    return render(request, 'kopdesign/about.html', {'title': 'About'})


def search(request):
    if request.method == 'POST':
        search_item = request.POST['search']
        print(f'searched query -- {search_item}')
        if search_item:
            post = UserPost.objects.filter(Q(content__icontains=search_item) | Q(tags__icontains=search_item))
            user_profile = User.objects.filter(Q(username__icontains=search_item)
                                               | Q(first_name__icontains=search_item)
                                               | Q(last_name__icontains=search_item))
            # found = False
            if post or user_profile:
                found = True
                context = {
                    'post': post,
                    'user_profile': user_profile,
                    'title': 'search {}'.format(search_item),
                    'text': f'Search result for "{search_item}":',
                    'found': found,
                }
                return render(request, 'users/search.html', context)
            else:
                context = {
                    'text': f'Nothing found for "{search_item}":',
                    'title': 'search {}'.format(search_item),
                }
                return render(request, 'users/search.html', context)
    return render(request, 'users/search.html', {'title': 'Search'})


def delete_user(request, username):
    user_delete = get_object_or_404(User, username=username)
    creator = user_delete.username

    if request.method == "POST" and request.user.is_authenticated and request.user.username == creator:
        user_delete.delete()
        messages.success(request, "User successfully deleted!")
        print('Account deleted for username:', creator)
        return HttpResponseRedirect("/explore")

    context = {
            'user_delete': user_delete,
            }
    return render(request, 'users/delete_user.html', context)
