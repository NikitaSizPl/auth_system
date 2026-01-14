from django.db import models


# Роли пользователей
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True) #admin , user,...

    def __str__(self):
        return self.name


# Бизнес элемент
class BusinessElement(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Правила ролей - доступ
class AccessRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE)
    
    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'element')
