
from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        # extra_fields.setdefault('is_leader', False) #staff
        # extra_fields.setdefault('is_member', False) #superuser
        return self._create_user(email, password, **extra_fields)

class AbstractUser(AbstractBaseUser, PermissionsMixin):
    # email_validator = validate_email()
    validate_email = EmailValidator()
    email = models.EmailField(('email address'), max_length=30, unique=True,validators=[validate_email],
        error_messages={
            'unique': ("User already exits. Create new user"),
        }, blank=True)

    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=150, blank=True)
   
    is_staff = models.BooleanField(('staff status'),default=False,)
    is_active = models.BooleanField(('active'),default=True,)
    date_joined = models.DateTimeField(('date joined'), default=timezone)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

class User(AbstractUser):
    is_leader = models.BooleanField(('leader'), default=False)

    def __str__(self):
        return self.email

class Team(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    team = models.ForeignKey(Team, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Task(models.Model):
    URGENT = "urgent"
    UPCOMING = "upcoming"

    # deadline 2 din me hai toh high priority, and arrange tasks by no of days remaining to end date 
    priority = (
        (URGENT, "urgent"),
        (UPCOMING, "upcoming")
    )

    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    UNDER_REVIEW = "under_review"
    DONE = "done"

    status = (
        (ASSIGNED, "assigned"),
        (IN_PROGRESS, "in_progress"),
        (UNDER_REVIEW, "under_review"),
        (DONE, "done"),
    )

    taskname = models.CharField(max_length=128)
    priority = models.CharField(max_length=16, default=URGENT, choices=priority)
    created_by = models.ForeignKey(User, models.CASCADE)
    start = models.DateField()
    end = models.DateField()
    status = models.CharField(max_length=16, default=ASSIGNED, choices=status)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.taskname

class AssignTask(models.Model):
    task = models.ForeignKey(Task, models.CASCADE)
    member = models.ForeignKey(User, models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task, self.member
        