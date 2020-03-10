from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser, UserManager as _UserManager


# 重写用户状态AbstractUser源代码
class UserManager(_UserManager):
    def create_superuser(self, username, password, email=None, **extra_fields):
        return super(UserManager, self).create_superuser(username=username, password=password, email=email,
                                                         **extra_fields)


# 重写用户状态AbstractUser源代码
class Users(AbstractUser):
    objects = UserManager()
    REQUIRED_FIELDS = ['mobile']
    mobile = models.CharField('手机号', max_length=11, unique=True, error_messages={'unique': '此手机号已经注册'})
    email_ac = models.BooleanField('邮箱状态', default=True)

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

# 用户模型
# setting加AUTH_USER_MODEL = 'users.Users'
# from django.conf.global_settings
