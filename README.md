# Setup
## Step one
Start by cloning this repository onto your machine.
## Step two
Navigate to your local repository

>pip install -r requirements.txt

## Step three
Seed the database
One way to do this: run ipython in the terminal
> ipython

> run seed.py

This may take a moment.

# Capstone One: Moviebuster
## Schema Selection
You can find the DB Schema under the csv folder. Within, there's a few files:
1. A raw CSV containing movie titles, years, and their associated IMDB_ID's (More on this later)
2. A Jupyter notebook titled "readFile.ipynb". This is a test file that demonstrates various API calls. You can see the process underwent from top to bottom, taking incremental steps toward solving the 'problem' of how to get the data we need for our game. (More on this later as well!)
3. A png titled "Capstone_Schema.png". This is an image of a DB Schema. Some data on this is subject to change, depending on where our goalpost is ultimately set.

### CSV
What is a CSV? A comma separated value sheet is similar to a spreadsheet. A raw CSV on its own isn't very pretty, but they're useful files in that they're easy to parse and easy to view using tools like Excel, Github, or even extensions on VSC. Our CSV is only moderately trimmed, and ultimately is really only needed for one piece of data depending on how we utilize our API. The piece of data I've chosen to work with is the IMDB ID. IMDB has a rich API that can be searched with their ID system. IMDB ID's are formatted like this: tt1711425.

### API
The API being used for this project is the OMDB api. This particular API comes with a fair share of limitations, which we can absolutely work around!
1. There is no search option that allows you to grab multiple movies without first entering a search paramater by title. Our project requires us to grab movies in as much of a randomized process as possible, with two major thoughts in mind:
    A: I want this game to be fun. If it's highly predictable, it isn't fun.
    B: I want our solution to be functional. While it is possible to make searches that offer multiple results, they are highly restricted. For instance, you could make a search for movies with the word "batman" in it, and you would receive back every film with the name batman in it. Functionally this works, but is extremely restrictive. How could we use that system to our advantage? It would be quite difficult.
2. Making a search essentially requires one of two things: a title, or an IMDB ID. Thankfully, there are several CSV's that contain both information. For our purposes, we are going to use the IMDB ID in order to grab the data we need (Title, description, and rotten tomatoes score). We *could* grab numerous CSV's, to expand our results, giving us far more films, but this comes with a few drawbacks. The primary drawback is time. We could grab several CSV's, but there may be overlap, and if there's overlap, our data will need to be cleaned, which may get messy. What if the data is not arranged the same way, despite giving similar data? This is obtainable, but time consuming. As this app exists more as a proof of concept, we won't be delving that deelpy into it.
3. We can't filter results by whether a rotten tomatoes score exists. This means we will have to do some validation in order to ensure the data we get matches our needs.

### Further Improvements
The possibility for improving the site are endless:
1. Pretty it up. Make it look good; currently it isn't pretty to look at, and lacks any accessbility features (ex. Dark theme / light theme)
2. Implement a leaderboard that refreshes live.
3. Add fonts to different films by genre. There are hundreds of free film fonts (think Harry Potter's font from the movie series), it would be cool to assign a page a font based on what genre it is, or even based on which film it is (which would be substantially more challenging).
4. Implement the ability to give a score, or a review, to films as you play.
5. Add difficulty settings. Easy mode might let you select from a list of films to play with.Medium mode might include the title of a film, as well as the year of its release, for example.
6. Data visualizations. It would be cool if, after providing an answer, you could get a statistic that displays how often people get an answer correct. For example, we could display the title and the data on how often people are correct, as well as how many people have attempted to guess the score of that particular movie.
7. Adding a "Level Up!" system -> Think of gaining points and achieving "ranks" -> Player starts at 0 points with a rank of "Private" -> Reaches 10 points and "graduates" to the next rank, "Private second class" -> later on gets more points, becomes corporal, sergeant, etc. Rank names would be pending, of course, I'd rather they be movie related in some way, rather than military related.
