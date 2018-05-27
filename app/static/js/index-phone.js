;$(function () {

    var sidebar = $('#sidebar');
    var mask = $('.mask');
    var sidebar_trigger = $('#sidebar_trigger');
    var sidebar_ul = $("#sidebar-ul");


    sidebar_trigger.on('click',function () {
        mask.fadeIn();
        sidebar.animate({right:0});
    })
    mask.on('click', function () {
        mask.fadeOut();
        sidebar.animate({right:-sidebar.width()-20});
    })
    sidebar_ul.on('click', "li", function () {
        $(this).css('background','#000');
        $(this).css('color','#fff');
        $(this).find('a').css('color','#fff');
        $(this).find('i').css('color','#fff');
        console.log($(this).find('a').attr('href'));
        window.location.href = $(this).find('a').attr('href');
    })


    //draw.css({'height':sidebar.css('height'), 'width':sidebar.css('width')});
    //console.log('height:' + draw.css('height'));

})