import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Initialise an instance of a SQLAlchemy object
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

def create_app(test_config=None):
     # create the Flask app
    app = Flask(__name__, instance_relative_config=True)
     # configure the Flask app (see later notes on how to generate your own SECRET_KEY)
    app.config.from_mapping(
         SECRET_KEY='08LVvxQkgjg1_0KJy_ILXA',
         # Set the location of the database file called paralympics.sqlite which will be in the app's instance folder
         SQLALCHEMY_DATABASE_URI= "sqlite:///" + os.path.join(app.instance_path, 'paralympics.sqlite'),  
    )

    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///paralympics.db"

    if test_config is None:
         # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
         # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialise the database
    # Make sure you already defined SQLALCHEMY_DATABASE_URI in the app.config
    db.init_app(app)



    with app.app_context():
        # Optionally, create the database tables
        # This will only work once the models are defined

        # This imports the models, the linter will flag warnings!
        from student.flask_paralympics import models

        # If the database file does not exist, it will be created
        # If the tables do not exist, they will be created but does not overwrite or update existing tables
        db.create_all()
        # Replace the above with db.reflect() 


        #db.reflect()

        # Import and use the function to add the data to the database
        # The add_all_data checks if the tables are empty first
        from student.flask_paralympics.add_data import add_all_data
        add_all_data()
        # Not needed if using db.reflect()

        # Register the blueprint
        from student.flask_paralympics.routes import main

        app.register_blueprint(main)

    return app