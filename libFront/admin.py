from django.contrib import admin

# Register your models here.

from libFront import models as md

#用户
@admin.register(md.libUser)
class libUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname']


@admin.register(md.libCategory)
class libCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(md.libBook)
class liBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'publisher', 'p_num', 'comment_num']


@admin.register(md.libComment)
class libCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'comment', 'p_num', 'c_time']


@admin.register(md.libBorrow)
class libBorrowAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'c_time', 'p_time', 'f_time']


@admin.register(md.libBack)
class libBackAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'c_time', 'p_time', 'f_time']


@admin.register(md.libMessage)
class libMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'c_time', 'message']


@admin.register(md.libAnnouncement)
class libAnnouncementAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'for_user', 'type', 'content', 'c_time']
