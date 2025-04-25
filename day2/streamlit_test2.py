import streamlit as st
import json
import requests

st.title("판매 시스템")

option = st.selectbox("작업을 선택해주세요",
                     ("상품 구매", "상품 환불"))

st.write("")
st.write("상품 정보를 입력해주세요")
price = st.slider("상품 가격 (단위: 천 원)", 1, 100, 1)
quantity = st.slider("수량", 0, 100, 1)

inputs = {"items": option, "x": price, "y": quantity}

if st.button("계산"):
    res = requests.post(url="http://127.0.0.1:8000/calculate_sale", 
                       data=json.dumps(inputs))
    st.subheader(f"계산 결과: {res.json()['result']}원")
