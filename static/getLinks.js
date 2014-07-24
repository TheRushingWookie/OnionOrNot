var isOnion = false;
function get_new_link(){
	return $.getJSON("/get_link", function(data){
		$("#post").text(data['title']);
		isOnion = data['onion'];
		$("#title").text('?');
	});
}
function get_highscores(){
	return $.getJSON("/get_scores", function(data){
		$("#board").html(data["scores"]);
	});
}
$(document).ready(function() {
	$( ".button" ).hover(
	function() {
		$(this).css( "background-color" ,"yellow");
	}, function() {
		$(this).css( "background-color" ,"white");
	}
	);
	$( "#left" ).click(function(){
		if (isOnion == true)
			$("#title").text('onion');
		else{
			$("#title").text('Real');
		}
		get_new_link()
	});
	$( "#right" ).click(function(){
		if (isOnion == true)
			$("#title").text('onion');
		else{
			$("#title").text('Real');
		}
		get_new_link()
	});
	$( "#next" ).click(function(){
		get_new_link();
	});
});
get_highscores();
get_new_link();