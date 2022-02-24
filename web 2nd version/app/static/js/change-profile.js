$(function(){
    $("#alterpasswdbtn").click(function (event) {
        event.preventDefault();
        var passwd1_input = $("input[name='passwd1']");
        var passwd2_input = $("input[name='passwd2']");

        var passwd1 = passwd1_input.val();
        var passwd2 = passwd2_input.val();
        zlajax.post({
            'url': '/alter_passwd/',
            'data': {
                'passwd1': passwd1,
                'passwd2': passwd2,
            },
            'success': function (data) {
                if(data['code'] == 200){
                    window.location = '/';
                }
                else{
                    window.location = '/alter_passwd/';
                    alert(data['message'])
                }
            }
        });
    });
});


$(function(){
    $("#alteremailbtn").click(function (event) {
        event.preventDefault();
        var email_input = $("input[name='email']");

        var email = email_input.val();
        zlajax.post({
            'url': '/alter_email/',
            'data': {
                'email': email,
            },
            'success': function (data) {
                if(data['code'] == 200){
                    window.location = '/';
                }
                else{
                    window.location = '/alter_email/';
                }
            }
        });
    });
});




$(function(){
    $("#alterusernamebtn").click(function (event) {
        event.preventDefault();
        var username_input = $("input[name='username']");

        var username = username_input.val();
        zlajax.post({
            'url': '/alter_username/',
            'data': {
                'username': username,
            },
            'success': function (data) {
                if(data['code'] == 200){
                    window.location = '/';
                }
                else{
                    window.location = '/alter_username/';
                }
            }
        });
    });
});