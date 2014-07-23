var isOnion = false;
function get_new_link(){
	return $.getJSON("/get_link", function(data){
		$("#post").text(data['title']);
		isOnion = data['onion'];

	});
}
$(document).ready(function() {
	$( ".button" ).hover(
	function() {
		$(this).css( "background-color" ,"yellow");
	}, function() {
		$(this).css( "background-color" ,"blue");
	}
	);
	$( "#left" ).click(function(){
		if (isOnion == true)
			$("#title").text('onion');
		else{
			$("#title").text('Real');
		}
	});
	$( "#right" ).click(function(){
		if (isOnion == true)
			$("#title").text('onion');
		else{
			$("#title").text('Real');
		}
	});
});
get_new_link();