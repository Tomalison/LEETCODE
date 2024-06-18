from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# 指定 ChromeDriver 的路徑
chromedriver_path = r"C:\Users\tomsu\OneDrive\文件\待移轉至硬碟\私人\聯成電腦\driver\chromedriver-win64\chromedriver.exe"

def create_driver():
    chrome_service = Service(chromedriver_path)
    chrome_options = Options()
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver

# 檢查字符串中是否包含非法字符
# 檢查字符串中是否包含 Excel 不允許的非法字符
def contains_illegal_characters(value):
    if isinstance(value, str):
        illegal_chars = [chr(i) for i in range(32) if i not in (9, 10, 13)] + [chr(127)]
        if any(char in value for char in illegal_chars):
            return True
    return False

# 抓取當前頁面的數據
def scrape_page(driver, data):
    try:
        # 等待食品卡片顯示
        print("等待食品卡片顯示...")
        food_cards = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card.hover-shadow"))
        )
        print(f"找到 {len(food_cards)} 張食品卡片")

        # 遍歷每個卡片，點擊並抓取詳細信息
        for index in range(len(food_cards)):
            try:
                print(f"處理第 {index + 1} 張卡片")
                food_cards = driver.find_elements(By.CSS_SELECTOR, ".card.hover-shadow")
                card = food_cards[index]

                # 檢查並關閉可能存在的彈出框
                try:
                    close_button = driver.find_element(By.CSS_SELECTOR, "button[data-micromodal-close]")
                    close_button.click()
                    WebDriverWait(driver, 10).until_not(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-container"))
                    )
                    print("關閉了現有的彈出框")
                except Exception as e:
                    pass  # 如果沒有找到關閉按鈕，繼續進行

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
                time.sleep(1)

                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(card)
                )
                print("嘗試點擊卡片...")
                card.click()

                detail_popup = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".modal__container"))
                )
                print("詳細資料頁面已加載")
                time.sleep(2)

                popup_html = detail_popup.get_attribute('innerHTML')
                print("彈出框 HTML 已抓取")

                soup = BeautifulSoup(popup_html, 'html.parser')
                product_name = soup.find("h3", class_="title-bottom text-center").get_text(strip=True)
                business_name = soup.find("ul", class_="list-disc mb-8 pl-5 leading-loose").find("li").get_text(strip=True)

                def get_info_by_tag(tag_name):
                    try:
                        tag = soup.find("span", class_="tag tag-primary-100 mb-2", string=tag_name)
                        if tag:
                            info_list = tag.find_next("ul").find_all("li")
                            info = "\n".join([li.get_text(strip=True) for li in info_list])
                            return info
                    except Exception as e:
                        return ""
                    return ""

                product_info = soup.find_all("ul", class_="list-disc mb-8 pl-5 leading-loose")

                def get_info_from_ul(ul_elements, span_text):
                    for ul in ul_elements:
                        span = ul.find("span", class_="font-bold")
                        if span and span_text in span.text:
                            info_list = ul.find_all("li")
                            info = "\n".join([li.get_text(strip=True) for li in info_list])
                            return info
                    return ""

                source_info = get_info_from_ul(product_info, "產品來源")
                category_info = get_info_from_ul(product_info, "產品種類")
                weight_info = get_info_from_ul(product_info, "重量 / 容量 / 錠數")

                ingredients_info = get_info_by_tag("主要原料及添加物")
                applicable_info = get_info_by_tag("適用 / 保存")

                nutrition_info = ""
                nutrition_tag = soup.find("span", class_="tag tag-primary-100 mb-2", string="主要營養成分及含量")
                if nutrition_tag:
                    nutrition_div = nutrition_tag.find_next("div", class_="mb-8")
                    if nutrition_div:
                        nutrition_info = nutrition_div.get_text(strip=True)

                # 檢查數據中是否包含非法字符，如果包含則跳過
                if any(contains_illegal_characters(value) for value in [product_name, business_name, source_info, ingredients_info, nutrition_info, applicable_info]):
                    print(f"跳過包含非法字符的數據: {product_name}")
                    continue

                data.append({
                    "商品名稱": product_name,
                    "業者名稱": business_name,
                    "產品來源": source_info,
                    "主要原料及添加物": ingredients_info,
                    "營養成分": nutrition_info,
                    "適用範圍": applicable_info
                })

                try:
                    close_button = driver.find_element(By.CSS_SELECTOR, "button[data-micromodal-close]")
                    close_button.click()
                    WebDriverWait(driver, 10).until_not(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-container"))
                    )
                    print("彈出框已關閉")
                except Exception as e:
                    print("無法找到或點擊關閉按鈕，嘗試點擊背景以關閉彈出框")
                    driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "body"))
                    WebDriverWait(driver, 10).until_not(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-container"))
                    )
            except Exception as e:
                print(f"處理卡片時出錯: {e}")

    except Exception as e:
        print(f"處理頁面時出錯: {e}")

def perform_search_and_scrape(driver, page_number, data):
    driver.get("https://petfood.moa.gov.tw/Web/Food")

    print("等待網頁加載完成...")
    time.sleep(5)

    try:
        print("嘗試找到查詢按鈕...")
        search_button = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-primary")
        print("查詢按鈕找到，嘗試點擊...")
        search_button.click()
    except Exception as e:
        print(f"查找或點擊查詢按鈕時出錯: {e}")
        driver.quit()
        exit()

    if page_number > 1:
        print(f"跳轉到第 {page_number} 頁")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select.select-more"))
        )
        select_more = driver.find_element(By.CSS_SELECTOR, "select.select-more")
        driver.execute_script("arguments[0].value = arguments[1];", select_more, str(page_number))
        time.sleep(1)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", select_more)
        time.sleep(5)  # 等待頁面加載完成

    scrape_page(driver, data)

def batch_scrape_and_write(start_page, end_page, batch_size, output_file):
    for batch_start in range(start_page, end_page + 1, batch_size):
        batch_end = min(batch_start + batch_size - 1, end_page)
        print(f"抓取第 {batch_start} 頁到第 {batch_end} 頁的數據")

        data = []
        driver = create_driver()

        try:
            for page_number in range(batch_start, batch_end + 1):
                try:
                    perform_search_and_scrape(driver, page_number, data)
                except Exception as e:
                    print(f"處理第 {page_number} 頁時出錯: {e}")
                    continue
        finally:
            driver.quit()

        if os.path.exists(output_file):
            existing_df = pd.read_excel(output_file)
            new_df = pd.DataFrame(data)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            combined_df = pd.DataFrame(data)

        combined_df.to_excel(output_file, index=False)
        print(f"數據已保存到 {output_file}")

start_page = 1
end_page = 6500  # 您可以根據需要調整這個範圍
batch_size = 20  # 每次抓取和寫入的頁數
output_file = os.path.join(os.path.expanduser("~"), 'pet_food_data_batch_correct.xlsx')

batch_scrape_and_write(start_page, end_page, batch_size, output_file)
