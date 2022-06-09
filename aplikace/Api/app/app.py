from cgitb import html
from select import select
from flask import Flask,jsonify, redirect, render_template, request
from flask_restful import reqparse, abort, Api, Resource
from matplotlib.pyplot import plot
from database import SelectMethods,InsertMethods
from calculus import Operation
import json
import os
import pandas as pd

app=Flask(__name__)

@app.route("/")
def hello_world():
    #return "<p> Hello World </p>"
    return render_template("main.html")

@app.route("/upload_csv", methods=["GET", "POST"])
def upload_csv():
    #filepath = "./Api/app/static/csv/"
    filepath = "./static/csv"
    print("1")
    if request.method == "POST":
        print("2")
        if request.files:
            print("3")
            data_csv = request.files["csv"]

            data_csv.save(os.path.join(filepath, "data.csv"))  
            
            print("CSV loaded")
            
            data = InsertMethods.load_data(os.path.join(filepath, "data.csv"))            
            
            data_new = Operation.DAS(data)

            print(data_new)
            dictionary={"table_name":"signals","field_names":"PS_sig,sig,DAS_sig","values":data_new}
            
            insert = InsertMethods(dictionary=dictionary).process()
            print("data uloženy do databáze")
                   
            return redirect(request.url)
       
    return render_template("upload_csv.html")

@app.route("/plot_data")
def plot_data():
    
    dictionary={"table_name":"signals"}
    data = SelectMethods(dictionary=dictionary).process()

    #print("start")
    #print(data)

    return Operation.plot(data)

if __name__=="__main__":
    print("ahoj")
    app.run(debug=True,host='0.0.0.0',port=5000)
    
    # Configuration changed to mysql from localhost, if in docker
    