import os
import hashlib
import binascii
from moviepy.editor import VideoFileClip
from werkzeug.utils import secure_filename
from datetime import datetime
import random
import string
import simplejpeg
import base64
from werkzeug.datastructures import FileStorage
from apps.data_static import provinces_data

# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mkv', 'mov'}


def _8bit_to_base64(frame,quality=50):
	frame_buffer =  simplejpeg.encode_jpeg(image=frame,quality=quality,colorspace='BGR',fastdct=True)
	frame_64 = base64.encodebytes(frame_buffer).decode("utf-8")
	return frame_64

def get_province_name(id):
    province_name = None  # Inisialisasi dengan None
    for province in provinces_data:
        if province['id'] == int(id):
            province_name = province['name']
            break

    return province_name  # Mengembalikan None jika tidak ditemukan


# FILE MANAGEMENT

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_string = ''.join(random.choice(string.ascii_letters) for _ in range(3))
    return f"{timestamp}_{random_string}.{extension}"


def check_video_size(video):
    max_size = 300 * 1024 * 1024  # 100 MB in bytes
    if isinstance(video, FileStorage):
        video.seek(0, os.SEEK_END)  # Pindah ke akhir file
        file_size = video.tell()  # Dapatkan ukuran file
        video.seek(0)  # Kembali ke awal file
        if file_size > max_size:
            return False
    return True

def compress_video(video, upload_folder, max_size=20):
    try:
        filename = secure_filename(video.filename)
        if allowed_file(filename):
            check_size = check_video_size(video)
            if check_size:
                new_filename = generate_unique_filename(filename)

                video_path = os.path.join(upload_folder, new_filename)
                video.save(video_path)

                video_clip = VideoFileClip(video_path)
                
                file_size = video_clip.fps * video_clip.duration / (1024 * 1024)

                if file_size > max_size:
             
                    new_file_path = os.path.join(upload_folder, "compressed_" + new_filename)


                    compression_factor = max_size / file_size
                    # Kompress video dengan faktor kompresi
                    compressed_clip = video_clip.fl(compression_factor)

                    compressed_clip.write_videofile(new_file_path)

                    # Hapus file video asli
                    os.remove(video_path)

                    # Ubah nama file kompresi ke nama asli
                    os.rename(new_file_path, video_path)

                    return True, video_path
                else:
                    return True, video_path
            else:
               return False, 'File to large, max: 100mb!' 
        else:
            return False, 'Format file not compatible, only (mp4, avi, mkv, mov)!'

    except Exception as e:
        print("===================MASUK6==============")
        print(e)
        return False, 'Failed Upload, Please try again!'

