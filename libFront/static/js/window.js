// 每个弹窗的标识
var x = 0;

var idzt = new Array();

var Window = function (config) {

    //ID不重复
    idzt[x] = "zhuti" + x;  //弹窗ID

    //初始化，接收参数
    this.config = {
        width: config.width || 300, //宽度
        height: config.height || 200, //高度
        buttons: config.buttons || '', //默认无按钮
        title: config.title || '标题', //标题
        content: config.content || '内容', //内容
        isMask: config.isMask == false ? false : config.isMask || true, //是否遮罩
        isDrag: config.isDrag == false ? false : config.isDrag || true, //是否移动
    };

    //加载弹出窗口
    var w = ($(window).width() - this.config.width) / 2;
    var h = ($(window).height() - this.config.height) / 2 + 200;

    var nr = "<div class='zhuti' id='" + idzt[x] + "' bs='" + x + "' style='width:" + this.config.width + "px; height:" + this.config.height + "px; background-color:white; left:" + w + "px; top:" + h + "px;'></div>";
    $("body").append(nr);

    //加载弹窗标题
    var content = "<div id='title" + x + "' class='title' bs='" + x + "'>" + this.config.title + "<div id='close" + x + "' class='close' bs='" + x + "'>×</div></div>";
    //加载弹窗内容
    var nrh = this.config.height - 75;
    content = content + "<div id='content" + x + "' bs='" + x + "' class='content' style='width:100%; height:" + nrh + "px;'>" + this.config.content + "</div>";
    //加载按钮
    content = content + "<div id='btnx" + x + "' bs='" + x + "' class='btnx'>" + this.config.buttons + "</div>";

    //将标题、内容及按钮添加进窗口
    $('#' + idzt[x]).html(content);


    //创建遮罩层
    if (this.config.isMask) {
        var zz = "<div id='zz'></div>";
        $("body").append(zz);
        $("#zz").css('display', 'block');
    }

    //最大最小限制，以免移动到页面外
    var maxX = $(window).width() - this.config.width;
    var maxY = $(window).height() - this.config.height;
    var minX = 0,
        minY = 0;

    //窗口移动
    if (this.config.isDrag) {
        //鼠标移动弹出窗
        $(".title").bind("mousedown", function (e) {

            var n = $(this).attr("bs"); //取标识

            //使选中的到最上层
            $(".zhuti").css("z-index", 3);
            $('#' + idzt[n]).css("z-index", 4);

            //取初始坐标
            var endX = 0, //移动后X坐标
                endY = 0, //移动后Y坐标
                startX = parseInt($('#' + idzt[n]).css("left")), //弹出层的初始X坐标
                startY = parseInt($('#' + idzt[n]).css("top")), //弹出层的初始Y坐标
                downX = e.clientX, //鼠标按下时，鼠标的X坐标
                downY = e.clientY; //鼠标按下时，鼠标的Y坐标

            //绑定鼠标移动事件
            $("body").bind("mousemove", function (es) {

                endX = es.clientX - downX + startX; //X坐标移动
                endY = es.clientY - downY + startY; //Y坐标移动

                //最大最小限制
                if (endX > maxX) {
                    endX = maxX;
                } else if (endX < 0) {
                    endX = 0;
                }
                if (endY > maxY) {
                    endY = maxY;
                } else if (endY < 0) {
                    endY = 0;
                }

                $('#' + idzt[n]).css("top", endY + "px");
                $('#' + idzt[n]).css("left", endX + "px");

                window.getSelection ? window.getSelection().removeAllRanges() : document.selection.empty(); //取消选中文本

            });
        });
        //鼠标按键抬起，释放移动事件
        $("body").bind("mouseup", function () {

            $("body").unbind("mousemove");

        });
    }

    //关闭窗口
    $(".close").click(function () {
        console.log("close");
        var m = this.getAttribute("bs"); //找标识
        $('#' + idzt[m]).remove(); //移除弹窗
        $('#zz').remove(); //移除遮罩

    })

    $(".closebtn").click(function () {
        console.log("closebtn");
        var m = $(".close")[0].getAttribute("bs"); //找标识
        $('#' + idzt[m]).remove(); //移除弹窗
        $('#zz').remove(); //移除遮罩
    })

    x++;  //标识增加

}