//登录通道转换
$(".logbtn").click(function () {
    $(".logbtn").addClass("btn-default");
    $(".logbtn").removeClass("btn-primary");
    $(this).removeClass("btn-default");
    $(this).addClass("btn-primary");
    var utp = $(this).text();
    console.log(utp);
    if (utp.indexOf("用") == 0) {
        $("#user_login_type").val("n");
        // console.log("NORMAL USER");
    } else {
        $("#user_login_type").val("r");
        // console.log("ADMIN");
    }
    console.log($("#user_login_type").val());
})
//搜索
$(".lfsbtn").click(function () {
    var kw = $(this).prev().val();
    console.log(kw);
    var url = "/lf/search/" + kw + "/1";
    console.log(url);
    $(window.location).attr('href', url);
})
//评论
$("#subcmt").click(function () {
    var bid = $("#book_id").val();
    var uid = $("#user_id").val();
    var content = $("#comment_content").val();
    $.ajax({
        url: "/lf/operation",
        method: "post",
        data: {
            operation: "push_comment",
            book_id: bid,
            user_id: uid,
            content: content,
        },
        success: function (data) {
            var code = data["code"];
            if (code === 500) {
                alert("尚未登陆，请先登陆再进行操作。");
            } else if (code === 200) {
                window.alert(data['msg']);
            } else if (data.code === 400) {
                window.alert(data['msg']);
            }
        },
        error: function () {
            window.alert("发生未知错误，评论失败！");
        }
    })
})
//评论点赞
$(".cmtlike").click(function () {
    var pp = $(this).parent().parent();
    var uid = $("#uid").text(),
        cid = pp.find(".cid").text(),
        pnum = pp.find(".pnum"),
        ppi = pp.find("i");

    // console.log(pp.html())
    // console.log(uid);
    // console.log(cid);

    var flag = true;
    if (ppi.hasClass("fa-thumbs-up")) {
        flag = false;
        alert("重复点赞，无效");
    }

    if (flag)
        $.ajax({
            url: "/lf/operation",
            method: "POST",
            data: {
                user_id: uid,
                id: cid,
                operation: "like",
                obj: "comment",
            },
            success: function (data) {
                var code = data["code"];
                if (code === 500) {
                    alert("尚未登陆，请先登陆再进行操作。");
                } else if (code === 200) {
                    var op = parseInt(pnum.text()) + 1;
                    pnum.text(op);
                    ppi.removeClass("fa-thumbs-o-up");
                    ppi.addClass("fa-thumbs-up");
                    alert("点赞成功");
                } else {
                    alert(data["msg"]);
                }
            },
            error: function () {
                window.alert("发生未知错误！");
            }
        })
})
//删除评论
$(".cmtdel").click(function () {
    var pp = $(this).parent().parent();
    var uid = $("#uid").text(),
        cid = pp.find(".cid").text();

    console.log(pp.html())
    console.log(uid);
    console.log(cid);

    $.ajax({
        url: "/lf/operation",
        method: "POST",
        data: {
            id: cid,
            operation: "delete",
            obj: "comment",
        },
        success: function (data) {
            var code = data["code"];
            if (code === 500) {
                alert("尚未登陆，请先登陆再进行操作。");
            } else if (code === 200) {
                pp.fadeOut();
                alert("删除成功");
            } else {
                alert(data["msg"]);
            }
        },
        error: function () {
            window.alert("发生未知错误！");
        }
    })
})
//点赞书籍
$("#favbook").click(function () {
    var uid = $("#uid").text(),
        bid = $("#bid").text();

    console.log(uid);
    console.log(bid);

    $.ajax({
        url: "/lf/operation",
        method: "POST",
        data: {
            user_id: uid,
            id: bid,
            operation: "like",
            obj: "book",
        },
        success: function f(data) {
            var code = data["code"];
            if (code === 500) {
                alert("尚未登陆，请先登陆再进行操作。");
            } else if (code === 200) {
                alert("点赞成功");
            } else {
                alert(data["msg"]);
            }
        },
        error: function () {
            window.alert("发生未知错误！");
        }
    })
})
//收藏
$("#collectbook").click(function () {
    var uid = $("#uid").text(),
        bid = $("#bid").text();

    console.log(uid);
    console.log(bid);

    $.ajax({
        url: "/lf/operation",
        method: "POST",
        data: {
            user_id: uid,
            id: bid,
            operation: "collect",
            obj: "book",
        },
        success: function f(data) {
            var code = data["code"];
            if (code === 500) {
                alert("尚未登陆，请先登陆再进行操作。");
            } else if (code === 200) {
                alert("收藏成功，去收藏夹看看吧。");
            } else {
                alert(data["msg"]);
            }
        },
        error: function () {
            window.alert("发生未知错误！");
        }
    })
})

$(document).keydown(function (event) {
    if (event.keyCode === 13) {
        $('.shbtn').click();
    }
})

$(".shbtn").click(function () {
    console.log("shbtn...");
})
//修改密码
$("#passeditbtn").click(function () {
    var oldpsd = $("#psdeditoldpsd").val(),
        newpsd = $("#psdeditnewpsd").val(),
        renewpsd = $("#psdeditrenewpsd").val(),
        flag = 1;
    console.log(oldpsd);
    console.log(newpsd);
    console.log(renewpsd);

    if (newpsd !== renewpsd) {
        flag = 0;
        $("#psdeditnewpsd").val("");
        $("#psdeditrenewpsd").val("");
        alert("两次密码不一致，请重新输入！");
    }
    if (newpsd.length < 8 || renewpsd.length < 8) {
        flag = 0;
        alert("密码长度至少为8位，请重新输入！");
    }
    var r = window.confirm("确认修改密码");
    if (r === true && flag === 1) {
        $.ajax({
            url: "/lf/operation",
            method: "POST",
            data: {
                operation: "change_password",
                oldpsd: oldpsd,
                newpsd: newpsd,
            },
            success: function f(data) {
                var code = data["code"];
                if (code === 500) {
                    alert("尚未登陆，请先登陆再进行操作。");
                } else if (code === 200) {
                    alert("密码更改成功，请重新登陆。");
                    location.href = "/lf/logout";
                } else {
                    alert(data["msg"]);
                }
            },
            error: function f() {
                alert("发生未知错误，密码更改失败。")
            }
        })
    }
})


$(".udcdel").click(function () {
    var pp = $(this).parent().parent();
    var colid = pp.children("td").html();
    console.log(colid);
    $.ajax({
        url: "/lf/operation",
        method: "POST",
        data: {
            operation: "delete",
            obj: "collection",
            id: colid,
        },
        success: function f(data) {
            console.log(data);
            var code = data['code'];
            if (code === 500) {
                alert("尚未登陆，请先登陆再进行操作。");
            } else if (code === 200) {
                alert("删除成功");
            } else {
                alert("删除失败");
            }
        },
        error: function f() {
            alert("发生未知错误，删除失败。")
        }
    })
})

// user detail libborrow delete 删除历史借阅
$(".udlbdel").click(function () {
    var pp = $(this).parent().parent();
    var lid = pp.children("td").html();
    console.log(lid);
    $.ajax({
        url: "/lf/operation",
        method: "POST",
        data: {
            operation: "delete",
            obj: "borrow",
            id: lid,
        },
        success: function f(data) {
            console.log(data);
            var code = data['code'];
            if (code === 500) {
                alert("尚未登陆，请先登陆再进行操作。");
            } else if (code === 200) {
                alert("删除成功");
            } else {
                alert("删除失败");
            }
        },
        error: function f() {
            alert("发生未知错误，删除失败。")
        }
    })
})


// user detail libborrow push - 即还书
$(".udlbpsh").click(function () {
    var pp = $(this).parent().parent();
    var lid = pp.children("td").html();
    console.log(lid);
    $.ajax({
        url: "/lf/operation",
        method: "POST",
        data: {
            operation: "back",
            obj: "borrow",
            id: lid,
        },
        success: function f(data) {
            console.log(data);
            var code = data['code'];
            if (code === 500) {
                alert("尚未登陆，请先登陆再进行操作。");
            } else if (code === 200) {
                alert(data['msg']);
                pp.fadeOut();
            } else if (code === 400) {
                alert(data['msg'])
            } else {
                alert("发生未知错误，还书失败。")
            }
        },
        error: function f() {
            alert("发生未知错误，还书失败。")
        }
    })
})

// user detail libback delete
$(".udlbbdel").click(function () {
    var pp = $(this).parent().parent();
    var lid = pp.children("td").html();
    console.log(lid);
    $.ajax({
        url: "/lf/operation",
        method: "POST",
        data: {
            operation: "delete",
            obj: "back",
            id: lid,
        },
        success: function f(data) {
            console.log(data);
            var code = data['code'];
            if (code === 500) {
                alert("尚未登陆，请先登陆再进行操作。");
            } else if (code === 200) {
                alert("删除成功");
            } else {
                alert("删除失败");
            }
        },
        error: function f() {
            alert("发生未知错误，删除失败。")
        }
    })
})


//user detail edit btn修改信息
$(".udebtn").click(function () {
    var uid = $("#id").val(),
        nickname = $("#nickname").val(),
        email = $("#email").val(),
        birthday = $("#birthday").val(),
        description = $("#description").val();
    var gender = "man";
    var gerds = $("input[name='gender']");

    var len = gerds.length;

    for (var i = 0; i < len; i++) {
        var p = gerds[i];
        if (p.checked) {
            console.log(p.value);
            gender = p.value;
            break;
        }
    }
    console.log("out");
    $.ajax({
        url: "/lf/operation",
        method: "POST",
        data: {
            operation: "push_user_detail",
            id: uid,
            nickname: nickname,
            email: email,
            birthday: birthday,
            gender: gender,
            description: description,
        },
        success: function f(data) {
            console.log(data);
            var code = data['code'];
            if (code === 500) {
                alert("尚未登陆，请先登陆再进行操作。");
            } else if (code === 200) {
                alert("用户信息修改成功");
            } else {
                alert("操作失败");
            }
        },
        error: function f() {
            alert("发生未知错误，密码更改失败。")
        }
    })
})

//msg send btn 留言
$(".msbtn").click(function () {
    var uid = $("#id").val(),
        title = $("#message_title").val(),
        message = $("#message_content").val();
    $.ajax({
        url: "/lf/operation",
        method: "POST",
        data: {
            operation: "new_message",
            id: uid,
            title: title,
            message: message,
        },
        success: function f(data) {
            console.log(data);
            var code = data['code'];
            if (code === 500) {
                alert("尚未登陆，请先登陆再进行操作。");
            } else if (code === 200) {
                alert(data['msg']);
            } else if (code === 400) {
                alert(data['msg']);
            } else {
                alert("发生未知错误，留言失败");
            }
        },
        error: function f() {
            alert("发生未知错误，留言失败。")
        }
    })
})


//announcement delete删除通知
$(".adel").click(function () {
    var pp = $(this).parent().parent()
    var aid = pp.children("td").html();
    var r = confirm("删除当前通知（全站通知无法删除）？");
    if (r)
        $.ajax({
            url: "/lf/operation",
            method: "POST",
            data: {
                operation: "delete",
                obj: "announcement",
                id: aid,
            },
            success: function (data) {
                console.log(data);
                var code = data['code'];
                if (code === 500) {
                    alert("尚未登陆，请先登陆再进行操作。");
                } else if (code === 200) {
                    alert("通知删除成功");
                    pp.hide();
                } else if (code === 400) {
                    alert(data['msg']);
                } else {
                    alert("删除失败");
                }
            },
            error: function () {
                alert("发生未知错误，删除失败");
            }
        });

});

// collection delete取消收藏
$(".coldbtn").click(function () {
    var pp = $(this);
    var colid = pp.parent().find(".colid").text();
    console.log(colid);
    var r = confirm("确认取消收藏?");
    if (r)
        $.ajax({
            url: "/lf/operation",
            method: "POST",
            data: {
                operation: "delete",
                obj: "collect",
                id: colid
            },
            success: function (data) {
                var code = data['code'];
                if (code === 500) {
                    alert("尚未登陆，请先登陆再进行操作。");
                } else if (code === 200) {
                    pp.parent().parent().hide();
                    alert("取消删除成功");
                } else if (code === 400) {
                    alert(data['msg']);
                } else {
                    alert("删除失败");
                }
            }
        })
});