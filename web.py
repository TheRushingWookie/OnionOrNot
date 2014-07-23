import praw
from flask import Flask, send_from_directory
from flask import Response
from random import randrange
import json
app = Flask(__name__,static_url_path='')

r = praw.Reddit(user_agent='OnionOrNot')
not_submissions = r.get_subreddit('nottheonion').get_top_from_month(limit=150)
stupid_submissions =  r.get_subreddit('NewsOfTheStupid').get_top_from_month(limit=150)
onion_submissions = r.get_subreddit('theonion').get_top_from_month(limit=300)
not_submissions = [link.title for link in stupid_submissions] + [link.title for link in not_submissions]
onion_submissions = [link.title for link in onion_submissions if "onion" not in link.title and "Onion" not in link.title]

@app.route("/get_link")
def get_link():
	onion = randrange(2)
	if onion == 0:
		return json.dumps({"title": onion_submissions[randrange(len(onion_submissions))].encode('utf-8'),'onion' : True})
	else:
		return json.dumps({"title": not_submissions[randrange(len(not_submissions))].encode('utf-8'),'onion' : False})
@app.route("/getLinks.js")
def getLinks():
	return """var isOnion = false;
function get_new_link(){
	return $.getJSON("/get_link", function(data){
		$("#post").text(data['title']);
		isOnion = data['onion'];
		$("#title").text('?');
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
	});
	$( "#right" ).click(function(){
		if (isOnion == true)
			$("#title").text('onion');
		else{
			$("#title").text('Real');
		}
	});
	$( "#next" ).click(function(){
		get_new_link();
	});
});
get_new_link();"""
@app.route("/style.css")
def getCss():
	return Response(""".centered {
    margin-left: auto;
    margin-right: auto;
    width: 70%;
    background-color: #b0e0e6;
    text-align: center;
    font:normal large verdana,arial,helvetica,sans-serif;z-index:1;min-height:100%;
}
.wrap {
   width:600px;
   margin:0 auto;
}
#left {
    float: left;
    width: 50%;
    text-align: center
}

#right {
    margin-left: 50%;
    text-align: center
}""", mimetype="text/css")
@app.route("/")
def home():
	return """<!DOCTYPE HTML>
<html lang="en-US">
    <head>
    	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script>
        <script src="/getLinks.js"></script>
        <link rel="stylesheet" type="text/css" href="/style.css">
    </head>
    <body>
    	<div class="centered", id="title"> Title </div>
    	<div> &nbsp;</div>
    	<div> &nbsp;</div>
    	<div> &nbsp;</div>
        <div> &nbsp;</div>
        <div> &nbsp;</div>
        <div> &nbsp;</div>
    	<div class="centered" id="post"></div>
        <div> &nbsp;</div>
        <div> &nbsp;</div>
        <div class="wrap">
            <div class="button" id="left"> Onion</div>
            <div class="button" id="right"> Real Life</div>
        </div>
         <div> &nbsp;</div>
          <div> &nbsp;</div>
        <div class="centered button" id="next">Next</div>
    </body>
</html>"""
if __name__ == "__main__":
    app.run(debug=True)