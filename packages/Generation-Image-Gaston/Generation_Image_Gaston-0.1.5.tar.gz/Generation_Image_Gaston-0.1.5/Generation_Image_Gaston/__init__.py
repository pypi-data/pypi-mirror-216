import time

from selenium.webdriver.common.by import By
import undetected_chromedriver as uc  # Importe le module time pour utiliser des fonctions liées au temps
from selenium import webdriver  # Importe la classe webdriver du module selenium
from selenium.webdriver.chrome.options import Options  # Importe la classe Options du module chrome_options
# Importe le module requests pour effectuer des requêtes HTTP
import os
import getpass


def SelectStyle(Prompt, Style):
    user = getpass.getuser()
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(fr"--user-data-dir=C:\Users\{user}\AppData\Local\Google\Chrome\User Data\Default")
    chrome_options.add_argument("--no-sandbox")  # Désactiver le bac à sable (sandbox)
    chrome_options.add_argument("--disable-dev-shm-usage")  # Désactiver l'utilisation de la mémoire partagée /dev/shm
    chrome_options.add_argument("--disable-gpu")  # Désactiver l'accélération matérielle graphique
    chrome_options.add_argument("--disable-extensions")  # Désactiver les extensions du navigateur
    directory = os.path.join(os.path.expanduser("~"), "Downloads")

    # Configuration du dossier de téléchargement
    prefs = {
        "download.default_directory": directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False
    }
    drivers = uc.Chrome(options=chrome_options)
    drivers.get("https://www.craiyon.com/")
    try:
        drivers.find_element(By.XPATH, """//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]""").click()
    except:
        pass
    if Style == "PHOTO":
        PhotoStyle = drivers.find_element(By.XPATH, """//*[@id="app"]/div[2]/div/div[2]/div[1]/button[3]""")
        PhotoStyle.click()
    if Style == "DESSIN":
        Dessiner = drivers.find_element(By.XPATH, """//*[@id="app"]/div[2]/div/div[2]/div[1]/button[2]""")
        Dessiner.click()
    if Style == """ART""":
        art = drivers.find_element(By.XPATH, """//*[@id="app"]/div[2]/div/div[2]/div[1]/button[1]""")
        art.click()

    enter = drivers.find_element(By.XPATH, """//*[@id="prompt"]""")
    enter.send_keys(Prompt)
    send = drivers.find_element(By.XPATH, """//*[@id="generateButton"]""")
    send.click()
    time.sleep(120)
    image = drivers.find_element(By.XPATH, """//*[@id="app"]/div[2]/div/div[3]/div/div/div/div[1]/div[1]/img""")
    image.click()
    downloadButton = drivers.find_element(By.XPATH, """//*[@id="main"]/main/div/div/div[2]/div[2]/div/div[2]/div[1]/div/button[1]""")
    drivers.execute_script("arguments[0].scrollIntoView();", downloadButton)
    downloadButton.click()
    time.sleep(20)
    try:
        drivers.quit()
        print("Le téléchargement est finie")
    except:
        pass

