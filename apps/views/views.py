from flask import jsonify
from bson import ObjectId
from ..schema.schema import User
from .. import mongo
from ..route.route import main_blueprint,request

@main_blueprint.route('/', methods=["GET"])
def home():
    return jsonify({"msg":" Successfully run"})

# @main_blueprint.route('/come', methods=["GET"])
# def act():                                                           
#     return jsonify({"msgg":"Done!"})


@main_blueprint.route('/users', methods=["GET","POST"])
def get_users():
    if request.method == "GET":
        #Here I am handling Get request 
        users = mongo.db.users.find()
        user_list = [User(user['username'], user['email']).to_dict() for user in users]
        return jsonify(users_list=user_list)
    elif request.method == "POST":
        # Here,I am handling Post request 
        try:
            data = request.get_json()
            new_user = User(username=data['username'], email=data['email'])
            new_user.save_to_db()
            return jsonify(message="User created successfully.")
        except Exception as e:
            return jsonify(error=f"Error creating user: {e}")
        
@main_blueprint.route('/users/<string:task_id>', methods=["GET", "PUT", "DELETE"])
def manage_task(task_id):
    task_object_id = ObjectId(task_id)  # Convert the task_id string to ObjectId
    if request.method == "GET":
        # Handle GET request (fetch a specific task by _id)
        user_data = mongo.db.users.find_one({"_id": task_object_id})
        if user_data:
            user = User(user_data['username'],user_data['email'])
            return jsonify(user.to_dict())
        else:
            return jsonify(error=f"No task found with id {task_id}.")

    elif request.method == "PUT":
        # Handle PUT request (update a task by _id)
        try:
            data = request.get_json()
            updated_data = {"$set": {"email": data.get('email')}}
            result = mongo.db.users.update_one({"_id": task_object_id}, updated_data)
            if result.modified_count > 0:
                return jsonify(message=f"Task with id {task_id} updated successfully.")
            else:
                return jsonify(message=f"No task found with id {task_id}.")
        except Exception as e:
            return jsonify(error=f"Error updating task: {e}")

    elif request.method == "DELETE":
        # Handle DELETE request (delete a task by _id)
        try:
            result = mongo.db.users.delete_one({"_id": task_object_id})
            if result.deleted_count > 0:
                return jsonify(message=f"Task with id {task_id} deleted.")
            else:
                return jsonify(message=f"No task found with id {task_id}.")
        except Exception as e:
            return jsonify(error=f"Error deleting task: {e}")