# DorokDork
DorokDork adalah alat Google Mass Dorker yang dikembangkan menggunakan Python3 untuk melakukan dorking secara massal melalui Google. Alat ini dirancang untuk membantu Anda menemukan domain yang relevan berdasarkan kata kunci (dork) yang Anda masukkan. Script ini secara otomatis menyaring hasil untuk menghindari duplikasi dan menghilangkan domain yang tidak diinginkan.

## Fitur
- Melakukan dorking menggunakan banyak kata kunci sekaligus.
- Secara otomatis menghindari duplikasi hasil pencarian.
- Menyaring domain yang tidak diinginkan dari hasil pencarian.
- Ketika terkena captcha, maka akan membuka browser menggunakan selenium (tentu anda yang harus solved-in captchanya, hehe)

## Persiapan
Sebelum menggunakan script ini, pastikan Anda telah menjalankan perintah berikut, dan jangan lupa menggunakan sudo jika diperlukan.

```bash
apt install python3
apt install python3-pip
pip3 install requests fake-useragent colorama selenium beautifulsoup4
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
sudo mv chromedriver /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
python3 dorokdork.py
```
DorokDork sangat cocok bagi Anda yang ingin melakukan dorking secara massal tanpa perlu melakukannya satu per satu, terutama saat menghadapi CAPTCHA yang sulit.

## Disclaimer
Anda bebas menggunakan alat ini, namun Anda bertanggung jawab penuh atas penggunaan dan konsekuensi dari penggunaan alat ini. Pengembang tidak bertanggung jawab atas kerugian atau masalah apa pun yang mungkin terjadi akibat penggunaan alat ini.
