from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# In-memory database (for testing purpose)
users = {}
user_id_counter = 1


class UserList(Resource):
    def get(self):
        """Return all users"""
        return users, 200

    def post(self):
        """Create new user"""
        global user_id_counter
        data = request.get_json()
        if not data or "name" not in data or "email" not in data:
            return {"error": "Name and Email required"}, 400

        users[user_id_counter] = {
            "id": user_id_counter,
            "name": data["name"],
            "email": data["email"]
        }
        user_id_counter += 1
        return users[user_id_counter - 1], 201


class User(Resource):
    def get(self, id):
        """Fetch single user by ID"""
        if id not in users:
            return {"error": "User not found"}, 404
        return users[id], 200

    def put(self, id):
        """Update user details"""
        if id not in users:
            return {"error": "User not found"}, 404

        data = request.get_json()
        users[id].update({
            "name": data.get("name", users[id]["name"]),
            "email": data.get("email", users[id]["email"])
        })
        return users[id], 200

    def delete(self, id):
        """Delete user"""
        if id not in users:
            return {"error": "User not found"}, 404
        deleted_user = users.pop(id)
        return {"message": "User deleted", "user": deleted_user}, 200


# Routes
api.add_resource(UserList, "/users")  # GET, POST
api.add_resource(User, "/users/<int:id>")  # GET, PUT, DELETE

if __name__ == "__main__":
    app.run(debug=True)
