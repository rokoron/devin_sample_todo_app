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

def migrate_tasks():
    """既存のタスクにIDを付与する"""
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if 'id' not in task:
            task['id'] = i + 1
    save_tasks(tasks)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_title = request.form.get('title')
    if task_title:
        tasks = load_tasks()
        task_id = 1
        if tasks:
            task_id = max(task.get('id', 0) for task in tasks) + 1
        tasks.append({'id': task_id, 'title': task_title})
        save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task.get('id') == task_id:
            del tasks[i]
            save_tasks(tasks)
            break
    return redirect('/')

if __name__ == '__main__':
    migrate_tasks()  # アプリ起動時に既存タスクにIDを付与
    app.run(host='0.0.0.0', port=5000)
