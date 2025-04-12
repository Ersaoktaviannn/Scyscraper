from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import time
import csv
import os
import getpass
import pyautogui

def setup_driver():
    """Setup WebDriver dengan konfigurasi yang tepat"""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Tetapkan preferensi download
    prefs = {
        "download.default_directory": os.path.abspath("./downloads"),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    
    # Uncomment baris berikut jika ingin melihat browser
    # options.add_argument('--headless')
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    return driver

def login(driver, username, password):
    """Login ke portal Telkom"""
    print("🔐 Mencoba login ke portal Telkom...")
    
    try:
        # Buka halaman login
        driver.get("https://newgobeyond.mytens.co.id/login")
        time.sleep(3)  # Tunggu halaman dimuat
        
        # Periksa apakah halaman login sudah terbuka
        if "login" not in driver.current_url.lower():
            print("⚠️ Tidak diarahkan ke halaman login")
            return False
        
        # Tangkap screenshot halaman login
        driver.save_screenshot("login_page.png")
        print("📷 Screenshot halaman login disimpan")
        
        # Cari dan isi field username/email
        try:
            username_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text'], input[type='email'], input[name='username'], input[name='email']"))
            )
            username_field.clear()
            username_field.send_keys(username)
            print("✅ Mengisi username")
        except Exception as e:
            print(f"❌ Error saat mengisi username: {str(e)}")
            return False
        
        # Cari dan isi field password
        try:
            password_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']"))
            )
            password_field.clear()
            password_field.send_keys(password)
            print("✅ Mengisi password")
        except Exception as e:
            print(f"❌ Error saat mengisi password: {str(e)}")
            return False
        
        # Cari dan klik checkbox Syarat dan Ketentuan & Kebijakan Privasi
        try:
            checkbox_selectors = [
                "//input[@type='checkbox']",
                "//label[contains(text(), 'Syarat dan Ketentuan') or contains(text(), 'Kebijakan Privasi')]//preceding::input[@type='checkbox'][1]",
                "//label[contains(., 'Syarat dan Ketentuan') or contains(., 'Kebijakan Privasi')]//input[@type='checkbox']",
                "//div[contains(@class, 'checkbox') or contains(@class, 'form-check')]//input",
                "//span[contains(text(), 'Saya menyetujui')]/preceding::input[@type='checkbox'][1]",
                "//span[contains(text(), 'Saya menyetujui')]/parent::*/preceding::input[@type='checkbox'][1]"
            ]
            
            checkbox_found = False
            for selector in checkbox_selectors:
                checkboxes = driver.find_elements(By.XPATH, selector)
                if checkboxes:
                    for checkbox in checkboxes:
                        try:
                            if not checkbox.is_selected():
                                checkbox.click()
                                checkbox_found = True
                                print("✅ Klik checkbox Syarat dan Ketentuan & Kebijakan Privasi")
                                break
                        except:
                            try:
                                driver.execute_script("arguments[0].click();", checkbox)
                                checkbox_found = True
                                print("✅ Klik checkbox dengan JavaScript")
                                break
                            except:
                                continue
                if checkbox_found:
                    break
            
            if not checkbox_found:
                label_selectors = [
                    "//label[contains(text(), 'Syarat dan Ketentuan') or contains(text(), 'Kebijakan Privasi')]",
                    "//span[contains(text(), 'Saya menyetujui')]",
                    "//div[contains(text(), 'Saya menyetujui')]",
                    "//p[contains(text(), 'Saya menyetujui')]"
                ]
                
                for selector in label_selectors:
                    labels = driver.find_elements(By.XPATH, selector)
                    if labels:
                        for label in labels:
                            try:
                                label.click()
                                checkbox_found = True
                                print("✅ Klik label Syarat dan Ketentuan & Kebijakan Privasi")
                                break
                            except:
                                try:
                                    driver.execute_script("arguments[0].click();", label)
                                    checkbox_found = True
                                    print("✅ Klik label dengan JavaScript")
                                    break
                                except:
                                    continue
                    if checkbox_found:
                        break
            
            if not checkbox_found:
                print("⚠️ Tidak dapat menemukan atau klik checkbox Syarat dan Ketentuan")
        except Exception as e:
            print(f"⚠️ Error saat mencoba klik checkbox: {str(e)}")
        
        # Klik tombol login
        time.sleep(1)
        login_buttons = driver.find_elements(By.XPATH, 
            "//button[contains(text(), 'Login') or contains(text(), 'Sign in') or contains(text(), 'Masuk')]")
        
        if not login_buttons:
            login_buttons = driver.find_elements(By.CSS_SELECTOR, 
                "button[type='submit'], input[type='submit']")
        
        if login_buttons:
            login_buttons[0].click()
            print("✅ Klik tombol login")
        else:
            print("❌ Tidak dapat menemukan tombol login")
            return False
        
        # Tunggu proses login selesai
        time.sleep(5)
        
        # Periksa apakah login berhasil
        if "login" in driver.current_url.lower():
            print("❌ Login gagal - masih di halaman login")
            driver.save_screenshot("login_failed.png")
            return False
        
        print("✅ Login berhasil")
        driver.save_screenshot("after_login.png")
        return True
        
    except Exception as e:
        print(f"❌ Error saat login: {str(e)}")
        driver.save_screenshot("login_error.png")
        return False

def navigate_to_dashboard(driver):
    """Navigasi ke halaman dashboard Rising Star"""
    print("🔄 Navigasi ke halaman dashboard Rising Star...")
    
    try:
        driver.get("https://newgobeyond.mytens.co.id/dashboard-rising-star?tab=bintang-1")
        time.sleep(5)
        driver.save_screenshot("dashboard_page.png")
        
        if "dashboard-rising-star" in driver.current_url.lower():
            print("✅ Berhasil navigasi ke halaman dashboard")
            return True
        else:
            print("❌ Gagal navigasi ke halaman dashboard")
            return False
            
    except Exception as e:
        print(f"❌ Error saat navigasi: {str(e)}")
        return False
    

def scroll_to_each_section(driver):
    """Fungsi untuk scroll ke setiap bagian penting dengan pendekatan yang lebih fleksibel"""
    print("🔍 Melakukan scroll ke setiap bagian...")
    try:
        # Screenshot awal
        driver.save_screenshot("before_scrolling.png")
        
        # Coba beberapa pendekatan untuk menemukan elemen dengan timeout lebih lama
        timeout = 20  # Meningkatkan timeout menjadi 20 detik
        
        # Pendekatan 1: Coba XPath yang diberikan
        # Pendekatan 2: Coba mencari berdasarkan teks
        # Pendekatan 3: Coba mencari berdasarkan ID parsial
        
        # List section untuk di-scroll
        sections = [
            {
                "name": "Witel Performance",
                "xpath_list": [
                    '//*[@id="slice_2082-controls"]',
                    '//*[contains(@id, "slice") and contains(@id, "2082")]',
                    '//div[contains(text(), "Witel Performance") or .//h3[contains(text(), "Witel Performance")]]'
                ]
            },
            {
                "name": "HOTD Performance",
                "xpath_list": [
                    '//*[@id="slice_2084-controls"]/div',
                    '//*[@id="slice_2084-controls"]',
                    '//*[contains(@id, "slice") and contains(@id, "2084")]',
                    '//div[contains(text(), "HOTD Performance") or .//h3[contains(text(), "HOTD Performance")]]'
                ]
            },
            {
                "name": "AM Performance",
                "xpath_list": [
                    '//*[@id="slice_2083-controls"]/div',
                    '//*[@id="slice_2083-controls"]',
                    '//*[contains(@id, "slice") and contains(@id, "2083")]',
                    '//div[contains(text(), "AM Performance") or .//h3[contains(text(), "AM Performance")]]'
                ]
            }
        ]
        
        for section in sections:
            print(f"  ↓ Scroll ke {section['name']}")
            
            # Tambahkan JavaScript fallback untuk mencari by text jika XPath gagal
            js_fallback = f"""
                var found = false;
                // Metode 1: Coba cari elemen dengan text {section['name']}
                var elements = document.querySelectorAll('*');
                for (var i = 0; i < elements.length; i++) {{
                    if (elements[i].innerText && elements[i].innerText.includes('{section['name']}')) {{
                        elements[i].scrollIntoView({{behavior: 'smooth', block: 'start'}});
                        found = true;
                        break;
                    }}
                }}
                
                // Metode 2: Coba cari berdasarkan ID jika metode 1 gagal
                if (!found) {{
                    var idPrefix = 'slice';
                    var elements = document.querySelectorAll('[id^="' + idPrefix + '"]');
                    if (elements.length > 0) {{
                        elements[0].scrollIntoView({{behavior: 'smooth', block: 'start'}});
                        found = true;
                    }}
                }}
                
                return found;
            """
            
            element_found = False
            
            # Coba setiap XPath
            for xpath in section['xpath_list']:
                try:
                    print(f"    Mencoba XPath: {xpath}")
                    element = WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", element)
                    element_found = True
                    print(f"    ✅ Berhasil menemukan elemen {section['name']} dengan XPath")
                    break
                except Exception as e:
                    print(f"    ⚠️ Tidak dapat menemukan dengan XPath {xpath}: {str(e)}")
                    continue
            
            # Jika semua XPath gagal, coba dengan JavaScript fallback
            if not element_found:
                print(f"    Mencoba dengan JavaScript fallback untuk {section['name']}")
                found = driver.execute_script(js_fallback)
                if found:
                    print(f"    ✅ Berhasil menemukan elemen {section['name']} dengan JavaScript")
                    element_found = True
                else:
                    print(f"    ⚠️ Tidak dapat menemukan {section['name']} dengan JavaScript")
            
            # Tangkap screenshot apakah berhasil atau tidak
            time.sleep(2)
            driver.save_screenshot(f"{section['name'].lower().replace(' ', '_')}_view.png")
        
        # Scroll kembali ke atas untuk melihat keseluruhan
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        driver.save_screenshot("back_to_top.png")
        
        print("✅ Scrolling ke setiap bagian selesai")
        return True
    except Exception as e:
        print(f"❌ Error saat scrolling: {str(e)}")
        driver.save_screenshot("scrolling_error.png")
        return False   
    
def main():
    """Improved main function with direct flow from login to extraction without reloading dashboard"""
    driver = None
    
    try:
        driver = setup_driver()
        username = "960104"
        password = "Tbpe1025"
        
        # 1. Login
        if not login(driver, username, password):
            print("❌ Login gagal pada percobaan awal")
            return
        
        # 2. Navigasi ke dashboard hanya sekali
        if not navigate_to_dashboard(driver):
            print("❌ Gagal navigasi ke dashboard")
            return
        
        print("⏳ Menunggu halaman dashboard dimuat sepenuhnya (7 detik)...")
        time.sleep(7)
                
        # 3. Scroll ke setiap bagian untuk memastikan semuanya dimuat
        if not scroll_to_each_section(driver):
            print("⚠️ Gagal scroll ke bagian-bagian penting, melanjutkan dengan tampilan saat ini")
        
        print("⏳ Menunggu setelah scrolling (3 detik)...")
        time.sleep(3)
        
        # Persiapkan direktori download
        download_dir = os.path.abspath("./downloads")
        os.makedirs(download_dir, exist_ok=True)
               
    except Exception as e:
        print(f"❌ Error dalam fungsi main: {str(e)}")
        if driver:
            driver.save_screenshot("main_error.png")
    finally:
        if driver:
            print("🔚 Menutup browser")
            driver.quit()

if __name__ == "__main__":
    main()