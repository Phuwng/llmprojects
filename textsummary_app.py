# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import ollama

# # Constants
# MODEL = "llama3.2"

# # A class to represent a Webpage
# class Website:
#     """
#     A utility class to represent a Website that we have scraped
#     """
#     url: str
#     title: str
#     text: str

#     def __init__(self, url):
#         """
#         Create this Website object from the given URL using the BeautifulSoup library
#         """
#         self.url = url
#         response = requests.get(url)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         self.title = soup.title.string if soup.title else "No title found"
#         for irrelevant in soup.body(["script", "style", "img", "input"]):
#             irrelevant.decompose()
#         self.text = soup.body.get_text(separator="\n", strip=True)

# # System prompt for the model
# system_prompt = (
#     "You are an assistant that analyzes the contents of a website "
#     "and provides a short summary, ignoring text that might be navigation related. "
#     "Respond in markdown."
# )

# # Function to create the user prompt
# def user_prompt_for(website):
#     user_prompt = f"You are looking at a website titled {website.title}. "
#     user_prompt += (
#         "The contents of this website are as follows; "
#         "please provide a short summary of this website in markdown. "
#         "If it includes news or announcements, then summarize these too.\n\n"
#     )
#     user_prompt += website.text
#     return user_prompt

# # Function to create messages for the model
# def messages_for(website):
#     return [
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": user_prompt_for(website)},
#     ]

# # Function to summarize a URL
# def summarize(url):
#     try:
#         website = Website(url)
#         messages = messages_for(website)
#         response = ollama.chat(model=MODEL, messages=messages)
#         return response['message']['content']
#     except Exception as e:
#         return f"An error occurred: {e}"

# # Streamlit app
# st.title("Website Summary App")
# st.markdown(
#     "Enter a URL to summarize the content of the website using the Ollama API."
# )

# # Input URL
# url = st.text_input("Enter a URL:", "")

# if st.button("Summarize"):
#     if url:
#         with st.spinner("Summarizing..."):
#             summary = summarize(url)
#         st.markdown(summary)
#     else:
#         st.warning("Please enter a valid URL.")

import streamlit as st
import requests
from deep_translator import GoogleTranslator

# các thư viện cần thiết
import os
import subprocess
import sys

# đảm bảo deep-translator được cài khi app khởi chạy
try:
    from deep_translator import GoogleTranslator
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "deep-translator"])
    from deep_translator import GoogleTranslator


# Hàm gọi Ollama để tóm tắt
def summarize_text(text):
    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "llama3.2",  
        "messages": [
            {"role": "user", "content": f"Summarize this text: {text}"}
        ]
    }
    response = requests.post(url, headers=headers, json=data, stream=True)
    
    result = ""
    for line in response.iter_lines():
        if line:
            try:
                json_line = line.decode("utf-8")
                import json
                data = json.loads(json_line)
                if "message" in data:
                    result += data["message"]["content"]
            except Exception as e:
                st.error(f"Lỗi khi parse: {e}")
    return result

# Hàm dịch thuật
def translate_text(text, target_lang):
    try:
        translated = GoogleTranslator(source="auto", target=target_lang).translate(text)
        return translated
    except Exception as e:
        return f"Lỗi dịch thuật: {e}"

# Giao diện Streamlit
st.title("📘 Ứng dụng Tóm tắt & Dịch thuật")

option = st.radio("Chọn chức năng:", ("Tóm tắt văn bản", "Dịch văn bản"))

if option == "Tóm tắt văn bản":
    input_text = st.text_area("Nhập văn bản cần tóm tắt:")
    if st.button("Tóm tắt"):
        if input_text.strip():
            summary = summarize_text(input_text)
            st.subheader("✨ Kết quả tóm tắt:")
            st.write(summary)
        else:
            st.warning("Vui lòng nhập văn bản!")

elif option == "Dịch văn bản":
    input_text = st.text_area("Nhập văn bản cần dịch:")
    target_lang = st.selectbox("Chọn ngôn ngữ đích:", ["en", "vi", "fr", "de", "ja", "zh-cn"])
    if st.button("Dịch"):
        if input_text.strip():
            translated = translate_text(input_text, target_lang)
            st.subheader("🌍 Kết quả dịch:")
            st.write(translated)
        else:
            st.warning("Vui lòng nhập văn bản!")
