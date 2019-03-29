from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import Q
from rest_framework.generics import GenericAPIView
from rest_framework import serializers, mixins

# Create your views here.

def home(request):
	return render(request, 'blog/home.html')


class GalleryListView(ListView):  
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = 'posts'
    paginate_by = 1  # Display 10 objects per page

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        mode = request.GET.get('mode', '')
        self.object_list = self.object_list.filter(mode__icontains=mode)
        search_text = request.GET.get('search_text', '')
        search_type = request.GET.get('search_type', '')
        if search_text:
            if search_type == 'tnc':
                self.object_list = self.object_list.filter(Q(title=search_text) | Q(content=search_text))
            elif search_type == 'title':
                self.object_list = self.object_list.filter(title__icontains=search_text)
            elif search_type == 'content':
                self.object_list = self.object_list.filter(content__icontains=search_text)
            elif search_type =='nickname':
                self.object_list = self.object_list.select_related('author').filter(author__username__icontains=search_text)
                


        for post in self.object_list:
            if post.content.find('src="') != -1:
                post_content_start = post.content.find('src="') + 5
                post_content_end = post_content_start + post.content[post_content_start:].find('"')
                post_thumbnail = post.content[post_content_start:post_content_end]
                post.thumbnail = post_thumbnail  
        context = self.get_context_data()
        context['search_type'] = search_type
        context['search_text'] = search_text
        context['mode'] = mode


        return self.render_to_response(context)



    def get_queryset(self): 
        queryset = super(GalleryListView, self).get_queryset()
        queryset = queryset.filter(published_date__lte=timezone.now()).order_by('-published_date')
        for post in queryset:
            if post.content.find('src="') != -1:
                post_content_start = post.content.find('src="') + 5
                post_content_end = post_content_start + post.content[post_content_start:].find('"')
                post_thumbnail = post.content[post_content_start:post_content_end]
                post.thumbnail = post_thumbnail     
        return queryset


    def get_context_data(self, **kwargs):
        context = super(GalleryListView, self).get_context_data(**kwargs)
        paginator = context['paginator']
        # search_text = self.request.GET.get('search_text', '')
        # search_type = self.request.GET.get('search_type', '')
        page_numbers_range = 1 # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        # context['search_type'] = search_type
        # context['search_text'] = search_text
        # context['posts'] = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

        # for post in context['posts']:
        #     if post.content.find('src="') != -1:
        #         post_content_start = post.content.find('src="') + 5
        #         post_content_end = post_content_start + post.content[post_content_start:].find('"')
        #         post_thumbnail = post.content[post_content_start:post_content_end]
        #         post.thumbnail = post_thumbnail
        return context


# def post_list(request):
# 	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
# 	for post in posts:
# 		if post.content.find('src="') != -1:
# 			post_content_start = post.content.find('src="') + 5
# 			post_content_end = post_content_start + post.content[post_content_start:].find('"')
# 			post_thumbnail = post.content[post_content_start:post_content_end]
# 			post.thumbnail = post_thumbnail
# 	return render(request, 'blog/post_list.html', {'posts': posts })

class BoardListView(ListView):  
    model = Post
    template_name = "blog/board_list.html"
    context_object_name = 'posts'
    paginate_by = 10  # Display 10 objects per page

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        mode = request.GET.get('mode', '')
        self.object_list = self.object_list.filter(mode__icontains=mode)
        search_text = request.GET.get('search_text', '')
        search_type = request.GET.get('search_type', '')
        if search_text:
            if search_type == 'tnc':
                self.object_list = self.object_list.filter(Q(title__icontains=search_text) | Q(content__icontains=search_text))
            elif search_type == 'title':
                self.object_list = self.object_list.filter(title__icontains=search_text)
            elif search_type == 'content':
                self.object_list = self.object_list.filter(content__icontains=search_text)
            elif search_type =='nickname':
                self.object_list = self.object_list.select_related('author').filter(author__username__icontains=search_text)
                


        context = self.get_context_data()
        context['search_type'] = search_type
        context['search_text'] = search_text
        context['mode'] = mode


        return self.render_to_response(context)



    def get_queryset(self): 
        queryset = super(BoardListView, self).get_queryset()
        queryset = queryset.filter(published_date__lte=timezone.now()).order_by('-published_date')   
        return queryset


    def get_context_data(self, **kwargs):
        context = super(BoardListView, self).get_context_data(**kwargs)
        paginator = context['paginator']
        # search_text = self.request.GET.get('search_text', '')
        # search_type = self.request.GET.get('search_type', '')
        page_numbers_range = 10 # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context


def post_detail(request, post_id):
    post_detail = get_object_or_404(Post, pk= post_id)
    return render(request, 'blog/post_detail.html', {'post': post_detail})

@login_required
def post_new(request, mode):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.mode = mode
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
def add_comment_to_post(request, post_id):
	#요청 메서드가 POST방식 일 때만 처리
    if request.method == "POST":
		# Post인스턴스를 가져오거나 404 Response를 돌려줌
        post = get_object_or_404(Post, pk=post_id)
        # request.POST에서 'content'키의 값을 가져옴
        content = request.POST.get('text')

        # 'content'키가 없었거나 내용이 입력되지 않았을 경우
        if not content:
            # 400(BadRequest)로 응답을 전송
            return HttpResponse('댓글 내용을 입력하세요', status=400)

        # 내용이 전달 된 경우, Comment객체를 생성 및 DB에 저장
        Comment.objects.create(
            post=post,
            # 작성자는 현재 요청의 사용자로 지정
            author=request.user,
            text=content
        )
        # 정상적으로 Comment가 생성된 후
        # 'post'네임스페이스를 가진 url의 'post_detail'이름에 해당하는 뷰로 이동
        return redirect('post_detail', post_id=post_id)
        

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, post_id):
	if request.method == "POST":
		del_indx = request.POST.get('del_comment_indx')
		comment = Comment.objects.get(pk=del_indx)
		comment.delete()
		return redirect('post_detail', post_id=post_id)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class blog_api(GenericAPIView, mixins.ListModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)