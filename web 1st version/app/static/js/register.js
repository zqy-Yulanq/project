$(function(){
    $("#registerbtn").click(function (event) {
        event.preventDefault();
        var username_input = $("input[name='username']");
        var telephone_input = $("input[name='telephone']");
        var password_input = $("input[name='password1']");
        var email_input = $("input[name='email']");

        var username = username_input.val();
        var telephone = telephone_input.val();
        var password = password_input.val();
        var email = email_input.val();


        zlajax.post({
            'url': '/register/',
            'data': {
                'username': username,
                'telephone': telephone,
                'password': password,
                'email': email
            },
            'success': function (data) {
                if(data['code'] == 200){
                    window.location = '/login/';
                }
                else{
                    window.location = '/register/';
                }
            }
        });
    });
});