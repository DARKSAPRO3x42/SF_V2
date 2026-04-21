from flask import Flask, render_template
import sys

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('missing.html')

if __name__ == '__main__':
    app.run(port=5005)
