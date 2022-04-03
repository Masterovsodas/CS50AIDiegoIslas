# Soos' Mystery!
#### Video Demo:  <https://studio.youtube.com/video/r0WtygM26pA/edit>
#### Description:
Soos' mystery is an online flask application which employs python, HTML, CSS, and SQLite3 in order to create an interactive and thematic website.
In this application the user is tasked with analyszing interviews and deciphering cryptograms in order to uncover the mystery of who stole Soos' cart.
In order to do so they must think critically about the story and learn to serpate themselves and their reasoning from the narrator, they must analyze web pages
closely and find secrets that propagate new information or give a new angle for the user to think / solve from. In the end from interviews and ciphers alone, they must deduce who the
criminal is and who helped them steal the cart. Along the way, much misleading information and emotions are put into the story in order to create the afforemetioned sense of
independace within the user as well as challenge the user's logic and suggestability, making the game more psychologically difficult and complex than one with simple hard evidence would.
Over the course of the game, the user is given their own tab in which to note logs, these logs are saved via SQL and are useful for recording the events of the story, opinions, and cryptograms.
Once the user has deduced the criminals, they can go to the ACCUSE tab and fill in the 3 pieces of information required to win the game. If they are wrong they lose, no second chances!
Only a username is required to log into the site, since there are many secret usernames with creative and and comical logs, registered as secrets. These secrets are used to
reward the player for thurough gameplay, bright observation, adn critical thinking. The story is meant to be comedic and easy to follow, whilst creating a more sinister
narrative between the lines, this I feel gives the game a sense of depth and deception which can give the user a sense of satisfaction upon seeing through it and
delving into the depths of the events that are truly at hand in the story. Each character is unqie with their own persoanlity, genrally adapted from the show or media they
were adopted form in this project, this creates variaety and an absrud atmosphere which many may find entertaining.

That is a brief but well-rounded overview of my project, the rest is further illustrated in my video.
This was CS50!!
Thank you!

The following script illustrates the above sinopsis in furthest detail:

Hey guys, My name is Diego, I am in British Columbia, Canada and this is my CS50 final project, Soos’ mystery, inspired by the pset 7 problem, fiftyville.This is a simple mystery solving application made using Flask, wherein the user must analyze a set of interviews and decipher simple cryptograms in order to discover who was responsible for stealing the golf cart of Soos, our main character.
Alright, so in order to login, a user can either login to the account of a preexisting user just by typing their name, an account containing a secret the names of which can be found throughout the game, or their own account via the creation of a new username or the repetition of one they made before.
This leads us to our first puzzle, finding the site’s secret password. Here we get a hint telling us to try something random, so let's do that. Now we get an apology prompt, we need to know this character’s name. If you’ve watched gravity falls or looked at the website icon, you know that this dude right here is Soos, so we can try that as our password. And now we see that we have successfully logged in!
Okay so here we have our logs tab, this area is essentially for the user to record their notes on the story which are saved via a SQLite3 database but must be saved using this yellow button here before leaving the page. In the navbar up top we can see 4 links to data on our prime suspects and a tab to make our final accusation. Anyway, let's go see what Eric Cartman has to say.
Okay so this is the general format of the story blocks in the site, they're set up like an interview with Soos asking all of the questions, where the user is supposed to read between the lines in order to make connections and develop conclusions. As we scroll we see the interaction progress as well as some information that sticks out regarding the situation which should probably go in our logs. But here at the bottom we see a little message that says it’s encrypted, could it be useful?
So with this piece of ciphertext, the user is then supposed to look around the site to find a way to decrypt it, or use an external source if they aren't fun. To shorten the matter, on this other page near the bottom, we can faintly see a gray question mark, when we hover over it seems to act like a button, we click it and a handy decryptor page appears! Let's put our link in the caesar cipher section. As you can see 26 results have appeared, corresponding to the 26 possible shifts of the alphabet in a caesar cipher. This one looks legible, let's paste it into our URL. And it takes us to this video that while not exactly useful, does introduce our decryption mechanic.
Eventually once a user has read through the site, they can make an accusation here. This accusation must have all 3 pieces of information or else the user loses!
Once your information is correct, you receive this screen and can return to the login area. But be sure to log back in, as you definitely missed secrets and cryptograms like this one.

Anyways, thanks for watching, this was CS50!.

