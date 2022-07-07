
from flask import Flask, redirect,request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from itsdangerous import Serializer 
import requests
import psycopg2
from flask import jsonify
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)
app.debug = True


from sqlalchemy.sql import func

URL ="https://restcountries.com/v3.1/all"


location = "Countries"

PARAMS = {'address':location}

r = requests.get(url = URL, params = PARAMS)

data = r.json()

latitude = data[0]['latlng'][0]
longitude = data[0]['latlng'][1]
# formatted_address = data['results'][0]['formatted_address']

print("Latitude:%s\nLongitude:%s"
      %(latitude, longitude))


basedir = os.path.abspath(os.path.dirname(__file__))



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost/Countries'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class Country(db.Model):

  id = db.Column(db.Integer, primary_key=True)
  country_name = db.Column(db.String(200), unique=False, nullable=False)
  capital_name = db.Column(db.JSON)
  flag = db.Column(db.JSON)
  currency= db.Column(db.JSON)
  region = db.Column(db.String(200))
  language = db.Column(db.JSON)
  area = db.Column(db.Float(200))
  population = db.Column(db.Integer())
  timezone = db.Column(db.JSON)




  # repr method represents how one object of this datatable
  # will look like
  def __repr__(self):
    return f"country: {self.country_name}, capital: {self.capital_name}"

# function to render index page
@app.route('/')
def index():
    countries=Country.query.all()
    return render_template('index.html',countries=Country)

@app.route('/rest/<int:page>',methods=['GET'])
def rest (page):
    paginated_obj=Country.query.paginate(per_page=10, page=page, error_out=True)
    
    paginated_list=[]
    for item in paginated_obj.items:
        obj={'country':item.country_name,
              'capital':item.capital_name,
                'flag' :item.flag ,
                'currency':item.currency, 
                'region':item.region,    
                ' language':item. language,
                'area':item.area,
                  'population':item.population, 
                  'timezone':item.timezone }
        paginated_list.append(obj)

    templateobj= {"has_next":paginated_obj.has_next,"total_pages":paginated_obj.pages,"total_items":paginated_obj.total,'countries':paginated_list}
    print(templateobj['countries'])
    # return render_template('index.html',templateobj=templateobj) 
    return (templateobj)
    

    # rest=paginated_obj.items
        # obj=Country.query.limit(1)
    # print(obj)
    # return('rrr')

@app.route('/capital/',methods=["GET"])
def sorted_by_captial():
    data=Country.query.filter(Country.country_name=="Cyprus")
    paginated_obj=data.paginate(per_page=10, page=1, error_out=True)
    
    paginated_list=[]
    for item in paginated_obj.items:
        obj={'country':item.country_name,
              'capital':item.capital_name,
                'flag' :item.flag ,
                'currency':item.currency, 
                'region':item.region,    
                ' language':item. language,
                'area':item.area,
                  'population':item.population, 
                  'timezone':item.timezone }
        paginated_list.append(obj)

    templateobj= {"has_next":paginated_obj.has_next,"total_pages":paginated_obj.pages,"total_items":paginated_obj.total,'countries':paginated_list}
    print(templateobj['countries'])
    # return render_template('index.html',templateobj=templateobj) 
    return (templateobj)
    

    
@app.route('/country', methods=["GET"])
def get_all_countries():


    URL ="https://restcountries.com/v3.1/all"

    r = requests.get(url = URL)

    countries = r.json()
    obj=[]
    # print(countries)
    countries_list= []
    for country in countries:
        print('---------------1---------->')
        country_obj = Country (
    
            country_name=country['name'] ['common'],
            capital_name=country['capital'][0] if 'capital' in country else None,
            currency=country['currencies'] if 'currencies' in country else None,
            region=country['region'] if 'region' in country else None,
            language=country['languages'] if 'languages' in country else None,
            area=country['area'] if 'area' in country else None,
            flag=country['flags'] if 'flags' in country else None,
            population=country['population'] if 'population' in country else None,
            timezone=country['timezones'] if 'timezones' in country else None,
        )
        countries_list.append(country_obj)
        db.session.add(country_obj)
        db.session.commit()



        print('---------------2---------->')
        print(countries_list)


        # country_data ={}
        # country_data ['country_name'] =country['name']['common']
        # country_data ['capital_name'] =country['capital'][0] if 'capital' in country else None
        # country_data ['currency'] =country['currencies'] if 'currencies' in country else None
        # country_data ['region'] =country['region'] if 'region' in country else None
        # country_data['language '] = country['languages'] if 'languages' in country else None
        # country_data['area '] = country['area'] if 'area' in country else None
        # country_data['flag '] = country['flags'] if 'flags' in country else None
        # country_data['population'] = country['population'] if 'population' in country else None
        # country_data['timezone'] = country['timezones'] if 'timezones' in country else None


        # obj.append(country_data)

    print(obj)
    
    return jsonify(countries)
 

 

if __name__ == '__main__':
  app.run()

