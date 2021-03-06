from django.db import models
from django.utils import timezone

class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # self.post.number_comments = self.post.number_comments +1
        self.post.number_comments += 1
        self.post.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}: {self.text[:20]}'