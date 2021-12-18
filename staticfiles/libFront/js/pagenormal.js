function generatepagenum(pg, all) {
    url = window.location.pathname;
    url = url.slice(0, url.lastIndexOf("/")+1);
    // console.log(url.lastIndexOf("/"))
    // console.log(url);
    document.getElementById("first").setAttribute("href", url + 1);
    document.getElementById("last").setAttribute("href", url + all);
    document.getElementById("pre").getElementsByTagName("a")[0].setAttribute("href", url + (pg - 1).toString());
    document.getElementById("suf").getElementsByTagName("a")[0].setAttribute("href", url + (pg + 1).toString());
    var astr = '<li><a href="#">';
    var bstr = '</a></li>';
    var pre = document.getElementById("pre");
    var suf = document.getElementById("suf");
    var pp = document.createElement("li");
    var aa = document.createElement("a");
    aa.innerText = pg;
    pp.setAttribute("class", "active")
    pp.insertAdjacentElement("afterbegin", aa);
    pre.insertAdjacentElement("afterend", pp);

    var count = 1;
    for (var i = 1; i <= 4; i++) {
        if (pg - i > 0) {
            count++;
            var pp = document.createElement("li");
            var aa = document.createElement("a");
            aa.setAttribute("href", url + (pg - i).toString());
            aa.innerText = pg - i;
            pp.insertAdjacentElement("afterbegin", aa);
            pre.insertAdjacentElement("afterend", pp);
        } else {
            break;
        }
    }
    for (var i = 1; count < 10; i++) {
        if (pg + i <= all) {
            count++;
            var pp = document.createElement("li");
            var aa = document.createElement("a");
            aa.setAttribute("href", url + (pg + i).toString());
            aa.innerText = pg + i;
            pp.insertAdjacentElement("afterbegin", aa);
            suf.insertAdjacentElement("beforebegin", pp);
        } else {
            break;
        }
    }
}


