from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Project(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return f"{self.name} - @{self.user.username}"

class Task(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return f"{self.title} - {self.project.name}"
