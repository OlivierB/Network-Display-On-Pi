/**
 * Handle the resize of the slide container to keep a ,full screen without scroll, page.
 * @author Matrat Erwan
 **/

function resize() {
	$('.slide-div').height(window.innerHeight - 100);
	$("#screen-container").slidesjs.width = window.innerHeight;
	$('.height-half').height((window.innerHeight - 120)/2);
	$('.height-full').height((window.innerHeight - 110));
}

// callback on the resize of the window
$(window).resize(function() {
	resize();
});

// call the function once the window is load
$(function(){
	resize();
});
