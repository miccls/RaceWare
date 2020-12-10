# API för storströgarnas racesystem, denna ska agera databas för det som mäts upp i bilen
# Local host för mig: http//:127.0.0.1:5000/
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class MeasurementsModel(db.Model):
    id = db.Column(db.String(50), primary_key = True)
    rpm = db.Column(db.Integer)
    kmh = db.Column(db.Integer)
    throttle = db.Column(db.Integer)
    water = db.Column(db.Integer)
    oiltemp = db.Column(db.Integer)
    load = db.Column(db.Integer)
    
    def __repr__(self):
        return f"rpm = {rpm}"


db.create_all()



measurements_put_arg = reqparse.RequestParser()

# Ser till att man skciakr rätt data till class Map(): eller att man kan kräva den

measurements_put_arg.add_argument("rpm", type=int, help = "Måste ladda upp data", required=True)
measurements_put_arg.add_argument("kmh", type=int, help = "Måste ladda upp data", required=True)
measurements_put_arg.add_argument("throttle", type=int, help = "Måste ladda upp data", required=True)
measurements_put_arg.add_argument("water", type=int, help = "Måste ladda upp data", required=True)
measurements_put_arg.add_argument("oiltemp", type=int, help = "Måste ladda upp data", required=True)
measurements_put_arg.add_argument("load", type=int, help = "Måste ladda upp data", required=True)


# Denna skapar ett dictionary som man kan skicka ut.
resource_fields = {
    'id' : fields.String,
    'rpm' : fields.Integer,
    'kmh' : fields.Integer,
    'throttle' : fields.Integer,
    'water' : fields.Integer,
    'oiltemp' : fields.Integer,
    'load' : fields.Integer
}

# Dict som lagrar banans bild.
map_im = {"map" : "placeholder"}


# Skapar en resurs:
class Map(Resource):
    '''Testresurs: Hur hanteras requests?'''
    def get(self, tk_map):
        return tk_map

    def put(self, tk_map):
        args = measurements_put_arg.parse_args()
        return {tk_map : args}

        #map_im["map"] = tk_map
class Measurements(Resource):
    '''Klass som hanterar mätardata'''
    @marshal_with(resource_fields)
    def get(self, message):
        result = MeasurementsModel.query.filter_by(id = message).first()
        if not result:
            abort(404, message = "Kunde inte hitta data.")
        return  result, 200


    @marshal_with(resource_fields)
    def put(self, message):
        args = measurements_put_arg.parse_args()
        measurements = MeasurementsModel(id = message,
            rpm = args['rpm'], kmh = args['kmh'], throttle = args['throttle'],
            water = args['water'], oiltemp = args['oiltemp'], load = args['load'])
        db.session.add(measurements)    
        db.session.commit()    
        # Status code 200 innebär att allt gick ok!
        return measurements, 200

    # Metod som uppdaterar värden i databasen.
    @marshal_with(resource_fields)
    def patch(self,message):
        args = measurements_put_arg.parse_args()
        result = MeasurementsModel.query.filter_by(id = message).first()
        for key, value in args.items():
            setattr(result, key, value)
        db.session.commit()
        return result


#Vad <string:name> name säger är att det är så man låter användare eller
#programmet skicka världen med en get eller post, gör jag detta bör jag lägga till
# name i någon metod under hello world. Som illustrerat kan man länka på fler 
# parametrar efter varandra
api.add_resource(Map, "/map/<string:tk_map>")
api.add_resource(Measurements, "/measurements/<string:message>")

if __name__ == "__main__":
    app.run(host='192.168.1.129')  #app.run(host='0.0.0.0') app.run(debug = True) 