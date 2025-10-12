from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Notification(models.Model):
     recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notification')
     actor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='actions')
     verb = models.CharField(max_length=150)

     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
     object_id = models.PositiveIntegerField()
     target = GenericForeignKey('content_type', 'object_id')

     timestamp = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return f'{self.actor} {self.verb} {self.target}'