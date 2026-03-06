import streamlit as st
import random
import requests
import os

# Массив из 30 вопросов по физике
questions = [
    {
        "question": "Что измеряет амперметр?",
        "options": ["Напряжение", "Сила тока", "Сопротивление", "Мощность"],
        "answer": "Сила тока"
    },
    {
        "question": "Какая единица измерения силы?",
        "options": ["Килограмм", "Ньютон", "Джоуль", "Ватт"],
        "answer": "Ньютон"
    },
    # ... (остальные вопросы оставляете без изменений)
]

# Функция для запроса к API ГигаЧата
def ask_gigachat(prompt):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    token = os.environ.get('API_TOKEN')
    st.write("Отладочная информация:")
    st.write(f"Токен (первые 5 символов): {token[:5]}...")  # Для безопасности выводим только начало токена
    st.write(f"URL: {url}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "model": "GigaChat-Pro",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data, verify=False)
        st.write(f"Status Code: {response.status_code}")
        st.write(f"Response: {response.text}")

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Ошибка API: {response.status_code}. Ответ: {response.text}"
    except Exception as e:
        return f"Исключение: {e}"

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
