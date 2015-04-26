$(document).ready(function(){
	$(".float-left").hover(function(){
		$(this).animate({fontSize:'150%'});
	},function(){
		$(this).animate({fontSize:'0%'});
	});
});