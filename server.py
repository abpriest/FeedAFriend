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

@app.route('/dashboard', methods=['GET', 'POST'])
def dash():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        try:
            session['user']=request.form['username']
            session['pass']=request.form['password']
            print(session['user'])
            print(session['pass'])
            query = cur.mogrify("SELECT * FROM users WHERE username = %s AND password = crypt(%s, password) " , 
                (session['user'], session['pass']))
            cur.execute(query)
            results=cur.fetchall()
            conn.commit()
            print (results)
            if (cur.rowcount==1):
              return render_template('newsFeed.html') 
            else:
              print("Invalid username or password!")
              conn.rollback()
              return render_template('login.html')
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
def login():

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

