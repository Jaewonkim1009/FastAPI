import streamlit as st
import json
import requests

st.title ("간단한 계산기 앱")

option = st.selectbox("연산을 수행 할 항목을 선택 해주세요",
                      ("더하기", "빼기", "곱하기", "나누기"))

st.write("")
st.write("피 연산자를 선택 해 주세요")
x = st.slider("X", 0, 100, 20)
y = st.slider("Y", 0, 130, 10)

inputs = {"operation": option, "x" : x, "y" : y}

if st.button("계산"):
    res = requests.post(url = "http://127.0.0.1:8000/calculate", data= json.dumps(inputs))
    st.write("headers: ", res.headers)
    st.write("status_code: ", res.status_code)
    st.write("json: ", res.json())

    st.subheader(f"API로 부터 온 응답입니다. = {res.text}")

if st.button("관리자"):
    res = requests.get(url = "http://127.0.0.1:8000/admins/list")

    st.write(res)
    st.subheader(f"API로 부터 온 응답입니다. = {res.text}")