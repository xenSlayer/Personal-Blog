from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from users import views as user_views
from users.views import PostDetailView, PostCreateView, UpdatePost, PostDeleteView, CommentCreateView, EditComment,\
    CommentDeleteView

urlpatterns = [
    path('', views.homepage),
    path('explore/', user_views.explore),
    path('post/<int:pk>/edit/', PostDetailView.as_view(template_name='kopdesign/post_detail.html'), name='post-detail'),
    path('about/', views.about),
    path('create/', PostCreateView.as_view(template_name='kopdesign/createpost.html'), name='create-post'),
    path('post/<int:pk>/update/', UpdatePost.as_view(template_name='kopdesign/createpost.html'), name='update-post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(template_name='kopdesign/post_confirm_delete.html'),
         name='post-delete'),
    path('accounts/profile/', user_views.profile, name='profile'),
    path('accounts/profile/<str:username>/', user_views.user_profile, name='user-profile'),
    path('post/<int:pk>/', user_views.comments, name='comments'),
    path('post/<int:pk>/comments/create/', CommentCreateView.as_view(template_name='users/comment_create.html'),
         name='create-comment'),
    path('find-people/', user_views.members, name='members'),
    path('follow/<str:operation>/<int:pk>/', user_views.add_friend, name='follow'),
    path('following/', user_views.following, name='following'),
    path('post/<int:pk>/like-dislike/', user_views.like_post, name='like-post'),
    path('accounts/delete/<str:username>/', views.delete_user, name='like-post'),
    path('post/<int:pk>/comment/edit', EditComment.as_view(template_name='users/comment_edit.html'),
         name='comment-edit'),
    path('post/<int:pk>/comment/delete/', CommentDeleteView.as_view(template_name='users/comment_delete.html'),
         name='comment-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
