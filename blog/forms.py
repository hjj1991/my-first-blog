from django import forms

from .models import Post, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# class PostForm(forms.ModelForm):

# 	#content = forms.CharField(widget=CKEditorWidget())
#     class Meta:
#         model = Post
#         fields = ('title', 'photo', 'content',)
#         labels = {
#         	'title': '제목',
#         }

# class PostForm(forms.Form):
# 	title = forms.CharField(label='')
# 	content = forms.CharField(widget=CKEditorUploadingWidget(), label='')

# 	def save(self, commit=True):
# 		post = Post(**self.cleaned_data)
# 		if commit:
# 			post.save()
# 		return post
class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('title', 'content')
		widgets = {
			'title': forms.TextInput(attrs={'placeholder': '제목을 입력해주세요.', 'class': 'form-control'}),
			'content': CKEditorUploadingWidget(),
		}
		labels ={
			'title':'',
			'content':'',
		}


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)