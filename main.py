from flask import Flask, jsonify, request
from __init__ import create_app, db
from models import Project
from datetime import datetime

app = create_app()

# Маршрут для просмотра поля active конкретного проекта
@app.route("/project/is_naeb/<int:id>")
def is_active(id):
    project = Project.query.get(id)
    if project:
        return jsonify({"id": project.id, "name": project.name, "active": project.active})
    else:
        return jsonify({"error": "Project not found"}), 404

# Маршрут для изменения поля active конкретного проекта
@app.route("/project/change_is_naeb/<int:id>", methods=['POST'])
def change_is_active(id):
    project = Project.query.get(id)
    if project:
        new_status = not project.active
        if new_status is not None:
            project.active = new_status
            project.updated_at = datetime.utcnow()
            db.session.commit()
            return jsonify({"id": project.id, "name": project.name, "active": project.active})
        else:
            return jsonify({"error": "Invalid data"}), 400
    else:
        return jsonify({"error": "Project not found"}), 404

# Маршрут для просмотра всех проектов и их состояния
@app.route("/project/all", methods=['GET'])
def all_projects():
    projects = Project.query.all()
    projects_list = [{"id": project.id, "name": project.name, "active": project.active} for project in projects]
    return jsonify(projects_list)

# Маршрут для создания нового проекта
@app.route("/project/create", methods=['POST'])
def create_project():
    data = request.json
    name = data.get('name', None)

    if not name:
        return jsonify({"error": "Project name is required"}), 400

    existing_project = Project.query.filter_by(name=name).first()
    if existing_project:
        return jsonify({"error": "Project with this name already exists"}), 400

    new_project = Project(name=name)
    db.session.add(new_project)
    db.session.commit()

    return jsonify({"id": new_project.id, "name": new_project.name, "active": new_project.active}), 201

if __name__ == "__main__":
    app.run(debug=True)
