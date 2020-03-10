$(function () {
    let $login = $('.form-contain');

    $login.submit(function (e) {
        e.preventDefault();

        // 用户名验证
        let sUsername = $('input[name=telephone]').val();
        if (sUsername === '') {
            message.showError('用户名不能为空');
            return
        }
        if (!(/^[\u4e00-\u9fa5\w]{5,20}$/.test(sUsername))) {
            message.showError('请输入5~20位字符用户名');
            return
        }

        // 密码验证
        let sPassword = $('input[name=password]').val();

        if (!sPassword) {
            message.showError('密码不能为空');
            return
        }

        if (sPassword.length < 6 || sPassword.length > 20) {
            message.showError('密码长度需要在6-20之间');
            return
        }

        let status = $("input[type='checkbox']").is(':checked');

        // 构造参数
        let sData = {
            'user_account': sUsername,
            'password': sPassword,
            'remember': status,
        };

        $.ajax({
            url: '/user/login/',
            type: 'POST',
            data: JSON.stringify(sData),
            contentType: 'application/json;charset=utf-8',
            dataType: 'json',

        })
        // 成功回调
            .done(function (res) {
                if (res.errno === '0') {
                    message.showSuccess('恭喜你，登录成功');
                    setTimeout(function () {
                        window.location.href = '/';
                    }, 1500)

                } else {
                    message.showError(res.errmsg)
                }
            })

            // 失败回调
            .fail(function () {
                message.showError('服务器超时，请重试')
            })


    })


});

