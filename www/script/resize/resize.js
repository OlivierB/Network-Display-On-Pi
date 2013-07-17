/**
 * Handle the resize of the slide container to keep a ,full screen without scroll, page.
 * @author Matrat Erwan
 **/

function resize() {
	$('.slide-div').height(window.innerHeight - 100);
	$("#screen-container").slidesjs.width = window.innerHeight;
}

// callback on the resize of the window
$(window).resize(function() {
	resize();
});

// call the function once the window is load
$(function(){
	resize();
});
