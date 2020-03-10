from django.db import models


# Create your models here.

class QQUser(models.Model):
    # 创建用户的时间
    create_times = models.DateTimeField(auto_now_add=True)
    update_times = models.DateTimeField(auto_now=True)

    user = models.ForeignKey('users.Users', on_delete=models.CASCADE)
    openid = models.CharField(verbose_name='openid', max_length=64)

    class Meta:
        db_table = 'tb_qq'
        verbose_name = 'QQ绑定用户'
        verbose_name_plural = verbose_name
