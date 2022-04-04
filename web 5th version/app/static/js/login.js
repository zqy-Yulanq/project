$(function(){
    $("#loginbtn").click(function (event) {
        event.preventDefault();
        var telephone_input = $("input[name='telephone']");
        var password_input = $("input[name='password']");

        var telephone = telephone_input.val();
        var password = password_input.val();


        zlajax.post({
            'url': '/login/',
            'data': {
                'telephone': telephone,
                'password': password
            },
            'success': function (data) {
                if(data['code'] == 200){
                    window.location = '/';
                }
                else{
                    window.location = '/login/';
                }
            }
        });
    });
});