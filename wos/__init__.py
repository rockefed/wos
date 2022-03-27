from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
#    return render_template('index.html')
    return render_template("index.html")
@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/export')
def export():
    return render_template('export.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')