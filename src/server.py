from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vbbqfuosshitez:137c3524d10dd1300ab12c71cc3a3c8736d7e290e6a755a466ebb4d15f22a93f@ec2-23-21-46-94.compute-1.amazonaws.com:5432/d3at405877pcav'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api = Api(app)
db = SQLAlchemy(app)

parser = reqparse.RequestParser()
parser.add_argument('author')
parser.add_argument('text')
parser.add_argument('id')


def dateTimeToString(commentObject):
	newObject = []
	for comment in commentObject: 
		newObject.append({
		'id': comment.id,
		'author': comment.author,
		'text':comment.text,
		'created_at': str(comment.created_at),
		'modified_at':str(comment.modified_at)
		})

	return newObject

# Define Models
class Comments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author = db.Column(db.String(80))
	text = db.Column(db.String(255))
	created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
	modified_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class CommentsAPI(Resource):
    def get(self):
    	comments = db.session.query(Comments)
        return dateTimeToString(comments), 200
   
    def post(self):
    	args = parser.parse_args()
    	newComment = Comments(author=args['author'], text=args['text'])
    	db.session.add(newComment)
    	db.session.commit()

    	return {'response':'Success'}, 201

    def put(self):
    	args = parser.parse_args()
    	db.session.query(Comments).filter(Comments.id == int(args['id'])).update({'text':args['text']})
    	db.session.commit()

    	return {'response': 'Comment Successfully Updated'}, 200

    def delete(self):
    	args = parser.parse_args()
    	comment = db.session.query(Comments).filter(Comments.id == int(args['id'])).one()
    	db.session.delete(comment)
    	db.session.commit()

    	return {'response':'Comment Sucessfully Deleted'}, 200



api.add_resource(CommentsAPI, '/api/v1/comments')

if __name__ == "__main__":
    app.run()

