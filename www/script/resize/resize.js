function resize() {
	$('.slide-div').height(window.innerHeight - 100);
	$("#screen-container").slidesjs.width = window.innerHeight;
	// console.log('resize ' + window.innerHeight);
}

$(window).resize(function() {
	resize();
});

$(function(){
	resize();
});
