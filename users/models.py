from django.db import models
import uuid

class AppUser(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    role = models.ForeignKey( 'access.Role', on_delete=models.PROTECT, related_name='users' )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
