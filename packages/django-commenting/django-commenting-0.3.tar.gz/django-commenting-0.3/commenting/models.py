from django.db import models


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
class Comment(models.Model):

    name=models.CharField(max_length=50)
    email=models.EmailField()
    parent=models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

# added forienkey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    
    def __str__(self):
        return self.body
    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)
