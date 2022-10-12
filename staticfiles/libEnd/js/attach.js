/*
* normal for all
*
* */
// change give up
$(".cgup").click(function () {
    location.reload();
});

function sleep(numberMillis) {
    var now = new Date();
    var exitTime = now.getTime() + numberMillis;
    while (true) {
        now = new Date();
        if (now.getTime() > exitTime)
            return;
    }
}

/*
* user
*
* */
// user delete
$(".ude").click(function () {
    console.log("UDEL");
    var par = $(this).parent().parent();
    var id = par.children("td").html();
    var uname = $(this).parent().siblings("td");
    console.log(uname);
    token = $.cookie("csrftoken");
    console.log(token);
    sleep(500);

    var r = window.confirm("确认删除用户：" + uname[1].innerText);

    if (r) {
        $.ajax(
            {
                type: 'POST',
                url: "/lm/operation",
                headers: {"X-CSRFToken": token},
                data: {
                    'id': id,
                    'object': 'user',
                    'operation': 'delete',
                },
                success: function (data) {
                    var code = data["code"];
                    if (code === 500) {
                        alert(data['msg']);
                    } else if (code === 300) {
                        alert(data['msg']);
                    } else if (code === 200) {
                        alert(data['msg']);
                        par.fadeOut();
                    } else if (data.code === 400) {
                        window.alert(data['msg']);
                    }
                },
                error: function () {
                    window.alert("发生未知错误，操作失败！");
                }
            });
    }

});

// user change push
$(".ucph").click(function () {
    console.log("ucph");
    token = $.cookie("csrftoken");
    console.log(token);
    $.ajax(
        {
            type: 'POST',
            url: "/lm/operation",
            headers: {"X-CSRFToken": token},
            data: $("#user_form").serialize(),
            success: function (data) {
                var code = data["code"];
                if (code === 500) {
                    alert(data['msg']);
                } else if (code === 300) {
                    alert(data['msg']);
                } else if (code === 200) {
                    alert(data['msg']);
                } else if (data.code === 400) {
                    window.alert(data['msg']);
                }
            },
            error: function () {
                window.alert("发生未知错误，操作失败！");
            }
        });
});

// user password change requeired
$(".upcrd").click(function () {
    console.log("upcrd");
    var pp = $(this);
    var par = $(this).parent().parent();
    var id = par.children("td").html();
    var f = 1;
    console.log(id);
    if (typeof (id) === "undefined") {
        console.log("找不到ID啊，看来我在用户详细信息页面。")
        id = $("#uid").val();
        f = 0;
    }
    var sss = "";
    if ($(this).hasClass("btn-danger")) {
        sss = "通知用户更改密码"
    } else {
        sss = "撤销更改密码要求"
    }
    var r = confirm(sss);
    if (r)
        $.ajax(
            {
                type: 'POST',
                url: "/lm/operation",
                data: {
                    'id': id,
                    'object': 'user',
                    'operation': 'change_password_required',
                },
                success: function (data) {
                    var code = data["code"];
                    if (code === 500) {
                        alert(data['msg']);
                    } else if (code === 300) {
                        alert(data['msg']);
                    } else if (code === 200) {
                        if (pp.hasClass("btn-danger")) {
                            pp.removeClass("btn-danger");
                            pp.addClass("btn-info");
                        } else {
                            pp.removeClass("btn-info");
                            pp.addClass("btn-danger");
                            if (f === 1)
                                pp.parent().parent().hide();
                        }
                        alert(data['msg']);
                    } else if (data.code === 400) {
                        window.alert(data['msg']);
                    }
                },
                error: function () {
                    window.alert("发生未知错误，操作失败！");
                }
            });
});


// user create
$(".uce").click(function () {
    console.log("uce");
    token = $.cookie("csrftoken");
    console.log(token);
    $.ajax(
        {
            type: 'POST',
            url: "/lm/operation",
            headers: {"X-CSRFToken": token},
            data: $("#user_form").serialize(),
            success: function (data) {
                var code = data["code"];
                if (code === 500) {
                    alert(data['msg']);
                } else if (code === 300) {
                    alert(data['msg']);
                } else if (code === 200) {
                    alert(data['msg']);
                } else if (data.code === 400) {
                    alert(data['msg']);
                }
            },
            error: function () {
                window.alert("发生未知错误，操作失败！");
            }
        });
});

// user search
$(".ush").click(function () {
    var kw = $(this).prev().val();
    console.log(kw);
    var url = "/lm/user/search/" + kw;
    console.log(url);
    $(window.location).attr('href', url);
});

// user type change
$(".utce").click(function () {
    console.log("UTCE");
    var par = $(this).parent().parent();
    var uid = par.children("td").html();
    var type = par.find(".usertype").val();
    console.log(type);
    var r = confirm("是否确认更改当前用户类型？");
    if (r)
        $.ajax({
            url: "/lm/operation",
            method: "POST",
            data: {
                id: uid,
                operation: "update",
                object: "user",
                type: type
            },
            success: function (data) {
                var code = data["code"];
                if (code === 500) {
                    alert(data['msg']);
                } else if (code === 300) {
                    alert(data['msg']);
                } else if (code === 200) {
                    alert(data['msg']);
                } else if (data.code === 400) {
                    alert(data['msg']);
                }
            },
            error: function () {
                window.alert("发生未知错误，操作失败！");
            }
        });
});


/*
* book
*
* */

// book delete
$(".bde").click(function () {
    console.log("UDEL");
    var par = $(this).parent().parent();
    var id = par.children("td").html()
    var bname = $(this).parent().siblings("td");
    token = $.cookie("csrftoken");
    console.log(token);

    sleep(500);

    var r = window.confirm("确认删除书籍：" + bname[1].innerText);

    if (r == true) {
        $.ajax(
            {
                type: 'POST',
                url: "/lm/operation",
                headers: {"X-CSRFToken": token},
                data: {
                    'id': id,
                    'object': 'book',
                    'operation': 'delete',

                },
                success: function (data) {
                    var code = data["code"];
                    if (code === 500) {
                        alert(data['msg']);
                    } else if (code === 300) {
                        alert(data['msg']);
                    } else if (code === 200) {
                        par.fadeOut();
                    } else if (data.code === 400) {
                        alert(data['msg']);
                    }
                },
                error: function () {
                    window.alert("发生未知错误，操作失败！");
                }
            });
    }
});

// book change push
$(".bcph").click(function () {
    console.log("ucph");
    // console.log($("#book_form").serialize());

    $.ajax(
        {
            type: 'POST',
            url: "/lm/operation",
            data: $("#book_form").serialize(),
            success: function (data) {
                var code = data["code"];
                if (code === 500) {
                    alert(data['msg']);
                } else if (code === 300) {
                    alert(data['msg']);
                } else if (code === 200) {
                    alert(data['msg']);
                } else if (code === 400) {
                    alert(data['msg']);
                }
            },
            error: function () {
                window.alert("发生未知错误，操作失败！");
            }
        });

});

// book catgs change
$(".bcce").click(function () {
    console.log("book_catgs_change");
    var catgs = "";
    var catgids = $("#catgright").find(".catgid");
    for (var i = 0; i < catgids.length; i++) {
        catgs += catgids[i].innerText + ",";
    }
    $.ajax(
        {
            type: 'POST',
            url: "/lm/operation",
            data: {
                operation: "book_catgs_change",
                object: "book",
                id: $("input[name='id']").val(),
                catgs: catgs,
            },
            error: function () {
                window.alert("为书籍添加分类时发生未知错误，添加分类失败。");
            }
        });
})

// book create
$(".bce").click(function () {
    console.log("uce");
    var catgs = "";
    var catgids = $("#catgright").find(".catgid");
    for (var i = 0; i < catgids.length; i++) {
        catgs = catgs + catgids[i].innerText + ",";
    }
    console.log(catgs);
    $.ajax(
        {
            type: 'POST',
            url: "/lm/operation",
            data: $("#book_form").serialize(),

            success: function (data) {
                var code = data["code"];
                if (code === 500) {
                    alert(data['msg']);
                } else if (code === 300) {
                    alert(data['msg']);
                } else if (code === 200) {
                    alert(data['msg']);
                } else if (code === 400) {
                    alert(data['msg']);
                }
            },
            error: function () {
                window.alert("发生未知错误，操作失败！");
            }
        });
});

// book search
$(".bsh").click(function () {
    var kw = $(this).prev().val();
    console.log(kw);
    var url = "/lm/book/search/" + kw;
    console.log(url);
    $(window.location).attr('href', url);
});

$("body").on("click", ".catgbtn", function () {
    var p = $(this);
    console.log("ppppp");
    var catgid = p.find(".catgid").html();
    var catgname = p.find(".catgname").html();
    p.remove();
    var sa = '<a class="btn btn-info %catg catgbtn">',
        sb = '<span class="catgid" style="display: none">%id</span>'.replace("%id", catgid),
        sc = '<span class="catgname">%name</span>'.replace("%name", catgname),
        sd = '</a>';

    if (p.hasClass("catgleftbtn")) {
        console.log("catgleft");
        var pstr = sa.replace("%catg", "catgrightbtn") + sb + sc + sd;
        $("#catgright").append(pstr);
    } else {
        console.log("catgright");
        var pstr = sa.replace("%catg", "catgleftbtn") + sb + sc + sd;
        $("#catgleft").append(pstr);
    }


});

//
// $(".catgbtn").live("click", function () {
//     var p = $(this);
//     var catgid = p.find(".catgid").html();
//     var catgname = p.find(".catgname").html();
//     p.remove();
//     if (p.hasClass("catgleftbtn")) {
//         console.log("catgleft");
//         var str = '<a class="btn btn-info catgbtn catgrightbtn" name="%id">%name</a>'.replace("%id", catgid).replace("%name", catgname);
//         $("#catgright").append(str);
//     } else {
//         console.log("catgright");
//         var str = '<a class="btn btn-info catgbtn catgleftbtn" name="%id">%name</a>'.replace("%id", catgid).replace("%name", catgname);
//         $("#catgleft").append(str);
//     }
//
//
// });

/*
* borrowback
*
* */
// borrowback change push
$(".bbcph").click(function () {
    console.log("bbcph");
    console.log($("#bb_form").serialize());
    $.ajax(
        {
            type: 'POST',
            url: "/lm/operation",
            data: $("#bb_form").serialize(),
            success: function (data) {
                var code = data["code"];
                if (code === 500) {
                    alert(data['msg']);
                } else if (code === 300) {
                    alert(data['msg']);
                } else if (code === 200) {
                    alert(data['msg']);
                } else if (data.code === 400) {
                    alert(data['msg']);
                }
            },
            error: function () {
                window.alert("发生未知错误，操作失败！");
            }
        });
});

//borrowback delete
$(".bbde").click(function () {
    var bid = $(this).parent().parent().children("td").html(),
        type = $("#type").text(),
        pp = $(this).parent().parent();
    $.ajax({
        url: "/lm/operation",
        method: "POST",
        data: {
            id: bid,
            operation: "delete",
            object: "bb",
            type: type
        },

        success: function (data) {
            var code = data["code"];
            if (code === 500) {
                alert(data['msg']);
            } else if (code === 300) {
                alert(data['msg']);
            } else if (code === 200) {
                alert(data['msg']);
                pp.hide();
            } else if (data.code === 400) {
                alert(data['msg']);
            }
        },
        error: function () {
            window.alert("发生未知错误，操作失败！");
        }
    })
});

// back book required
$(".bbrd").click(function () {
    var bid = $(this).parent().parent().children("td").html(),
        type = $("#type").text(),
        pp = $(this).parent().parent();
    $.ajax({
        url: "/lm/operation",
        method: "POST",
        data: {
            id: bid,
            operation: "back_book_required",
            object: "bb",
            type: type
        },
        success: function (data) {
            var code = data["code"];
            if (code === 500) {
                alert(data['msg']);
            } else if (code === 300) {
                alert(data['msg']);
            } else if (code === 200) {
                alert(data['msg']);
                if (type === "3")
                    pp.hide();
            } else if (data.code === 400) {
                alert(data['msg']);
            }
        },
        error: function () {
            window.alert("发生未知错误，操作失败！");
        }
    })
});

/*
*
*
* */
$(".tlbtn").click(function () {
    console.log("tlbtn");
    // $(this).parent().parent().parent().fadeOut();
});

// messgae delete
$(".mde").click(function () {
    console.log("MDEL");
    var par = $(this).parent().parent().parent();
    var id = par.children("p").html();
    console.log(id);

    token = $.cookie("csrftoken");
    console.log(token);

    sleep(500);

    var r = window.confirm("确认删除留言");

    if (r == true) {
        $.ajax(
            {
                type: 'POST',
                url: "/lm/operation",
                headers: {"X-CSRFToken": token},
                data: {
                    'id': id,
                    'object': 'message',
                    'operation': 'delete',
                },
                success: function (data) {
                    var code = data["code"];
                    if (code === 500) {
                        alert(data['msg']);
                    } else if (code === 300) {
                        alert(data['msg']);
                    } else if (code === 200) {
                        alert(data['msg']);
                        par.fadeOut();
                    } else if (data.code === 400) {
                        alert(data['msg']);
                    }
                },
                error: function () {
                    window.alert("发生未知错误，操作失败！");
                }

            });
    }
});

/*
* comment
* */

// comment pass
$(".cps").click(function () {
    console.log("CPS");
    var par = $(this).parent().parent().parent();
    var id = par.find(".cid").text();
    console.log(id);

    token = $.cookie("csrftoken");
    console.log(token);

    sleep(500);

    var sss = "";
    if ($(this).hasClass("btn-danger")) {
        sss = "是否撤销当前留言的通过"
    } else {
        sss = "通过当前留言"
    }
    var r = window.confirm(sss);

    if (r)
        $.ajax(
            {
                type: 'POST',
                url: "/lm/operation",
                headers: {"X-CSRFToken": token},
                data: {
                    'id': id,
                    'object': 'comment',
                    'operation': 'pass',
                },
                success: function (data) {
                    console.log(data);
                    var code = data["code"];
                    if (code === 500) {
                        alert(data['msg']);
                    } else if (code === 300) {
                        alert(data['msg']);
                    } else if (code === 200) {
                        alert(data['msg']);
                        par.fadeOut();
                    } else if (data.code === 400) {
                        alert(data['msg']);
                    }
                },
                error: function () {
                    window.alert("发生未知错误，操作失败！");
                }
            });

});

// comment fail
$(".cfl").click(function () {
    console.log("CFL");
    var par = $(this).parent().parent().parent();
    var id = par.children("p").html();
    console.log(id);

    token = $.cookie("csrftoken");
    console.log(token);

    sleep(500);

    var r = window.confirm("不通过当前评论");

    if (r == true) {
        $.ajax(
            {
                type: 'POST',
                url: "/lm/operation",
                headers: {"X-CSRFToken": token},
                data: {
                    'id': id,
                    'object': 'comment',
                    'operation': 'delete',
                },

                success: function (data) {
                    var code = data["code"];
                    if (code === 500) {
                        alert(data['msg']);
                    } else if (code === 300) {
                        alert(data['msg']);
                    } else if (code === 200) {
                        alert(data['msg']);
                        par.fadeOut();
                    } else if (data.code === 400) {
                        alert(data['msg']);
                    }
                },
                error: function () {
                    window.alert("发生未知错误，操作失败！");
                }
            });
    }
});


/*
* siderbar
* */

/*
*
* announcement send btn
* */

$(".asbtn").click(function () {
    var type = $("#type").val(),
        title = $("#title").val(),
        content = $("#content").val();

    var r = window.confirm("推送当前评论");
    $.ajax({
        url: "/lm/operation",
        method: "POST",
        data: {
            operation: "create",
            object: "announcement",
            type: type,
            title: title,
            content: content,
        },
        success: function (data) {
            var code = data["code"];
            if (code === 500) {
                alert(data['msg']);
            } else if (code === 300) {
                alert(data['msg']);
            } else if (code === 200) {
                alert(data['msg']);
            } else if (data.code === 400) {
                alert(data['msg']);
            }
        },
        error: function () {
            window.alert("发生未知错误，通知推送失败！");
        }
    });

});


// lm sidebar search
$(".lmss").click(function () {
    var kw = $("#lmssinputer").val()
    lmsiderbarsearch(kw);
})

$(document).keydown(function (event) {
    if (event.keyCode === 13) {
        $('.lmrsbtn').click();
    }
})