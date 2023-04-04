from django.shortcuts import render
import os
import openai
from dotenv import load_dotenv
load_dotenv()
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

api_key = os.getenv('OPENAI_KEY', None)

def get_data():
    path = 'C:\Program Files\Mozilla Firefox\firefox.exe'
    browser = webdriver.Firefox(executable_path=path)
    browser.get('https://www.sharecare.com/healthy-aging/want-keep-heart-brain-young')
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    sleep(2)
    article_div = browser.find_element(By.CLASS_NAME, 'article__content')
    paragraphs = article_div.find_elements(By.TAG_NAME, 'p')
    return paragraphs

def chatbot(request) :
  # chatbot_response = None
  my_list= []
  if api_key is not None and request.method == 'POST':
    paragraphs = get_data()
    openai.api_key = api_key
    user_input = request.POST.get('user_input')
    for p in paragraphs:
      prompt = f'{user_input}: "{p.text}"'
      response = openai.Completion.create(
        engine = 'text-davinci-003', # text-ada-001
        prompt = prompt,
        max_tokens=256,
        # stop=","
        temperature=0.5
      )
      my_list.append(response["choices"][0]["text"])
      sleep(0.5)
  return render(request, 'main.html', {"my_list": my_list})
