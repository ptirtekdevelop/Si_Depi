from apps import app, db, socketio
import os


if __name__ == '__main__':
    # Crate a user test with
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.import_name, app.config['DATABASE_FILE'])
    
    with app.app_context():
        db.create_all()
        db.session.commit()
            
    socketio.run(app, host='0.0.0.0', port=5003)
    
        
