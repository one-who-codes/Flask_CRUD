from flask import Flask, request ,jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= environ.get('DB_URL')


db=SQLAlchemy(app)

class User(db.Model):
    __tablename__="users"

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)

    def json(self):
        return {'id':self.id, 'username':self.username,'email':self.email}

db.create_all()

#Creating a test route
@app.route('/test',methods=['GET'])
def test():
    return make_response(jsonify({'message':'test route'}),200)


#Creating a user
@app.route('/users',methods=['POST'])
def createUser():
    try:
        data=request.get_json()
        newUser=User(username=data['username'],email=data['email'])
        db.session.add(newUser)
        db.session.commit()
        return make_response(jsonify({'message':'User created successfully'}),201)
    except Exception as e:
        return make_response(jsonify({'message':'Error creating user','exception': str(e)}),500)

# Get all the users
@app.route('/users',methods=['GET'])
def getUser():
    try:
        users=User.query.all()
        return make_response(jsonify([user.json() for user in users]),200)
    except Exception as e:
        return make_response(jsonify({'message':'error getting users','exception':str(e)}),500)

# Get a user by ID
@app.route('/users/<int:id>',methods=['GET'])
def getUserbyID(id):
    try:
        user=User.query.get(id)
        if user:
            return jsonify(user.json())
        else:
            return make_response(jsonify({'message':'user not found'}),404)
    except Exception as e:
        return make_response(jsonify({'message':'error retrieving user','exception':str(e)}),500)

# Update a user by ID
@app.route('/users/<int:id>',methods=['PUT'])
def updateUserbyID(id):
    try:
        user=User.query.get(id)
        if user:
            data=request.get_json()
            user.username=data['username']
            user.email=data['email']
            db.session.commit()
            return jsonify({'message':'user is updated'})
        else:
            return make_response(jsonify({'message':'user not found'}),404)
    except Exception as e:
        return make_response(jsonify({'message':'error updating user'}),500)

# Delete a user by ID
@app.route('/users/<int:id>',methods=['DELETE'])
def delUserbyID(id):
    try:
        user=User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message':'user sucessfully removed'})
        else:
            return make_response(jsonify({'message':'user not found'}),404)
    except Exception as e:
        return make_response(jsonify({'message':'error deleting user','exception':str(e)}),500)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)