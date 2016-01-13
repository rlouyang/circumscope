$('.form').find('input, textarea').on('keyup blur focus', function (e) {
    var $this = $(this),
    label = $this.prev('label');

    if (e.type === 'keyup') {
		if ($this.val() === '') {
            label.removeClass('active highlight');
        } 
        else {
            label.addClass('active highlight');
        }
    } 
    else if (e.type === 'blur') {
    	if ($this.val() === '') {
    		label.removeClass('active highlight'); 
		} 
		else {
		    label.removeClass('highlight');   
		}   
    } 
    else if (e.type === 'focus') {
        if ($this.val() === '') {
    		label.removeClass('highlight'); 
		} 
        else if ($this.val() !== '') {
		    label.addClass('highlight');
		}
    }
});

/*----------------------------------------------------*/
/* Adjust Primary Navigation Background Opacity
------------------------------------------------------*/
$(window).on('scroll', function() {
    var h = $('#siteNav').height();
    var y = $(window).scrollTop();
    var header = $('#siteNav');
    var active = $('.active');
    
    if ((y > h + 20) && ($(window).outerWidth() > 768)) {
        header.addClass('opaque');
    }
    else {
        if (y < h + 20) {
            header.removeClass('opaque');
        }
        else if ($(window).outerWidth() > 768) {
            header.addClass('opaque');
        }
    }
});

// Display loading gif when you submit form
function startLoading() {
    $("form").hide();
    $(".search").hide();
    $(".loading").show();
    $(".footer-text").html("");
}