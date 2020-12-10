# API för storströgarnas racesystem, denna ska agera databas för det som mäts upp i bilen
# Local host för mig: http//:127.0.0.1:5000/
from flask import Flask
from flask_restful import Api, Resource, reqparse
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

map_put_arg = reqparse.RequestParser()
measurements_put_arg = reqparse.RequestParser()

# Ser till att man skciakr rätt data till class Map(): eller att man kan kräva den
map_put_arg.add_argument("map", type=str, help = "Skicka bild på banan", required=True)
map_put_arg.add_argument("knapp", type=str, help = "Måste ladda upp data", required=True)

measurements_put_arg.add_argument("data", type=str, help = "Måste skicka dict", required=True)

# Dict som lagrar banans bild.
map_im = {"map" : "placeholder"}

# Mätar data som ska visas på skärmen
measurements = {}

# Skapar en resurs:
class Map(Resource):
    '''Testresurs: Hur hanteras requests?'''
    def get(self, tk_map):
        return tk_map

    def put(self, tk_map):
        args = map_put_arg.parse_args()
        return {tk_map : args}

        #map_im["map"] = tk_map
class Measurements(Resource):
    '''Klass som hanterar mätardata'''
    def get(self, message):
        return  measurements[message], 200

    def put(self, message):
        args = measurements_put_arg.parse_args()
        measurements[message] = json.loads(args["data"])
        print(measurements)
        # Status code 200 innebär att allt gick ok!
        return measurements, 200



#Vad <string:name> name säger är att det är så man låter användare eller
#programmet skicka världen med en get eller post, gör jag detta bör jag lägga till
# name i någon metod under hello world. Som illustrerat kan man länka på fler 
# parametrar efter varandra
api.add_resource(Map, "/map/<string:tk_map>")
api.add_resource(Measurements, "/measurements/<string:message>")

if __name__ == "__main__":
    app.run(debug = True)