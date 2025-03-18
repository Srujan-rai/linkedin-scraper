import os
import random
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def type_text(element, text, min_delay=0.1, max_delay=0.3):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))


def random_sleep(min_seconds=1, max_seconds=5):
    delay = random.uniform(min_seconds, max_seconds)
    print(f"Sleeping for {delay:.2f} seconds...")
    time.sleep(delay)


def login(driver, username, password):
    email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    email_field.clear()
    type_text(email_field, username)
    
    random_sleep(1, 4)
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
    password_field.clear()
    type_text(password_field, password)
    
    random_sleep(1, 5)
    sign_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'btn__primary--large')]")))
    sign_in_button.click()
    random_sleep(2, 5)


def save_page_content(driver, profile_name, category, base_output_folder):
    profile_folder = os.path.join(base_output_folder, profile_name)
    os.makedirs(profile_folder, exist_ok=True)
    
    page_html = driver.page_source
    file_path = os.path.join(profile_folder, f"{category}.html")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(page_html)
    print(f"Saved {category} HTML: {file_path}")
    
    soup = BeautifulSoup(page_html, "html.parser")
    text = soup.get_text(separator='\n', strip=True)
    start_index = text.find("Skip to search") + len("Skip to search")
    text = text[start_index:].strip()  
    text_file_path = os.path.join(profile_folder, f"{category}.txt")
    with open(text_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(text)
    print(f"Extracted text saved: {text_file_path}")
    
    urls = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith("http")]
    urls_file_path = os.path.join(profile_folder, f"{category}_urls.txt")
    with open(urls_file_path, "w", encoding="utf-8") as output_file:
        output_file.write("\n".join(urls))
    print(f"Extracted URLs saved: {urls_file_path}")


def scrape_linkedin_profiles(driver, profile_urls, output_folder):
    for profile_url in profile_urls:
        driver.get(profile_url)
        random_sleep(1, 3)
        
        profile_name = profile_url.split("/")[-2]
        print(f"Scraping profile: {profile_name}")
        
        save_page_content(driver, profile_name, "profile", output_folder)
        
        random_sleep(2, 5)
        
        with open(os.path.join(output_folder, profile_name, "profile_urls.txt"), "r", encoding="utf-8") as file:
            urls = file.read().splitlines()
        
        sub_paths = ["details/skills", "details/certifications", "details/interests"]
        for path in sub_paths:
            matching_urls = [url for url in urls if path in url]
            if matching_urls:
                driver.get(matching_urls[0])
                random_sleep(1, 3)
                save_page_content(driver, profile_name, path.split("/")[-1], output_folder)
                random_sleep(2, 5)


def main():
    output_folder = "linkedin_profiles"
    os.makedirs(output_folder, exist_ok=True)
    
    options = webdriver.ChromeOptions()
    options.add_argument("/home/srujan/.config/google-chrome")
    options.headless = False
    driver = uc.Chrome(options=options)
    
    driver.get("https://www.linkedin.com/login")
    login(driver, username="raisrujangcp@gmail.com", password="4SF21CI047")
    
    profile_urls = [
        "https://www.linkedin.com/in/omkar-sawant-706549107/",
    ]
    
    scrape_linkedin_profiles(driver, profile_urls, output_folder)
    
    driver.quit()
    print("Scraping completed. All profiles saved, text extracted, and URLs saved.")


if __name__ == "__main__":
    
    main()