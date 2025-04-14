from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import traceback
import pyautogui
import datetime

def setup_driver():
    """Setup WebDriver dengan konfigurasi yang tepat"""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Tetapkan preferensi download
    download_dir = os.path.abspath("./downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=options)
    driver.set_window_position(0, 0)
    driver.maximize_window()  # Maksimalkan jendela untuk konsistensi
    driver.set_page_load_timeout(60)
    return driver

def login(driver, username, password):
    """Login ke portal Telkom dengan pendekatan yang lebih simple"""
    print("🔐 Mencoba login ke portal Telkom...")
    try:
        # Buka halaman login
        driver.get("https://newgobeyond.mytens.co.id/login")
        time.sleep(3)
        
        # Isi username
        username_field = driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[type='email']")
        username_field.clear()
        username_field.send_keys(username)
        print("✅ Username diisi")
        
        # Isi password
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_field.clear()
        password_field.send_keys(password)
        print("✅ Password diisi")
        
        # Tangani checkbox jika ada
        checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        if checkboxes:
            driver.execute_script("arguments[0].click();", checkboxes[0])
            print("✅ Checkbox diklik")
        
        # Klik tombol login
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", login_button)
        print("✅ Tombol login diklik")
        
        # Tunggu login selesai
        time.sleep(5)
        
        if "login" not in driver.current_url.lower():
            print("✅ Login berhasil")
            driver.save_screenshot("after_login.png")
            return True
        else:
            print("❌ Login gagal - masih di halaman login")
            return False
            
    except Exception as e:
        print(f"❌ Error saat login: {str(e)}")
        return False

def wait_for_download_complete(download_dir, timeout=30):
    """Tunggu file download selesai"""
    start_time = time.time()
    
    # Dapatkan daftar file CSV yang sudah ada
    initial_files = set([f for f in os.listdir(download_dir) if f.endswith(".csv")])
    print(f"File CSV awal: {initial_files}")
    
    # Polling untuk file baru
    while time.time() - start_time < timeout:
        time.sleep(1)
        current_files = set([f for f in os.listdir(download_dir) if f.endswith(".csv")])
        new_files = current_files - initial_files
        
        # Cek file download yang sedang berjalan
        downloading_files = [f for f in os.listdir(download_dir) if f.endswith((".crdownload", ".part", ".download"))]
        
        if new_files and not downloading_files:
            print(f"✅ Download selesai. File baru: {new_files}")
            return list(new_files)
            
        elapsed = time.time() - start_time
        if int(elapsed) % 5 == 0 and int(elapsed) > 0:
            print(f"⏳ Menunggu download selesai... ({int(elapsed)}/{timeout} detik)")
    
    print(f"⚠️ Timeout setelah {timeout} detik. Tidak ada file baru yang terdeteksi.")
    return []

def download_with_pyautogui(driver, table_names):
    """Download tabel menggunakan PyAutoGUI untuk mengklik menu dan tombol berdasarkan koordinat"""
    print("\n🔄 Mencoba download tabel menggunakan PyAutoGUI...")
    
    # Navigasi ke dashboard
    driver.get("https://newgobeyond.mytens.co.id/dashboard-rising-star?tab=bintang-1")
    print("⏳ Menunggu dashboard dimuat...")
    time.sleep(10)
    
    # Coba klik tombol Bintang 1 jika perlu
    try:
        bintang_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'Bintang 1')]")
        if bintang_buttons:
            for btn in bintang_buttons:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].click();", btn)
                    print("✅ Tombol Bintang 1 diklik")
                    time.sleep(5)
                    break
    except:
        print("⚠️ Tidak perlu klik tombol Bintang 1 atau gagal")
    
    # Ambil screenshot untuk referensi
    driver.save_screenshot("dashboard_for_pyautogui.png")
    
    # Maksimalkan jendela untuk konsistensi
    driver.maximize_window()
    time.sleep(1)
    
    successful_downloads = 0
    download_dir = os.path.abspath("./downloads")
    
    # Definisikan koordinat menu kebab untuk setiap tabel
    # Koordinat ini mungkin perlu disesuaikan berdasarkan resolusi layar
    kebab_coordinates = [
        {"name": "Witel Performance", "x": 1798, "y": 540},  # Koordinat untuk menu kebab Witel Performance
        {"name": "HOTD Performance", "x": 1798, "y": 660},   # Koordinat untuk menu kebab HOTD Performance
        {"name": "AM Performance", "x": 1798, "y": 920}     # Koordinat untuk menu kebab AM Performance
    ]
    
    # Koordinat untuk tombol Download dan CSV
    download_offset_y = 35  # Jarak vertikal dari kebab ke tombol Download
    csv_offset_y = 35       # Jarak vertikal dari tombol Download ke tombol CSV
    
    for kebab in kebab_coordinates:
        try:
            table_name = kebab["name"]
            print(f"\n🔄 Mencoba download {table_name} dengan PyAutoGUI...")
            
            # Scroll ke tempat yang sesuai berdasarkan table name
            scroll_script = f"document.querySelector(\"div[contains(text(), '{table_name}')]\").scrollIntoView({{block: 'center'}});"
            try:
                driver.execute_script(scroll_script)
                print(f"✅ Scrolled ke {table_name}")
            except:
                # Jika gagal, coba scroll berdasarkan koordinat Y
                scroll_y = kebab["y"] - 200  # Scroll sedikit di atas kebab button
                driver.execute_script(f"window.scrollTo(0, {scroll_y});")
                print(f"✅ Scrolled ke posisi Y: {scroll_y}")
            
            time.sleep(2)
            driver.save_screenshot(f"before_kebab_{table_name.replace(' ', '_')}.png")
            
            # Ambil jumlah file CSV sebelum download
            files_before = set([f for f in os.listdir(download_dir) if f.endswith('.csv')])
            
            # Klik menu kebab
            pyautogui.click(kebab["x"], kebab["y"])
            print(f"✅ Kebab menu untuk {table_name} diklik pada koordinat ({kebab['x']}, {kebab['y']})")
            time.sleep(2)
            
            # Klik tombol Download
            download_y = kebab["y"] + download_offset_y
            pyautogui.click(kebab["x"], download_y)
            print(f"✅ Tombol Download diklik pada koordinat ({kebab['x']}, {download_y})")
            time.sleep(2)
            
            # Klik tombol Export to CSV
            csv_y = download_y + csv_offset_y - 10
            pyautogui.click(kebab["x"] - 140 , csv_y)  # +50 horizontal offset untuk submenu
            print(f"✅ Tombol Export to CSV diklik pada koordinat ({kebab['x'] -140 }, {csv_y})")
            
            # Tunggu download selesai
            time.sleep(5)  # Tunggu dialog download muncul
            
            # Cek apakah ada file baru yang telah diunduh
            files_after = set([f for f in os.listdir(download_dir) if f.endswith('.csv')])
            new_files = files_after - files_before
            
            if new_files:
                latest_file = list(new_files)[0]
                # Rename file
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = f"{table_name.replace(' ', '_').lower()}_{timestamp}.csv"
                old_path = os.path.join(download_dir, latest_file)
                new_path = os.path.join(download_dir, new_name)
                
                try:
                    os.rename(old_path, new_path)
                    print(f"✅ File diubah nama: {latest_file} -> {new_name}")
                except:
                    print(f"⚠️ Tidak dapat mengubah nama file: {latest_file}")
                
                successful_downloads += 1
                print(f"✅ Download {table_name} berhasil")
            else:
                print(f"⚠️ Tidak terdeteksi file baru untuk {table_name}")
            
        except Exception as e:
            print(f"❌ Error saat mencoba download {table_name}: {str(e)}")
            driver.save_screenshot(f"error_{table_name.replace(' ', '_')}.png")
    
    return successful_downloads

def try_click_with_javascript(driver):
    """Coba klik tombol dengan JavaScript untuk mengatasi masalah deteksi elemen"""
    print("\n🔄 Mencoba klik dengan JavaScript...")
    
    # Navigasi ke dashboard
    driver.get("https://newgobeyond.mytens.co.id/dashboard-rising-star?tab=bintang-1")
    print("⏳ Menunggu dashboard dimuat...")
    time.sleep(10)
    
    # Screenshot awal
    driver.save_screenshot("before_js_click.png")
    
    successful_downloads = 0
    download_dir = os.path.abspath("./downloads")
    
    # JavaScript untuk menemukan dan mengklik semua tombol kebab
    find_and_click_kebab_script = """
    // Fungsi untuk menemukan dan mengklik elemen kebab
    function findAndClickKebabMenus() {
        // Cari semua kemungkinan menu tombol tiga titik/kebab
        var kebabButtons = document.querySelectorAll('.ant-dropdown-trigger, [id*="controls"]');
        console.log('Found ' + kebabButtons.length + ' potential kebab menus');
        
        var clickedButtons = 0;
        for (var i = 0; i < kebabButtons.length; i++) {
            if (kebabButtons[i].offsetParent !== null) {  // Check if element is visible
                kebabButtons[i].scrollIntoView({block: 'center'});
                kebabButtons[i].click();
                console.log('Clicked kebab menu #' + (i+1));
                clickedButtons++;
            }
        }
        return clickedButtons;
    }
    
    return findAndClickKebabMenus();
    """
    
    try:
        clicked_kebabs = driver.execute_script(find_and_click_kebab_script)
        print(f"✅ JavaScript mengklik {clicked_kebabs} tombol kebab potensial")
        
        if clicked_kebabs > 0:
            time.sleep(2)
            driver.save_screenshot("after_js_kebab_click.png")
            
            # Coba klik tombol Download jika muncul
            download_script = """
            var downloadItems = document.querySelectorAll('[class*="dropdown-menu"] div:not([style*="display: none"]):not([style*="visibility: hidden"]):not([class*="hidden"])');
            var clickedDownload = 0;
            
            for (var i = 0; i < downloadItems.length; i++) {
                if (downloadItems[i].innerText && downloadItems[i].innerText.includes('Download')) {
                    downloadItems[i].click();
                    console.log('Clicked Download option');
                    clickedDownload++;
                }
            }
            
            return clickedDownload;
            """
            
            clicked_downloads = driver.execute_script(download_script)
            print(f"✅ JavaScript mengklik {clicked_downloads} tombol Download")
            
            if clicked_downloads > 0:
                time.sleep(2)
                driver.save_screenshot("after_js_download_click.png")
                
                # Coba klik tombol CSV jika muncul
                csv_script = """
                var csvItems = document.querySelectorAll('[class*="dropdown-menu"] div:not([style*="display: none"]):not([style*="visibility: hidden"]):not([class*="hidden"])');
                var clickedCSV = 0;
                
                for (var i = 0; i < csvItems.length; i++) {
                    if (csvItems[i].innerText && (csvItems[i].innerText.includes('CSV') || csvItems[i].innerText.includes('.CSV'))) {
                        csvItems[i].click();
                        console.log('Clicked CSV option');
                        clickedCSV++;
                    }
                }
                
                return clickedCSV;
                """
                
                clicked_csvs = driver.execute_script(csv_script)
                print(f"✅ JavaScript mengklik {clicked_csvs} tombol CSV")
                
                if clicked_csvs > 0:
                    # Tunggu download
                    time.sleep(5)
                    
                    # Cek apakah ada file baru
                    files = [f for f in os.listdir(download_dir) if f.endswith('.csv')]
                    successful_downloads = len(files)
    except Exception as e:
        print(f"❌ Error saat mencoba klik dengan JavaScript: {str(e)}")
    
    return successful_downloads

def main():
    """Fungsi utama dengan pendekatan PyAutoGUI"""
    driver = None
    
    try:
        # Setup driver
        driver = setup_driver()
        
        # Login
        username = "960104"
        password = "Tbpe1025"
        
        if not login(driver, username, password):
            print("❌ Login gagal, menghentikan proses")
            return
        
        # Coba pendekatan dengan PyAutoGUI
        successful_downloads1 = download_with_pyautogui(driver, ["Witel Performance", "HOTD Performance", "AM Performance"])
        
        # Jika pendekatan PyAutoGUI gagal, coba dengan JavaScript
        if successful_downloads1 < 3:
            successful_downloads2 = try_click_with_javascript(driver)
        else:
            successful_downloads2 = 0
        
        # Hitung total
        total_successful = successful_downloads1 + successful_downloads2
        
        # Tampilkan hasil
        download_dir = os.path.abspath("./downloads")
        csv_files = [f for f in os.listdir(download_dir) if f.endswith('.csv')]
        
        print("\n===== HASIL PENGAMBILAN DATA =====")
        print(f"✅ Berhasil mengambil data dari {total_successful}/3 tabel")
        print(f"📊 Total file CSV: {len(csv_files)}")
        
        for file in csv_files:
            file_path = os.path.join(download_dir, file)
            file_size = os.path.getsize(file_path) / 1024  # KB
            print(f"  - {file} ({file_size:.2f} KB)")
        
        print("==================================")
        
    except Exception as e:
        print(f"❌ Error dalam fungsi main: {str(e)}")
        print(traceback.format_exc())
        if driver:
            driver.save_screenshot("main_error.png")
    finally:
        if driver:
            print("🔚 Menutup browser")
            driver.quit()

if __name__ == "__main__":
    main()
