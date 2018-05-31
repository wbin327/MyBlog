;$(function () {

    $('#sidebar_trigger').on('click',function () {
        $('aside').show();
        $('#header').hide();
        $('.mask').fadeIn();
        $('#sidebar').animate({right:0});
    })
    $('.mask').on('click', function () {
        $('#header').show();
        $('.mask').fadeOut();
        $('#sidebar').animate({right:-$('#sidebar').width()-20});
    })
    $("#sidebar-ul").on('click', "li", function () {
        $(this).css('background','#000');
        $(this).css('color','#fff');
        $(this).find('a').css('color','#fff');
        $(this).find('i').css('color','#fff');
        console.log($(this).find('a').attr('href'));
        window.location.href = $(this).find('a').attr('href');
    })

    $('.left_sidebar').on('mousemove','a',function(){
        $(this).css('background','#C62F2F');
        $(this).css('color','#fff');
    })
    $('.left_sidebar').on('mouseout','a', function () {
        $(this).css('background','#fff');
        $(this).css('color','#000');
    })

    function mouseIn(obj){
        var test = obj;
        $(test).css("color", "#000");
    }
    function mouseOut(obj){
        var test = obj;
        $(test).css("color", "#9d9d9d");
    }

    function searchBlog(){
        var condition = $("#condition").val();
        console.log(condition);
        $.ajax({
            type : "post",
            dataType: "json",
            url : "/blog/search_blog",
            data : {
                "condition" : condition,
            },
            async : false,  //同步处理
            success : function(data, status) { //这里的status是ajax自己的参数，请求成功就success
                if(data.status){
                    //删除子元素
                    $("#related_blog").empty();
                    $(".page").hide();
                    for (i=0;i<data.data.length;i++){
                        var text=
                            '<div class="related_blog">'+
                                '<a href="/blog/read_blog/'+data.data[i].id+'">' +
                                       '<div class="first_line">' +
                                           '<span class="title">'+data.data[i].title+'</span>' +
                                       '</div>'+
                                       '<div class="second_line">'+
                                           '<span class="type">'+data.data[i].type+'</span>'+
                                           '<div class="read_count">'+
                                               '<i class="fa fa-book" aria-hidden="true"></i>'+data.data[i].read_count+''+
                                           '</div>'+
                                           '<span class="update_time">'+data.data[i].update_time+'</span>'+
                                       '</div>'+
                                   '</a>'+
                            '</div>'+
                            '<hr/>';
                        $("#related_blog").append(text);
                    }

                }else{
                   toastr.error(data.msg);
                }
            }
         });
    }
})

