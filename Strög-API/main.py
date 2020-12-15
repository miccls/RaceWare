# API för storströgarnas racesystem, denna ska agera databas för det som mäts upp i bilen
# Local host för mig: http//:127.0.0.1:5000/
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import json
from flask_sqlalchemy import SQLAlchemy

# Initierar APIn och databasen.
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Skapar en modell av den data som kommer behandlas av measurements resourcen
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

# Definierar de argument som kommer skickas till measurements.

measurements_put_arg.add_argument("rpm", type=int, help = "Måste ladda upp data", required=True)
measurements_put_arg.add_argument("kmh", type=int, help = "Måste ladda upp data", required=True)
measurements_put_arg.add_argument("throttle", type=int, help = "Måste ladda upp data", required=True)
measurements_put_arg.add_argument("water", type=int, help = "Måste ladda upp data", required=True)
measurements_put_arg.add_argument("oiltemp", type=int, help = "Måste ladda upp data", required=True)
measurements_put_arg.add_argument("load", type=int, help = "Måste ladda upp data", required=True)


# Denna skapar ett dictionary som man kan skicka ut.
# Vad den gör är att den översätter argumenten som kommer till 
# följande form som är trevlig att lagra i db och att skicka till
# dator
resource_fields = {
    'id' : fields.String,
    'rpm' : fields.Integer,
    'kmh' : fields.Integer,
    'throttle' : fields.Integer,
    'water' : fields.Integer,
    'oiltemp' : fields.Integer,
    'load' : fields.Integer
}


# Klassen nedan sköter all dataöverföring som har med mätvärden att göra
class Measurements(Resource):
    '''Klass som hanterar mätardata'''
    @marshal_with(resource_fields)
    def get(self, message):
        # Hämtar världen från databasen
        result = MeasurementsModel.query.filter_by(id = message).first()
        if not result:
            # Om id inte matchar någon data, skicka felmeddelande
            abort(404, message = "Kunde inte hitta data.")
        return  result, 200


    @marshal_with(resource_fields)
    def put(self, message):
        # Spara argument som dict med parse_args() som också gör massa annat godis
        args = measurements_put_arg.parse_args()
        measurements = MeasurementsModel(id = message,
            rpm = args['rpm'], kmh = args['kmh'], throttle = args['throttle'],
            water = args['water'], oiltemp = args['oiltemp'], load = args['load'])
        #Lägg till i databas
        db.session.add(measurements)    
        db.session.commit()    
        # Status code 200 innebär att allt gick ok!
        return measurements, 200

    # Metod som uppdaterar värden i databasen.
    @marshal_with(resource_fields)
    def patch(self,message):
        args = measurements_put_arg.parse_args()
        result = MeasurementsModel.query.filter_by(id = message).first()
        # Uppdaterar databas med nya värden.
        for key, value in args.items():
            setattr(result, key, value)
        db.session.commit()
        return result

class TestConnection(Resource):
    ''' Resource som skickar ett enkelt svar för att verifiera anslutning '''
    def get(self):
        return {'answer' : 'Ansluten'}

#Vad <string:name> name säger är att det är så man låter användare eller
#programmet skicka världen med en get eller post, gör jag detta bör jag lägga till
# name i någon metod under hello world. Som illustrerat kan man länka på fler 
# parametrar efter varandra

api.add_resource(Measurements, "/measurements/<string:message>")
api.add_resource(TestConnection, "/testconnection")

if __name__ == "__main__":
    # Detta är min ip.
    app.run(host='192.168.1.129')  #app.run(host='0.0.0.0') app.run(debug = True) 