from datetime import datetime

from django.db import models


# Create your models here.

class libUser(models.Model):
    gender = (
        ('男', 'man'),
        ('女', 'woman'),
        ('保密', 'unknown'),
    )
    nickname = models.CharField(max_length=256, unique=False, default='default')
    account = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    type = models.IntegerField(default=2)  # 3invaild 2normal 1 admin 0 superadmin
    has_confirmed = models.BooleanField(default=False)
    change_password_required = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=32, choices=gender, default='unknown')
    birthday = models.DateField(default=datetime.strptime('1970-1-1', '%Y-%m-%d'), blank=True, null=True)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)
    l_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=256, blank=True, default='')
    description = models.CharField(max_length=256, blank=True, default='')

    def __str__(self):
        return self.account

    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class libCategory(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1024, default="")
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        # fields = ['name']
        verbose_name_plural = verbose_name = "类别"


class libBook(models.Model):
    IBSN = models.CharField(max_length=256, default="")
    name = models.CharField(max_length=256, null=False, unique=True)
    author = models.CharField(max_length=256, null=False)
    publisher = models.CharField(max_length=256, null=False)
    pubdate = models.DateField()
    categ = models.ManyToManyField("libCategory")
    stock_all = models.IntegerField(default=0)
    stock_now = models.IntegerField(default=0)
    borrow_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    p_num = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)
    chapters = models.CharField(max_length=6666)
    description = models.CharField(max_length=6666)

    def __str__(self):
        return self.name

    class Meta:
        # fields = ['name', 'author', 'publisher', 'pubdate', 'stock_all']
        verbose_name_plural = verbose_name = "书籍"


class libBookFavourite(models.Model):
    user = models.ForeignKey("libUser", on_delete=models.CASCADE)
    book = models.ForeignKey("libBook", on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)


class libBookCollection(models.Model):
    user = models.ForeignKey("libUser", on_delete=models.CASCADE)
    book = models.ForeignKey("libBook", on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)


class libComment(models.Model):
    user = models.ForeignKey("libUser", on_delete=models.CASCADE)
    book = models.ForeignKey("libBook", on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    has_confirmed = models.BooleanField(default=False)
    p_num = models.IntegerField(default=0)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    class Meta:
        # fields = ['user', 'book', 'comment', 'c_time']
        verbose_name_plural = verbose_name = "评论"


class libCommentFavourite(models.Model):
    user = models.ForeignKey("libUser", on_delete=models.CASCADE)
    comment = models.ForeignKey("libComment", on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)


class libBorrow(models.Model):
    user = models.ForeignKey("libUser", on_delete=models.CASCADE)
    book = models.ForeignKey("libBook", on_delete=models.CASCADE)
    c_time = models.DateTimeField()
    p_time = models.DateTimeField()
    f_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = verbose_name = "借书记录"


class libBack(models.Model):
    user = models.ForeignKey("libUser", on_delete=models.CASCADE)
    book = models.ForeignKey("libBook", on_delete=models.CASCADE)
    c_time = models.DateTimeField()
    p_time = models.DateTimeField()
    f_time = models.DateTimeField(auto_created=True)

    class Meta:
        verbose_name_plural = verbose_name = "还书记录"


class libMessage(models.Model):
    user = models.ForeignKey("libUser", on_delete=models.CASCADE)
    title = models.CharField(max_length=1024, default="")
    message = models.CharField(max_length=1024)
    c_time = models.DateField(auto_now_add=True)
    readed = models.BooleanField(default=False)


class libAnnouncement(models.Model):
    from_user = models.ForeignKey("libUser", on_delete=models.CASCADE, related_name="from_user", null=True)
    for_user = models.ForeignKey("libUser", on_delete=models.CASCADE, related_name="for_user", null=True)
    title = models.CharField(max_length=1024, default="")
    content = models.CharField(max_length=1024)
    type = models.IntegerField(default=2)  # 1管理员 2普通用户 3所有用户 4 对于特定用户
    c_time = models.DateField(auto_now_add=True)
    readed = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class libConfirmString(models.Model):
    user = models.ForeignKey("libUser", on_delete=models.CASCADE)
    code = models.CharField(max_length=1024)
    c_time = models.DateTimeField(auto_now_add=True)
