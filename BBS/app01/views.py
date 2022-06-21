from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
from app01 import myforms
from app01 import models
from django.http import JsonResponse


def register(request):
    """前后端使用ajax交互 一般采用字典(json格式数据)作为数据媒介"""
    back_dic = {'code': 10000, 'msg': ''}  # code模拟响应状态码  msg模拟数据
    form_obj = myforms.RegisterForm()
    if request.method == 'POST':
        # 1.将request.POST里面的数据全部交给forms类校验
        form_obj = myforms.RegisterForm(request.POST)  # 多余的字段默认就不校验
        # 2.判断是否符合条件
        if form_obj.is_valid():
            cleaned_data = form_obj.cleaned_data  # username password confirm_password email
            # 3.移除创建用户数据时没有用的键值对confirm_password
            cleaned_data.pop('confirm_password')  # username password email
            # 4.获取用户头像
            avatar_obj = request.FILES.get('avatar')
            # 5.判断用户是否自定义了头像
            if avatar_obj:
                cleaned_data['avatar'] = avatar_obj  # username password email avatar
            # 6.创建用户对象
            models.UserInfo.objects.create_user(**cleaned_data)
            back_dic['msg'] = '用户注册成功'
            back_dic['url'] = '/login/'
        else:
            back_dic['code'] = 10001
            back_dic['msg'] = form_obj.errors
        return JsonResponse(back_dic)
    return render(request, 'register.html', locals())


from django.contrib import auth


def login(request):
    back_dict = {'code': 10000, 'msg': ''}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        # 1.先比对验证码是否正确 忽略大小写
        if request.session.get('code').upper() == code.upper():
            # 2.再比对用户名 密码是否正确
            is_obj = auth.authenticate(request, username=username, password=password)
            if is_obj:
                # 3.保存用户登录状态
                auth.login(request, is_obj)
                back_dict['msg'] = f'{username}登录成功'
                back_dict['url'] = '/home/'  # 可以做成之前定向跳转的需求
            else:
                back_dict['code'] = 10001
                back_dict['msg'] = '用户名或密码错误'
        else:
            back_dict['code'] = 10002
            back_dict['msg'] = '验证码错误'
        return JsonResponse(back_dict)
    return render(request, 'login.html')


"""
图形化相关模块:pillow
    pip3 install pillow
"""
from PIL import Image, ImageFont, ImageDraw

"""
Image       生成图片对象
ImageDraw   生成画笔对象 可以在图片上乱涂乱画
ImageFont   如果写文字 可以控制字体样式
"""

from io import BytesIO, StringIO

"""
BytesIO     内存中保存数据 并且取的时候返回bytes类型
StringIO    内存中保存数据 并且取的时候返回字符串类型
"""

# 专门随机生成三个数
import random


def get_random():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def get_code(request):
    # 1.推导步骤1:直接读取图片的二进制数据返回
    # with open(r'avatar/555.jpg','rb') as f:
    #     data = f.read()
    # return HttpResponse(data)
    # 2.推导步骤2:利用模块产生图片
    # img_obj = Image.new('RGB',(350, 35),'yellow')
    # with open(r'xxx.png','wb') as f:
    #     img_obj.save(f,'png')
    # with open(r'xxx.png','rb') as f:
    #     data = f.read()
    # return HttpResponse(data)
    # 3.推导步骤3:图片颜色随机产生
    # img_obj = Image.new('RGB',(350, 35),get_random())
    # with open(r'xxx.png','wb') as f:
    #     img_obj.save(f,'png')
    # with open(r'xxx.png','rb') as f:
    #     data = f.read()
    # return HttpResponse(data)
    # 4.推导步骤4:使用内存管理器临时存取图片  (前端处理)用户点击图片刷新验证码
    # img_obj = Image.new('RGB', (350, 35), get_random())
    # io_obj = BytesIO()
    # img_obj.save(io_obj,'png')
    # res = io_obj.getvalue()
    # return HttpResponse(res)
    # 5.推导步骤5:用户点击图片刷新验证码  课下先研究pillow模块
    img_obj = Image.new('RGB', (350, 35), get_random())
    draw_obj = ImageDraw.Draw(img_obj)
    font_obj = ImageFont.truetype('static/font/111.ttf', 30)
    code = ''
    for i in range(5):
        random_upper = chr(random.randint(65, 90))
        random_lower = chr(random.randint(97, 122))
        random_int = str(random.randint(0, 9))
        temp_choice = random.choice([random_upper, random_lower, random_int])
        # 每选择出一个 就写上一个 这样还可以控制每个字的间距
        draw_obj.text((i * 60 + 45, 0), temp_choice, font=font_obj)
        code += temp_choice
    # 将验证码保存一份 便于后续比对
    request.session['code'] = code
    io_obj = BytesIO()
    img_obj.save(io_obj, 'png')
    return HttpResponse(io_obj.getvalue())


def home(request):
    # 获取当前网站所有的文章(最理想的情况 应该加分页器处理)
    article_queryset = models.Article.objects.all()
    return render(request, 'home.html', locals())


from django.contrib.auth.decorators import login_required


@login_required
def set_pwd(request):
    back_dic = {'code': 10000, 'msg': ''}
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')
    # 1.先判断老密码是否正确
    is_right = request.user.check_password(old_password)
    if is_right:
        # 2.判断新密码是否一致 并且还应该限制不能为空
        if new_password == confirm_password and new_password and confirm_password:
            # 3.修改密码
            request.user.set_password(new_password)
            request.user.save()
            back_dic['msg'] = f'用户:{request.user.username}修改密码成功'
            back_dic['url'] = '/login/'  # 修改完密码 应该去重新登录
        else:
            back_dic['code'] = 10001
            back_dic['msg'] = '两次密码不一致或密码不能为空'
    else:
        back_dic['code'] = 10002
        back_dic['msg'] = '原密码错误'
    return JsonResponse(back_dic)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/home/')


from django.db.models import Count


def site(request, username, **kwargs):
    # 1.先校验用户名是否存在
    user_obj = models.UserInfo.objects.filter(username=username).first()
    if not user_obj:
        # 2.返回一个404页面
        return render(request, 'errors.html')
    blog = user_obj.blog
    # 3.获取当前用户所有的文章数据
    article_list = models.Article.objects.filter(blog=blog)

    '''刚刚分析了三个筛选功能其实就是对个人文章做二次筛选'''
    # 如何判断二次筛选>>>:判断kwargs是否有值
    if kwargs:  # {'condition': 'category', 'params': '1'}
        # 获取筛选条件
        condition = kwargs.get('condition')
        params = kwargs.get('params')  # 分类的主键值 标签的主键值 年月日期
        if condition == 'category':
            # 根据分类的主键值二次筛选文章(只要是queryset对象就可以无限制的点queryset对象的方法)
            article_list = article_list.filter(category__pk=params)
        elif condition == 'tag':
            # 根据标签的主键值二次筛选文章
            article_list = article_list.filter(tags__pk=params)
        elif condition == 'archive':
            # 日期格式我们采用 年-月
            year, month = params.split('-')
            # 神奇的双下划线查询
            article_list = article_list.filter(
                create_time__year=year,
                create_time__month=month
            )
    return render(request, 'site.html', locals())


def article_detail(request, username, article_id):
    """在查询文章之前 还应该校验用户名是否存在 文章id是否存在(小的校验)"""
    user_obj = models.UserInfo.objects.filter(username=username).first()
    if not user_obj:
        return render(request, 'errors.html')
    article_obj = models.Article.objects.filter(blog__userinfo=user_obj, pk=article_id).first()
    # TODO:文章阅读数功能
    if not article_obj:
        return render(request, 'errors.html')

    # 获取当前文章所有的评论数据展示到前端
    comment_list = models.Comment.objects.filter(article=article_obj)
    return render(request, 'articleDetail.html', locals())


import json
from django.db.models import F
from django.utils.safestring import mark_safe


def up_or_down(request):
    """
    1.用户必须登录
    2.文章不能是当前用户的
    3.文章没有被当前用户点过
    4.操作数据库:注意我们之前设置的普通字段 up_num down_num 同步更新
    ps:编写复杂业务逻辑 先考虑全部正确的情况
    """
    back_dic = {'code': 10000, 'msg': ''}
    if request.method == 'POST':
        # 1.校验用户是否登录
        if request.user.is_authenticated():
            # 获取文章id和点赞点踩数据
            article_id = request.POST.get('article_id')
            up_or_down = request.POST.get('up_or_down')  # 注意是字符串
            '''处理成python的布尔值类型'''
            up_or_down = json.loads(up_or_down)
            # 之所以做转换 是因为后面需要根据该字段决定给哪个普通字段自增 便于后续的判断
            # 根据文章id获取文章对象
            article_obj = models.Article.objects.filter(pk=article_id).first()
            # 2.判断当前文章不属于当前登录用户
            if not request.user == article_obj.blog.userinfo:
                # 3.判断当前用户是否给当前文章点过  去点赞点踩表中筛选数据
                is_click = models.UpAndDown.objects.filter(user=request.user, article=article_obj)
                if not is_click:
                    # 操作数据库完成数据更改
                    if up_or_down:  # 点赞
                        # 给普通字段自增1   F查询
                        models.Article.objects.filter(pk=article_id).update(up_num=F('up_num') + 1)
                        back_dic['msg'] = '点赞成功'
                    else:  # 点踩
                        models.Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
                        back_dic['msg'] = '点踩成功'
                    # 点赞点踩表数据录入
                    models.UpAndDown.objects.create(user=request.user, article=article_obj, is_up=up_or_down)
                else:
                    back_dic['code'] = 10001
                    back_dic['msg'] = '已经点过了!!!'  # 这里其实可以细分到底是已经点了赞还是踩
            else:
                back_dic['code'] = 10002
                back_dic['msg'] = '你个臭不要脸的 不能给自己点!!!'
        else:
            back_dic['code'] = 10003
            back_dic['msg'] = mark_safe('请先<a href="/login/">登录</a>')
        return JsonResponse(back_dic)
    return HttpResponse('OK')


def comment(request):
    back_dic = {'code': 10000, 'msg': ''}
    if request.user.is_authenticated():
        if request.method == 'POST':
            user_obj = request.user
            article_id = request.POST.get('article_id')
            content = request.POST.get('content')
            # 直接获取parent_id字段数据
            parent_id = request.POST.get('parent_id')
            # 需要操作两张表
            models.Article.objects.filter(pk=article_id).update(comment_num=F('comment_num') + 1)
            models.Comment.objects.create(
                user=user_obj,
                article_id=article_id,
                content=content,
                parent_id=parent_id
                # 根评论parent_id是null 相当于没传
                # 子评论parent_id有值 也是正常创建即可
                # 综上 根评论子评论后端代码是兼容的 传了值就是子评论 不传或者传null就是根评论
            )
            back_dic['msg'] = '评论成功'
    else:
        back_dic['code'] = 10001
        back_dic['msg'] = '请先登录'
    return JsonResponse(back_dic)


from app01.utils import mypage


@login_required
def backend(request):
    # 获取当前用户所有的文章
    article_queryset = models.Article.objects.filter(blog__userinfo=request.user)
    page_obj = mypage.Pagination(current_page=request.GET.get("page"),
                                 all_count=article_queryset.count(),
                                 )
    page_queryset = article_queryset[page_obj.start:page_obj.end]
    return render(request, 'backend/backend.html', locals())


@login_required
def add_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')  # 单选
        tag_id_list = request.POST.getlist('tag')  # 多选  [1,2,3,4]
        '''我们先直接创建 不考虑额外情况'''
        # TODO:使用bs4模块优化文章简介和xss攻击问题
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, 'lxml')
        # 1.先筛选出所有的script标签
        tags = soup.find_all()  # 获取所有的标签类型
        for tag in tags:  # 循环判断所有的标签类型
            if tag.name == 'script':
                tag.decompose()  # 删除script标签
        article_obj = models.Article.objects.create(title=title, desc=soup.text[0:150], content=str(soup),
                                                    blog=request.user.blog,
                                                    category_id=category_id
                                                    )
        # '''第三张关系表是我们自己写的 所以没法使用 add remove set clear方法'''
        # for tag_id in tag_id_list:  # 先简单的处理 后续完善
        #     models.Article2Tag.objects.create(article=article_obj, tag_id=tag_id)
        # TODO:可以考虑使用批量插入提升效率
        obj_list = []
        for tag_id in tag_id_list:
            obj_list.append(models.Article2Tag(article=article_obj, tag_id=tag_id))
        models.Article2Tag.objects.bulk_create(obj_list)
        # 上述四行代码也可以使用一行列表生成式完成
        return redirect('back_view')
    # 获取当前用户已经创建的分类和标签
    category_list = models.Category.objects.filter(blog__userinfo=request.user)
    tag_list = models.Tag.objects.filter(blog__userinfo=request.user)
    return render(request, 'backend/add_article.html', locals())


import os
from day62_BBS import settings


def file_upload(request):
    back_dict = {
        "error": 0,
    }
    # print(request.FILES)  # 先查看键值对 之后根据键取值
    # 获取文件对象
    article_file_obj = request.FILES.get('imgFile')
    # 文章上传的图片算用户上传的静态资源  可以考虑存放到media内部
    article_package_path = os.path.join(settings.BASE_DIR, 'media', 'article')
    # 判断路径是否存在 不存在自动创建
    if not os.path.exists(article_package_path):
        os.mkdir(article_package_path)
    # 拼接文件的完整路径并存储
    article_file_path = os.path.join(article_package_path, article_file_obj.name)
    with open(article_file_path, 'wb') as f:
        for line in article_file_obj:
            f.write(line)
    # 拼接返回给前端的字典
    # back_dict['url'] = article_file_path  # 不行  /Users/jiboyuan/PycharmProjects/day62_BBS/media/article/111.png
    back_dict['url'] = '/media/article/%s' % article_file_obj.name
    return JsonResponse(back_dict)


@login_required
def edit_article(request):
    # 获取用户想要编辑的文章对象
    article_pk = request.GET.get('edit_id')
    article_obj = models.Article.objects.filter(pk=article_pk).first()
    if not article_obj:
        return render(request, 'errors.html')
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')  # 单选
        tag_id_list = request.POST.getlist('tag')  # 多选  [1,2,3,4]
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, 'lxml')
        # 1.先筛选出所有的script标签
        tags = soup.find_all()  # 获取所有的标签类型
        for tag in tags:  # 循环判断所有的标签类型
            if tag.name == 'script':
                tag.decompose()  # 删除script标签
        models.Article.objects.filter(pk=article_pk).update(title=title, desc=soup.text[0:150], content=str(soup),
                                                            blog=request.user.blog,
                                                            category_id=category_id
                                                            )

        models.Article2Tag.objects.filter(article_id=article_pk).delete()
        obj_list = []
        for tag_id in tag_id_list:
            obj_list.append(models.Article2Tag(article=article_obj, tag_id=tag_id))
        models.Article2Tag.objects.bulk_create(obj_list)
        # 上述四行代码也可以使用一行列表生成式完成
        return redirect('back_view')

    category_list = models.Category.objects.filter(blog__userinfo=request.user)
    tag_list = models.Tag.objects.filter(blog__userinfo=request.user)
    # 返回一个编辑页面
    return render(request, 'backend/edit_article.html', locals())


@login_required
def delete_article(request):
    back_dic = {'code': 10000, 'msg': ''}
    delete_id = request.GET.get('delete_id')
    delete_queryset = models.Article.objects.filter(pk=delete_id)
    if not delete_queryset:
        return HttpResponse("别胡闹")
    delete_queryset.delete()
    back_dic['msg'] = '删除成功'
    back_dic['url'] = '/backend/'
    return JsonResponse(back_dic)


@login_required
def update_avatar(request):
    if request.method == 'POST':
        new_avatar = request.FILES.get('avatar')
        # models.UserInfo.objects.filter(pk=request.user.pk).update(avatar=new_avatar)
        request.user.avatar = new_avatar
        request.user.save()
    return redirect('/backend/')
