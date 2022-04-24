from django.db import models

# Create your models here.


class MyManager(models.QuerySet):
    def approved(self):
        return self.filter(status='A')

    def rejected(self):
        return self.filter(status='R')

    def pending(self):
        return self.filter(status='P')


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Idea(models.Model):
    PENDING = 'P'
    REJECTED = 'R'
    APPROVED = 'A'
    CHOICES = (
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
        (APPROVED, 'Approved'),
    )

    content = models.TextField()
    user = models.CharField(max_length=50, default='AnonymousUser')
    status = models.CharField(choices=CHOICES, max_length=1, default=PENDING)
    chat_id = models.CharField(max_length=100)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    objects = models.Manager.from_queryset(MyManager)()

    def get_status(self):
        answers = {
            'P': 'Pending',
            'R': 'Rejected',
            'A': 'Approved',
        }
        return answers[self.status]

    def get_status_theme(self):
        answers = {
            'P': 'info',
            'R': 'danger',
            'A': 'success',
        }
        return answers[self.status]

    def __str__(self):
        return self.user
