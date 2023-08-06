from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def aiot_screenshot(url, image_path):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")

    driver = webdriver.Remote(command_executor="https://creative-lab.cameo.tw/creative_lab_selenium/", options=chrome_options)
    driver.set_window_size(1600, 900)
    driver.get(url)
    wait = WebDriverWait(driver, 240)
    wait.until(EC.invisibility_of_element_located((By.ID, "loading-layer")))
    driver.save_screenshot(image_path)
    driver.quit()


if __name__ == '__main__':
    aiot_screenshot(
        url='https://aiot.epa.gov.tw/web/iot/history/animation?start=2023-04-16 11:00:00&end=2023-04-16 12:00:00&start_lat=25.0037&end_lat=25.0128&start_lon=121.4982&end_lon=121.5161',
        image_path='./image/test.png'
    )
