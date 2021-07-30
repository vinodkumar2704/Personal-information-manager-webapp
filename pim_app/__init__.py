from flask import Flask




def create_app():
    
    app = Flask("pim_app")
    
    
    app.config.from_mapping(
        DATABASE = "postgres://wgklquffwkngqd:28bbbd590fd7a474b644e1eb03bd28e3e6ffedc41b61faa779e5aec27f29a631@ec2-54-145-185-178.compute-1.amazonaws.com:5432/daiss07i4ejvib"
    )
    
    from . import notes
    app.register_blueprint(notes.bp)
    
    from . import db
    db.init_app(app)
    
   
        
    return app
