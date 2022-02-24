$(function(){
    $("#addrecordbtn").click(function (event) {
        event.preventDefault();
        var ty_input = $("select[name='tv']");
        var score_input = $("input[name='score']");
        var view_input1 = $("input[name='view_date']");
        var view_input2 = $("input[name='view_time']");
        var content_input = $("textarea[name='content']");
        var tv = ty_input.val();
        var score = score_input.val();
        var view_date = view_input1.val();
        var view_time = view_input2.val();
        var content = content_input.val();
        zlajax.post({
            'url': '/add_record/',
            'data': {
                'tv': tv,
                'score': score,
                'view_date': view_date,
                'view_time': view_time,
                'content': content
            },
            'success': function (data) {
                if(data['code'] == 200){
                    window.location = '/record';
                }
                else{
                    window.location = '/add_record/';
                }
            }
        });
    });
});