from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('post_new/<int:mode>', views.post_new, name='post_new'),
	#path('ckeditor/', include ('ckeditor_uploader.urls')),
	#path('post_list/', views.post_list, name='post_list'),
	path('post_list/', views.GalleryListView.as_view(), name='post_list'),
	path('post_list/<int:post_id>', views.post_detail, name="post_detail"),
	path('post_list/<int:post_id>/comment/create', views.add_comment_to_post, name="add_comment_to_post"),
	path('post_list/<int:post_id>/comment/remove', views.comment_remove, name="comment_remove"),
	path('board_list/', views.BoardListView.as_view(), name='board_list'),
	path('api/blog/', views.blog_api.as_view(), name='blog_api'),

]