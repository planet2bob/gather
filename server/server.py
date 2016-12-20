from flask import Flask, render_template
app = Flask(__name__, template_folder='./html')
@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    return render_template('index.html')
#   dump()
#   if request.method == 'POST':
#      return render_template("index.html",result = result)

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)