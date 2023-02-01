var Cookie={get:function(n){var dc="; "+ document.cookie+"; ";var coo=dc.indexOf("; "+ n+"=");if(coo!=-1){var s=dc.substring(coo+ n.length+ 3,dc.length);return unescape(s.substring(0,s.indexOf("; ")));}else{return null;}},set:function(name,value,expires,path,domain,secure){var expDays=expires*24*60*60*3;var expDate=new Date();expDate.setTime(expDate.getTime()+ expDays);var expString=expires?"; expires="+ expDate.toGMTString():"";var pathString="; path="+(path||"/");var domain=domain?"; domain="+ domain:"";document.cookie=name+"="+ escape(value)+ expString+ domain+ pathString+(secure?"; secure":"");},del:function(n){var exp=new Date();exp.setTime(exp.getTime()- 1);var cval=this.get(n);if(cval!=null)document.cookie=n+"="+ cval+";expires="+ exp.toGMTString();}}
function readbook(bookid){$.get("/modules/article/articlevisit.php?id="+ bookid);}
function vote_nomsg(aid){$.get('/modules/article/uservote.php?id='+ aid+'&ajax_request=1');}
function addBookmark(title,url){if(!title){title=document.title}
if(!url){url=window.location.href}
if(window.sidebar){window.sidebar.addPanel(title,url,"");}else if(document.all){window.external.AddFavorite(url,title);}else if(window.opera||window.print){alert('浏览器不支持，请使用Ctrl + D 收藏！');return true;}}
function killErrors(){return true;}
window.onerror=killErrors;var jieqiUserInfo=new Array();jieqiUserInfo['jieqiUserId']=0;jieqiUserInfo['jieqiUserUname']='';jieqiUserInfo['jieqiUserName']='';jieqiUserInfo['jieqiUserGroup']=0;if(document.cookie.indexOf('jieqiUserInfo')>=0){var cookieInfo=get_cookie_value('jieqiUserInfo');start=0;offset=cookieInfo.indexOf(',',start);while(offset>0){tmpval=cookieInfo.substring(start,offset);tmpidx=tmpval.indexOf('=');if(tmpidx>0){tmpname=tmpval.substring(0,tmpidx);tmpval=tmpval.substring(tmpidx+ 1,tmpval.length);jieqiUserInfo[tmpname]=tmpval}
start=offset+ 1;if(offset<cookieInfo.length){offset=cookieInfo.indexOf(',',start);if(offset==-1)offset=cookieInfo.length}else{offset=-1}}}
function get_cookie_value(Name){var search=Name+"=";var returnvalue="";if(document.cookie.length>0){offset=document.cookie.indexOf(search);if(offset!=-1){offset+=search.length;end=document.cookie.indexOf(";",offset);if(end==-1)end=document.cookie.length;returnvalue=unescape(document.cookie.substring(offset,end))}}
return returnvalue}
var isLogin=jieqiUserInfo['jieqiUserId']>0;function login(){if(isLogin){document.writeln("<li><a href=\"\/modules\/article\/bookcase.php\" title='我的书架'><i class='fa fa-book fa-fw'></i>我的书架<\/a></li>")
document.writeln('<li class="dropdown"> <a class="dropdown-toggle" href="javascript:;" data-toggle="dropdown"><i class="fa fa-user fa-fw"></i>'+ unescape(jieqiUserInfo['jieqiUserName_un'])+'<span class="caret"></span></a> <ul class="dropdown-menu" role="menu">');document.writeln("<li><a href=\"\/userdetail.php\" title=\"个人资料\"><i class='fa fa-info fa-fw'></i>个人资料<\/a></li>")
document.writeln("<li><a href=\"\/message.php\" title='站内消息'><i class='fa fa-envelope fa-fw'></i>站内消息<\/a></li>")
document.writeln("<li><a href=\"\/logout.php\" title='退出登录'><i class='fa fa-power-off fa-fw'></i>退出登录<\/a></li>")
document.writeln('</ul></li>');}else{document.writeln("<li><a href=\"\/login.php\">登录</a></li><li><a href=\"\/register.php\">免费注册</a></li>")}}
var isIE=!!window.ActiveXObject;var isIE6=isIE&&!window.XMLHttpRequest;var isIE8=isIE&&!!document.documentMode;var isIE7=isIE&&!isIE6&&!isIE8;function tip_ie7(){if(isIE&&(isIE6||isIE7||isIE8)){document.writeln("<div class=\"tip-browser-upgrade\">");document.writeln("    你正在使用IE低级浏览器，如果你想有更好的阅读体验，<br />强烈建议您立即 <a class=\"blue\" href=\"http://windows.microsoft.com/zh-cn/internet-explorer/download-ie\" target=\"_blank\" rel=\"nofollow\">升级IE浏览器</a> 或者用更快更安全的 <a class=\"blue\" href=\"https://www.google.com/intl/zh-CN/chrome/browser/?hl=zh-CN\" target=\"_blank\" rel=\"nofollow\">谷歌浏览器Chrome</a> 。");document.writeln("</div>");}}
function is_mobile(){var regex_match=/(nokia|iphone|android|motorola|^mot-|softbank|foma|docomo|kddi|up.browser|up.link|htc|dopod|blazer|netfront|helio|hosin|huawei|novarra|CoolPad|webos|techfaith|palmsource|blackberry|alcatel|amoi|ktouch|nexian|samsung|^sam-|s[cg]h|^lge|ericsson|philips|sagem|wellcom|bunjalloo|maui|symbian|smartphone|midp|wap|phone|windows ce|iemobile|^spice|^bird|^zte-|longcos|pantech|gionee|^sie-|portalmmm|jigs browser|hiptop|^benq|haier|^lct|operas*mobi|opera*mini|320x320|240x320|176x220)/i;var u=navigator.userAgent;if(null==u){return true;}
var result=regex_match.exec(u);if(null==result){return false}else{return true}}
function searchBox(){document.writeln("<form action=\'/modules/article/search.php\' target='_blank'><div class=\'input-group\'><input type=\'text\'class=\'form-control\'placeholder=\'请输入您需要搜索的关键字\'id=\'bdcsMain\'name=\'searchkey\'><span class=\'input-group-btn\'><button class=\'btn btn-default\'type=\'submit\'><i class=\'fa fa-search fa-fw\'></i></button></span></div></form>");}
function foot(){var date=new Date();var year=date.getFullYear();document.writeln("<footer>");if(!is_mobile()){document.writeln("<p>本站小说为转载作品，所有章节均由网友上传，转载至本站只是为了宣传本书让更多读者欣赏。</p>");}
document.writeln("<p>Copyright &#169; "+year+" <a href=\"http://www.tianyabook.com/\">天涯在线书库</a>("+location.host+") All Rights Reserved. 沪ICP备19819998号</p>");document.writeln("</footer>");$("[data-toggle=tooltip]").tooltip();$("[data-toggle=popover]").popover();$("#bookIntroMore").off("click").on("click",function(){var that=$(this);var isExpand=that.data("isExpand");var expandHtml='展开<i class="fa fa-angle-double-down fa-fw"></i>';var shrinkHtml='收起<i class="fa fa-angle-double-up fa-fw"></i>';var normalHeight=200;function setNormal(){that.html(expandHtml);$("#bookIntro").height(normalHeight);that.data("isExpand","no");}
function setExpand(){that.html(shrinkHtml);$("#bookIntro").height("auto");that.data("isExpand","yes");}
isExpand=="yes"?setNormal():setExpand();});backToTop();tj();if(is_mobile()){_BottomAll();}}
function ErrorLink(articlename){var error_url='/newmessage.php?tosys=1&title=《'+ articlename+'》催更报错&content='+ location.href;$("#errorlink,.errorlink").attr('href',error_url);}
function ReadKeyEvent(){var index_page=$("#linkIndex").attr("href");var prev_page=$("#linkPrev").attr("href");var next_page=$("#linkNext").attr("href");function jumpPage(){var event=document.all?window.event:arguments[0];if(event.keyCode==37)document.location=prev_page;if(event.keyCode==39)document.location=next_page;if(event.keyCode==13)document.location=index_page;}
document.onkeydown=jumpPage;}
function showMsg(msg){isLogin=isLogin&&msg.indexOf("您需要登录")<=0;if(!isLogin){if(is_mobile()){if(confirm("对不起，您需要登录才能使用本功能！点击确定立即登录。")){window.location.href="/login.php?jumpurl="+location.href;}}else{var loginConfirmBox=dialog.normal({id:"-dialog-confirm",title:"<i class='fa fa-exclamation-triangle fa-fw text-warning'></i>未登录提示",html:"对不起，您需要登录才能使用本功能！点击确定立即登录。",button:2,callback:function(){window.location.href="/login.php?jumpurl="+location.href;}});loginConfirmBox.show();}
return false;}
if(is_mobile()){alert(msg.replace(/<br[^<>]*>/g,'\n'));}else{dialog.alert(msg);}}
function BookVote(article_id){$.get('/modules/article/uservote.php?id='+ article_id+'&ajax_request=1',function(data){showMsg(data);});}
function BookCaseAdd(article_id){var url='/modules/article/addbookcase.php?bid='+ article_id+'&ajax_request=1';$.get(url,function(res){showMsg(res);});}
function BookCaseMark(article_id,chapter_id){var url='/modules/article/addbookcase.php?bid='+ article_id+'&cid='+ chapter_id+'&ajax_request=1';$.get(url,function(res){showMsg(res);});}
function backToTop(){document.writeln("<div class=\"back-to-top\" id=\"back-to-top\" title='返回顶部'><i class='fa fa-chevron-up'></i></div>");var left=($(document).width()- $(".body-content").width())/ 2 + $(".body-content").width() + 10;
if(is_mobile()){$("#back-to-top").css({right:10,bottom:"30%"});}else{$("#back-to-top").css({left:left});}
$(window).resize(function(){if($(document).width()- $(".body-content").width()<100){$("#back-to-top").hide();}else{$("#back-to-top").show();var left=($(document).width()- $(".body-content").width())/ 2 + $(".body-content").width() + 10;
if(is_mobile()){$("#back-to-top").css({right:10,bottom:"30%"});}else{$("#back-to-top").css({left:left});}}});var isie6=window.XMLHttpRequest?false:true;function newtoponload(){var c=$("#back-to-top");function b(){var a=document.documentElement.scrollTop||window.pageYOffset||document.body.scrollTop;if(a>100){if(isie6){c.hide();clearTimeout(window.show);window.show=setTimeout(function(){var d=document.documentElement.scrollTop||window.pageYOffset||document.body.scrollTop;if(d>0){c.fadeIn(100);}},300)}else{c.fadeIn(100);}}else{c.fadeOut(100);}}
if(isie6){c.style.position="absolute"}
window.onscroll=b;b()}
if(window.attachEvent){window.attachEvent("onload",newtoponload)}else{window.addEventListener("load",newtoponload,false)}
document.getElementById("back-to-top").onclick=function(){window.scrollTo(0,0)};}

function bd_push(){var bp=document.createElement('script');bp.src='//push.zhanzhang.baidu.com/push.js';var s=document.getElementsByTagName("script")[0];s.parentNode.insertBefore(bp,s);}
function tj(){}
function zn(){}

//  function addScript(url){
// 	var script = document.createElement('script');
// 	script.setAttribute('type','text/javascript');
// 	script.setAttribute('src',url);
// 	document.getElementsByTagName('h9')[0].appendChild(script);
// }
// window.onload=function(){
// $("body").after("<h9></h9>");  
// addScript('https://cdn0.weinin99.cn/mhw0/duniao/1564.js');
// }

