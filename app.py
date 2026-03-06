import streamlit as st
import random
import requests
import os

# Массив из 30 вопросов по физике
questions = [
    # ... (твой массив вопросов остаётся без изменений)
]

# Функция для запроса к API ГигаЧата
def ask_gigachat(prompt):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ['MDE5Y2MzOTItZDU4MS03M2I3LWE1MDItNjUyNGIxNzIyYjEwOmM5OTJiN2VkLWMxOGEtNDk1Ny1hZGQwLTEwZmM5Mjk2MDY1Zg==']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "GigaChat",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=data, verify=False)  # <-- Отключена проверка SSL
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Извините, не удалось получить ответ от API. Код ошибки: {response.status_code}"
    except Exception as e:
        return f"Произошла ошибка: {e}"

# Основной интерфейс
st.title("🤖 Бот по физике")

# Поле ввода и кнопка для вопроса
user_input = st.text_input("Задайте вопрос по физике:")

if st.button("Отправить вопрос"):
    if user_input:
        if any(word in user_input.lower() for word in ["физик", "сила", "ток", "энергия", "скорость", "давление"]):
            answer = ask_gigachat(user_input)
            st.write(f"Бот: {answer}")
        else:
            st.write("Бот: Давайте обсудим физику!")

# Кнопка для случайного вопроса
if st.button("🎲 Задать случайный вопрос"):
    question = random.choice(questions)
    st.write(f"Бот: {question['question']} (Варианты: {', '.join(question['options'])})")

    user_answer = st.text_input("Ваш ответ:")
    if user_answer:
        if user_answer.lower() == question["answer"].lower():
            st.write("Бот: Правильно!")
        else:
            st.write(f"Бот: Неправильно. Правильный ответ: {question['answer']}")
