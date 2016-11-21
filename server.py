import time
import psycopg2
import psycopg2.extras
import os
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
              return render_template('newsFeed.html', userT = "g") 
            #Incorrect password or not a user
            else:
              fail = 'true'
              print("Invalid username or password!")
              conn.rollback()
              return render_template('login.html', fail = fail)
        except:
            print("Error!")
            conn.rollback()
            return render_template('login.html')
        conn.commit()
    
@app.route('/signup')
def signup():
  return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup2():
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  
  uTaken = 'false'
  noPassMatch = 'false'
  eTaken = 'false'
  noUMW = 'false'
   
  #Error message
  message1 = ''
  
  #Search for username
  query = cur.mogrify("select * from users WHERE username = %s", (request.form['username'], ))
  cur.execute(query)
  out = cur.fetchall()
  userresults = cur.rowcount
  conn.commit()
  
  #Search for email
  query = cur.mogrify("select * from profile WHERE email = %s", (request.form['email'], ))
  cur.execute(query)
  out = cur.fetchall()
  emailresults = cur.rowcount
  conn.commit()
  
  #Get email domain name
  domain1=request.form['email'][-8:]
  print(domain1)
  domain2=request.form['email'][-13:]
  print(domain2)
  
  if(request.form['username']=='' or request.form['password']=='' or request.form['confirmpassword']=='' or request.form['email']=='' or request.form['name']==''):
    message1='Error field is empty'
    print("Error field is empty")
    return render_template('signup.html')
  
  elif (userresults != 0):
    uTaken = 'true'
    message1='Username already taken'
    print("Username already taken")
    return render_template('signup.html', uTaken = uTaken)
    
  #Check for matching confirmation password
  elif(request.form['password'] != request.form['confirmpassword']):
    noPassMatch = 'true'
    message1='Passwords do not match'
    print("Passwords do not match")
    return render_template('signup.html', noPassMatch = noPassMatch)
  
  #Check for taken email
  elif(emailresults != 0):
    message1='Email already being for an account'
    print("Email already being used for an account")
    return render_template('signup.html', eTaken = eTaken)
  
  #Check for UMW email
  elif(domain1 != '@umw.edu' and domain2 != '@mail.umw.edu'):
    noUMW = 'true'
    message1="Not a UMW email"
    print("Not a UMW email")
  elif(domain1 != '@umw.edu' and domain2 != '@mail.umw.edu'):
    message1="Not a UMW email"
    print("Not a UMW email")
    return render_template('signup.html', noPassMatch = noPassMatch)
  
  #Check for taken email
  elif(emailresults != 0):
    eTaken = 'true'
    message1='Email already being for an account'
    print("Email already being used for an account")
    return render_template('signup.html', eTaken = eTaken)
  
  #Check for UMW email
  elif(domain1 != '@umw.edu' and domain2 != '@mail.umw.edu'):
    noUMW = 'true'
    message1="Not a UMW email"
    print("Not a UMW email")
    return render_template('signup.html', noUMW = noUMW)
  
  #Sign up user
  else:  
    try:
      cur.execute("""INSERT INTO profile(name, email, usertype) VALUES(%s, %s, %s)""", 
       (request.form['name'], request.form['email'], request.form['usertype']))
      conn.commit()
      cur.execute("""INSERT INTO users(username, password) VALUES(%s, crypt(%s, gen_salt('bf')))""", 
       (request.form['username'], request.form['password']) )
      conn.commit()
      return render_template('login.html')
  
    except:
      print("ERROR inserting into user")
      print("TRIED: INSERT INTO users(username, password) VALUES(%s, %s)" %
       (request.form['username'], request.form['password']) )
      print("""TRIED: INSERT INTO profile(name, email, usertype, userid) VALUES(%s, %s , %s)""" % 
       (request.form['name'], request.form['email'], request.form['usertype']))
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

