from flask import Flask, render_template, request, session, redirect, url_for
import time
import random
import urllib.request
import re
from werkzeug.exceptions import HTTPException
from flask_session import Session
from waitress import serve

app = Flask(__name__,  template_folder='site', static_folder='assets')
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
#TMDB DATABASE SETUP
from tmdbv3api import TMDb, Movie, Person, Discover, TV,Season
tmdb = TMDb()
tmdb.api_key = "49bd129cc8221a79022ce0f6073f765d"
genres = [{"id":'28',"name":"Action", "url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9dmastuNWJRCmSYhsFuWUey8S-Yx0ZnyzuZbFJnEMih_Uqle9dhB8z9fei0PciMrafUI&usqp=CAU"}, 
          {"id":'12',"name":"Adventure", "url":"https://unitingartists.org/wp-content/uploads/2020/06/Adventure-Genre-800x445.jpg"}, 
          {"id":'16',"name":"Animation", "url":"https://4.bp.blogspot.com/-7f0Ull4tk2U/WxrZhyHjI5I/AAAAAAABN4U/h6z6iuVV_ssZHt_iDoJ8DLldjS01QReQwCLcBGAs/s1600/Spider-Man-Into-the-Spiderverse-2018-trailer-10-1280x546.jpg"}, 
          {"id":'35',"name":"Comedy", "url":"https://static0.srcdn.com/wordpress/wp-content/uploads/2018/08/Ryan-Reynolds-in-Deadpool.jpg"}, 
          {"id":'80',"name":"Crime", "url":"https://img.mensxp.com/media/content/2017/Dec/the-top-10-crime-thriller-movies-of-20171400-1513772701.jpg"}, 
          {"id":'878',"name":"Science-Fiction","url":"https://s.yimg.com/ny/api/res/1.2/iV700HRBI6XCFXvGUT_5TA--/YXBwaWQ9aGlnaGxhbmRlcjt3PTY0MDtoPTM2MA--/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2020-02/564efb10-53c9-11ea-86fb-f4072beb20b2"},
         {"id":'14',"name":"Fantasy","url":"https://bookstr.com/wp-content/uploads/2020/06/harry-potter-movies-on-netflix.jpg"},
          {"id":'27',"name":"Horror", "url":"https://www.commonsensemedia.org/sites/default/files/styles/ratio_16_9_small/public/video-thumbnails/it-thumb.jpg"}, {"id":'9648',"name":"Mystery","url":"https://thecinemaholic.com/wp-content/uploads/2021/01/ezgif.com-gif-maker-5.jpg"}, {"id":'10749',"name":"Romance","url":"https://cdn.onebauer.media/one/empire-images/features/5a84102108d1e196265a9d4f/38-titanic.jpg?format=jpg&quality=80&width=440&ratio=1-1&resize=aspectfit"},  {"id":'10770',"name":"TV-Movie", "url":"https://c.files.bbci.co.uk/22AC/production/_118667880_ka_05_friendsreunion.jpg"}, {"id":'53',"name":"Thriller", "url":"https://www.billboard.com/wp-content/uploads/stylus/109300-inception_617_409.jpg?w=617"}]


def genre_movie(genre, type):
  movie = Discover()
  dico_movies = movie.discover_movies({
    'with_genres':str(genre),})
  movies = []
  for movie in dico_movies:
    movies.append({"id":str(movie['id']),'title':movie['title'],'year': movie['release_date'][:4],'bio' : movie['overview'],'adult':movie['adult'],'type': "Movie",'rating':str(movie['vote_average']),'img':"https://image.tmdb.org/t/p/w200/"+ movie['poster_path'],'img_hd':"https://image.tmdb.org/t/p/w500/"+ movie['poster_path']})
  random.shuffle(movies)
  if (type == "card"):
   return(movies)
  else:
    return(movies[0])

def filter_search(genre, rating,year,age):
  movie = Discover()
  if rating=="NONE" and genre=="NONE":
    dico_movies = movie.discover_movies()
  elif rating!="NONE" and genre=="NONE":
    dico_movies = movie.discover_movies({'vote_average.gte':int(rating.split("rating-")[1]),})
  elif rating=="NONE" and genre!="NONE":
    dico_movies = movie.discover_movies({'with_genres':tuple(map(str, genre.split("_"))),})
  elif rating!="NONE" and genre!="NONE":
    dico_movies = movie.discover_movies({'with_genres':tuple(map(str, genre.split("_"))),'vote_average.gte':int(rating.split("rating-")[1]),})
  movies = []
  for movie in dico_movies:
    try:
      movies.append({"id":str(movie['id']),'title':movie['title'],'year': movie['release_date'][:4],'bio' : movie['overview'],'adult':movie['adult'],'type': "Movie",'rating':str(movie['vote_average']),'img':"https://image.tmdb.org/t/p/w200/"+ movie['poster_path'],'img_hd':"https://image.tmdb.org/t/p/w500/"+ movie['poster_path']})
    except Exception:
      pass
  if year!="NONE":
    try:
      movies2 = [x for x in movies if int(x['year'])>int(year)]
      movies = movies2
    except Exception:
      movies2 = [x for x in movies if x['year']!=""]
      movies = movies2
      movies2 = [x for x in movies if int(x['year'])>int(year)]
      movies = movies2

  if age=="under_age":
    try:
      movies2 = [x for x in movies if x['adult']== False]
      movies = movies2
    except Exception:
      movies2 = [x for x in movies if x['adult']!=""]
      movies = movies2
      movies2 = [x for x in movies if x['adult']== False]
      movies = movies2

  
  random.shuffle(movies)
  return(movies)
    
def similar_movies(id):
  movie = Movie()
  similar_movie = movie.similar(id)
  movies = []
  for movie in similar_movie:
    movies.append({"id":str(movie['id']),'title':movie['title'],'year': movie['release_date'][:4],'bio' : movie['overview'],'adult':movie['adult'],'type': "Movie",'rating':str(movie['vote_average']),'img':"https://image.tmdb.org/t/p/w200/"+ movie['poster_path'],'img_hd':"https://image.tmdb.org/t/p/w500/"+ movie['poster_path']})
  random.shuffle(movies)
  return(movies)

def similar_tv(id):
  movie = TV()
  similar_movie = movie.similar(id)
  movies = []
  for movie in similar_movie:
    try:
      movies.append({"id":str(movie['id']),'title':movie['name'],'year': movie['first_air_date'][:4],'bio' : movie['overview'],'adult':None,'type': "TV Show",'rating':str(movie['vote_average']),'img':"https://image.tmdb.org/t/p/w300/"+ movie['backdrop_path'],'img_hd':"https://image.tmdb.org/t/p/w500/"+ movie['backdrop_path']})
    except Exception:
      pass
  return(movies)



def popular_movies(type):
  movie = Movie()
  popular_movies = movie.popular()
  movies = []
  for movie in popular_movies:
    movies.append({"id":str(movie['id']),'title':movie['title'],'year': movie['release_date'][:4],'bio' : movie['overview'],'adult':movie['adult'],'type': "Movie",'rating':str(movie['vote_average']),'img':"https://image.tmdb.org/t/p/w200/"+ movie['poster_path'],'img_hd':"https://image.tmdb.org/t/p/w500/"+ movie['poster_path']})
  random.shuffle(movies)
  movies2 = [x for x in movies if x['adult']== False]
  if (type == "card"):
   return(movies2)
  else:
    return(movies2[0])
def popular_tv():
  tv = TV()
  popular_tv = tv.popular()
  movies = []
  for movie in popular_tv:
    movies.append({"id":str(movie['id']),'title':movie['name'],'year': movie['first_air_date'][:4],'bio' : movie['overview'],'adult':None,'type': "TV Show",'rating':str(movie['vote_average']),'img':"https://image.tmdb.org/t/p/w300/"+ movie['backdrop_path'],'img_hd':"https://image.tmdb.org/t/p/w500/"+ movie['backdrop_path']})
  random.shuffle(movies)
  return(movies)
    
def search_movie(QUERY):
  try:
    try:
      movie = Movie()
      search = movie.search(QUERY)
      movies = []
      for movie in search:
        try:
          movies.append({"id": str(movie['id']),'title':movie['title'],'year': movie['release_date'][:4],'bio' : movie['overview'],'adult':movie['adult'],'type': "Movie",'rating':str(movie['vote_average']),'img':"https://image.tmdb.org/t/p/w200/"+ movie['poster_path'],'img_hd':"https://image.tmdb.org/t/p/w500/"+ movie['poster_path']})
        except Exception:
          movies.append({"id": str(movie['id']),'title':movie['title'],'year': movie['release_date'][:4],'bio' : movie['overview'],'adult':movie['adult'],'type': "Movie",'rating':str(movie['vote_average']),'img':"/assets/images/default.png",'img_hd':"/assets/images/default.png"})
      return(movies)
    except Exception:
        movie = Movie()
        search = movie.search("s")
        movies = []
        for movie in search:
          try:
            movies.append({"id": str(movie['id']),'title':movie['title'],'year': movie['release_date'][:4],'bio' : movie['overview'],'adult':movie['adult'],'type': "Movie",'rating':str(movie['vote_average']),'img':"https://image.tmdb.org/t/p/w200/"+ movie['poster_path'],'img_hd':"https://image.tmdb.org/t/p/w500/"+ movie['poster_path']})
          except Exception:
            pass
        return(movies)
  except Exception:
    return([])
def search_tv(QUERY):
  try:
    movie = TV()
    search = movie.search(QUERY)
    movies = []
    for movie in search:
      try:
        movies.append({"id":str(movie['id']),'title':movie['name'],'year': movie['first_air_date'][:4],'bio' : movie['overview'],'adult':None,'type': "TV Show",'rating':str(movie['vote_average']),'img':"https://image.tmdb.org/t/p/w300/"+ movie['backdrop_path'],'img_hd':"https://image.tmdb.org/t/p/w500/"+ movie['backdrop_path']})
      except Exception:
        pass
    return(movies)
  except Exception:
    return([])
    
def get_trailer(title, year):
    search_keyword=title.replace(" ", "%20") + "trailer%20"+ str(year)
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return ("https://www.youtube.com/embed/" + video_ids[0])


def get_movie_data(id):
  movie = Movie()
  movie = movie.details(int(id))
  cast = []
  for people in (movie['casts']['cast']):
      try:
        cast.append({'name':people['name'],'id':str(people['id']),'char': people['character'],'img':"https://image.tmdb.org/t/p/w200/"+ people['profile_path']})
      except Exception:
        pass
  cast = cast
  movie = ({"id": str(movie['id']),'cast':cast,"dur": str(movie['runtime']),'title':movie['title'],'year': movie['release_date'][:4],'bio' : movie['overview'],'adult':movie['adult'],'type': "Movie",'rating':str(movie['vote_average']),'img':"https://image.tmdb.org/t/p/w200/"+ movie['poster_path'],'img_hd':"https://image.tmdb.org/t/p/w500/"+ movie['poster_path']})
  return movie
  
def get_season(show, season1):
  seasons = Season()
  season = []
  seasons = seasons.details(show, season1)
  episode = []
  x=1
  for i in(seasons['episodes']):
    try:
      episode.append({"sno":i['season_number'],
    "name":i['name'],
    'number':str(i["episode_number"]),
    "id":"/episode?id="+str(show)+"&s="+str(i['season_number'])+"&e="+str(i['episode_number']-1),
    "bio":i['overview'],
    "rating":i['vote_average'],
    "img":"https://image.tmdb.org/t/p/w500/"+ i['still_path']})
    except Exception:
      episode.append({"sno":i['season_number'],
    "name":i['name'],
    'number':str(i["episode_number"]),
    "id":"/episode?id="+str(show)+"&s="+str(i['season_number'])+"&e="+str(i['episode_number']-1),
    "bio":i['overview'],
    "rating":i['vote_average'],
    "img":"/assets/images/default.png"})
   
  try:
    season = ({"sno":seasons['season_number'],
  "name":seasons['name'],
  "episodes":str(len(seasons['episodes'])),
  'episode':episode,
  "id":"/tv?id="+str(show)+"&s="+str(season1),
  "bio":seasons['overview'],
  "img":"https://image.tmdb.org/t/p/w500/"+ seasons['poster_path']})
  except Exception:
    season = ({"sno":seasons['season_number'],
  "name":seasons['name'],
  "episodes":str(len(seasons['episodes'])),
  'episode':episode,
  "id":"/tv?id="+str(show)+"&s="+str(season1),
  "bio":seasons['overview'],
  "img":"/assets/images/default.png"})
  return season


# get episode
def get_episode(show, season1, episode1):
  season = Season()
  show_season = season.details(show, season1)
  episode = []
  cast = []
  for people in (show_season['credits']['cast']):
    try:
      cast.append({'name':people['name'],'id':str(people['id']),'char': people['character'],'img':"https://image.tmdb.org/t/p/w200/"+ people['profile_path']})
    except Exception:
      pass
  for i in(show_season['episodes']):
    try:
      episode.append({"sno":str(i['season_number']),
    "name":i['name'],
    "cast":cast,
    "number":str(i['episode_number']),
    "bio":i['overview'],
    "id":"/tv?id="+str(show)+"&s="+str(i['season_number'])+"&e="+str(i['episode_number']),
    "rating":str(i['vote_average']),
    "img":"https://image.tmdb.org/t/p/w500/"+ i['still_path']})
    except Exception:
      episode.append({"sno":str(i['season_number']),
    "name":i['name'],
    "cast":cast,
    "number":str(i['episode_number']),
    "bio":i['overview'],
    "id":"/tv?id="+str(show)+"&s="+str(i['season_number'])+"&e="+str(i['episode_number']),
    "rating":str(i['vote_average']),
    "img":"/assets/images/default.png"})
  return episode[episode1]
def get_tv_data(id):
  tv = TV()
  cast2=[]
  movie = tv.details(id)
  try:
    movies = ({ "id": str(movie['id']),'cast':cast2,"dur": str(movie['episode_run_time']),'title':movie['name'],'year': movie['first_air_date'][:4],'bio' : movie['overview'],'adult':movie['adult'],'seasons':(movie['seasons']),'season_count':str(len(movie['seasons'])),'type': "TV Show",'rating':str(movie['vote_average']),'img':"https://image.tmdb.org/t/p/w200/"+ movie['backdrop_path'],'img_hd':"https://image.tmdb.org/t/p/w500/"+ movie['backdrop_path']})
  except Exception:
    movies = ({ "id": str(movie['id']),'cast':cast2,"dur": str(movie['episode_run_time']),'title':movie['name'],'year': movie['first_air_date'][:4],'bio' : movie['overview'],'adult':movie['adult'],'seasons':(movie['seasons']),'season_count':str(len(movie['seasons'])),'type': "TV Show",'rating':str(movie['vote_average']),'img': '/assets/images/default.png','img_hd':"/assets/images/default.png"})
  s = []
  x=0
  for item in movies['seasons']:
    item['id'] = str(item["season_number"])
    item['sno'] = str(item['season_number'])
    try:
      item['img'] = "https://image.tmdb.org/t/p/w500/"+ item['poster_path']
    except Exception:
      item['img'] = "/assets/images/default.png"
    item["episodes"] = item['episode_count']
    s.append(item)
    x+=1
  del movies['seasons']
  movies['season'] = s
    
  return movies
  



#APP ROUTES/ WEBSITES
@app.route('/', methods=["POST", "GET"])
def base_page():
  global movies
  movies=popular_movies("card")
  global banner
  banner = popular_movies("banner")
  if session.get("name"):
    return render_template('index.html',
                           banner=banner,
                           movies=movies, login=session.name)
  else:
   return render_template('index.html',
                           banner=banner,
                           categories = genres,
                          tv_shows = popular_tv(),
                           movies=movies, login="Login")


@app.route('/gin', methods=["POST", "GET"])
def loggin_page():
  print(request.form.get('username'))

@app.errorhandler(Exception)
def http_error_handler(error):
  return redirect('/')

@app.errorhandler(405)
def error_page405(e):
  return redirect('/error')

@app.errorhandler(404)
def error_page404(e):
  return render_template('error.html')


@app.errorhandler(HTTPException)
def error_page404(e):
  return render_template('error.html')

@app.route('/search', methods=['POST'])
def search_page():
  movies = search_movie(request.form['search'])
  tv = search_tv(request.form['search'])
  if movies != None:
    return render_template('search.html',movies=movies, tv_shows = tv)


@app.route('/genre/')
def genre_page():
  id = request.args.get('id', default='', type=int)
  name = request.args.get('genre', default='', type=str)
  movie=genre_movie(id,"card")
  banner = movie[0]
  movie = movie[1:]
  return render_template('genre.html',
                           banner=banner,
                           movies=movie, login="Login",name=name+" Movies")


@app.route('/fsearch')
def filter_search_page():
  id_genre = request.args.get('genre', default='', type=str)
  id_rating_star = request.args.get('rating', default='', type=str)
  id_age = request.args.get('age', default='', type=str)

  id_year = request.args.get('year', default='', type=str)
  movie=filter_search(id_genre,id_rating_star,id_year, id_age)
  banner = movie[0]
  movie = movie[1:]
  return render_template('genre.html',
                           banner=banner,
                           movies=movie, login="Login",name="Movies Based on Your Filter")
  
@app.route('/login', methods=["POST", "GET"])
def login_page():
  return render_template('login.html')

  
@app.route('/movie/')
def movie_page():
  id = request.args.get('id', default='', type=str)
  movie=get_movie_data(id)
  link = get_trailer(movie['title'], movie['year'])
  return render_template('movie.html',movie=movie, link=link,similar_movies=similar_movies(int(id)))
  
@app.route('/tvshow/')
def tv_page():
  id = request.args.get('id', default='', type=str)
  movie=get_tv_data(id)
  link = get_trailer(movie['title'], movie['year'])
  movie_link = "https://www.2embed.ru/embed/tmdb/movie?id="+ movie["id"]
  return render_template('tvshow.html',movie=movie, link=link, movie_link=movie_link, similar_movies=similar_tv(id))
  
@app.route('/season/')
def season_page():
  id = request.args.get('id', default='', type=str)
  id2 = request.args.get('s', default='', type=str)
  movie=get_season(int(id), int(id2))
  print(movie)
  return render_template('season.html',movie=movie, episodes = movie['episode'])

@app.route('/episode/')
def episode_page():
  id = request.args.get('id', default='', type=str)
  id2 = request.args.get('s', default='', type=str)
  id3 = request.args.get('e', default='', type=str)
  movie=get_episode(int(id), int(id2), int(id3))
  return render_template('episode.html',movie=movie)

  
@app.route('/filter', methods=['GET', 'POST'])
def filter():
  genrelist = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Science Fiction", "Thriller", "TV Movie", "War", "Western"]
  return render_template('filter.html', genrelist=genrelist, movies=popular_movies("card"), banner = popular_movies("banner"), categories = genres, tv_shows = popular_tv(), login="Login")

  
@app.route('/person/')
def person_page():
  id = request.args.get('id', default='', type=str)
  person = Person()  
  p = person.details(int(id))
  person = {'name':p['name'],
  'bio':p['biography'],
   'dob':p['birthday'],
  'work':p['known_for_department'],
  'place':p['place_of_birth'],
  'img': "https://image.tmdb.org/t/p/w500/"+ p['profile_path']}
  return render_template('person.html',person=person)

@app.route('/results', methods=["POST", "GET"])
def results():
  if request.method == "POST":
    return request.form
sess = Session()
sess.init_app(app)
serve(
app, 
host='0.0.0.0',
port=8080
)


  
