#!flask/bin/python
from flask import Flask, jsonify,abort,make_response,request
import time
import os
import requests
import sqlite3
import re
import requests
from flask import make_response
import datetime
from flask_cors import CORS,cross_origin
import os
import random
app = Flask(__name__)
CORS(app,support_credentials=True)

def updatestatus(email,phno):
    conn=sqlite3.connect('users1.db')
    query="UPDATE user SET status="+str(1)+" WHERE email="+"'"+email+"'"+" OR"+" phno="+"'"+phno+"' ;"
    try:
        conn.execute(query)
        conn.commit()
        return 1
    except:
        conn.commit()
        return 0 

@app.route('/register',methods=['POST'])
def registerNewUser():
    data=request.json
    name=request.json['name']
    phno=request.json['phno']
    email=request.json['email']
    pwd=request.json['pwd']
    conn=sqlite3.connect('users1.db')
    query = "INSERT INTO user(email,phno,pwd,name) VALUES ("'"'+str(email)+'"'+","+str(phno)+","+'"'+pwd+'"'+","+'"'+ name+'"'+");"
    try:
        conn.execute(query)
    except sqlite3.IntegrityError:
        data=["Your are already registered"]
        return make_response(jsonify(data),400)
    print(query)
    conn.commit()
    return make_response(jsonify(data),200)

@app.route('/login',methods=['POST'])
def login():
    data= request.json
    email=request.json['email']
    email=str(email)
    pwd=request.json['pwd']
    pwd =str(pwd)
    conn=sqlite3.connect('users1.db')
    #email="cha"
    is_email=0
    t=""
    try:
        match = re.search(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', email, re.I)
        t=match.group()
    except:
        pass
    if t==email:
        is_email=1
        query= " select * from user where email="+'"'+ email+'" ;'
        res =conn.execute(query)
    
    else:
        query= " select * from user where phno="+'"'+email+'"'+";"
        res =conn.execute(query)
    conn.commit()
    data={}
    for line in res:
        data["email"]=str(line[2])
        data["pwd"]=str(line[0])
        data["name"]=str(line[1])
        data["phno"]=str(line[3])
        data["status"]=str(line[4])
        #print(line)
    #print(data)
    if(len(data)==0):
        return make_response(jsonify("user does not exists"),400)
    elif(is_email==1):
        if(data["email"]==email and data["pwd"]==pwd):
            #print(type(data["pwd"]),"=",type(pwd))
            updatestatus(data["email"],data["phno"])
            return make_response(jsonify(data["name"]), 200)
        
    elif(is_email==0):
        if(data["phno"]==email and data["pwd"]==pwd):
            updatestatus(data["email"],data["phno"])
            return make_response(jsonify(data["name"]),200)
    #print(data["email"],"=",email)
   # print(data["pwd"],"=",pwd)
    return make_response(jsonify("invalid credentials"), 400)




@app.route('/predective',methods=['GET'])
def pred():
    rannum=random.randint(1,50)
    conn =sqlite3.connect("users1.db")
    query ="select * from product where id="+str(rannum)+";"
    res=conn.execute(query)
    conn.commit()
    #print(res)
    data={}
    for row in res:
        data["id"]=row[0]
        data["name"]=row[1]
        data["photo"]=row[2]
        data["rating"]=row[3]
        data["category"]=row[4]
        data["desc"]=row[5]
        data["price"]=row[6]
    print(res)
    return make_response(jsonify(data),200)
    #return make_response(jsonify(random.randint(1,2)))


@app.route('/product/<c>',methods=['GET'])
def retdata(c):
    conn =sqlite3.connect("users1.db")
    query ="select * from product where id="+c+";"
    res=conn.execute(query)
    conn.commit()
    #print(len(res))
    data={}
    for row in res:
        data["id"]=row[0]
        data["name"]=row[1]
        data["photo"]=row[2]
        data["rating"]=row[3]
        data["category"]=row[4]
        data["desc"]=row[5]
        data["price"]=row[6]
    return make_response(jsonify(data),200)

@app.route('/product/<cat>/<count>',methods=['GET'])
def retdataforcat(cat,count):
    #rannum=random.randint(1,50)
    conn =sqlite3.connect("users1.db")
    query ="select * from product where category="+"'"+str(cat)+"'"+";"
    query1 ="select * from product where category="+"'"+str(cat)+"'"+";"
    res=conn.execute(query)
    res1=conn.execute(query1)
    conn.commit()
    #print(res)
    data={}
    size=0
    for row in res:
        size=size+1
    print(size)
    if(int(count)>size):
        return make_response(jsonify(data),402)
    i=0
    for row in res1:
        if(i==int(count)):
            data["id"]=row[0]
            data["name"]=row[1]
            data["photo"]=row[2]
            data["rating"]=row[3]
            data["category"]=row[4]
            data["desc"]=row[5]
            data["price"]=row[6]
            print(row)
        i=i+1
    return make_response(jsonify(data),200)

@app.route('/productname',methods=['POST'])
def productname():
    data =request.json
    name=data["name"]
    print(name)
    conn =sqlite3.connect("users1.db")
    query ="select * from product ;"
    res=conn.execute(query)
    conn.commit()
    l=[]
    for row in res:
        if(bool(name.lower() in row[1].lower())):
            l.append([row[1],row[2]])
    ll=[]
    print(l)
    ll.sort(key = lambda x: x[1]) 
    for line in l:
        ll.append(line[0])
    l=[]
    return make_response(jsonify(ll),200)

@app.route('/producttoid',methods=['POST'])
def producttoid():
    data=request.json
    name=data["name"]
    print(name)
    conn =sqlite3.connect("users1.db")
    query ="select id from product where name="+"'"+name+"';"
    res=conn.execute(query)
    for row in res:
        data=row[0]
    return make_response(jsonify(data),200)

if __name__=='__main__':
    app.run(debug=True,port=5000,host="127.0.0.1")