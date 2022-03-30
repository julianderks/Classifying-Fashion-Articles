import os
from flask import Flask, url_for
from blueprints.main.views import main
from blueprints.about.views import about
from blueprints.classifier.views import classifier

# $ export CONFIGURATION_SETUP="config.DevelopmentConfig"

def create_app():
    app = Flask(__name__)    

    #  Get config settings
    environment_configuration = os.environ['CONFIGURATION_SETUP']
    app.config.from_object(environment_configuration)
    # setup all our dependencies
    # database.init_app(app)
    # commands.init_app(app)
    
    # register blueprint
    app.register_blueprint(main)
    app.register_blueprint(about)
    app.register_blueprint(classifier)

    return app

if __name__ == "__main__":
    app = create_app()
    print(app.url_map)
    app.run()

