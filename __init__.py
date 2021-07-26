from flask import Flask




def create_app():
    
    app = Flask("pim_app")
    
    
    app.config.from_mapping(
        DATABASE = "pim"
    )
    
    from . import notes
    app.register_blueprint(notes.bp)
    
    from . import db
    db.init_app(app)
    
   
        
    return app
