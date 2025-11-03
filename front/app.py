from flask import Flask, render_template, request, redirect, flash
import os

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('base/base.html')

@app.errorhandler(404)
def error(e):
   return render_template('404.html'), 404

if __name__ == '__main__':
    app.run("localhost", port= 5000, debug=True)