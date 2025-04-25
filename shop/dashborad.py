import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

# 데이터 가져오기
try:
    customer_data = requests.get("http://127.0.0.1:8000/analysis/customer")
    customer_data = customer_data.json()
    # print(data)
except Exception as e:
    st.error(f"API 요청 실패 {e}")
    customer_data = {}

# 탭 생성
tab1, tab2, tab3 = st.tabs(["고객 분석", "판매 분석", "마케팅 분석"])

# 고객 분석 탭
with tab1:
    st.header("고객 분석 데이터")
    # 성별 분포
    st.subheader("성별 분포")
    st.dataframe(customer_data['gender_distribution'])

    # 회원별 구매 횟수 및 금액
    st.subheader("회원별 구매 횟수 및 총 금액")
    purchase_df = pd.DataFrame(customer_data['purchase_data'])
    st.dataframe(purchase_df)
