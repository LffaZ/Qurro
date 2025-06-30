from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AudioFile(db.Model):
    __tablename__ = 'audio_files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    content = db.Column(db.LargeBinary)
    
    def __repr__(self):
        return f"<AudioFile {self.filename}>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)