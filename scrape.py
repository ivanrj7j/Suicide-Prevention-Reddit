from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
import time
from pandas import DataFrame
from uuid import uuid1
import sys
import random
from tqdm import tqdm
from ai import getSuicidal

driver = Firefox()
# initiating driver 

totalScroll = int(sys.argv[1:][0])
print(f"[INFO] Loaded all modules, scrolling {totalScroll} time(s).")

driver.get("https://www.reddit.com")
time.sleep(3)
# going to reddit 

print("[INFO] loaded website")

def getScrollCommand():
    scrollAmount = random.randint(600, 1700)
    command = f"window.scrollBy(0, {scrollAmount});"
    duration = random.randint(1, 3)/2

    return command, duration

def getTitles():
    titles = list(map(lambda x:(x.text, x.get_attribute("href")), driver.find_elements(By.CSS_SELECTOR, "[id*=post-title]")))
    return titles

titles = []

for _ in tqdm(range(totalScroll), desc="Scraping"):
    command, duration = getScrollCommand()
    driver.execute_script(command)
    titles += getTitles()
    time.sleep(duration)

driver.close()

titles = list(set(titles))
print(f"[INFO] Finished scraping")

outputFile = f"files/{str(uuid1())}.csv"
df = DataFrame(titles, columns=["title", "url"])
df, suicidalURLs = getSuicidal(df)
print(f"[INFO] Predictions complete")

df.to_csv(outputFile)
print(f"[INFO] File saved to {outputFile}")



print('\n\n')
if suicidalURLs.size == 0:
    print(f"[INFO] No Suicidal posts found")
else:
    print(suicidalURLs)