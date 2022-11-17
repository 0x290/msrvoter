
# Setup

try:
    import time
    import os
    import sys
    import datetime
    from selenium.webdriver.remote.command import Command
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import Select
    import json
    from colorama import Fore
    import pathlib
except:
    print("Brakuje niektórych modułów.")
    os.system('pip install -r requirements.txt')
    print('Zainstalowano wszystkie wymagane moduły.')
    print('Uruchom ponownie program.')
    time.sleep(5)
    sys.exit()

os.system('cls')

# Set up the driver

try:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    os.system('cls')
except:
    print(Fore.RED + "Nie udało się zainicjalizować przeglądarki. Pobierz chromedriver.exe z https://chromedriver.chromium.org/downloads")
    time.sleep(5)
    sys.exit()

# Load the config file

print("""
                    _           _   _            
                   | |         | | | |           
 _ __ ___  ___ _ __| |__   ___ | |_| |_ ___ _ __ 
| '_ ` _ \/ __| '__| '_ \ / _ \| __| __/ _ \ '__|
| | | | | \__ \ |  | |_) | (_) | |_| ||  __/ |   
|_| |_| |_|___/_|  |_.__/ \___/ \__|\__\___|_|                                             
                                                 
""")
print("[" +Fore.GREEN + "+" + Fore.WHITE + "] Driver został załadowany")

def load_config():
    path = pathlib.Path('config.json')
    if path.exists():
        with open('config.json', 'r', encoding="utf-8") as f:
            config = json.load(f)
            f.close()
        global word_id
        global email
        word_id = config['word_id']
        email = config['email']
        print("[" +Fore.GREEN + "+" + Fore.WHITE + "] Config został załadowany")
    else:
        print("[" +Fore.RED + "-" + Fore.WHITE + "] Nie znaleziono pliku config.json.")
        time.sleep(5)
        sys.exit()

# Get the email

def get_email():
    if email == "random":
        if len(driver.window_handles) >= 2:
            driver.switch_to.window(driver.window_handles[1])
        else:
            driver.execute(Command.NEW_WINDOW)
            driver.switch_to.window(driver.window_handles[1])
        driver.get("https://tempail.com")
        while True:
            time.sleep(0.1)
            if 'Verifying your request' in driver.page_source:
                print("[" +Fore.RED + "-" + Fore.WHITE + "] Wyskoczył błąd, wykonaj CAPTCHA.")
            else:
                email2 = driver.find_element(By.XPATH, '//*[@id="eposta_adres"]').get_attribute('value')
                break
        while not "@" in email2:
            time.sleep(2)
            email2 = driver.find_element(By.XPATH, '//*[@id="eposta_adres"]').get_attribute('value')
        print("[" +Fore.GREEN + "+" + Fore.WHITE + "] Wygenerowano email: "+email2)
        driver.switch_to.window(driver.window_handles[0])
        return email2
    else:
        return email

# Open sjp.pl

def start():
    starttime = time.time()
    driver.get("https://msr.pwn.pl")
    print("[" +Fore.GREEN + "+" + Fore.WHITE + "] Strona została załadowana")
    select = Select(driver.find_element(By.ID, 'floater-word'))
    select.select_by_value(word_id)
    b2=driver.find_element(By.XPATH, "//select[@id='floater-word']")
    driver.implicitly_wait(4)
    ActionChains(driver).move_to_element(b2).click(b2).perform()
    emailinput = driver.find_element(By.ID, "floater-email")
    emailinput.send_keys(get_email())
    print("[" +Fore.GREEN + "+" + Fore.WHITE + "] Wpisano email")
    select = Select(driver.find_element(By.ID, 'age-range'))
    select.select_by_value('13 - 17')
    b2=driver.find_element(By.XPATH, "//input[@type='checkbox']")
    driver.implicitly_wait(4)
    ActionChains(driver).move_to_element(b2).click(b2).perform()
    b3=driver.find_element(By.XPATH, "//div[@id='floater-send']")
    ActionChains(driver).move_to_element(b3).click(b3).perform()
    time.sleep(0.1)
    while True:
        time.sleep(0.1)
        if "Dziękujemy za udział" in driver.page_source:
            driver.switch_to.window(driver.window_handles[1])
            break
        else:
            time.sleep(1)
    while True:
        time.sleep(1)
        try:
            el=driver.find_element(By.XPATH, "//a[contains(@href, 'https://tempail.com/en/mail_')]")
        except:
            el = None
            time.sleep(1)
        if el is not None:
            driver.get(el.get_attribute('href'))
            break
    print('[' +Fore.YELLOW + '!' + Fore.WHITE + '] Kliknij przycisk "Potwierdź"')
    while not len(driver.window_handles) >= 2:
        time.sleep(1)
    try:
        driver.switch_to.window(driver.window_handles[2])
    except:
        driver.switch_to.window(driver.window_handles[-1])
    driver.delete_all_cookies()
    driver.close()
    print("[" +Fore.GREEN + "+" + Fore.WHITE + "] Zakończono")
    driver.switch_to.window(driver.window_handles[1])
    driver.delete_all_cookies()
    time.sleep(0.1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.delete_all_cookies()
    end = time.time()
    print("[" +Fore.GREEN + "+" + Fore.WHITE + "] Czas wykonania: "+str(round(end - starttime, 2))+"s")
    os.system("echo Voted for id " + word_id + " at " + str(datetime.datetime.now()) + "/ Elapsed time: " + str(round(end-starttime,2)) + " >> log.txt")
    start()


if __name__ =="__main__":
    load_config()
    start()