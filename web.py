import praw
from flask import Flask, request
from flask import Response
from random import randrange
from Queue import PriorityQueue
import feedparser
import json
from threading import Thread
import time
app = Flask(__name__)
onion_submissions = []
not_submissions = []
#not_submissions = [(u'Kentucky State Senator: Mars Has the Same Temperature as Earth, so Climate Change is a Hoax', u'http://www.patheos.com/blogs/friendlyatheist/2014/07/07/kentucky-state-senator-mars-has-the-same-temperature-as-earth-so-climate-change-is-a-hoax/'), (u"Texas judge busted for drunk driving pleads for special treatment: 'You are going to ruin my life'", u'http://www.nydailynews.com/news/crime/texas-judge-busted-drunk-driving-pleads-special-treatment-article-1.1867241'), (u'Russian religious groups seek ban on \u2018blasphemous\u2019 Marilyn Manson, apparently unaware of what decade it is.', u'http://www.patheos.com/blogs/friendlyatheist/2014/06/23/russian-religious-groups-seek-ban-on-blasphemous-marilyn-manson/'), (u'Thief Forgets To Log Off Facebook After Burglarizing Home', u'http://minnesota.cbslocal.com/2014/06/23/thief-forgets-to-log-out-of-facebook-after-burglarizing-home/'), (u'Pat Robertson tells mother: Your son\u2019s stomach pains are caused by a witch ancestor', u'http://www.rawstory.com/rs/2014/07/14/pat-robertson-tells-mother-your-sons-stomach-pains-are-caused-by-a-witch-ancestor/'), (u'VA offers appointment to man 2 years after he dies', u'http://www.detroitnews.com/article/20140701/NATION/307010053/1361/VA-offers-appointment-to-man-2-years-after-he-dies'), (u'Christian motivational speaker who says \u201cdateable girls know how to shut up\u201d arrested for public intoxication', u'http://www.salon.com/2014/06/26/christian_motivational_speaker_who_says_dateable_girls_know_how_to_shut_up_arrested_for_public_intoxication/'), (u'Minnesota Archbishop Who Denounces Homosexuality Now Being Investigated for Having Sex with Priests', u'http://www.patheos.com/blogs/friendlyatheist/2014/07/02/minnesota-archbishop-who-denounces-homosexuality-now-being-investigated-for-having-sex-with-priests/'), (u'Shia LaBeouf Spat at Police Officer, Yelled: "Do You Know Who the F--k I Am?"', u'http://www.usmagazine.com/celebrity-news/news/shia-labeouf-spat-at-police-officer-yelled-do-you-know-who-i-am-2014276?utm_medium=twitter&amp;utm_source=twitterfeed'), (u"Tip: if you club your husband on the head several times, zap him with a stun gun, then suffocate him with plastic wrap, don't expect cops to believe you when you claim he killed himself.", u'http://www.rawstory.com/rs/2014/07/13/police-charge-ohio-woman-with-murder-in-husbands-bizarre-suicide-by-plastic-wrap/'), (u'Kanye West does not read books or respect them but nevertheless he has written one that he would like you to buy and read.', u'http://www.reuters.com/article/2009/05/26/us-kanyewest-idUSTRE54P5L820090526'), (u"Statements surfacing from Georgia House candidate express that Islam doesn't deserve First Amendment protection because it's not a religion, women can run for office as long as it's okay with their husband, and young people are being converted to homosexuality", u'http://www.msnbc.com/msnbc/gop-jody-hice-islam-doesnt-deserve-first-amendment-protections'), (u'American Apparel sorry for using Challenger disaster photo in their 4th of July post', u'http://www.chicagotribune.com/news/chi-american-apparel-sorry-for-using-challenger-disaster-photo-20140704,0,2892263.story'), (u'Israelis gather on hillsides to watch and cheer as military drops bombs on Gaza. People drink, snack and pose for selfies against a background of explosions as Palestinian death toll mounts in ongoing offensive.', u'http://www.theguardian.com/world/2014/jul/20/israelis-cheer-gaza-bombing'), (u'Comatose Man Dies After Policemen Try to Check Him in As Luggage on Flight', u'http://www.themoscowtimes.com/news/article/man-dies-after-policemen-try-to-check-him-in-as-luggage/502280.html'), (u"Texas judge busted for drunk driving pleads for special treatment: 'You are going to ruin my life'", u'http://www.nydailynews.com/news/crime/texas-judge-busted-drunk-driving-pleads-special-treatment-article-1.1867241'), (u'New San Francisco billboard warns workers they\u2019ll be replaced by iPads if they demand a fair wage', u'http://pando.com/2014/07/17/new-san-francisco-billboard-warns-workers-theyll-be-replaced-by-ipads-if-they-demand-a-fair-wage/'), (u'Republican candidate is convinced his opponent is dead and using a body double as a stand-in', u'http://www.dailykos.com/story/2014/06/27/1310026/-Republican-candidate-is-convinced-his-opponent-is-dead-and-using-a-body-double-as-a-stand-in?detail=facebook'), (u'Target security officer fired after reporting shoplifting', u'http://www.washingtonpost.com/local/target-security-officer-fired-after-reportingshoplifting/2014/07/10/f3d6f606-0854-11e4-bbf1-cc51275e7f8f_story.html'), (u"Reporter stopped by TSA agent who didn't know District of Columbia is in US", u'http://www.wftv.com/news/news/local/orlando-tsa-agents-getting-geography-refresher/ngfmH/'), (u"Police officer shoots 'aggressive' tortoise dead", u'http://www.independent.ie/world-news/africa/police-officer-shoots-aggressive-tortoise-dead-30419096.html'), (u'Rhode Island accidentally decriminalized prostitution, and good things happened', u'http://www.vox.com/2014/7/15/5898187/prostitution-rhode-island-decriminalized'), (u'Homelessness now a crime in cities throughout the U.S.', u'http://www.pbs.org/newshour/rundown/homelessness-now-crime-cities-throughout-u-s/'), (u'Man Who Took Poverty Vow Wins $259.8M Powerball Jackpot', u'http://abcnews.go.com/US/man-poverty-vow-wins-2598m-powerball-jackpot/story?id=24427490'), (u"Pornhub pleads with users to stop uploading videos of Brazil 'getting f**ked by Germany' in the World Cup", u'http://www.nationalheadlines.co.uk/pornhub-pleads-with-users-to-stop-uploading-videos-of-brazil-getting-fked-by-germany-in-the-world-cup/396249/'), (u'French boy, 12, fakes own kidnapping to avoid going to dentist', u'http://www.nydailynews.com/news/world/boy-fakes-kidnapping-avoid-dentist-article-1.1838046'), (u'Russia spotted editing Wikipedia page about downed Malaysia Airlines jet', u'http://www.theverge.com/2014/7/18/5917099/russia-spotted-editing-wikipedia-page-of-downed-malaysia-air-jet'), (u'Man Raises $10,000 on Kickstarter to Make a Bowl of Potato Salad (UPDATE: Make that $23,000)', u'http://www.slate.com/blogs/moneybox/2014/07/07/potato_salad_on_kickstarter_the_project_has_raised_more_than_9_000.html'), (u'Man Sues Airline After Landing in Grenada Instead of Granada', u'http://www.nbcnews.com/business/travel/man-sues-airline-after-landing-grenada-rather-granada-n138026'), (u'You are more likely to be bitten by Luis Suarez (1 in 2,000) than a shark (1 in 3,700,000)', u'http://www.newstatesman.com/future-proof/2014/06/you-are-more-likely-be-bitten-luiz-suarez-1-2000-shark-1-3700000')]
#onion_submissions = [(u'Everyone In Middle East Given Own Country In 317,000,000-State Solution', u'http://www.theonion.com/articles/everyone-in-middle-east-given-own-country-in-31700,36484/'), (u'Report: Shame Of Walking Out Without Buying Anything Drives 90% Of Purchases At Small Businesses', u'http://www.theonion.com/articles/report-shame-of-walking-out-without-buying-anythin,36357/'), (u'Breaking: LeBron James Leaning Toward Joining Al-Qaeda', u'http://www.theonion.com/articles/breaking-lebron-james-leaning-toward-joining-alqae,36417/'), (u'George R. R. Martin Kills Off Whole Family', u'http://www.theonion.com/articles/george-r-r-martin-kills-off-whole-family,32767/'), (u'Coworker with two computer screens not fucking around', u'http://www.theonion.com/articles/coworker-with-two-computer-screens-not-fucking-aro,29151/'), (u'LeBron to Announce Decision at United Nations', u'http://www.newyorker.com/online/blogs/borowitzreport/2014/07/lebron-to-announce-decision-at-united-nations.html?utm_source=tny&amp;utm_campaign=generalsocial&amp;utm_medium=facebook&amp;mbid=social_facebook'), (u'Pool Owner Has Bathing Suit That Touched His Penis You Can Borrow', u'http://www.theonion.com/articles/pool-owner-has-bathing-suit-that-touched-his-penis,33222/?utm_source=Facebook&amp;utm_medium=SocialMarketing&amp;utm_campaign=LinkPreview:NA:InFocus'), (u'Report: Majority Of UFO Abductions Committed By Alien That Person Knows', u'http://www.theonion.com/articles/report-majority-of-ufo-abductions-committed-by-ali,36499/'), (u'LeBron James Guarantees Cleveland Will Win Numerous Regular Season Games', u'http://www.theonion.com/articles/lebron-james-guarantees-cleveland-will-win-numerou,36446/'), (u'Palestinians Starting To Have Mixed Feelings About Being Used As Human Shields', u'http://www.theonion.com/articles/palestinians-starting-to-have-mixed-feelings-about,36497/?utm_source=Twitter&amp;utm_medium=SocialMarketing&amp;utm_campaign=Default:2:Default'), (u'Are We Setting Unrealistic Standards Of Beauty For Our Felons?', u'http://www.clickhole.com/article/are-we-setting-unrealistic-standards-beauty-our-fe-371'), (u'Nation Wondering Why Struggling Mental Health System Can\u2019t Just Pull Itself Together', u'http://www.theonion.com/articles/nation-wondering-why-struggling-mental-health-syst,36318/'), (u'New PS4 Feature Allows User To Close Eyes And Imagine Really Fun Game', u'http://www.theonion.com/video/new-ps4-feature-allows-user-to-close-eyes-and-imag,36251/'), (u'Man Confused By Compliment From Person Whose Career He Can\u2019t Help', u'http://www.theonion.com/articles/man-confused-by-compliment-from-person-whose-caree,36439/'), (u'Every Way The U.S. Can Advance In The World Cup', u'http://www.clickhole.com/article/every-way-us-can-advance-world-cup-359'), (u'The 7 Coolest Creatures Brought To Life By Andy Serkis', u'http://www.clickhole.com/article/7-coolest-creatures-brought-life-andy-serkis-503'), (u'Suicide Letter Full Of Simpsons References', u'http://www.theonion.com/articles/suicide-letter-full-of-simpsons-references,1717/'), (u'LeBron James: "I\u2019m Not Afraid Of Losing In Cleveland; I\u2019m Only Afraid Of Jumping Into The Air For A Slam Dunk And Never Coming Down"', u'http://www.clickhole.com/blogpost/im-not-afraid-losing-cleveland-im-only-afraid-jump-517'), (u'\u2018It\u2019s Real Easy,\u2019 Declares IT Guy About To Speak Incoherently For Next 30 Seconds', u'http://www.theonion.com/sponsored/its-real-easy-declares-it-guy-about-to-speak-incoh,109/'), (u'Humanity Surprised It Still Hasn\u2019t Figured Out Better Alternative To Letting Power-Hungry Assholes Decide Everything', u'http://www.theonion.com/articles/humanity-surprised-it-still-hasnt-figured-out-bett,36361/'), (u'British Royal Family Places Queen Elizabeth In Nursing Home', u'http://www.theonion.com/articles/british-royal-family-places-queen-elizabeth-in-nur,36429/'), (u'\u2018To Defeat Them, I Must Become Them,\u2019 John Kerry Says While Putting On Black Face Mask', u'http://www.theonion.com/articles/to-defeat-them-i-must-become-them-john-kerry-says,36356/')]
def update_submissions():
	global onion_submissions, not_submissions
	onion_feed = feedparser.parse("feed://feeds.feedburner.com/theonion/daily?fmt=xml&max-results=100")
	r = praw.Reddit(user_agent='OnionOrNot')
	temp_not_submissions = r.get_subreddit('nottheonion').get_top_from_month(limit=150)
	stupid_submissions =  r.get_subreddit('NewsOfTheStupid').get_top_from_month(limit=150)
	temp_not_submissions = [(link.title, link.url) for link in stupid_submissions] + [(link.title, link.url) for link in temp_not_submissions]
	temp_onion_submissions = r.get_subreddit('theonion').get_top_from_month(limit=275)
	temp_onion_submissions = [(link.title, link.url) for link in temp_onion_submissions] + [(post.title, post.link) for post in onion_feed['entries']]
	onion_submissions = temp_onion_submissions
	not_submissions = temp_not_submissions
def timer(n):
    while True:
    	update_submissions()
        time.sleep(n)
update_submissions()
t = Thread(target=timer, args=(10,))
t.start()
@app.route("/get_link")
def get_link():
	onion = randrange(2)
	if onion == 0:
		submission = onion_submissions[randrange(len(onion_submissions))]
		return json.dumps({"title": submission[0].encode('utf-8'),'onion' : True,
							"link" : submission[1]})

	else:
		submission = not_submissions[randrange(len(not_submissions))]
		return json.dumps({"title": submission[0].encode('utf-8'),'onion' : False,
							"link" : submission[1]})
scores = PriorityQueue(5)
for i in range(5):
	scores.put([0,""])
@app.route("/get_scores")
def getScores():
	return json.dumps(scores.queue)
@app.route("/set_score")
def setScores():
	global scores
	score = int(request.args.get("score"))
	print int(score)
	author = request.args.get("author")
	if scores.full():
		scores.get()
	scores.put([score,author])
	print scores
	return ""

@app.route("/getLinks.js")
def getLinks():
	return """var isOnion = false;
var submission = ""
function get_new_link(){
	return $.getJSON("/get_link", function(data){
		$("#post").text(data['title']);
		submission = data;
		isOnion = data['onion'];
		$("#title").text('?');
		$("#link").text("")
		scored = false
	});
}
var score = 0
var scored = false
function incfScore(){
	if (scored == false)
	{
		score += 1
		$("#score").text("Current Streak: " + score)
		scored = true
	}
}
function resetScore(){
	if (scored == false)
	{
		get_highscores().done(function (){
		render_highscores();
		score = 0
		$("#score").text("Current Streak: " + score)
		scored = true
		});
	}
}
function get_highscores(){
	return $.getJSON("/get_scores", function(data){
		for(i = 0; i < data.length;i++){
		console.log(data[i][0])
		console.log(score)
			if(score > data[i][0]){
				name = prompt("You got a highscore! Enter your name.","");
				set_score(score, name);
				break;
			}
		}
	});
}
function render_highscores(data){
	$.getJSON("/get_scores", function(data){
		html = ""

		for(i = 0; i < data.length;i++){
			if(data[i][0] > 0){
				html += "<p>" + data[i][1] + " Score: " + data[i][0] + "</p>"
				}

		}
		$("#board").html(html)
	});
}
function set_score(score, author)
{
	$.get("/set_score",{"score": score, "author" : author})
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
		{
			$("#title").text('You got it! Its from the onion.');
			incfScore()
		}
		else{
			$("#title").text('Nope, its real.');
			resetScore()
		}
		$("#link").attr("href", submission["link"])
		$("#link").text("Story")
	});
	$( "#right" ).click(function(){
		if (isOnion == true)
		{
			$("#title").text('Nope, its from the onion');
			resetScore()
		}
		else{
			incfScore()
			$("#title").text('Yup, real');
		}
		$("#link").attr("href", submission["link"])
		$("#link").text("Story")

	});
	$( "#next" ).click(function(){
		get_new_link();
	});
});
render_highscores();
get_new_link();"""
@app.route("/style.css")
def getCss():
	return Response(""".centered {
	margin-left: auto;
	margin-right: auto;
	width: 70%;
	text-align: center;
	font:normal large verdana,arial,helvetica,sans-serif;z-index:1;min-height:100%;
}
.wrap {
   width:600px;
   margin:0 auto;
}
.button {
	text-align: center;
	border: 1px solid;
	border-radius: 10px;
}
#left {
	float: left;
	width: 33%;
	text-align: center
}
#right {
	margin-left: 66%;
	text-align: center
}
#scoreboard {
	font:normal large verdana,arial,helvetica,sans-serif;z-index:1;min-height:100%;
	width:80%;
	margin:0 auto;
}
#next {
	width: 10%;
	margin-left: 45%;
}
#background {
	width: 50%;
	margin-left:25%;
}
#score {
	float: left;
	width: 50%

}
#highscoreboard {
	margin-left: 66%;
	width: 50%

}
""", mimetype="text/css")
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
		<div id="background">
			<div> &nbsp;</div>
			<div class="centered"> Onion or not? </div>
			<div class="centered", id="title"> Title </div>
			<div id="scoreboard">
				<div id="score"> Current Streak: 0 </div>
				<div id="highscoreboard">
					<p>High Scores<p>
					<div id="board">
					</div>
				</div>
			</div>
			</div>
			<div> &nbsp;</div>
			<div> &nbsp;</div>
			<div> &nbsp;</div>
			<div> &nbsp;</div>
			<div> &nbsp;</div>
			<div class="centered" >
				<a id="link" href=""></a>
			</div>
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
		</div>
	</body>
</html>"""
if __name__ == "__main__":
	app.run(debug=True)