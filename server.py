import time
import psycopg2
import psycopg2.extras
import os

import uuid #socket imports -N8
from flask.ext.socketio import SocketIO, emit #socket imports -N8

from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')


socketio = SocketIO(app) #socket -N8


#connects the socket from the server side ##########################################################
@socketio.on('connect')
def socketConnect():
    print 'Connected from server'
    
@socketio.on('sSearch')
def search(findMe):
    print('Looking for ' + findMe)
    
    if findMe == 'Breakfast' or findMe == 'Lunch' or findMe == 'Dinner':
        print(findMe)
        results = searchMealTime(findMe)
    else:
        results = searchUsers(findMe)
  
    if len(results) == 0:
        results = [[-1,'No results']]
        print(results)
    else:
        print(results)
    
    emit('found', results)

def searchMealTime(findMealTime):
    print("looking for meal times")
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    try:
        #print('booyah')
        #query = cur.mogrify("SELECT * FROM users WHERE username = %s" , (findUser))
            
        cur.execute("SELECT mealtype.meal, availability.starttime, availability.endtime, users.username FROM availability JOIN mealtype ON availability.mealtype = mealtype.id JOIN users ON availability.userid = users.id WHERE mealtype.meal = '%s'" % (findMealTime))
        
    except:
        print ('search failed')
        
    results=cur.fetchall()
        
    #print (results)
    
    return(results)
    
def searchUsers(findUser):
    print('Looking for user ' + findUser)
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    try:
        #print('booyah')
        #query = cur.mogrify("SELECT * FROM users WHERE username = %s" , (findUser))
            
        cur.execute("SELECT id, username FROM users WHERE username LIKE '%%%s%%'" % (findUser))
        
    except:
        print ('search failed')
        
    results=cur.fetchall()
        
    #print (results)
    
    return(results)
    
#####################################################################################################
    
def connectToDB():
  connectionString = 'dbname=feedfriend user=student password=mealswipes123 host=localhost'
  print connectionString
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")

@app.route('/home')
def home():
    profinfo=getProf()
    userT=getUserT()
    breakfast=getBreak()
    lunch=getLunch()
    dinner=getDinner()
                
    return render_template('newsFeed.html', userT=userT, breakfast=breakfast, lunch=lunch, dinner=dinner, profinfo=profinfo, username=session['user'])
    

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
                profinfo=getProf()
                userT=getUserT()
                breakfast=getBreak()
                lunch=getLunch()
                dinner=getDinner()
                #return render_template('newsFeed.html', breakfast=breakfast, lunch=lunch, dinner=dinner, profinfo=profinfo, username=session['user'])
                return render_template('newsFeed.html', userT=userT, breakfast=breakfast, lunch=lunch, dinner=dinner, profinfo=profinfo, username=session['user'])
                
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
    
@app.route('/editprofile')
def editpro():
    message1=''
    profinfo=getProf()
    userT=getUserT()
    breakfast=getBreak()
    lunch=getLunch()
    dinner=getDinner()
    return render_template('editpro.html', userT=userT, breakfast=breakfast, lunch=lunch, dinner=dinner, profinfo=profinfo, username=session['user'], message = message1)   

@app.route('/updateprofile', methods=['POST'])
def updatepro():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    #change username
    if(request.form['username'] != '' ):
        print("in username")
        #check for taken username
        cur.execute("SELECT * FROM users WHERE username = %s", (request.form['username'],))
        results=cur.fetchall()
        print(results)
        conn.commit()
        
        if(cur.rowcount == 0):
            results=cur.mogrify("UPDATE users SET username = %s WHERE username = %s", 
                (request.form['username'], session['user']))
            cur.execute(results)
            print(results)
            conn.commit()
            session['user']=request.form['username']
        else:
            profinfo=getProf()
            userT=getUserT()
            breakfast=getBreak()
            lunch=getLunch()
            dinner=getDinner()
            message1=" Username taken."
            return render_template('editpro.html', userT=userT, breakfast=breakfast, lunch=lunch, dinner=dinner, profinfo=profinfo, username=session['user'], message = message1)
    
    #change name
    if(request.form['name'] != ''):
        print("in name")
        results=cur.mogrify("UPDATE profile SET name = %s WHERE userid = (SELECT id FROM users WHERE username = %s)", 
                (request.form['name'], session['user']))
        cur.execute(results)
        
        conn.commit()
        print(results)
    #change password
    if(request.form['confirmpassword'] != '' and request.form['newpassword'] != '' ):
        print("in password")
        if(request.form['confirmpassword'] == request.form['newpassword']):
            results=cur.mogrify("UPDATE users SET password = crypt(%s, gen_salt('bf')) WHERE username = %s", 
                (request.form['newpassword'], session['user']))
            cur.execute(results)
            print(results)
            conn.commit()
            print(results)
        else:
            profinfo=getProf()
            userT=getUserT()
            breakfast=getBreak()
            lunch=getLunch()
            dinner=getDinner()
            message1=" Passwords do not match."
            return render_template('editpro.html', userT=userT, breakfast=breakfast, lunch=lunch, dinner=dinner, profinfo=profinfo, username=session['user'], message = message1)
    
    #change usertype
    if(request.form['usertype'] != ''):
        print("in usertype")
        results=cur.mogrify("UPDATE profile SET usertype = (SELECT id FROM usertype WHERE userT = %s) WHERE userid = (SELECT id FROM users WHERE username = %s)", 
                (request.form['usertype'], session['user']))
        print(results)
        cur.execute(results)
        conn.commit()
        
    
    profinfo=getProf()
    userT=getUserT()
    breakfast=getBreak()
    lunch=getLunch()
    dinner=getDinner()
                
    return render_template('newsFeed.html', userT=userT, breakfast=breakfast, lunch=lunch, dinner=dinner, profinfo=profinfo, username=session['user'])
    
@app.route('/editavailability')
def editavail():
    return render_template('editavail.html')

@app.route('/updateavailability', methods=['POST'])
def updateavail():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute("SELECT * FROM availability WHERE userid = (SELECT id FROM users WHERE username = %s)", (session['user'],))
    cur.fetchall()
    conn.commit()
    if(cur.rowcount != 0):
        cur.execute("DELETE FROM availability WHERE userid = (SELECT id FROM users WHERE username = %s)", (session['user'],))
        conn.commit()
        
    if(request.form['bstart'] != '' and request.form['bend'] != ''):
        cur.execute("""INSERT INTO availability(mealtype, starttime, endtime, userid) VALUES((SELECT id FROM mealtype WHERE meal = 'Breakfast'), %s, %s, (SELECT id FROM users WHERE username = %s))""", 
            (request.form['bstart'], request.form['bend'], session['user']))
        conn.commit()
        
    if(request.form['lstart'] != '' and request.form['lend'] != ''):
        cur.execute("""INSERT INTO availability(mealtype, starttime, endtime, userid) VALUES((SELECT id FROM mealtype WHERE meal = 'Lunch'), %s, %s, (SELECT id FROM users WHERE username = %s))""", 
            (request.form['lstart'], request.form['lend'], session['user']))
        conn.commit()
        
    if(request.form['dstart'] != '' and request.form['dend'] != ''):
        cur.execute("""INSERT INTO availability(mealtype, starttime, endtime, userid) VALUES((SELECT id FROM mealtype WHERE meal = 'Dinner'), %s, %s, (SELECT id FROM users WHERE username = %s))""", 
            (request.form['dstart'], request.form['dend'], session['user']))
        conn.commit()
    
    profinfo=getProf()
    userT=getUserT()
    breakfast=getBreak()
    lunch=getLunch()
    dinner=getDinner()
                
    return render_template('newsFeed.html', userT=userT, breakfast=breakfast, lunch=lunch, dinner=dinner, profinfo=profinfo, username=session['user'])

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
      cur.execute("""INSERT INTO profile(name, email, usertype, userid) VALUES(%s, %s, (SELECT id FROM usertype WHERE userT = %s), (SELECT id FROM users WHERE username = %s))""", 
       (request.form['name'], request.form['email'], request.form['usertype'], request.form['username']))
      conn.commit()
      return render_template('login.html')
  
    except:
      print("ERROR inserting into user")
      print("TRIED: INSERT INTO users(username, password) VALUES(%s, %s)" %
       (request.form['username'], request.form['password']) )
      print("""TRIED: INSERT INTO profile(name, email, usertype, userid) VALUES(%s, %s, (SELECT id FROM usertype WHERE userT = %s), (SELECT id FROM users WHERE username = %s))""" % 
       (request.form['name'], request.form['email'], request.form['usertype'], request.form['username']))
      conn.rollback()
      return render_template('signup.html')
    conn.commit()

#print (time.strftime("%I:%M:%S"))
#now = time.strftime("%c")
#print ("Current time %s"  % now )'''

def getProf():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    try:
        cur.execute("SELECT * FROM profile WHERE userid = (SELECT id from users WHERE username = %s)", (session['user'], ))
        conn.commit()
        profileinfo = cur.fetchall()
        print(profileinfo)
        return profileinfo
        
    except:
        print("Could not retrieve profile information.")
        
def getUserT():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    try:
        cur.execute("SELECT userT FROM usertype WHERE id = (SELECT usertype FROM profile WHERE userid = (SELECT id FROM users WHERE username = %s))", (session['user'],))
        userT=cur.fetchall()
        conn.commit()
        print(userT)
        return(userT) #There's a bug somewhere in this function
        
    except:
        print("Could not retrieve userT information.")
        
def getBreak():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    try:
        cur.execute("SELECT starttime, endtime FROM availability WHERE mealtype = (SELECT id FROM mealtype WHERE meal = 'Breakfast') AND userid = (SELECT id FROM users WHERE username = %s) " , 
                    (session['user'], ))
        breakfast = cur.fetchall()
        conn.commit()
                
        if(cur.rowcount==0):
            print("btest")
            breakfast = ''
        else:
            print(breakfast)
        return breakfast
        
    except:
        print("Could not retrieve breakfast information.")

def getLunch():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    try:
        cur.execute("SELECT starttime, endtime FROM availability WHERE mealtype = (SELECT id FROM mealtype WHERE meal = 'Lunch') AND userid = (SELECT id FROM users WHERE username = %s) " , 
                    (session['user'], ))
        lunch = cur.fetchall()
        conn.commit()
                
        if(cur.rowcount==0):
            print("ltest")
            lunch = ''
        else:
            print(lunch)
        return lunch
    except:
        print("Could not retrieve lunch information.")
        
def getDinner():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    try:
        cur.execute("SELECT starttime, endtime FROM availability WHERE mealtype = (SELECT id FROM mealtype WHERE meal = 'Dinner') AND userid = (SELECT id FROM users WHERE username = %s) " , 
                    (session['user'], ))
        dinner = cur.fetchall()
        conn.commit()
                
        if(cur.rowcount==0):
            print("dtest")
            dinner = ''
        else:
            print(dinner)
        return dinner
    except:
        print("Could not retrieve dinner information.")

@app.route('/')
def home2():

 #print (time.strftime("%I:%M:%S"))
 #now = time.strftime("%c")
 #print ("Current time %s"  % now )
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
    socketio.run(app,host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
    #app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)


