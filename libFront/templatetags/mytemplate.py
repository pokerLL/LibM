from django import template
import random
import datetime
from libFront import models as md
from django.utils.html import format_html

register = template.Library()
STATIC_URL = "/static/"

@register.simple_tag
def randbgimg(a=1, b=13):
    cho = random.randint(int(a), int(b))
    return STATIC_URL + "picture/mypic/bg/" + str(cho) + ".png"

@register.simple_tag
def randbookimg(bid="-1", a=1, b=22):
    if bid == "-1":
        cho = random.randint(int(a), int(b))
    else:
        cho = int(bid) % b + 1
    return STATIC_URL + "picture/mypic/book/" + str(cho) + ".png"

@register.simple_tag
def randprofileimg(uid="-1", a=1, b=25):
    if uid == "-1":
        cho = random.randint(int(a), int(b))
    else:
        cho = int(uid) % b + 1
    return STATIC_URL + "picture/mypic/tx/" + str(cho) + ".png"

@register.simple_tag()
def cmtlikebtn(cmtid, userid=-1):
    try:
        mc = md.libCommentFavourite.objects.filter(comment_id=cmtid, user_id=userid).count()
        if mc != 0:
            return "fa-thumbs-up"
    except:
        pass
    return "fa-thumbs-o-up"


@register.simple_tag
def randcatgbg():
    cho = ["bg-info",
           "bg-success",
           "bg-warning",
           "bg-danger",
           ]
    return random.choice(cho)


@register.simple_tag
def judgeline(a=1, b=1, t=0):
    if t == 0:
        if a % b == 1:
            return format_html("<div class='row'>")
    return ""


@register.filter()
def judgeline_filter(a=1, b=1):
    # print(a, b)
    return a % b == 0


@register.simple_tag
def timediff(start=datetime.datetime.now(), end=datetime.datetime.now()):
    diff = end - start
    if start > end:
        diff = start - end
    secs = diff.seconds
    days = diff.days
    hours = int(secs % (24 * 60 * 60) / (60 * 60))
    minutes = int(secs % (60 * 60) / 60)
    res = "{}天{}小时{}分钟".format(days, hours, minutes)
    return res


@register.simple_tag
def intdiff(a, b):
    return int(a) - int(b)


@register.simple_tag()
def timelessthannow(timea=datetime.datetime.now(), timeb=datetime.datetime.now()):
    if timea > timeb:
        return format_html("正常")
    else:
        return format_html("已逾期")


@register.simple_tag()
def cmtlikebtn(cmtid, userid=-1):
    try:
        mc = md.libCommentFavourite.objects.filter(comment_id=cmtid, user_id=userid).count()
        if mc != 0:
            return "fa-thumbs-up"
    except:
        pass
    return "fa-thumbs-o-up"


@register.simple_tag()
def booklikebtn(bookid, userid=-1):
    try:
        mc = md.libBookFavourite.objects.filter(book_id=bookid, user_id=userid).count()
        if mc != 0:
            return "fa-thumbs-up"
    except:
        pass
    return "fa-thumbs-o-up"
