# Stage 1
1) Extracting the title, imdb_id, release date, genre, crew, rating and votes for each movie using *omdbapi.

2) Creating mongodb database in local , named contelligenz

3) Inserting each of the movie details in mongodb collection called movies


# Stage 2
1) Creating an empty fields for cast, crew, synopsis, reviews for movies.

2) Extracting cast (top 4), crew, synopsis, reviews from imdb website using requests, bs4, html.parser.

3) Adding each of these details to the respective movie id in movies collection.


# Stage 3
1) creating new collection for actors, named popcastscores.

2) creating new collection for crew popularity score, named popcrewscores.

3) creating emplty fields for sentiment-score, review-keyword, plot-keyword, popularity-score.

4) calculating crew, cast score: (how popular actor or crew member is compared to others)

            $\frac{cast\_votes}{total\_votes-cast\_votes}*10$

            here, 
            * cast_votes is the total votes of movies recieved by actor for all movies (shows how popular the actor is)
            * total_votes - cast_votes is for popularity of other actors.
            * 10 is the scaler.

5) calculating popularity score: (how popular the movie is compared to others ratings)

    $\frac{(avg\_rating*n\_votes) + (c*m)}{n\_votes+c}$

here, 
* avg_rating is the rating recieved.
* n_votes is the total votes recieved.
* c is the confidence number (calculated as 25% quantile from votes of each movie).
* m is the avg_rating of all movies.

6) calculating sentiment score
* The vader of nltk library is used.
* preprocessing of removing new line characters is done.
* The compound polarity score is used for sentiment score.

7) review keyword extraction
* Spacy is used to add pos tag for words in review and usual text preprocessing.
* top(most frequent) 5 occuring adjective + preposition are returned from first 10 reviews.
* YAKE is used to extract keywords from plot summary.

# Stage 4
1) Creating the corpus for model training for (symantic search of movies from synopsis).
* removing spaces, punctuations, new line characters, extra spaces, alphanumerics, short words.
* Tokenizing ,lowering and lemmatizing the words.
* creating dictionary (contains word, index mapping) of the words using gensim.
* adding few more stop words to remove, 
    hello and if this can would should could tell ask stop come go

2) training model
* creating BOW(bag of words) for corpus. (calculates frequency for each word)
* TF-IDF model is build on top of new corpus (to calcualate a score represeneting the frequency of words throughout the corpus and relevant document.)
* pass TF-IDF corpus to LSI model (determines association & closeness between terms occuring in similar context).
* saving the model

3) symantic search
* loading the model.
* cosine similarity to compare query(input) with corpus and return top matching movie titles.

# Stage 5
1) Top n movies
* Top titles with line plot, using movie's popularity score.
* Top Genres with word cloud using genres frequency.
* Top Actors with pie chart usign actor's popularity score.

2) Single movie analysis
* get movie from collection
* cast popularity with bar chart.
* crew popularity with bar charts.
* plot keywords with word cloud.
* review keywords with word cloud.
* sentiment analysis with pie chart.

# Rest Api
* http://127.0.0.1:8000/top_movies?year=2012 returns movie for year 2012
* http://127.0.0.1:8000/top_movies?genre=action returns movie for genre action
* http://127.0.0.1:8000/top_movies?plot_key=alien returns movie for plot keyword alien

