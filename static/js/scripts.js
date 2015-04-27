$(document).ready(function(){
	$("body").delay(500).animate({opacity:1});
	$(".indexMenuItem").hover(function(){
		$(this).animate({fontSize:'150%'});
	},function(){
		$(this).animate({fontSize:'0%'});
	});
});