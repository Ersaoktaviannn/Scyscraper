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
    
def scroll_page(driver, scroll_amount=1000, num_scrolls=5, interval=1.5):
    """Scroll the page down a specified number of times"""
    try:
        print(f"🔄 Scrolling page {num_scrolls} times, {scroll_amount}px each...")
        for i in range(num_scrolls):
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            print(f"✅ Scroll #{i+1}/{num_scrolls} completed")
            time.sleep(interval)  # Wait for content to load
        return True
    except Exception as e:
        print(f"❌ Error saat scrolling: {str(e)}")
        driver.save_screenshot("scroll_error.png")
        return False

def scroll_to_hotd_performance(driver, max_attempts=5):
    """Improved function to scroll to and interact with the HOTD Performance section"""
    print("🔍 Trying to locate and access HOTD Performance section...")
    
    # Save initial screenshot
    driver.save_screenshot("before_hotd_search.png")
    
    # Method 1: Try JavaScript direct access to the HOTD element
    try:
        print("Method 1: Direct JavaScript access to HOTD element")
        # Try to find the HOTD element by header text
        script = """
            var elements = document.querySelectorAll('h1, h2, h3, h4, h5, h6, div, span, th');
            for (var i = 0; i < elements.length; i++) {
                if (elements[i].innerText && elements[i].innerText.includes('HOTD Performance')) {
                    elements[i].scrollIntoView({behavior: 'smooth', block: 'center'});
                    return true;
                }
            }
            return false;
        """
        found = driver.execute_script(script)
        if found:
            print("✅ Found and scrolled to HOTD Performance element with JavaScript")
            time.sleep(2)
            driver.save_screenshot("js_direct_scroll.png")
            
            # Try to click on HOTD Performance header to expand it
            script_click = """
                var elements = document.querySelectorAll('h1, h2, h3, h4, h5, h6, div, span, th');
                for (var i = 0; i < elements.length; i++) {
                    if (elements[i].innerText && elements[i].innerText.includes('HOTD Performance')) {
                        elements[i].click();
                        return true;
                    }
                }
                return false;
            """
            clicked = driver.execute_script(script_click)
            if clicked:
                print("✅ Clicked on HOTD Performance header")
                time.sleep(2)
                driver.save_screenshot("after_hotd_click.png")
            
            return True
    except Exception as e:
        print(f"⚠️ Method 1 failed: {str(e)}")
    
    # Method 2: Force scroll with multiple small increments
    try:
        print("Method 2: Using multiple small scroll increments to trigger dynamic content")
        # Get current scroll position
        start_position = driver.execute_script("return window.pageYOffset;")
        print(f"Starting scroll position: {start_position}px")
        
        # Scroll down in small increments to trigger any lazy loading
        total_height = driver.execute_script("return document.body.scrollHeight")
        increment = 90  # Small increment of 100px
        
        for scroll_pos in range(start_position, total_height, increment):
            driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
            print(f"Scrolled to {scroll_pos}px")
            time.sleep(0.5)  # Short pause between scrolls
            
            # Check if we've reached the end of the page
            current_height = driver.execute_script("return document.body.scrollHeight")
            if current_height > total_height:
                print(f"✅ Page height increased from {total_height}px to {current_height}px")
                total_height = current_height
                
            # Take a screenshot every 300px
            if scroll_pos % 300 == 0:
                driver.save_screenshot(f"scroll_pos_{scroll_pos}.png")
        
        # Final scroll to make sure we're at the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.save_screenshot("after_incremental_scroll.png")
    except Exception as e:
        print(f"⚠️ Method 2 failed: {str(e)}")
    
    # Method 3: Try simulated scrolling with key presses
    try:
        print("Method 3: Simulating key presses to scroll")
        # Focus on the body element first
        driver.execute_script("document.body.focus();")
        time.sleep(1)
        
        # Press PAGE_DOWN key multiple times
        body = driver.find_element(By.TAG_NAME, "body")
        for i in range(10):
            body.send_keys(Keys.PAGE_DOWN)
            print(f"Sent PAGE_DOWN key {i+1}/10")
            time.sleep(1)
            
            # Take screenshot every few presses
            if i % 3 == 0:
                driver.save_screenshot(f"page_down_{i+1}.png")
                
        # Final screenshot
        driver.save_screenshot("after_key_scroll.png")
    except Exception as e:
        print(f"⚠️ Method 3 failed: {str(e)}")
    
    # Method 4: Try to interact with table expand controls
    try:
        print("Method 4: Looking for table expand controls or buttons")
        # Look for expand/collapse buttons near tables
        expand_selectors = [
            "button.expand", "button.collapse", "i.fa-chevron-down", "i.fa-plus", 
            "span.expand-icon", "div.expand-control", ".toggle-view", ".view-more",
            "button[aria-expanded='false']", "div[aria-expanded='false']"
        ]
        
        for selector in expand_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    for i, el in enumerate(elements):
                        try:
                            if el.is_displayed():
                                print(f"Found potential expand control: {selector}")
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                                time.sleep(1)
                                driver.save_screenshot(f"expand_control_{i}.png")
                                
                                # Try to click the element
                                driver.execute_script("arguments[0].click();", el)
                                print(f"Clicked on potential expand control #{i+1}")
                                time.sleep(2)
                                driver.save_screenshot(f"after_expand_click_{i}.png")
                        except:
                            continue
            except:
                continue
    except Exception as e:
        print(f"⚠️ Method 4 failed: {str(e)}")
    
    # Try to find the HOTD Performance section by text one more time
    try:
        print("Final attempt: Searching for HOTD Performance by text content...")
        elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'HOTD Performance')]")
        if elements:
            for element in elements:
                try:
                    if element.is_displayed():
                        print("✅ Found HOTD Performance text element")
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                        time.sleep(1)
                        driver.save_screenshot("final_hotd_element_found.png")
                        
                        # Try to click it
                        driver.execute_script("arguments[0].click();", element)
                        time.sleep(1)
                        driver.save_screenshot("final_hotd_element_clicked.png")
                        return True
                except:
                    continue
    except Exception as e:
        print(f"⚠️ Final attempt failed: {str(e)}")
    
    print("⚠️ All methods attempted, continuing with process regardless")
    return True


def check_iframe_content(driver):
    """Check if HOTD Performance might be in an iframe"""
    print("🔍 Checking for iframes that might contain HOTD Performance...")
    
    try:
        # Find all iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Found {len(iframes)} iframes on page")
        
        iframe_found = False
        for i, iframe in enumerate(iframes):
            try:
                print(f"Examining iframe #{i+1}")
                driver.switch_to.frame(iframe)
                
                # Check for HOTD text in this iframe
                page_source = driver.page_source
                if "HOTD" in page_source or "Performance" in page_source:
                    print(f"✅ Found HOTD-related content in iframe #{i+1}")
                    
                    # Take a screenshot within this iframe
                    driver.save_screenshot(f"iframe_{i+1}_content.png")
                    
                    # Try to scroll within the iframe
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                    driver.save_screenshot(f"iframe_{i+1}_scrolled.png")
                    
                    iframe_found = True
                
                # Switch back to default content
                driver.switch_to.default_content()
            except Exception as e:
                print(f"⚠️ Error examining iframe #{i+1}: {str(e)}")
                driver.switch_to.default_content()
        
        return iframe_found
    except Exception as e:
        print(f"❌ Error checking iframes: {str(e)}")
        # Make sure we're back in the main document
        driver.switch_to.default_content()
        return False


def try_alternative_navigation(driver):
    """Try alternative navigation methods to access HOTD Performance"""
    print("🔍 Trying alternative navigation methods to access HOTD Performance...")
    
    try:
        # Method 1: Check if there are tabs we can click
        try:
            print("Checking for navigation tabs...")
            tabs = driver.find_elements(By.CSS_SELECTOR, ".nav-tabs li, .tabs-nav li, .tab, button[role='tab']")
            
            if tabs:
                print(f"Found {len(tabs)} potential navigation tabs")
                for i, tab in enumerate(tabs):
                    try:
                        if tab.is_displayed():
                            text = tab.text
                            print(f"Tab #{i+1} text: {text}")
                            
                            # If it might be related to HOTD/Performance
                            if "HOTD" in text or "Performance" in text or text.strip() == "":
                                print(f"Clicking tab #{i+1}")
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab)
                                time.sleep(1)
                                driver.save_screenshot(f"before_tab_{i+1}_click.png")
                                
                                driver.execute_script("arguments[0].click();", tab)
                                time.sleep(2)
                                driver.save_screenshot(f"after_tab_{i+1}_click.png")
                    except Exception as e:
                        print(f"Error interacting with tab #{i+1}: {str(e)[:50]}...")
        except Exception as e:
            print(f"Tab navigation check failed: {str(e)}")
        
        # Method 2: Try direct URL navigation
        try:
            print("Trying direct URL navigation to potential HOTD Performance page...")
            current_url = driver.current_url
            
            # Try adding fragments or parameters that might show HOTD section
            hotd_url_variants = [
                f"{current_url}#hotd",
                f"{current_url}#hotd-performance",
                f"{current_url}?tab=hotd",
                f"{current_url.split('?')[0]}?tab=hotd",
                f"{current_url.split('?')[0]}?view=hotd"
            ]
            
            for url in hotd_url_variants:
                print(f"Trying URL: {url}")
                driver.get(url)
                time.sleep(3)
                driver.save_screenshot(f"url_variant_{url.split('?')[-1].split('#')[-1]}.png")
            
            # Go back to original URL
            driver.get(current_url)
            time.sleep(2)
        except Exception as e:
            print(f"URL navigation approach failed: {str(e)}")
            
        # Method 3: Look for any buttons that might load HOTD data
        try:
            print("Looking for buttons that might load HOTD Performance...")
            button_selectors = [
                "button:not([disabled])", 
                "a.btn", 
                ".card-header button",
                ".icon-button",
                "i.fa, i.fas, i.fab"
            ]
            
            for selector in button_selectors:
                buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                if buttons:
                    print(f"Found {len(buttons)} potential interactive elements with selector '{selector}'")
                    for i, button in enumerate(buttons[:5]):  # Limit to first 5 to avoid too many
                        try:
                            if button.is_displayed():
                                # Get a text description for logging
                                try:
                                    button_text = button.text.strip() or "No text"
                                    button_classes = button.get_attribute("class") or "No class"
                                    print(f"Button #{i+1} - Text: '{button_text}', Classes: '{button_classes}'")
                                except:
                                    print(f"Button #{i+1} - Could not get attributes")
                                
                                # Take screenshot before clicking
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                                time.sleep(1)
                                driver.save_screenshot(f"before_button_{selector.replace(':', '_').replace('.', '_').replace(',', '_')}_{i+1}_click.png")
                                
                                # Click the button
                                driver.execute_script("arguments[0].click();", button)
                                time.sleep(2)
                                driver.save_screenshot(f"after_button_{selector.replace(':', '_').replace('.', '_').replace(',', '_')}_{i+1}_click.png")
                                
                                # Check if HOTD content appeared
                                if "HOTD Performance" in driver.page_source:
                                    print(f"✅ HOTD Performance content appeared after clicking button #{i+1}")
                                    return True
                        except Exception as e:
                            print(f"Error interacting with button #{i+1}: {str(e)[:50]}...")
        except Exception as e:
            print(f"Button interaction approach failed: {str(e)}")
            
        return False  # None of the alternative methods worked
    except Exception as e:
        print(f"❌ Error in alternative navigation attempts: {str(e)}")
        return False

def extract_and_save_from_grid_id(driver, download_dir, force_scroll=True):
    """Navigasi ke GRID_ID dan ekstrak data tabel dengan opsi mendownload dari menu."""
    try:
        print("🔍 Mencari elemen tabel dan menu opsi pada halaman...")
        time.sleep(10)
        driver.save_screenshot("before_extraction.png")
        
        # Fungsi untuk membuat screenshot dengan marker koordinat klik
        def save_screenshot_with_marker(filename, x, y):
            """Menyimpan screenshot dengan penanda koordinat klik."""
            from PIL import Image, ImageDraw, ImageFont
            driver.save_screenshot(filename + "_raw.png")
            img = Image.open(filename + "_raw.png")
            draw = ImageDraw.Draw(img)
            
            # Pastikan koordinat dalam batas layar yang terlihat
            screen_width, screen_height = img.size
            x = min(max(0, x), screen_width - 1)
            y = min(max(0, y), screen_height - 1)
            
            # Gambar lingkaran merah pada koordinat klik (dengan ukuran lebih besar)
            draw.ellipse((x-20, y-20, x+20, y+20), outline='red', width=4)
            # Gambar tanda silang pada koordinat klik
            draw.line((x-15, y-15, x+15, y+15), fill='red', width=4)
            draw.line((x-15, y+15, x+15, y-15), fill='red', width=4)
            
            # Tambahkan teks koordinat dengan font yang lebih besar
            try:
                font = ImageFont.truetype("arial.ttf", 16)
                draw.text((x+25, y), f"({x}, {y})", fill='red', font=font)
            except:
                # Jika font tidak tersedia, gunakan metode default
                draw.text((x+25, y), f"({x}, {y})", fill='red')
            
            img.save(filename + ".png")
            print(f"✅ Screenshot dengan marker disimpan di {filename}.png")
            return filename + ".png"
        
        # Pendekatan dengan PyAutoGUI - klik berdasarkan koordinat eksplisit
        download_success = False
        csv_files_before = set([f for f in os.listdir(download_dir) if f.endswith('.csv')])
        print(f"File CSV yang sudah ada sebelum download: {csv_files_before}")
        
        try:
            print("🔍 Mencoba pendekatan PyAutoGUI untuk klik menu...")
            
            # Dapatkan dimensi layar browser
            window_size = driver.get_window_size()
            win_width = window_size['width']
            win_height = window_size['height']
            
            # Simpan screenshot awal untuk referensi
            driver.save_screenshot("for_coordinates_raw.png")
            
            # Koordinat "kebab" menu (tiga titik) di bagian atas tabel
            # Berdasarkan screenshot dan koordinat halaman
            kebab_x, kebab_y = 1821, 551  # Posisi tombol kebab menu (tiga titik) dari screenshot
            
            # Simpan screenshot dengan marker untuk kebab menu
            kebab_screenshot = save_screenshot_with_marker(
                "pyautogui_kebab_before_click", 
                kebab_x, kebab_y
            )
            
            # Klik pada koordinat kebab menu
            pyautogui.click(kebab_x, kebab_y)
            print(f"✅ Klik pada koordinat menu tiga titik ({kebab_x}, {kebab_y})")
            time.sleep(2)
            
            # Ambil screenshot setelah klik kebab menu untuk verifikasi
            driver.save_screenshot("after_kebab_click.png")
            
            # Koordinat untuk opsi "Download" dalam menu dropdown
            # Berdasarkan estimasi posisi menu dropdown
            download_option_x = kebab_x - 50  # Sedikit ke kiri dari kebab menu
            download_option_y = kebab_y + 40   # 40px ke bawah dari kebab menu
            
            # Simpan screenshot dengan marker untuk opsi Download
            download_screenshot = save_screenshot_with_marker(
                "pyautogui_download_option_before_click", 
                download_option_x, download_option_y
            )
            
            # Klik pada opsi Download
            pyautogui.click(download_option_x, download_option_y)
            print(f"✅ Klik pada koordinat opsi Download ({download_option_x}, {download_option_y})")
            time.sleep(2)
            
            # Ambil screenshot setelah klik opsi Download untuk verifikasi
            driver.save_screenshot("after_download_option_click.png")
            
            # Koordinat untuk opsi "Export to .CSV" dalam menu dropdown kedua
            csv_x = download_option_x + 100  # Asumsi menu export to csv muncul ke kanan
            csv_y = download_option_y + 30   # Asumsi menu export to csv muncul sedikit ke bawah
            
            # Pastikan koordinat dalam batas layar
            csv_x = min(csv_x, win_width - 40)  # Beri margin 50px
            
            # Simpan screenshot dengan marker untuk opsi CSV
            csv_screenshot = save_screenshot_with_marker(
                "pyautogui_csv_option_before_click", 
                csv_x, csv_y
            )
            
            # Klik pada opsi Export to CSV
            pyautogui.click(csv_x, csv_y)
            print(f"✅ Klik pada koordinat opsi Export to .CSV ({csv_x}, {csv_y})")
            time.sleep(5)
            
            # Ambil screenshot akhir untuk verifikasi
            driver.save_screenshot("after_csv_click.png")
            
            # Periksa apakah file CSV sudah didownload
            # Tunggu maksimal 30 detik untuk proses download
            print("⏳ Menunggu file CSV selesai didownload... (maksimal 30 detik)")
            for i in range(30):
                time.sleep(1)
                csv_files_current = set([f for f in os.listdir(download_dir) if f.endswith('.csv')])
                new_files = csv_files_current - csv_files_before
                
                if new_files:
                    print(f"✅ File CSV baru terdeteksi pada detik ke-{i+1}: {new_files}")
                    download_success = True
                    break
                
                if (i + 1) % 5 == 0:  # Log setiap 5 detik
                    print(f"⏳ Masih menunggu download selesai... ({i+1}/30 detik)")
            
            if download_success:
                print("✅ Download CSV berhasil!")
            else:
                print("⚠️ Download gagal atau timeout - tidak ada file CSV baru yang terdeteksi")
                
        except Exception as e:
            print(f"⚠️ Error dalam pendekatan PyAutoGUI: {str(e)}")
            driver.save_screenshot("pyautogui_error.png")
        
        # Lanjutkan dengan scrolling terlepas dari hasil download jika force_scroll=True
        if download_success or force_scroll:
            print("🔄 Melanjutkan dengan proses scrolling halaman...")
            
            # 1. Lakukan scrolling untuk melihat konten lainnya pada halaman
            print("1️⃣ Melakukan scrolling umum untuk melihat konten lainnya...")
            scroll_count = 15  # Jumlah scrolling yang lebih banyak
            scroll_delay = 1.5  # Jeda antar scrolling
            
            for i in range(scroll_count):
                # Scroll down dengan jarak yang lebih besar
                driver.execute_script(f"window.scrollBy(0, 800);")
                print(f"✅ Scrolling #{i+1}/{scroll_count}")
                
                # Ambil screenshot pada interval tertentu
                if (i + 1) % 3 == 0 or i == 0 or i == scroll_count - 1:
                    driver.save_screenshot(f"after_download_scroll_{i+1}.png")
                
                time.sleep(scroll_delay)
            
            # 2. Cari dan focus pada elemen HOTD Performance (jika ada)
            print("2️⃣ Mencari elemen HOTD Performance...")
            try:
                # Coba cari elemen dengan teks HOTD dengan JavaScript
                hotd_found = driver.execute_script("""
                    var elements = document.querySelectorAll('*');
                    for (var i = 0; i < elements.length; i++) {
                        if (elements[i].innerText && 
                            (elements[i].innerText.includes('HOTD') || 
                             elements[i].innerText.includes('Performance'))) {
                            elements[i].scrollIntoView({behavior: 'smooth', block: 'center'});
                            return elements[i];
                        }
                    }
                    return null;
                """)
                
                if hotd_found:
                    print("✅ Elemen HOTD Performance ditemukan dan di-scroll")
                    time.sleep(2)
                    driver.save_screenshot("hotd_found.png")
                    
                    # Setelah menemukan elemen HOTD Performance, lakukan fokus scrolling pada area ini
                    print("🔄 Melakukan scrolling pada area HOTD Performance...")
                    
                    # Ambil posisi elemen HOTD Performance
                    hotd_position = driver.execute_script("return arguments[0].getBoundingClientRect().top + window.pageYOffset;", hotd_found)
                    
                    # Lakukan scrolling bertahap di sekitar area HOTD Performance
                    scroll_steps = 20  # Jumlah scrolling yang lebih banyak
                    scroll_step_size = 300  # Ukuran scrolling yang lebih besar (pixel)
                    
                    print(f"🔍 Posisi HOTD Performance: {hotd_position}px dari atas")
                    print(f"🔄 Melakukan {scroll_steps} kali scrolling bertahap di area HOTD Performance")
                    
                    for i in range(scroll_steps):
                        # Hitung posisi scroll (mulai dari sedikit di atas HOTD Performance)
                        current_position = hotd_position - 200 + (i * scroll_step_size)
                        
                        # Scroll ke posisi tersebut
                        driver.execute_script(f"window.scrollTo(0, {current_position});")
                        print(f"✅ HOTD Performance scroll #{i+1}/{scroll_steps} ke posisi {current_position}px")
                        
                        # Jeda setiap scrolling
                        time.sleep(1)
                        
                        # Ambil screenshot pada interval tertentu
                        if (i + 1) % 3 == 0 or i == 0 or i == scroll_steps - 1:
                            driver.save_screenshot(f"hotd_performance_scroll_{i+1}.png")
                else:
                    print("⚠️ Elemen HOTD Performance tidak ditemukan dengan JavaScript")
            except Exception as e:
                print(f"⚠️ Error saat mencari HOTD Performance: {str(e)}")
            
            # 3. Scroll ke bagian bawah halaman HOTD Performance (tanpa klik elemen lain)
            print("3️⃣ Melakukan scroll ke bagian bawah HOTD Performance...")
            
            # Coba temukan elemen tabel atau konten dalam HOTD Performance
            try:
                hotd_tables = driver.execute_script("""
                    var hotdElement = null;
                    var elements = document.querySelectorAll('*');
                    
                    // Pertama cari elemen HOTD Performance
                    for (var i = 0; i < elements.length; i++) {
                        if (elements[i].innerText && 
                            (elements[i].innerText.includes('HOTD') || 
                             elements[i].innerText.includes('Performance'))) {
                            hotdElement = elements[i];
                            break;
                        }
                    }
                    
                    if (!hotdElement) return null;
                    
                    // Temukan tabel atau elemen konten di sekitar elemen HOTD
                    var tables = [];
                    
                    // Cek semua tabel atau div yang berisi data sebagai siblings atau children
                    var candidates = document.querySelectorAll('table, .table, [role="table"], .data-grid, .grid-container');
                    for (var i = 0; i < candidates.length; i++) {
                        // Ambil posisi relatif terhadap elemen HOTD
                        var rect = candidates[i].getBoundingClientRect();
                        var hotdRect = hotdElement.getBoundingClientRect();
                        
                        // Jika elemen berada di bawah HOTD (dalam jarak tertentu)
                        if (Math.abs(rect.top - hotdRect.bottom) < 500) {
                            tables.push(candidates[i]);
                        }
                    }
                    
                    return tables.length > 0 ? tables : null;
                """)
                
                if hotd_tables:
                    print(f"✅ Menemukan {len(hotd_tables)} elemen tabel/konten di area HOTD Performance")
                    
                    # Scroll bertahap melalui tabel-tabel tersebut
                    for i, table in enumerate(hotd_tables):
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", table)
                        print(f"✅ Scrolling ke tabel HOTD #{i+1}/{len(hotd_tables)}")
                        time.sleep(1.5)
                        driver.save_screenshot(f"hotd_table_scroll_{i+1}.png")
                        
                        # Lakukan scrolling tambahan di dalam tabel ini
                        table_height = driver.execute_script("return arguments[0].offsetHeight;", table)
                        if table_height > 300:  # Jika tabel cukup tinggi, lakukan scrolling bertahap
                            scroll_count = min(10, max(5, table_height // 80))  # Jumlah scrolling yang lebih banyak berdasarkan tinggi
                            print(f"📏 Tinggi tabel: {table_height}px, melakukan {scroll_count} kali scrolling")
                            
                            for j in range(scroll_count):
                                # Scroll ke berbagai bagian tabel
                                fraction = (j + 1) / scroll_count
                                scroll_pos = driver.execute_script(
                                    f"var rect = arguments[0].getBoundingClientRect(); " +
                                    f"var targetY = rect.top + (rect.height * {fraction}) - (window.innerHeight / 2); " +
                                    f"window.scrollBy(0, targetY); return window.pageYOffset;", 
                                    table
                                )
                                print(f"  ↓ Scrolling dalam tabel #{i+1}: {j+1}/{scroll_count}")
                                time.sleep(1)
                else:
                    print("⚠️ Tidak menemukan tabel atau konten di area HOTD Performance")
            except Exception as e:
                print(f"⚠️ Error saat mencari tabel HOTD: {str(e)}")
            
            # 4. Scroll kembali ke atas dan ke bawah sekali lagi untuk memastikan semua konten dimuat
            print("4️⃣ Melakukan final scrolling untuk HOTD Performance...")
            
            # Coba temukan lagi elemen HOTD untuk final scrolling
            try:
                hotd_element = driver.execute_script("""
                    var elements = document.querySelectorAll('*');
                    for (var i = 0; i < elements.length; i++) {
                        if (elements[i].innerText && 
                            (elements[i].innerText.includes('HOTD') || 
                             elements[i].innerText.includes('Performance'))) {
                            return elements[i];
                        }
                    }
                    return null;
                """)
                
                if hotd_element:
                    # Scroll ke elemen HOTD
                    driver.execute_script("arguments[0].scrollIntoView({block: 'start'});", hotd_element)
                    time.sleep(1)
                    driver.save_screenshot("final_hotd_top.png")
                    
                    # Dapatkan posisi dan dimensi elemen HOTD
                    hotd_position = driver.execute_script("""
                        var rect = arguments[0].getBoundingClientRect();
                        return {
                            top: rect.top + window.pageYOffset,
                            height: rect.height
                        };
                    """, hotd_element)
                    
                    # Estimasi area scrolling (dimulai dari elemen HOTD dan 3000px ke bawah)
                    start_pos = hotd_position['top']
                    area_height = 3000  # Estimasi area konten HOTD Performance yang lebih besar
                    
                    print(f"🔍 Area HOTD Performance: mulai dari {start_pos}px, memperkirakan tinggi {area_height}px")
                    
                    # Lakukan scrolling bertahap di area HOTD Performance
                    scroll_steps = 15  # Lebih banyak langkah untuk scrolling yang lebih jauh
                    for i in range(scroll_steps):
                        # Hitung posisi scroll
                        current_position = start_pos + (i * (area_height / scroll_steps))
                        
                        # Scroll ke posisi
                        driver.execute_script(f"window.scrollTo(0, {current_position});")
                        print(f"✅ Final HOTD scroll #{i+1}/{scroll_steps} ke posisi {current_position}px")
                        time.sleep(1.5)
                        
                        # Ambil screenshot
                        if (i + 1) % 2 == 0 or i == 0 or i == scroll_steps - 1:
                            driver.save_screenshot(f"final_hotd_scroll_{i+1}.png")
                else:
                    print("⚠️ Tidak dapat menemukan elemen HOTD untuk final scrolling")
                    
                    # Sebagai fallback, lakukan scrolling umum
                    total_height = driver.execute_script("return document.body.scrollHeight")
                    view_height = driver.execute_script("return window.innerHeight")
                    scrolls_needed = max(3, round(total_height / view_height))
                    
                    for i in range(scrolls_needed):
                        scroll_amount = (i + 1) * view_height
                        driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
                        print(f"Final fallback scroll #{i+1}/{scrolls_needed}")
                        time.sleep(1)
                        
                        if (i + 1) % 2 == 0 or i == scrolls_needed - 1:
                            driver.save_screenshot(f"final_fallback_scroll_{i+1}.png")
            except Exception as e:
                print(f"⚠️ Error saat melakukan final scrolling: {str(e)}")
            
            print("✅ Proses scrolling selesai dilakukan!")
            return True
        else:
            print("⚠️ Download CSV gagal dan force_scroll=False, menghentikan proses")
            return False
                
    except Exception as e:
        print(f"❌ Error utama saat mengakses menu download: {str(e)}")
        driver.save_screenshot("menu_access_error.png")
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
        
        print("⏳ Menunggu halaman dashboard dimuat sepenuhnya (10 detik)...")
        time.sleep(10)
        
        # Persiapkan direktori download
        download_dir = os.path.abspath("./downloads")
        os.makedirs(download_dir, exist_ok=True)
        
        # 3. Langsung lakukan ekstraksi dan download tanpa navigasi ulang ke dashboard
        print("🔄 Memulai proses ekstraksi data...")
        
        success = extract_and_save_from_grid_id(driver, download_dir, force_scroll=True)
        
        if success:
            print("✅ Proses ekstraksi data berhasil selesai")
            
            # 4. Verifikasi hasil
            csv_files = [f for f in os.listdir(download_dir) if f.endswith('.csv')]
            if csv_files:
                print(f"📊 File CSV yang berhasil didownload: {csv_files}")
            else:
                print("⚠️ Tidak ada file CSV yang ditemukan di direktori download")
            
            # 5. Ambil screenshot final untuk dokumentasi
            driver.save_screenshot("extraction_complete.png")
        else:
            print("❌ Proses ekstraksi data gagal")
        
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
