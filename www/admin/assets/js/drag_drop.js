	// ajoute la propriété pour le drop et le transfert de données
	$.event.props.push('dataTransfer');

	$(document).ready(function() {


	    $('*[draggable="true"]').on({
	        // on commence le drag
	        dragstart: function(e) {
	            $(this).css('opacity', '0.5');

	            // on garde le texte en mémoire (A, B, C ou D)
	            e.dataTransfer.setData('text', this.id);
	            // console.log(this)
	        },
	        // fin du drag (même sans drop)
	        dragend: function() {
	            $(this).css('opacity', '1');
	        }
	    });


	    refreshDropper();

        resizePagesContainer();
	    $(window).resize(resizePagesContainer);

	    $('#add_page').click(addPage);
	    nb_page = 5;


	});

	function refreshDropper() {
	    $('.page-dropper').on({
	        // on lâche l élément
	        drop: function(e) {
	            e.preventDefault();
	            var id = e.dataTransfer.getData('text');
	            // console.log(e.dataTransfer.getData('id'))

	            // this.html(e.dataTransfer.getData('id'))
	            // console.log(this)
	            $('#' + this.id).html($('#' + id).html());
	        },

	        dragover: function(e) {
	            e.preventDefault();
	        }
	    })
	}

	function addPage() {
	    nb_page++;
	    var html = "<div class='page thumbnail'>\
        <div class='legend_page'>Page " + nb_page + "</div>\
        <div class='page-dropper module' id='page" + nb_page + "'>\
        <img src='assets/images/default_thumbnail.png'>\
        </div>\
    </div>";
	    $('#add_page').before(html);

	    refreshDropper();
	}

    function resizePagesContainer(){
        $('#pages').height(window.innerHeight - 100);
        $('#panel').height(window.innerHeight - 100);
        console.log(window.innerHeight - 200)
    }