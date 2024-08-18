import os
import requests
import re
import time
from fake_useragent import UserAgent
from colorama import Fore, init, Style
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Setup warna-warna biar terminal keliatan kece
ua = UserAgent(browsers=['chrome'])
init()
red = Fore.RED
reset = Fore.RESET
green = Fore.GREEN
yellow = Fore.YELLOW
cyan = Fore.CYAN

class Dork:
    result = set()  # Ini buat nampung hasil biar ga double
    blacklist = [
        # Daftar kata-kata yang ga mau kita masukin ke hasil
        "cpcontacts", "www", "smtp", "autodiscover", "mail", "cpanel", "my.id", "google",
        "www.", "gacor", "slot", "hoki", "casino", "88", "77", "ipv6.", ".tr", ".net",
        ".edu", ".uk", "bit.ly", "kemdikbud.go.id", "ibb", "pages.dev", "r2.dev", ".org",
        ".com", "autodiscover.", "google.com", "gstatic.com", "schema.org", "google.co.id",
        "goo.gl", "google", "googleusercontent.com", "w3.org", "ytimg.com", "webmail.", "youtube", 
        "cpanel.", "webdisk.", "cpcalendars.", "cpcontacts.", "mail.", "blogspot", "google"
    ]  # Tambah aja kalo ada kata-kata yang ga mau ikutan ke-save

    def __init__(self):
        self.session = requests.Session()  # Pake session biar enak ngatur cookies sama headers
        # URL search engine yang bakal kita pake
        self.search_engine = [
            "http://google.com/search?q={DorokDorkKeyword}&num=100&start=0",
            "http://google.com/search?q={DorokDorkKeyword}&num=100&start=100",
            "http://google.com/search?q={DorokDorkKeyword}&num=100&start=200",
            "http://www.google.com/search?q={DorokDorkKeyword}&num=100&start=0",
            "http://www.google.com/search?q={DorokDorkKeyword}&num=100&start=100",
            "http://www.google.com/search?q={DorokDorkKeyword}&num=100&start=200"
        ]

    def save_file(self, file_name):
        try:
            if self.result:
                existing_results = set()
                if os.path.exists(file_name):
                    with open(file_name, 'r', encoding='utf8') as f:
                        existing_results.update(f.read().splitlines())

                # Gabungin hasil baru sama yang lama, terus save tanpa duplicate
                final_results = existing_results.union(self.result)
                with open(file_name, 'w', encoding='utf8') as f:
                    f.write('\n'.join(sorted(final_results)) + '\n')
                print(f"{yellow}[{reset}INFO{yellow}]{reset} Hasil tersimpan di {file_name}")
            else:
                print(f"{yellow}[{reset}ERROR{yellow}]{reset} Ga ada hasil yang bisa disimpan.")
        except Exception as e:
            print(f"{yellow}[{reset}ERROR{yellow}]{reset} {e}")

    def openbrowser(self, url):
        # Setup ChromeDriver biar bisa buka browser
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chromedriver_path = "/usr/bin/chromedriver"  # Pastikan path ini bener ke ChromeDriver
        driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)
        driver.get(url)
        input(f"{yellow}[{reset}INFO{yellow}]{reset} Selesaikan CAPTCHA di browser, terus tekan Enter buat lanjut...")
        selenium_cookies = driver.get_cookies()
        for cookie in selenium_cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

        driver.quit()

    def is_valid_domain(self, domain):
        for f in self.blacklist:
            if f in domain:
                return False
        return True

    def search(self, dork, namaresult):
        print(f"{yellow}[{reset}INFO{yellow}]{reset} Lagi dorking pake keyword: {yellow}{dork}{reset}")
        try:
            for searcheng in self.search_engine:
                try:
                    req = self.session.get(
                        searcheng.replace('{DorokDorkKeyword}', dork),
                        headers={'User-Agent': ua.random}
                    ).text
                    if 'captcha' in req:
                        print(f"\n{yellow}[{reset}WARNING{yellow}]{reset} CAPTCHA terdeteksi, buka browser buat nyelesainnya!")
                        self.openbrowser(searcheng.replace('{DorokDorkKeyword}', dork))
                        continue  # Ulangin request setelah CAPTCHA selesai

                    # Ambil semua URL yang ketemu dan bersihin dari protokol (http/https)
                    regx = re.findall(r'https?://[-\w.]+(?:/[-\w./?%&=]*)?', req)
                    cleaned_results = set()
                    for domain in regx:
                        domain = domain.replace("&amp;", "")  # Hapus &amp; dari URL
                        domain_name = re.sub(r'^https?://', '', domain)
                        if self.is_valid_domain(domain_name) and '&' not in domain:  # Cek jika ada & di URL, skip
                            cleaned_results.add(domain)  # Simpan URL lengkapnya

                    if cleaned_results:
                        self.result.update(cleaned_results)  # Simpen hasilnya biar ga double
                        # Langsung save hasilnya ke file
                        self.save_file(namaresult)
                        print(green + '\n'.join(sorted(cleaned_results)) + reset)
                    else:
                        print(f"{yellow}[{reset}INFO{yellow}]{reset} Ga ada domain valid yang ketemu.")
                
                except requests.exceptions.RequestException as e:
                    print(f"\n{yellow}[{reset}ERROR{yellow}]{reset} Ga bisa akses search engine, cek koneksi internet kamu.")
                    input()  # Tunggu sampe user tekan Enter buat lanjut

        except FileNotFoundError:
            print(f"\n{red}[ERROR]:{reset} File search engine ga ketemu.")
            exit()

    def main(self):
        try:
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
            banner = f'''
    ____                    __   ____             _  
   / __ \ Google Mass Dorker /__/ __ \___  _____/ /__
  / / / / __ \/ ___/ __ \/ //_/ / / / __ \/ ___/ //_/
 / /_/ / /_/ / /  / /_/ / ,< / /_/ / /_/ / /  / ,<   
/_____/\____/_/   \____/_/|_/_____/\____/_/  /_/|_| @wongalus7{reset}
'''
            print(banner)
            dork = open(input("[?] Masukin daftar dork (contoh: dork.txt): "), 'r', encoding='utf8').read().splitlines()
            namaresult = input("[?] Nama file hasil (contoh: result.txt): ")
            try:
                for dorksiji in dork:
                    self.search(dorksiji, namaresult)
            except KeyboardInterrupt:
                print(f"\n{yellow}[{reset}WARNING{yellow}]{reset} CTRL+C terdeteksi. Proses dihentikan, nyimpen hasil yang ada.")
                time.sleep(1)
                self.save_file(namaresult)

        except FileNotFoundError:
            print(f"\n{yellow}[{reset}ERROR{yellow}]{reset} File dork ga ketemu.")
            exit()
        except Exception as e:
            print(f"\n{yellow}[{reset}ERROR{yellow}]{reset} {e}")
            pass

if __name__ == "__main__":
    Dork().main()
