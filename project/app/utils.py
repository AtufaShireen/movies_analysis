import pymongo
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import seaborn as sns

plt.switch_backend('agg')
import base64
from io import BytesIO

visual_base = ""
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["contelligenz"]
mycol = mydb["movies"]
scorecastcol = mydb['popscastcores']
scorecrewcol = mydb['popscrewcores']


def plot_config(**kwargs):
        # plt.figure(figsize=kwargs.get('figsize',(8,8)))
        plt.title(kwargs.get('title',''))
        plt.xlabel(kwargs.get("xlabel",'feature'))
        plt.ylabel(kwargs.get('ylabel','stat'))
        tmpfile = BytesIO()
        plt.savefig(f"/Users/atufashireen/projects/Tamu_Bloomberg/project/app/templates/temp/top.png", format='png')
        plt.close()
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')    
        
        return tmpfile, encoded

def top_n_movs(n=10,genre=None,year=None,plot_key=None):
    genres = ['comedy','drama','musical','sport','crime','history','biography','action','family','romance','adventure','mystery','thriller','sci-fi']
    movs = mycol.find({}).sort("popularity-score", -1).limit(n)
    movs = [i for i in movs]
    if genre:
        try:
            if genre.lower() in genres:
                movs= mycol.find( { 'genre' : { '$regex' : genre, '$options' : 'i' } } ).limit(n)
                movs = [i for i in movs]
                assert movs == None
                return movs
        except Exception as e:
            print(e)
            pass
    elif year:
        try:
            int(year)
            movs= mycol.find( { 'release' : { '$regex' : year, '$options' : 'i' } } ).limit(n)
            movs = [i for i in movs]
            assert movs == None
            return movs
        except Exception as e:
            print(e)
    elif plot_key:
        try:
            movs= mycol.find( { 'synopsis' : { '$regex' : plot_key, '$options' : 'i' } } ).limit(n)
            movs = [i for i in movs]
            assert movs == None
            return movs
        except Exception as e:
            print(e)
    return movs


def visualize_top_n_movs(n=10):
    top = top_n_movs(n)
    titles = []
    scores = []
    genres = []
    senti = []
    for i in top:
        titles.append(i['title'])
        genres.append(i['genre'])
        senti.append(i['sentiment-score'])
        scores.append(i['popularity-score'])
    # Genre distribution
    wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                min_font_size = 10).generate(' '.join(genres))
    wordcloud.to_file(f'/Users/atufashireen/projects/Tamu_Bloomberg/project/app/templates/temp/words_cloud.png')
    plt.figure(figsize=(20,3))
    sns.lineplot(x=titles,y=scores, marker="o")
    img = plot_config(title ='Popularity score')
    return img
