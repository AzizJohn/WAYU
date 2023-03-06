import time
import urllib.request
import instaloader
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from .models import InstagramPost

from django.core.files import File
import urllib.request
import os
from django.conf import settings


def web_scraping():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("http://www.instagram.com")
    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
    username.clear()
    username.send_keys('azizjon_eshpulatov')
    password.clear()
    password.send_keys('AB8689692')

    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[type='submit']"))).click()

    time.sleep(5)
    alert = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    alert2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    time.sleep(5)
    driver.get("https://www.instagram.com/wayu.uz/")
    time.sleep(5)
    n_scrolls = 1
    for _ in range(n_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
    anchors = driver.find_elements(By.TAG_NAME, 'a')
    anchors = [a.get_attribute('href') for a in anchors]
    parent_dir = "C:/Users/User/Desktop/Intern UIC/WayuProject/media/photos"

    for i, a in enumerate(anchors):
        if str(a).startswith("https://www.instagram.com/p/"):
            L = instaloader.Instaloader()
            post = instaloader.Post.from_shortcode(L.context, a.split("/")[-2])
            if not post.is_video:
                urllib.request.urlretrieve(str(post.url), f"{parent_dir}/{i}.jpg")
                obj = InstagramPost.objects.create(url_address=a, image=f"photos/{i}.jpg")
                #img = InstagramPost.image.save(os.path.basename(f"{i}.jpg"), File(f"{parent_dir}/{i}.jpg"))
                #img.save()
                #obj.save()


def add_to_model(InstagramPost):
    # создает объект модели Insta и сохраняет его в базу данных
    image_url, image_path = web_scraping(InstagramPost.url_address)
    with open(image_path, 'rb') as f:
        InstagramPost.image.save(os.path.basename(image_url), File(f))
    InstagramPost.save()


#web_scraping()
