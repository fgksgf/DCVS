$("#btn1").on('click', function () {
    const url = $('#url-input').val();
    const code = $('#code-input').val();

    // 检验输入是否为空
    if (url.length === 0) {
        alert('请输入商品详情页URL!');
        return;
    }
    if (code.length === 0) {
        alert('请输入验证码!');
        return;
    } else if (code.length !==4) {
        alert('输入的验证码有误!');
        return;
    }

    // 隐藏按钮，防止重复请求
    $('#btn1').css('display', 'none');

    // 正则验证URL是否符合格式
    const pattern = /^(http(s)?:\/\/item\.jd\.com\/)[0-9]+(\.html)$/;
    const re = new RegExp(pattern);
    if (!re.test(url)) {
        alert('URL不符合示例格式，请重试！');
        $('#btn1').css('display', 'inline');
        return;
    }

    const pid = url.slice(20, -5);
    $('.alert').css('display', 'block');
    const params = {
        pid: pid,
        code: code
    };
    $.ajax({
        type: 'POST',                         //请求方式为post方式
        url: 'crawl/jd/',              //请求地址
        dataType: 'json',                    //服务器返回类型为JSON类型
        data: params,
        success: function (data) {           //请求成功后的回调函数
            if (data.result === 'ok') {
                alert('爬取完成！');
                // 页面跳转
                location.href = 'http://' + location.host + '/analyze/jd/bar/' + data.pid
            } else if (data.result === 'wrong_code') {
                alert('验证码错误！');
                $('.alert').css('display', 'none');
                $('#btn1').css('display', 'inline');
            }
        },
        error: function () {
            alert('连接服务器失败，请稍后重试！');
            $('.alert').css('display', 'none');
            $('#btn1').css('display', 'inline');
        }
    });
});