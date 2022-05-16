from flask import Flask,jsonify
from database import SelectMethods,InsertMethods
import json

app=Flask(__name__)

@app.route("/")
def hello_world():
    return "<p> Hello World </p>"

@app.route("/select/<table_name>/<fields>") # http://localhost:5000/select/people/name,surname
def test(table_name,fields=None):
    dictionary={"table_name":table_name,"columns":fields}
    select=SelectMethods(dictionary=dictionary)
    return select.process()

@app.route("/select/<table_name>") # http://localhost:5000/select/people
def getTable(table_name):
    dictionary={"table_name":table_name}
    select=SelectMethods(dictionary=dictionary)
    return select.process()

@app.route("/insert/<table_name>/<field_names>/<values>") # http://localhost:5000/insert/people/name,surname,age/Marek,Mezera,24
def insertTable(table_name,field_names,values):
    dictionary={"table_name":table_name,"field_names":field_names,"values":values}
    insert=InsertMethods(dictionary=dictionary)
    return insert.process()

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)

    # Configuration changed to mysql from localhost, if in docker