from flask import *  
app = Flask(__name__)  

@app.route('/')  
def chartwithXY():
    data = { 10: 30, 20: 40, 30: 50, 40:70, 50: 80 }  
    return render_template('index.html',data=data) 


if __name__ == '__main__':  
   app.run()  