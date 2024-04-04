from flask import Flask, jsonify, render_template
from pymongo import MongoClient


app= Flask(__name__)

@app.route('/')
def index():
    return render_template('mikeindex.html')



@app.route('/console/<consola>', methods=['GET'])
def consolas(consola):
   consola= consola.upper()
   videogames = MongoClient('mongodb+srv://miketrueno:arman7x3@cluster0.46l1iaa.mongodb.net/')
   db = videogames['METACRITIC_MIKE']
   coll=db['GAMES']
   lista=[]
   platform_eq= coll.find({"platform":{"$eq":consola}}, {"_id": False, "positive_critics":False, "neutral_critics":False, "negative_critics": False, "positive_users": False, "neutral_users": False, "negative_users": False})
   for games in platform_eq:
      lista.append(games)
   response = jsonify(
       {
          "STATUS_CODE": 200,
          "MESSAGE": f'VIDEOJUEGOS CUYA PLATAFORMA ES {consola}',
          "CONSOLE": lista          
       }
    )
   return response
   
@app.route('/rating/<int:rev>', methods=['GET'])
@app.route('/rating/<int:rev>/<consola>', methods=['GET'])
def review(rev, consola=None):
    
    videogames = MongoClient('mongodb+srv://miketrueno:arman7x3@cluster0.46l1iaa.mongodb.net/')
    db = videogames['METACRITIC_MIKE']
    coll = db['GAMES']
    lista = []
    if consola==None:
        games_rev = coll.find({"metascore": {"$gte": rev}},
                              {"_id": False, "positive_critics": False, "neutral_critics": False,
                               "negative_critics": False, "positive_users": False, "neutral_users": False,
                               "negative_users": False})
    else:
        consola=consola.upper()
        games_rev = coll.find({"metascore": {"$gte": rev}, "platform": consola},
                              {"_id": False, "positive_critics": False, "neutral_critics": False,
                               "negative_critics": False, "positive_users": False, "neutral_users": False,
                               "negative_users": False})
    

    for rates in games_rev:
        lista.append(rates)

    response = jsonify({
        "STATUS_CODE": 200,
        "MESSAGE": f'VIDEOJUEGOS CUYA CALIFICACION EN METACRITIC SON MAYOR O IGUAL QUE {rev}',
        "CONSOLE": lista
    })

    return response

@app.route('/cantidad/<consola>', methods=['GET'])
def cantidad_juegos(consola):
    consola = consola.upper()
    videogames = MongoClient('mongodb+srv://miketrueno:arman7x3@cluster0.46l1iaa.mongodb.net/')
    db = videogames['METACRITIC_MIKE']
    coll = db['GAMES']

    if consola == 'TOTAL':
        total_juegos = coll.count_documents({}) 
        response = jsonify({
            "STATUS_CODE": 200,
            "MESSAGE": 'CANTIDAD TOTAL DE JUEGOS CALIFICADOS POR METACRITIC',
            "TOTAL_JUEGOS": total_juegos
        })
    else:
        juegos_por_consola = coll.count_documents({"platform": {"$eq": consola}})
        response = jsonify({
            "STATUS_CODE": 200,
            "MESSAGE": f'Cantidad de juegos calificados por metacritic para la consola {consola}',
            "TOTAL_JUEGOS": juegos_por_consola
        })

    return response




app.run(debug=True, host='localhost', port=5000)

 