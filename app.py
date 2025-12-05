from flask import Flask, request, jsonify
from models.task import Task
app = Flask(__name__)

tasks = []
task_id_counter = 1

#Cria uma task
@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()
    new_task = Task(id=task_id_counter, title=data['title'], description=data.get("description", ""), completed=False)
    task_id_counter += 1
    tasks.append(new_task)
    for task in tasks:
        print(task)
    return jsonify({"Message": "Task Created"})

#Obtém todas as tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    output = {"tasks": [task.to_dict() for task in tasks],
              "total": len(tasks)
              }
    return jsonify(output)

#Obtem uma task pelo ID
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task_by_id(id):
    for task in tasks:
        if task.id == id:
            return jsonify(task.to_dict())
    return jsonify({"message": "Task not found"}), 404
    
#Atualiza uma task pelo ID
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    
    if task == None:
        return jsonify({"message": "Task not found"}), 404

    req_data = request.get_json()
    task.completed = req_data.get("completed", task.completed)
    task.title = req_data.get("title", task.title)
    task.description = req_data.get("description", task.description)
    return jsonify({"Message": "Task Updated"})

#Deleta uma task pelo ID
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    for i, task in enumerate(tasks):
        if id == task.id:
            tasks.pop(i)
            return jsonify({"message": "Task deleted"})
    return jsonify({"message": "Task not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)