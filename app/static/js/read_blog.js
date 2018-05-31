
$('#sidebar_trigger').on('click',function () {
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
    $(test).css("color", "#333333");
}
function mouseOut(obj){
    var test = obj;
    $(test).css("color", "#5C5C5C");
}
function mouseOut2(obj){
    var test = obj;
    $(test).css("color", "#bbb");
}

