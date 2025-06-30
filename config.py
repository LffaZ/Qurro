from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_API_KEY = os.getenv('SUPABASE_KEY')
