from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_title = request.form.get('title')
    if task_title:
        tasks = load_tasks()
        tasks.append({'title': task_title})
        save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
