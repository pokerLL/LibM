import hashlib
from datetime import timedelta

from django.conf import settings
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from Utils.decorators import *
from Utils.redis_lrucache import *
# from LibM.scripts.decorators import *
# from LibM.scripts.redis_lrucache import *
from libEnd import views as ENDVIEW
from .forms import *
from .models import *

def login(request):
    if request.method == "GET":
        lgf = loginForm()
        return render(request, "login.html", locals())

    lgf = loginForm(request.POST)
    if not lgf.is_valid():# 进行数据校验
        #校验失败
        msg = "验证码错误，请重新输入！"
        return render(request, "login.html", locals())

    account = request.POST.get("account")
    password = request.POST.get("password")
    user_login_type = request.POST.get("user_login_type")
    user = libUser.objects.filter(account=account, password=password)

    if user.count() == 0:
        msg = "账号或密码错误，请检查。"
        return render(request, "login.html", locals())

    user = user[0]

    if not user.has_confirmed:
        msg = "账号尚未进行邮箱验证，请前往邮箱验证后再登陆。"
        return render(request, "login.html", locals())

    # 设置过期时间
    request.session.set_expiry(settings.SESSION_EXPIRE_TIME)
    #会话保持
    request.session.__setitem__("has_login", True)#标记过期未结束
    request.session.__setitem__("user_id", user.id)
    request.session.__setitem__("account", user.account)
    request.session.__setitem__("nickname", user.nickname)
    request.session.__setitem__("user_type", user.type)
    if user.change_password_required:
        request.session.__setitem__("change_password_required", user.change_password_required)

    data = {
        "l_time": datetime.now(),
    }
    libUser.objects.update(**data)

    # 判断是否有权限进入后台
    if user_login_type == "r":
        if user.type == 1 or user.type == 0:
            return ENDVIEW.index(request)
        else:
            request.session.clear()
            msg = "非管理员账号，无法登入后台。"
            return render(request, "login.html", locals())
    else:
        return redirect(reverse("libfront:index"))

def index(request):
    print("loading index")
    books = libBook.objects.all()
    newest = books.order_by("-c_time")[:15]#排行
    newest2 = books.order_by("-c_time")[:5]#速递
    scorehighest = books.order_by("-score")[:15]
    commentest = books.order_by("-comment_num")[:15]
    recommends = books.order_by("?")[:8]
    list1 = libCategory.objects.all()[0].libbook_set.all().select_related()[:5]
    list2 = libCategory.objects.all()[1].libbook_set.all().select_related()[:5]
    list3 = libCategory.objects.all()[2].libbook_set.all().select_related()[:5]
    list4 = libCategory.objects.all()[3].libbook_set.all().select_related()[:5]
    cms = libComment.objects.filter(has_confirmed=True).order_by('-p_num').select_related()[:5]
    msg = libAnnouncement.objects.filter(
        Q(type=request.session.get("user_type", "-1")) | Q(type=3)
        | Q(for_user_id=request.session.get("user_id", "-1"))
    ).filter(c_time__gte=datetime.now() - timedelta(days=7))
    msgnum = msg.count()
    msg = {"msg": msg, "msgnum": msgnum}
    userid = request.session.get("user_id", -1)

    return render(request, "index.html", locals())

def categorylist(request, categid, pg):
    ONE_PAGE_ITEM_NUM = 15
    cat = libCategory.objects.get(id=categid)
    books = cat.libbook_set.all()
    all_num = int(books.count() / ONE_PAGE_ITEM_NUM) + (1 if books.count() % ONE_PAGE_ITEM_NUM != 0 else 0)
    rmds = books.order_by("-score")[:ONE_PAGE_ITEM_NUM]
    books = books.select_related()[(pg - 1) * ONE_PAGE_ITEM_NUM:(pg - 1) * ONE_PAGE_ITEM_NUM + ONE_PAGE_ITEM_NUM]
    return render(request, "category.html", locals())

def ranklist(request, st, pg):
    ONE_PAGE_ITEM_NUM = 15
    st = "-" + st
    books = libBook.objects.all()
    all_num = int(books.count() / ONE_PAGE_ITEM_NUM) + (1 if books.count() % ONE_PAGE_ITEM_NUM != 0 else 0)
    qs = books.order_by(st)[(pg - 1) * ONE_PAGE_ITEM_NUM:(pg - 1) * ONE_PAGE_ITEM_NUM + ONE_PAGE_ITEM_NUM]
    return render(request, "ranklist.html", locals())


def bookdetail(request, bookid):
    book = libBook.objects.get(id=bookid)
    catgs = book.categ.all()[:3]
    if len(catgs) > 0:
        catg = catgs[0]
    chapters = book.chapters.split(",")
    rmds = libBook.objects.all().order_by("-score")[:10]
    cms = book.libcomment_set.filter(has_confirmed=True).order_by("-c_time").select_related()
    cmsnum = book.libcomment_set.filter(has_confirmed=True).count()
    userid = request.session.get("user_id", -1)
    return render(request, "bookdetail.html", locals())


@login_required_json
def borrow_ajax(request):
    u_id = request.POST.get("user_id")
    b_id = request.POST.get("book_id")
    endtime = request.POST.get("endtime")
    print(111)
    print(endtime)
    user = get_object_or_404(libUser, id=u_id)
    book = get_object_or_404(libBook, id=b_id)
    data = {
        "code": 200,
    }
    if book.stock_now <= 0:
        data['code'] = 401
    else:
        # try:
        borrow = libBorrow()
        borrow.user = user
        borrow.book = book
        borrow.c_time = datetime.now()
        print(endtime)
        borrow.p_time = endtime + " 23:59:00"
        borrow.save()
        libBook.objects.filter(id=b_id).update(stock_now=book.stock_now - 1, borrow_num=book.borrow_num + 1)
        # except :
        #     data['code'] = 400


    return JsonResponse(data)


def logout(request):
    request.session.clear()
    try:
        CACHE.delete("lfindex(){}")
    except:
        pass
    return redirect(reverse("libfront:index"))
    # return index(request)

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.account, now)
    return code


def send_email(email, code):
    host_name = "127.0.0.1:8000"
    from django.core.mail import EmailMultiAlternatives
    subject = '来自贺院云书苑的注册确认邮件'

    text_content = '''感谢注册贺院云书苑，\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/lf/confirm/?code={}" target=blank>贺院云书苑</a>。</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    <p>唯君不思，无我不为。祝你在书苑有一个良好的体验。</p>
                    '''.format(host_name, code, settings.EMAIL_CONFIRM_EXPIRE_TIME)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def register(request):
    global msg
    if request.method == "GET":
        return render(request, "register.html",locals())

    typ = 1

    account = request.POST.get("account")
    same_account_user_count = libUser.objects.filter(account=account).count()
    if same_account_user_count != 0:
        msg = "用户名重复"

    email = request.POST.get("email")
    same_email_user_account = libUser.objects.filter(email=email).count()
    if same_account_user_count != 0:
        msg += "邮箱重复"

    psd = request.POST.get("password")
    nickname = request.POST.get("nickname")
    gender = request.POST.get("gender")
    birthday = request.POST.get("birthday")
    description = request.POST.get("description")

    if same_account_user_count + same_account_user_count != 0:
        return render(request, "register.html", {'msg': msg})

    user = libUser()
    user.nickname = nickname
    user.account = account
    user.password = psd
    user.email = email
    user.gender = gender
    user.birthday = birthday
    user.description = description

    user.save()
    code = make_confirm_string(user)
    libConfirmString.objects.create(user=user, code=code)
    send_email(email, code)
    lgf = loginForm()
    msg = "成功注册，请前往邮箱进行验证后进行登陆。"

    return render(request, "login.html", {'msg': msg, 'lgf': lgf})


#@cache_it_httpresponse(prefix="lf", expiration=10)
@login_required
def userdetail(request, id):
    user = libUser.objects.filter(id=request.session.get("user_id"))[0]

    borrow = libBorrow.objects.select_related().filter(user=user).order_by('-c_time')
    borrow = {"borrow": borrow, "borrownum": borrow.count()}

    back = libBack.objects.select_related().filter(user=user)
    back = {"back": back, "backnum": back.count()}

    comments = libComment.objects.select_related().filter(user=user)
    comments = {"comments": comments, "commentsnum": comments.count()}

    collection = libBookCollection.objects.select_related().filter(user=user)
    collection = {"collection": collection, "collectionnum": collection.count()}

    msg = libAnnouncement.objects.filter(
        Q(type=request.session.get("user_type", "-1")) | Q(type=3)
        | Q(for_user_id=request.session.get("user_id", "-1"))
    ).filter(c_time__gte=datetime.now() - timedelta(days=7))
    msg = {"msg": msg, "msgnum": msg.count()}

    firenum = libComment.objects.filter(user_id=request.session.get("user_id")).aggregate(Sum('p_num'))['p_num__sum']
    if firenum is None:
        firenum = 0
    print(type(firenum))
    print(firenum)
    return render(request, "userdetail.html", locals())


#@cache_it_httpresponse(60 * 60 * 24, prefix="lf")
def categorys(request):
    catgs = libCategory.objects.all()
    return render(request, "categorys.html", locals())


#@cache_it_httpresponse(prefix="lf")
def search(request, kw, pg):
    ONE_PAGE_ITEM_NUM = 15
    books = libBook.objects.filter(Q(name__icontains=kw) | Q(author__icontains=kw) | Q(publisher__icontains=kw))
    all_num = int(books.count() / ONE_PAGE_ITEM_NUM) + (1 if books.count() % ONE_PAGE_ITEM_NUM != 0 else 0)
    rmds = books.order_by("-score")[:ONE_PAGE_ITEM_NUM]
    books = books.select_related()[(pg - 1) * ONE_PAGE_ITEM_NUM:(pg - 1) * ONE_PAGE_ITEM_NUM + ONE_PAGE_ITEM_NUM]
    return render(request, "category.html", locals())


def push_comment_ajax(request):
    user_id = request.POST.get("user_id", 0)
    book_id = request.POST.get("book_id", 0)
    content = request.POST.get("content", " ")
    data = {"code": 400, }
    user = libUser.objects.filter(id=user_id)
    book = libBook.objects.filter(id=book_id)
    if user.count() * book.count() == 0:
        data['msg'] = "错误：用户或书籍不存在！"
    elif len(content) < 8:
        data['msg'] = "错误：评论过短，自动驳回，请至少输入八个字符！"
    else:
        libComment.objects.create(user=user[0], book=book[0], comment=content)
        data["code"] = 200
        data['msg'] = "成功：评论成功，等待管理员审核。"

    return JsonResponse(data)


@login_required_json
def operation(request):
    operation = request.POST.get("operation")
    print(request.POST.dict())
    if operation == "like":
        return like_ajax(request)
    elif operation == "collect":
        return collect_ajax(request)
    elif operation == "change_password":
        return change_password_ajax(request)
    elif operation == "delete":
        return delete_ajax(request)
    elif operation == "back":
        return back_ajax(request)
    elif operation == "push_user_detail":
        return push_user_detail_ajax(request)
    elif operation == "new_message":
        return new_message_ajax(request)
    elif operation == "load_headerbar":
        return load_headerbar_ajax(request)
    elif operation == "push_comment":
        return push_comment_ajax(request)


def like_ajax(request):
    user_id = request.POST.get("user_id", 0)
    id = request.POST.get("id", 0)
    target = request.POST.get("obj", None)
    data = {}
    data['code'] = 200

    user = libUser.objects.get(id=user_id)
    data['msg'] = "操作成功"
    if target == "book":
        book = libBook.objects.get(id=id)
        if libBookFavourite.objects.filter(book=book, user=user).count() != 0:
            data['msg'] = "重复点赞，无效！"
            data['code'] = 400
        else:
            libBookFavourite.objects.create(book=book, user=user)
            lsp = book.p_num + 1
            libBook.objects.filter(id=id).update(p_num=lsp)
    elif target == "comment":
        comment = libComment.objects.get(id=id)
        if libCommentFavourite.objects.filter(comment=comment, user=user).count() != 0:
            data['msg'] = "重复点赞，无效！"
            data['code'] = 400
        else:
            libCommentFavourite.objects.create(comment=comment, user=user)
            lsp = comment.p_num + 1
            libComment.objects.filter(id=id).update(p_num=lsp)

    return JsonResponse(data)


def collect_ajax(request):
    user_id = request.POST.get("user_id", 0)
    book_id = request.POST.get("id", 0)
    libBookCollection.objects.get_or_create(user=libUser.objects.get(id=user_id),
                                            book=libBook.objects.get(id=book_id))
    data = {
        "code": 200,
        "msg": "收藏成功，快去收藏夹看看吧",
    }
    return JsonResponse(data)


def change_password_ajax(request):
    formdata = request.POST
    oldpsd = formdata.get("oldpsd")
    newpsd = formdata.get("newpsd")
    user_id = request.session.get("user_id")
    user_count = libUser.objects.filter(Q(id=user_id) & Q(password=oldpsd)).count()
    data = {
        "code": 200,
        "msg": "",
    }
    if user_count == 0:
        data["code"] = 400
        data["msg"] = "原始密码错误"
    else:
        libUser.objects.filter(Q(id=user_id) & Q(password=oldpsd)).update(password=newpsd,
                                                                          change_password_required=False)
    return JsonResponse(data)


def delete_ajax(request):
    if request.method == "GET":
        return JsonResponse({})

    object = request.POST.get("obj")
    id = request.POST.get("id")

    ob = None
    data = {"code": 200, 'msg': "删除成功"}

    if object == "collection":
        ob = libBookCollection
    elif object == "borrow":
        ob = libBorrow
    elif object == "back":
        ob = libBack
    elif object == "announcement":
        ob = libAnnouncement
    elif object == "comment":
        ob = libComment
    elif object == "collect":
        ob = libBookCollection

    try:
        ob.objects.filter(id=id).delete()
        # pass
    except:
        data["code"] = 400
        data["msg"] = "错误，删除对象不存在。"

    return JsonResponse(data)


def back_ajax(request):
    id = request.POST.get("id")
    lb = libBorrow.objects.filter(id=id)
    if lb.count() == 0:
        return JsonResponse({})
    lb = lb[0]
    data = {
        "code": 200,
        "msg": "还书成功"
    }
    try:
        libBack.objects.create(user=lb.user, book=lb.book, c_time=lb.c_time, p_time=lb.p_time, f_time=datetime.now())
        lb.delete()
        if lb.user.type == 3:
            libUser.objects.filter(id=lb.user.id).update(type=2)
    except:
        data['code'] = 400
        data['msg'] = "还书失败"
    return JsonResponse(data)


def push_user_detail_ajax(request):
    data = request.POST.dict()
    id = int(data['id'])
    del data['id']
    del data['operation']
    res = {
        "code": 200,
        "msg": "信息修改成功"
    }
    print(libUser.objects.filter(id=id)[0].gender)
    try:
        libUser.objects.filter(id=id).update(**data)
    except:
        res['code'] = 400
        res['msg'] = "信息修改失败"

    print(data)
    print(libUser.objects.filter(id=id)[0].gender)
    return JsonResponse(res)


def new_message_ajax(request):
    id = request.POST.get("id")
    title = request.POST.get("title")
    message = request.POST.get("message")
    data = {
        'code': 400,
        'msg': '留言失败'
    }
    libMessage.objects.create(user=libUser.objects.get(id=id), title=title, message=message)
    data['code'] = 200
    data['msg'] = '留言成功'

    return JsonResponse(data)


#@cache_it_json(600, prefix="lf")
def load_headerbar_ajax(request):
    print("loading header")
    catgs = list(libCategory.objects.values_list("name", "id").all().order_by("-c_time"))
    catg1 = catgs[:7]
    catg2 = catgs[7:10]
    data = {
        "catg1": catg1,
        "catg2": catg2
    }

    return JsonResponse(data)


def user_confirm(request):
    code = request.GET.get('code', None)
    msg = ""

    # libConfirmString.objects.filter()

    try:
        confirm = libConfirmString.objects.get(code=code)
    except:
        msg = '无效的确认请求'
        return render(request, 'confirm.html', {'msg': msg})

    c_time = confirm.c_time
    now = datetime.now()
    if now > c_time + timedelta(settings.EMAIL_CONFIRM_EXPIRE_TIME):
        confirm.user.delete()
        msg = '您的邮件已经过期！请重新注册!'
        return render(request, 'confirm.html', {'msg': msg})
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        msg = '感谢确认，请使用账户登录！'
        return render(request, 'confirm.html', {'msg': msg})










# 前后端分离序列化程序
# class BookViewSet(viewsets.ModelViewSet):
#     queryset = libBook.objects.all().order_by('-score')[:10]
#     serializer_class = BookSerializer
#
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = libCategory.objects.all().order_by('-c_time')
#     serializer_class = CategorySerializer
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = libUser.objects.all().order_by('-c_time')
#     serializer_class = UserSerializer
#
# class BooklikeViewSet(viewsets.ModelViewSet):
#     queryset = libBookFavourite.objects.all().order_by('-c_time')
#     serializer_class = BooklikeSerializer
#
# class BookCollectionViewSet(viewsets.ModelViewSet):
#     queryset = libBookCollection.objects.all().order_by('-c_time')
#     serializer_class = BookCollectionSerializer
#
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = libComment.objects.all().order_by('-c_time')
#     serializer_class = CommentSerializer
#
# class CommentlikeViewSet(viewsets.ModelViewSet):
#     queryset = libCommentFavourite.objects.all().order_by('-c_time')
#     serializer_class = CommentlikeSerializer
#
# class BackViewSet(viewsets.ModelViewSet):
#     queryset = libBack.objects.all().order_by('-c_time')
#     serializer_class = BackSerializer
#
# class MessageViewSet(viewsets.ModelViewSet):
#     queryset = libMessage.objects.all().order_by('-c_time')
#     serializer_class = MessageSerializer
#
# class AnnouncementViewSet(viewsets.ModelViewSet):
#     queryset = libAnnouncement.objects.all().order_by('-c_time')
#     serializer_class = AnnouncementSerializer
#
# class ConfirmStringViewSet(viewsets.ModelViewSet):
#     queryset = libConfirmString.objects.all().order_by('-c_time')
#     serializer_class = ConfirmStringSerializer
#

# 前后端分离视图
# from rest_framework.views import APIView
# from django.http import JsonResponse
# from rest_framework.request import Request
# from rest_framework import exceptions
# from rest_framework.authentication import BasicAuthentication
#
# def md5(user):
#     import hashlib
#     import time
#     ctime = str(time.time())
#     m=hashlib.md5(bytes(user,encoding='utf-8'))
#     m.update(bytes(ctime,encoding='utf-8'))
#     return m.hexdigest()
#
# class AuthView(APIView):
#     def post(self,request,*args,**kwargs):
#         ret = {'code':1000,'msg':None}
#         try:
#             user=request._request.POST.get('account')
#             pwd=request._request.POST.get('password')
#             obj=libUser.objects.filter(account=user,password=pwd).first()
#             obj1=obj.__dict__.keys()
#             if not obj:
#                 ret['code']=1001
#                 ret['msg']="用户名或密码错误"
#             print(obj1)
#             token=md5(user)
#             libConfirmString.objects.update_or_create(user=obj,defaults={'token':token})
#             ret['token']=token
#
#         except Exception as e:
#             print(obj)
#             ret['code']=1002
#             ret['msg']="请求异常"
#
#         return JsonResponse(ret)
#
# ORDER_DICT = {
#     1:{
#         'name':"yeyeye",
#         'age':18,
#         'gender':'1'
#     },
#     2:{
#         'name':"wuwuwu",
#         'age':19,
#         'gender':'2'
#     },
# }
#
# class Authtication(object):
#     def autentication(self,request):
#         token = request._request.GET.get('token')
#         token_obj=libConfirmString.objects.filter(token=token).first()
#         if not token_obj:
#             raise exceptions.AuthenticationFailed('用户认证失败')
#         # 会赋值给request供后续操作
#         return (token_obj.user,token_obj)
#     def authenticate_header(self,request):
#         pass
#
# class OrderView(APIView):
#     authentication_classes = [Authtication,]
#     def get(self,request,*args,**kwargs):
#         # request.user
#         # request.auth
#         ret = {'code': 1000, 'msg': None,'data':None}
#         try:
#             ret['data']=ORDER_DICT
#         except Exception as e:
#             pass
#         return JsonResponse(ret)
