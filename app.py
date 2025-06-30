from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, AudioFile
from supabase_client import get_supabase
from config import Config
import imageio_ffmpeg as ffmpeg
import subprocess
import whisper
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object(Config)
supabase = get_supabase()

db = SQLAlchemy(app)

model = whisper.load_model("base", device="cpu")  # Atau model lainnya dari Whisper

@app.route("/api/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    print(audio_file)
    audio_path = os.path.join("uploads", audio_file.filename)
    print(audio_path)
    audio_file.save(audio_path)

    wav_path = os.path.splitext(audio_path)[0] + ".wav"
    try:
        ffmpeg_exe = ffmpeg.get_ffmpeg_exe()  
        print(f"FFmpeg executable: {ffmpeg_exe}")
        subprocess.run([ffmpeg_exe, "-i", audio_path,"-vn", wav_path], check=True)
        print(f"Audio converted to {wav_path}")
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"FFmpeg conversion failed: {e}"}), 500

    # Jalankan Whisper untuk transkripsi
    result = model.transcribe(wav_path)
    transcription = result['text']
    os.remove(wav_path)
    
    return jsonify({"transcription": transcription})
    # Lakukan perbandingan dengan teks Al-Qur'an (misalnya)
    correct_text = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ"
    similarity = compare_texts(correct_text, transcription)

    return jsonify({
        "transcription": transcription,
        "similarity": similarity * 100
    })

def compare_texts(correct_text, transcription):
    # Fungsi perbandingan sederhana (bisa dikembangkan lebih lanjut)
    return len(set(correct_text) & set(transcription)) / len(set(correct_text))

@app.route('/feat')
def feat():
    audio_files = AudioFile.query.all()
    return render_template('index.html', audio_files=audio_files)

# @app.route('/debug')
# def debug():
#     user = supabase.table('users').select('*').eq('email', 'alifah.zuhrah@gmail.com').single().execute()
#     # user = supabase.table('users').select('*').execute()
#     if user.data:
#         print("Data found:", user.data)
#     elif user.error:
#         print("Error:", user.error)
#     else:
#         return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uid = request.form['uid']
        # uid = 'user001'
        password = request.form['password']
        # password = '12345'

        filter_query = f"email.eq.{uid},username.eq.{uid}"
        user = supabase.table('users').select('*').or_(filter_query).execute()

        if user.data:
            if len(user.data) == 1:
                user.data = user.data[0]
                print(f"Pengguna ditemukan: {user.data['username']}")
            else:
                print(f"Ditemukan {len(user.data)} pengguna, yang mungkin tidak sesuai dengan ekspektasi.")

        if user.data: 
            if user.data['password'] == password:
                session['id'] = user.data['id']
                flash(f'Welcome, {user.data["username"]}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect password', 'danger')
        else:
            flash('User not found', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        flash('You must be logged in to access this page', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['id']
    user = supabase.table('users').select('username').eq('id', user_id).single().execute()

    if user.data:
        username = user.data['username']
        return render_template('homepage.html', username=username)
    else:
        flash('User not found', 'danger')
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    return render_template('profilepage.html')
if __name__ == "__main__":
    app.run(debug=True)
