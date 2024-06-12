from pydub import AudioSegment
import os
import base64
from flask import Flask
from flask_socketio import SocketIO, emit
import speech_recognition as sr
import re

AudioSegment.converter = "D:\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffmpeg = "D:\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffprobe ="D:\\ffmpeg\\bin\\ffprobe.exe"

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return "Server is running"

@socketio.on('audio-stream')
def handle_audio_stream(data):
    try:
        audio_data = base64.b64decode(data['uri'].split(',')[1])
        with open('temp.3gp', 'wb') as f:
            f.write(audio_data)
        convert_audio_to_text('temp.3gp')
    except Exception as e:
        print(f"Error processing audio stream: {e}")

def convert_audio_to_text(file_path):
    recognizer = sr.Recognizer()
    try:
        # Chuyển đổi file .3gp sang .wav
        audio = AudioSegment.from_file(file_path, format="3gp")
        audio.export("temp.wav", format="wav")

        # Sử dụng file .wav đã chuyển đổi để convert
        with sr.AudioFile("temp.wav") as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='vi-VN')
            # print(text)
            # action = process_voice_command(text)
            # print(action)
            # emit('transcription', action)
            emit('transcription', text)

        # Xóa file .wav sau khi convert hoàn tất
        os.remove("temp.wav")
        os.remove("temp.3gp")
    except Exception as e:
        print(f"Error converting audio to text: {e}")

def process_voice_command(text):
    text = text.lower()

    keywords = {
        "đọc": ["đọc", "bắt đầu đọc", "tiếp tục đọc", "đọc tiếp"],
        "dừng": ["dừng", "tạm dừng", "ngừng", "dừng lại"],
        "chuyển": ["chuyển", "đến", "tới", "chuyển đến", "chuyển tới"],
        "trang": ["trang", "page"],
        "chương": ["chương", "chapter"],
        "tìm": ["tìm", "tìm kiếm", "search"],
        "mở": ["mở", "mở sách", "open"],
        "đóng": ["đóng", "đóng sách", "close"],
        "tăng": ["tăng", "lớn hơn", "to hơn"],
        "giảm": ["giảm", "nhỏ hơn", "bé hơn"],
        "tốc độ": ["tốc độ", "tốc độ đọc"],
        "âm lượng": ["âm lượng"],
        "sách": ["sách", "quyển", "cuốn"],
        "thư viện": ["thư viện", "playlist", "danh mục", "lịch sử"]
    }

    result = {
        "action": None,
        "from": None,
        "to": None,
        "object": None,
        "detail": None,
    }

    # Xác định hành động
    for action, words in keywords.items():
        if any(word in text for word in words):
            result["action"] = action
            break

    # Xử lý đặc biệt cho câu lệnh "Tìm sách ..."
    if result["action"] == "tìm" and "sách" in text:
        result["object"] = text.split("tìm sách")[-1].strip()

    # Xác định đối tượng và vị trí cho các hành động khác
    if result["action"] in ["đọc", "chuyển"]:
        if "trang" in text:
            result["object"] = "trang"
        elif "chương" in text:
            result["object"] = "chương"

        # Sử dụng biểu thức chính quy để tìm số trang/chương
        numbers = re.findall(r"\d+", text)
        if numbers:
            result["from"] = int(numbers[0])
            if len(numbers) > 1:
                result["to"] = int(numbers[1])

    # Xác định chi tiết cho hành động "tăng/giảm"
    if result["action"] in ["tăng", "giảm"]:
        if "tốc độ" in text:
            result["detail"] = "tốc độ đọc"
        elif "âm lượng" in text:
            result["detail"] = "âm lượng"

    return result if result["action"] else None

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)