from django.db import models
from user.models import User

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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='ideas', null=True, blank=True)
    status = models.CharField(choices=CHOICES, max_length=1, default=PENDING)
    chat_id = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name="ideas", blank=True, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    requester = models.ManyToManyField('Requester', blank=True)
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
        return str(self.user)


class Requester(models.Model):
    TYPES = (
        ('I', 'Investor'),
        ('B', 'Buyer'),
        ('C', 'Customer')
    )
    user = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=100)
    type = models.CharField(max_length=5, choices=TYPES)


class ImprovedIdea(models.Model):
    base_idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    new_idea = models.TextField()
    user = models.CharField(max_length=150)
