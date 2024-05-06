import streamlit as st
import openai

openai.api_key = st.secrets["api_key"]

st.title("DJ's ChatGPT Plus DALL-E2")

# 세션 상태에 user_input이 없으면 초기화
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""

with st.form("form"):
    # 세션 상태를 사용하여 사용자 입력 관리
    user_input = st.text_input("Prompt", value=st.session_state['user_input'], placeholder="텍스트를 입력해 주세요")
    size = st.selectbox("Size", ["1024x1024", "512x512", "256x256"])
    submit = st.form_submit_button("Submit")

if submit and user_input:
    st.session_state['user_input'] = user_input  # 세션 상태 업데이트

    gpt_prompt = [{
        "role": "system",
        "content": "Imagine the detailed appearance of the input. Respond around 20 words."
    }, {
        "role": "user",
        "content": user_input
    }]

    with st.spinner("기다려주세요!"):
        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=gpt_prompt
        )

    prompt = gpt_response.choices[0].message['content']
    st.write(prompt)

    with st.spinner("그림 생성 중입니다.. 잠시만 기다려주세요!"):
        dalle_response = openai.Image.create(
            prompt=prompt,
            n=4,
            size=size
        )

    # 생성된 이미지를 표시
    for image_data in dalle_response['data']:
        st.image(image_data['url'])

    # 제출 후 입력 필드 초기화
    st.session_state['user_input'] = ""  # 입력 필드를 비웁니다.