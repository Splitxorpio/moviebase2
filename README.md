# Inspiration
We had 2 inspirations, which were great movies, and media information such as Netflix and IMDB. Sometimes, we don't know what to watch, and waste precious time, sometimes hours, just scrolling through hard to navigate UI experiences to find good movies. As a result of this, we created MovieBase, which is similar to IMDB, but with a much better, more user friendly UI, and a much better, much more advanced recommendation system.

# What it does
MovieBase helps you find the perfect movie using AI and the help of the largest, most efficient open source movie database, TMDB. It’s not just a movie recommender, but acts like a whole movie database website where you can read about any movie or tv show, from its rating, to its synopsis, to the members of the cast. It even provides recommendations for similar movies.

# How we built it
We used Flask for the server-side work (the backend).
We created an AI model to categorize the movies, and display the best results.
For the frontend, we used:
Vanilla HTML/CSS/JS
Jinja, Flask's built in feature that allows you to connect frontend and backend.
To get data for movies, we used the TMDB API, which is the latest, most efficient API for movies.
Challenges we ran into
We constantly ran into irritating errors, which were extremely time consuming to fix.
We encountered over 20 server errors which we didn't even know about.
Our backend was kind of cluttered, so we had to reorganize it a few times to make it easier to work on

# Accomplishments that we're proud of
- Making the filters page to work well
- Fixing all errors in the program
- Creating a nice UI

# What we learned
- We learned how to leverage apis to fit our need, and make features that are not built into the API
- We learned a lot more about UI design
 -We learned more about -- and how to fix -- Flask and HTTP errors.

# What's next for MovieBase
- Add MPAA Ratings to each movie (G, PG, PG-13, R, M)
- Maybe make an app, since our website is mobile friendly
- Make an account system, where people can save movies and tv shows to their own watchlist, or create playlists to share with their friends and family.
