from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# 初始化 DataFrame
all_data = pd.DataFrame()


def fetch_table_data(year, month, area_id):
    global all_data

    driver.get(f"https://cabu.kcg.gov.tw/Stat/StatRpts/StatRpt6.aspx?qm=ByYearMonth&yq={year}&mq={month}&dq={area_id}")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_cphContent_tableQueryByYM"))
    )

    table_html = driver.execute_script(
        "return document.getElementById('ctl00_cphContent_tableQueryByYM').outerHTML;"
    )

    df = pd.read_html(table_html)[0]
    df = df.iloc[0:, [0, 1, 2, 6, 7, 8, 10]]
    df = df[df['性別'] == '計']
    df['年份'] = year
    df['月份'] = month
    df['區域ID'] = area_id
    df.columns = ['區別', '性別', '總計', '0-14歲', '15-39歲', '40-64歲', '65歲以上', '年份', '月份', '區域ID']

    # 將新抓取的資料附加到 all_data DataFrame
    all_data = pd.concat([all_data, df], ignore_index=True)


# 初始化 Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    for year in range(110, 114):  # 110年到113年
        for month in range(1, 13):  # 1月到12月
            for area in range(10, 381, 10):  # 64000010到64000380，間隔為10
                area_id = f"64000{area:03d}"
                fetch_table_data(year, month, area_id)
                time.sleep(2)  # 每次請求後暫停2秒
finally:
    driver.quit()  # 確保瀏覽器最後被關閉

# 將所有資料寫入同一份 CSV 檔案
all_data.to_csv('population_data.csv', index=False, encoding='utf-8')
print('所有資料已寫入 CSV 檔案。')
