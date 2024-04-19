from django.db import models


class Permission(models.Model):
    """
        This is where all permissions that we use in our system defined
    """
    permission = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.description


class User(models.Model):
    """
        This is a user model with role and specific permission tied
        to them at the user creation
    """
    ROLES = (
        ('admin', "Admin"),
        ('user', 'User')
    )
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=150, default='1234')
    role = models.CharField(max_length=6, choices=ROLES)
    groups = models.ManyToManyField("Group", related_name="members", blank=True, null=True)
    permissions = models.ManyToManyField(Permission, related_name="individual_perm", blank=True, null=True)
    picture = models.ImageField(upload_to='media/images/', default='media/images/default_profile_pic.jpg')
    in_trash = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Group(models.Model):
    """
        It's a group that has specific permission from Permission table
        and any user placed in this group shares the same permissions
    """

    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, related_name="group_perm", blank=True, null=True)

    def __str__(self):
        return self.name


class TestModel(models.Model):

    name = models.CharField(max_length=100)
    change = models.CharField(max_length=200)
    remote = models.CharField(max_length=300)

    def __str__(self):
        return self.name + " " + self.change


