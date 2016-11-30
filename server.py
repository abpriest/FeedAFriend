import time
import psycopg2
import psycopg2.extras
import os

import uuid #socket imports -N8
from flask.ext.socketio import SocketIO, emit #socket imports -N8

from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

def connectToDB():
  connectionString = 'dbname=feedfriend user=student password=mealswipes123 host=localhost'
  print connectionString
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    fail = 'false'

    if request.method == 'POST':
        try:
            session['user']=request.form['username']
            session['pass']=request.form['password']
            print(session['user'])
            print(session['pass'])
            
            #Check for matching username and password
            query = cur.mogrify("SELECT * FROM users WHERE username = %s AND password = crypt(%s, password) " , 
                (session['user'], session['pass']))
            cur.execute(query)
            results=cur.fetchall()
            conn.commit()
            print (results)
            
            #Check if there is a result 
            if (cur.rowcount==1):
                query = cur.mogrify("SELECT usertype FROM profile WHERE userid = (SELECT id FROM users WHERE username = %s) " , 
                    (session['user'], ))
                print(query)
                cur.execute(query)
                userT=cur.fetchall()
                print(userT)
                conn.commit()
                
                #check for breakfast availability
                cur.execute("SELECT starttime, endtime FROM availability WHERE mealtype = 'b' AND userid = (SELECT id FROM users WHERE username = %s) " , 
                    (session['user'], ))
                breakfast = cur.fetchall()
                conn.commit()
                
                if(cur.rowcount==0):
                    print("btest")
                    breakfast = ''
                else:
                    print(breakfast)
                
                #check for lunch availability    
                cur.execute("SELECT starttime, endtime FROM availability WHERE mealtype = 'l' AND userid = (SELECT id FROM users WHERE username = %s) " , 
                    (session['user'], ))
                lunch = cur.fetchall()
                conn.commit()
                
                if(cur.rowcount==0):
                    print("ltest")
                    lunch = ''
                else:
                    print(lunch)
                
                #check for dinner availability
                cur.execute("SELECT starttime, endtime FROM availability WHERE mealtype = 'd' AND userid = (SELECT id FROM users WHERE username = %s) " , 
                    (session['user'], ))
                dinner = cur.fetchall()
                conn.commit()
                
                if(cur.rowcount==0):
                    print("dtest")
                    dinner = ''
                else:
                    print(dinner)
                
                return render_template('newsFeed.html', userT=userT, breakfast=breakfast, lunch=lunch, dinner=dinner)
                
            #Incorrect password or not a user
            else:
              fail = 'true'
              print("Invalid username or password!")
              conn.rollback()
              return render_template('login.html', fail = fail)
        except:
            print("Error login!")
            conn.rollback()
            return render_template('login.html')
        conn.commit()
    
@app.route('/editavailability')
def editavail():
    return render_template('editavail.html')

@app.route('/updateavailability', methods=['POST'])
def updateavail():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    bstart = request.form['bstart']
    bend = request.form['bend']
    lstart = request.form['lstart']
    lend = request.form['lend']
    dstart = request.form['dstart']
    dend = request.form['dend']
    
    cur.execute("SELECT usertype FROM profile WHERE userid = (SELECT id FROM users WHERE username = %s)", (session['user'],))
    userT=cur.fetchall()
    conn.commit()
    
    cur.execute("SELECT * FROM availability WHERE userid = (SELECT id FROM users WHERE username = %s)", (session['user'],))
    cur.fetchall()
    conn.commit()
    if(cur.rowcount != 0):
        cur.execute("DELETE FROM availability WHERE userid = (SELECT id FROM users WHERE username = %s)", (session['user'],))
        conn.commit()
        
    if(request.form['bstart'] != '' and request.form['bend'] != ''):
        cur.execute("""INSERT INTO availability(mealtype, starttime, endtime, userid) VALUES('b', %s, %s, (SELECT id FROM users WHERE username = %s))""", 
            (bstart, bend, session['user']))
        conn.commit()
        
    if(request.form['lstart'] != '' and request.form['lend'] != ''):
        cur.execute("""INSERT INTO availability(mealtype, starttime, endtime, userid) VALUES('l', %s, %s, (SELECT id FROM users WHERE username = %s))""", 
            (lstart, lend, session['user']))
        conn.commit()
        
    if(request.form['dstart'] != '' and request.form['dend'] != ''):
        cur.execute("""INSERT INTO availability(mealtype, starttime, endtime, userid) VALUES('d', %s, %s, (SELECT id FROM users WHERE username = %s))""", 
            (dstart, dend, session['user']))
        conn.commit()
    
    #check for breakfast availability
    cur.execute("SELECT starttime, endtime FROM availability WHERE mealtype = 'b' AND userid = (SELECT id FROM users WHERE username = %s) " , 
                (session['user'], ))
    breakfast = cur.fetchall()
    conn.commit()
                
    if(cur.rowcount==0):
        print("btest")
        breakfast = ''
    else:
        print(breakfast)
                
    #check for lunch availability    
    cur.execute("SELECT starttime, endtime FROM availability WHERE mealtype = 'l' AND userid = (SELECT id FROM users WHERE username = %s) " , 
                (session['user'], ))
    lunch = cur.fetchall()
    conn.commit()
                
    if(cur.rowcount==0):
        print("ltest")
        lunch = ''
    else:
        print(lunch)
                
    #check for dinner availability
    cur.execute("SELECT starttime, endtime FROM availability WHERE mealtype = 'd' AND userid = (SELECT id FROM users WHERE username = %s) " , 
                (session['user'], ))
    dinner = cur.fetchall()
    conn.commit()
                
    if(cur.rowcount==0):
        print("dtest")
        dinner = ''
    else:
        print(dinner)
                
    
    return render_template('newsFeed.html', userT=userT, breakfast=breakfast, lunch=lunch, dinner=dinner)

@app.route('/signup')
def signup():
  return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup2():
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  
  empty = 'false'
  uTaken = 'false'
  noPassMatch = 'false'
  eTaken = 'false'
  noUMW = 'false'
   
  #Error message
  message1 = ''
  
  #Search for username
  query = cur.mogrify("select * from users WHERE username = %s", (request.form['username'], ))
  cur.execute(query)
  cur.fetchall()
  userresults = cur.rowcount
  conn.commit()
  
  #Search for email
  query = cur.mogrify("select * from profile WHERE email = %s", (request.form['email'], ))
  cur.execute(query)
  cur.fetchall()
  emailresults = cur.rowcount
  conn.commit()
  
  #Get email domain name
  domain1=request.form['email'][-8:]
  print(domain1)
  domain2=request.form['email'][-13:]
  print(domain2)
  
  if(request.form['username']=='' or request.form['password']=='' or request.form['confirmpassword']=='' or request.form['email']=='' or request.form['name']==''):
    message1='Error field is empty'
    empty = 'true'
    print(message1)
    return render_template('signup.html', empty = empty)
  
  elif (userresults != 0):
    uTaken = 'true'
    message1='Username already taken'
    print(message1)
    return render_template('signup.html', uTaken = uTaken)
    
  #Check for matching confirmation password
  elif(request.form['password'] != request.form['confirmpassword']):
    noPassMatch = 'true'
    message1='Passwords do not match'
    print(message1)
    return render_template('signup.html', noPassMatch = noPassMatch)
  
  #Check for taken email
  elif(emailresults != 0):
    message1='Email already being for an account'
    print(message1)
    return render_template('signup.html', eTaken = eTaken)
  
  #Check for UMW email
  elif(domain1 != '@umw.edu' and domain2 != '@mail.umw.edu'):
    noUMW = 'true'
    message1="Not a UMW email"
    print(message1)
    return render_template('signup.html', noUMW = noUMW)

  #Sign up user
  else:  
    try:
      cur.execute("""INSERT INTO users(username, password) VALUES(%s, crypt(%s, gen_salt('bf')))""", 
       (request.form['username'], request.form['password']) )
      conn.commit()
      cur.execute("""INSERT INTO profile(name, email, usertype, userid) VALUES(%s, %s, %s, (SELECT id FROM users WHERE username = %s))""", 
       (request.form['name'], request.form['email'], request.form['usertype'], request.form['username']))
      conn.commit()
      return render_template('login.html')
  
    except:
      print("ERROR inserting into user")
      print("TRIED: INSERT INTO users(username, password) VALUES(%s, %s)" %
       (request.form['username'], request.form['password']) )
      print("""TRIED: INSERT INTO profile(name, email, usertype, userid) VALUES(%s, %s, %s, (SELECT id FROM users WHERE username = %s))""" % 
       (request.form['name'], request.form['email'], request.form['usertype'], request.form['username']))
      conn.rollback()
      return render_template('signup.html')
    conn.commit()

#print (time.strftime("%I:%M:%S"))
#now = time.strftime("%c")
#print ("Current time %s"  % now )'''

@app.route('/')
def home():

 print (time.strftime("%I:%M:%S"))
 now = time.strftime("%c")
 print ("Current time %s"  % now )
 return render_template('login.html')

#@app.route('/projects')
#def showProj():
#    developing = False
#    return render_template('projects.html', active='projects', dev=developing)
    
#@app.route('/contact', methods=['GET', 'POST'])
#def showContact():
#    conn = connectToDB()
#    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #try:
     #   cur.execute("select name, comment, color, permission from comments")
    #except:
     #   print("Error executing select")
    #results = cur.fetchall()
    
#    if request.method == 'POST':
 #       try:
 #           cur.execute("""INSERT INTO comments (name, comment, color, permission) VALUES ('%s', '%s', %s, %s);""", (request.form['name'], request.form['comment'], request.form['color'], request.fetchall['permission']))
 #       except:
  #          print("ERROR inserting into comments")
  #          print("Tried: INSERT INTO comments (name, comment, color, permission) VALUES ('%s', '%s', %s, %s);" %
 #           (request.form['name'], request.form['comment'], request.form['color'], request.form['permission']) )
 #           conn.rollback()
 #       conn.commit()
     #   x.append(request.form['inp'])
#    try:
#        cur.execute("select name, comment, color, permission from comments")
#    except:
#        print("Error executing select")
#    results = cur.fetchall()
#    print results
#    for r in results:
#        print r['name']

#    conInfo = [{'label': 'Email: ','info': 'n8bitanimations@gmail.com'}, {'label': 'Facebook/Twitter/Instagram: ', 'info': '@n8bitanimations'}, {'label': 'Phone: ','info': '1(234) 567-8899'}, {'label':'Address: ','info': '456 Street City, ST 45236'}]
#    return render_template('contact.html', active='contact', loop = conInfo, coms = results)
    

# start the server
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)

