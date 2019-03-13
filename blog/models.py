from django.db import models
from django.utils import timezone

from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    #photo = models.ImageField(blank=True, upload_to="blog/%Y/%m/%d")
    photo = ProcessedImageField(
        upload_to = 'blog/post/%Y/%m/%d',
        processors = [Thumbnail(100, 100)], # 처리할 작업 목룍
        format = 'JPEG',                    # 최종 저장 포맷
        options = {'quality': 60},
        blank=True, null=True)          # 저장 옵션

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
    	return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text