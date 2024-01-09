# REST API Verifikasi Email Menggunakan Code OTP

project ini menggunakan fastapi untuk membuat REST API, mysql sebagai database, sqlalchemy untuk orm, smtplib digunakan untuk mengirim email, dan bcrypt digunakan untuk melakukan hash password

# Installasi

1. Download repo atau bisa juga di clone
2. Masuk ke folder projek yang sudah didownload
3. Buka cmd di dalam folder projek
4. Buat venv dengan menggunakan perintah:
    - python -m venv myenv
5. Masuk ke venv nya dengan menggunakan perintah:
    - myenv\Scripts\activate -> Windows
    - source myenv/bin/activate -> Linux
6. Install dependensi yang ada di requirments.txt dengan perintah:
    - pip install -r requirments.txt
7. Jalankan aplikasi dengan perintah:
    - uvicorn main:app --reload
8. Buka browser lalu masukan url: localhost:8000/docs
9. Jangan lupa aktifkan service mysql anda