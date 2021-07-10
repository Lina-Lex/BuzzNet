# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView

# initializing our app
app = Flask(__name__)
app.debug = True

# Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 

# Modules
db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __init__(self, username, email):
      self.username = username
      self.email = email

    def __repr__(self):
        return '<User %r>' % self.id

class UserObject(SQLAlchemyObjectType):
   class Meta:
       model = User
       interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserObject)

schema = graphene.Schema(query=Query)

# Routes
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

@app.route('/')
def index():
    return 'Welcome to your Api'

if __name__ == '__main__':
     app.run()
