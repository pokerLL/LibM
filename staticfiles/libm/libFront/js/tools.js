function checkRegisterForm(form) {
    var nickname = $("#nickname").val(),
        account = $("#account").val(),
        password = $("#password").val(),
        repassword = $("#repassword").val(),
        email = $("#email").val(),
        birthday = $("#birthday").val(),
        description = $("#description").val();

    var msg = "", flag = 1;
    if (nickname === "") {
        flag = 0;
        msg += "请填写昵称\n";
    }
    if (account === "") {
        flag = 0;
        msg += "请填写账号\n";
    }
    if (password === "") {
        flag = 0;
        msg += "请填写密码\n";
    }
    if (email === "") {
        flag = 0;
        msg += "请填写邮箱\n";
    }


    if (password !== repassword && password !== "") {
        flag = 0;
        msg += "密码不一致\n";
    }

    if (password.length < 8 || repassword.length < 8) {
        flag = 0;
        msg += "密码长度至少为8位\n";
    }

    if (flag === 1) {
        return true;
    } else {
        alert(msg);
        return false;
    }
}

function hideall() {
    $("div").addClass("hidden");
    $("#bgimg").removeClass("hidden");
}

function loadheaderbar() {
    $.ajax({
        url: "/lf/operation",
        method: "POST",
        data: {
            operation: "load_headerbar"
        },
        success: function (data) {
            var catg1 = data["catg1"],
                catg2 = data["catg2"],
                href = $("#headurl").text();
            var html1 = "", html2 = "";
            for (var i = 0; i < catg1.length; i++) {
                var name = catg1[i][0], id = catg1[i][1];
                html1 += '<li><a href="' + href.substring(0, href.length - 3) + id + '/1">' + name + "</a></li>";
            }
            $(".fake-li").hide();
            $("#ulbar").prepend(html1);
            for (var i = 0; i < catg2.length; i++) {
                var name = catg2[i][0], id = catg2[i][1];
                html2 += '<li><a href="' + href.substring(0, href.length - 3) + id + '/1">' + name + "</a></li>";
            }
            $("#dropdownbar").prepend(html2);
        },
        error: function () {

        }
    })
}

function sleep(numberMillis) {
    var now = new Date();
    var exitTime = now.getTime() + numberMillis;
    while (true) {
        now = new Date();
        if (now.getTime() > exitTime)
            return;
    }
}

function positionFooter() {
    var footerHeight = 0,
        footerTop = 0,
        $footer = $("#footer");
    footerHeight = $footer.height()
    footerTop = ($(window).scrollTop() + $(window).height() - footerHeight) + "px";

    if (($(document.body).height() + footerHeight) < $(window).height()) {
        console.log("页面内容高度小于屏幕高度");
        $footer.css({
            position: "absolute",
            bottom: "0px"
        });
    } else {
        console.log("页面内容高度大于屏幕高度");
        $footer.css({
            position: "static"
        });
    }
}