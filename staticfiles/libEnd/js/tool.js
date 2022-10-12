function postToNewTabWithJSONByjQuery(url, json) {
    var $form = $('<form action="' + url + '" method="POST" target="_blank" style="display:none;"></form>');
    for (var param in json) {
        $form.append('<input type="hidden" name="' + param + '" value="' + json[param] + '" />');
    }
    $("body").append($form);

    $form.submit();
    $form.remove();
};

function generatePageNum(pg, all) {
    pg = pg + 1
    var pre = "<li class='paginate_button page-item '><a href='#' class='page-link'>";
    var pre_active = "<li class='paginate_button page-item active'><a href='#' class='page-link'>";
    var suf = "</a></li>";
    $("#previous").after(pre_active + (pg).toString() + suf);
    var count = 1;
    for (var i = 1; i <= 4; i++) {
        if (pg - i > 0) {
            count++;
            $("#previous").after(pre + (pg - i).toString() + suf);
        } else {
            break;
        }
    }
    for (var i = 1; count < 10; i++) {
        if (pg + i <= all) {
            count++;
            $("#next").before(pre + (pg + i).toString() + suf);
        } else {
            break;
        }
    }
}

function lmsiderbar() {
    $(".lm-siderbar").removeClass("menu-open");
    var url = window.location.pathname;
    var here = url.substring(4, 6);
    if (here === "us") {
        console.log(1);
        $("#user").addClass("menu-open");
    } else if (here === "bo") {
        console.log(2);
        $("#book").addClass("menu-open");
    } else if (here === "bb") {
        console.log(3);
        $("#bb").addClass("menu-open");
    } else if (here === "ot") {
        $("#other").addClass("menu-open");
    }
}

function genpage(obj) {

    var url = window.location.pathname;
    var one_page_item_num = $("[name=one_page_item_num]").val();
    var pg = $(this).text();
    var token = $.cookie("csrftoken");
    console.log(one_page_item_num);
    console.log(pg);
    data = {
        'object': obj,
        'one_page_item_num': one_page_item_num,
        'page': pg,
        "X-CSRFToken": token,
    };
    postToNewTabWithJSONByjQuery(url, data);
    window.opener = null;
    window.open('', '_self');
    window.close();

}

function lmsiderbarsearch(kw) {
    var lis = $("ul > li > ul > li.nav-item");
    console.log(lis);
    sleep(500);
    var flag = true;
    $(".lm-siderbar").removeClass("menu-open");
    for (var i = 0; i < lis.length; i++) {
        var t = lis[i].innerText.trim();
        var p = $(lis[i]);
        if (t.search(kw) !== -1) {
            flag = false;
            p.parent().parent().addClass("menu-open");
            console.log(kw);
            console.log(t);
            console.log(p.parent().html());
        }
    }
    if (flag) {
        alert("菜单中未找到匹配项。");
    }
}


function loadcatg(catgid) {
    var s = "#catg" + catgid;
    var p = $(s);
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
}