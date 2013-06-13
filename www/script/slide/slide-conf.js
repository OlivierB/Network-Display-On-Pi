$(function(){
	$("#slides").slidesjs({
		width: 940,
		height: 600,
		start: 4,
		play: {
			active: true,
	        // [boolean] Generate the play and stop buttons.
	        // You cannot use your own buttons. Sorry.
	        effect: "slide",
	        // [string] Can be either "slide" or "fade".
	        interval: 5000,
	        // [number] Time spent on each slide in milliseconds.
	        auto: false,
	        // [boolean] Start playing the slideshow on load.
	        swap: false,
	        // [boolean] show/hide stop and play buttons
	        pauseOnHover: false,
	        // [boolean] pause a playing slideshow on hover
	        restartDelay: 2500
	        // [number] restart delay on inactive slideshow
	    },
	    navigation: false
	});


	$(window).keyup(function(e){
        var key = e.which | e.keyCode;
        if(key === 37){ // 37 is left arrow
            $('.slidesjs-previous').click();
        }
        else if(key === 39){ // 39 is right arrow
            $('.slidesjs-next').click();
        }
    });
});


