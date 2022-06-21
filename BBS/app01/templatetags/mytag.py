"""
讲师:JasonJi    外号:鸡哥
邮箱:18817628568@163.com
微信:15618087189、18817628568(备注来源)
"""
from django import template
from app01 import models
from django.db.models import Count

register = template.Library()


@register.inclusion_tag('left_menu.html',name='left_menu')
def func1(blog):
    username = blog.userinfo.username
    # 获取当前用户所有的分类名称及分类下的文章数
    category_list = models.Category.objects.filter(blog=blog).annotate(article_num=Count('article__pk')).values('name',
                                                                                                                'article_num',
                                                                                                                'pk'
                                                                                                                # 添加分类的主键值 用于后续的筛选功能
                                                                                                                )

    # 获取当前用户所有的标签名称及标签下的文章数
    tag_list = models.Tag.objects.filter(blog=blog).annotate(article_num=Count('article__pk')).values('name',
                                                                                                      'article_num',
                                                                                                      'pk'
                                                                                                      # 添加标签的主键值 用于后续的筛选功能
                                                                                                      )
    # 获取年月及年月下的文章数
    from django.db.models.functions import TruncMonth
    date_list = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values(
        'month').annotate(c=Count('pk')).values(
        'month', 'c')
    return locals()