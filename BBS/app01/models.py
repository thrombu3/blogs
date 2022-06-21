from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserInfo(AbstractUser):
    """用户表"""
    phone = models.BigIntegerField(verbose_name='手机号', null=True, blank=True)  # blank告诉admin后台 该字段可以不填
    avatar = models.FileField(verbose_name='头像', upload_to='avatar/', default='avatar/default.jpg')
    '''给该字段传文件对象 会保存到upload_to指定的位置 然后该字段存储该位置的路径'''
    create_time = models.DateField(verbose_name='注册时间', auto_now_add=True)

    blog = models.OneToOneField(to='Blog', null=True)  # 外键设置null=True便于后期录入数据的方便

    # admin后台管理指定表名称
    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.username

class Blog(models.Model):
    """个人站点表"""
    site_name = models.CharField(verbose_name='站点名称', max_length=32)
    site_title = models.CharField(verbose_name='站点标题', max_length=32)
    site_theme = models.CharField(verbose_name='站点样式', max_length=32)

    def __str__(self):
        return self.site_name


class Article(models.Model):
    """文章表"""
    title = models.CharField(verbose_name='文章标题', max_length=32)
    desc = models.CharField(verbose_name='文章简介', max_length=255)
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateTimeField(verbose_name='创作时间', auto_now_add=True)
    # 优化字段
    up_num = models.IntegerField(verbose_name='点赞数', default=0)
    down_num = models.IntegerField(verbose_name='点踩数', default=0)
    comment_num = models.IntegerField(verbose_name='评论数', default=0)
    # 外键字段
    blog = models.ForeignKey(to='Blog', null=True)
    category = models.ForeignKey(to='Category', null=True)
    tags = models.ManyToManyField(to='Tag',
                                  through='Article2Tag',
                                  through_fields=('article', 'tag')
                                  )
    def __str__(self):
        return self.title

class Article2Tag(models.Model):
    article = models.ForeignKey(to='Article')
    tag = models.ForeignKey(to='Tag')



class Category(models.Model):
    """文章分类表"""
    name = models.CharField(verbose_name='分类名称', max_length=32)
    blog = models.ForeignKey(to='Blog', null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    """文章标签表"""
    name = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(to='Blog', null=True)

    def __str__(self):
        return self.name

class UpAndDown(models.Model):
    """点赞点踩表"""
    user = models.ForeignKey(to='UserInfo', null=True)
    article = models.ForeignKey(to='Article', null=True)
    is_up = models.BooleanField(verbose_name='点赞点踩')


class Comment(models.Model):
    """评论表"""
    user = models.ForeignKey(to='UserInfo')
    article = models.ForeignKey(to='Article')
    content = models.CharField(verbose_name='评论内容', max_length=255)
    comment_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    # 自关联
    parent = models.ForeignKey(to='self', null=True)  # 有些评论就是根评论
