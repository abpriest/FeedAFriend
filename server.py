import time
import psycopg2
import psycopg2.extras
import os
from flask import Flask, render_template, request
app = Flask(__name__)


#def connectToDB():
#  connectionString = 'dbname=music user=postgres password=kirbyk9 host=localhost'
#  connectionString = 'dbname=people user=guy password=12345 host=localhost'
#  print connectionString
#  try:
#    return psycopg2.connect(connectionString)
#  except:
#    print("Can't connect to database")

@app.route('/')
def mainIndex():
    print (time.strftime("%I:%M:%S"))
    now = time.strftime("%c")
    print ("Current time %s"  % now )
    return render_template('index.html')

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

