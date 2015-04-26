$(document).ready(function(){
	$("body").delay(500).animate({opacity:1});
	$(".float-left").hover(function(){
		$(this).animate({fontSize:'150%'});
	},function(){
		$(this).animate({fontSize:'0%'});
	});
});