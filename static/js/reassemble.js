$(function() {

	// Function to call reassemble function using Ajax and display results.
    $('#btnOutput').click(function() {
        $.ajax({
            url: '/output',
            data: $('form').serialize(),
	    method: 'POST',
            success: function(response) {
               var list = $('<ul />'); // create UL
			   // run function and fill the UL with LI's
               $('#result').html(response)
               $(window).scrollTop($('#result').offset().top-20)
            },
            error: function(error) {
                console.log(error);
            }
        });
    });


	//To load Shake-frags in the input text area
	$('#ShImg').click(function() {
	 	jQuery.get('static/data/Shake-frags.txt', function(data) {
   			$('#inputText').val(data)
		});
	})

	//To load IpsumLorem-short-frags in the input text area
	$('#LSImg').click(function() {
	 	jQuery.get('static/data/IpsumLorem-short-frags.txt', function(data) {
   			$('#inputText').val(data)
		});
	})

	//To load IpsumLorem-med-frags in the input text area
	$('#LMImg').click(function() {
	 	jQuery.get('static/data/IpsumLorem-med-frags.txt', function(data) {
   			$('#inputText').val(data)
		});
	})

	//To load IpsumLorem-frags in the input text area
	$('#LFImg').click(function() {
	 	jQuery.get('static/data/IpsumLorem-frags.txt', function(data) {
   			$('#inputText').val(data)
		});
	})

});
