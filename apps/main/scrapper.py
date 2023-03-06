import time
import urllib

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("http://www.instagram.com")


def web_scraping():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("http://www.instagram.com")
    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
    username.clear()
    username.send_keys("azizjon_eshpulatov")
    password.clear()
    password.send_keys("AB8689692")
    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[type='submit']"))).click()

    time.sleep(5)
    alert = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    alert2 = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    time.sleep(5)

    driver.get("https://www.instagram.com/wayu.uz/")
    time.sleep(5)
    n_scrolls = 2
    for _ in range(n_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
    anchors = driver.find_elements(By.TAG_NAME, 'a')
    anchors = [a.get_attribute('href') for a in anchors]
    anchors = [a for a in anchors if str(a).startswith("https://www.instagram.com/p/")]

    """anchors = driver.find_elements(By.CLASS_NAME, '_aagv')
    anchors = [a.get_attribute('src') for a in anchors]
    anchors = [a for a in anchors if str(a).startswith("https://www.instagram.com/p/")]"""

    print(f'Found {len(anchors)} links to images')
    print(anchors)
    with open("links.json", "w") as f:
        f.write(str(anchors))

    """# Find all the image elements
    image_elements = driver.find_elements_by_xpath('//div[@class="_aagv"]/a')

    # Download the images
    for i, image_element in enumerate(image_elements):
        # Get the URL of the image
        image_url = image_element.find_element_by_tag_name('img').get_attribute('src')
        # Download the image
        image_path = f'images/{i}.jpg'
        urllib.request.urlretrieve(image_url, image_path)"""

    driver.quit()


web_scraping()
