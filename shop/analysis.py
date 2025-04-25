import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import numpy as np
import json
from pandas import Timestamp
import math
from sklearn.linear_model import LinearRegression



# SQLAlchemy의 데이터 베이스 연결 설정 객체
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/shop"
engine = create_engine(DATABASE_URL)
def convert_timestamp(obj, format='%Y-%m-%d %H:%M:%S'):
    # Timestamp 또는 datetime 객체 처리
    if isinstance(obj, (Timestamp, datetime)):
        return obj.strftime(format)
    
    # 리스트 처리
    elif isinstance(obj, list):
        return [convert_timestamp(item, format) for item in obj]
    
    # 딕셔너리 처리
    elif isinstance(obj, dict):
        return {key: convert_timestamp(value, format) for key, value in obj.items()}
    
    # 그 외 객체는 그대로 반환
    else:
        return obj

# Period 객체를 문자열로 변환하는 함수
def convert_periods(obj):
    if isinstance(obj, pd.Period):
        return obj.strftime('%Y-%m')
    elif isinstance(obj, list):
        return [convert_periods(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_periods(value) for key, value in obj.items()}
    else:
        return obj

# JSON 직렬화 과정에서 NaN(Not a Number), 무한대(inf)
# 또는 음의 무한대 (-inf)와 같은 비정상적인 부동 소수점 값을 처리
# 비정상적인 float 값을 변환하는 함수
def handle_float_values(obj):
    if isinstance(obj, float):
        if math.isnan(obj):
            return None
        elif math.isinf(obj):
            return None
        else:
            return obj
    elif isinstance(obj, list): # 리스트 순회
        return [handle_float_values(item) for item in obj]
    elif isinstance(obj, dict): # 딕셔너리 순회
        return {key: handle_float_values(value) for key, value in obj.items()}
    else:
        return obj


def get_customer_analysis():
    try:
        # 고객 테이블과 판매 테이블에서 데이터 불러오기
        customers_df = pd.read_sql("SELECT * FROM customers", engine)
        sales_df = pd.read_sql("SELECT * FROM sales", engine)

        # 성별 인원수, 총 거래 건수, 총 판매 금액 집계
        gender_distribution = (
            customers_df
            .merge(sales_df, on='customer_id', how='left') # 고객과 판매 데이터 조인
            .groupby('gender') # 성별로 그룹화
            .agg(                                            # 집계 함수 적용 (컬럼이름, 집계 함수)
                customer_count = ('customer_id', 'nunique'), # 성별 고객 수
                total_sales = ('sale_id', 'count'),          # 성별 총 거래 건수
                total_revenue = ('total_price', 'sum')       # 성별 총 판매 금액
            )
            .reset_index()
        )
        # 회원별 구매 건수 및 금액 집계
        purchase_data = sales_df.groupby(['customer_id']).agg(
            purchase_count = ('sale_id', 'size'),
            total_amount = ('total_price', 'sum')
        ).reset_index()

        # 고객 정보와 결합
        purchase_data = pd.merge(customers_df[['customer_id', 'name']], purchase_data, on = 'customer_id', how='left')

        # 구매 건수 및 금액에 대한 통계 테이터 계산
        purchase_statistics = purchase_data[['purchase_count', 'total_amount']].describe().to_dict()

        # 최근 31일 동안 구매하지 않은 고객 조회
        current_date = datetime.now()
        thirty_one_days_ago = current_date - timedelta(days=30)
        last_purchase = sales_df.groupby('customer_id')['sale_date'].max().reset_index()
        last_purchase['sale_date'] = pd.to_datetime(last_purchase['sale_date'])
        inactive_customers = pd.merge(customers_df[['customer_id', 'name', 'userid', 'email', 'phone']],
                                      last_purchase, on ='customer_id', how='left')
        inactive_customers = inactive_customers[inactive_customers['sale_date'].isna() | (inactive_customers['sale_date'] < thirty_one_days_ago)]

        print("sales_df date range: ", sales_df['sale_date'].min(), sales_df['sale_date'].max())
        print("inactive_customers shape: ", inactive_customers.shape)

        # 상위 5명 고객 조회 (총 구매 금액 기준)
        top5_customers = sales_df.groupby(['customer_id']).agg(
            total_spent = ('total_price', 'sum')
        ).reset_index().sort_values('total_spent', ascending=False).head(5)
        top5_customers = pd.merge(customers_df[['customer_id', 'name', 'userid', 'email', 'phone']],
                                  top5_customers, on='customer_id', how='left').sort_values('total_spent', ascending=False).head(5)
        print("상위 5명 고객 조회 (총 구매 금액 기준)", top5_customers)

        # 데이터 변환
        results = {
            "gender_distribution" : gender_distribution.to_dict(orient='records'),
            "purchase_date" : purchase_data.to_dict(orient="records"),
            "purchase_statistics" : purchase_statistics, # 추가된 통계 데이터
            "inactive_customers" : inactive_customers.to_dict(orient='records'),
            "top5_customers" : top5_customers.to_dict(orient='records'),
        }
        results = convert_timestamp(results)
        return results
    except Exception as e:
        print(f"Error: {str(e)}")
        raise Exception (f"An error occurred while retrieving data: {str(e)}")


def def_months_predict(monthly_sales):
    # 월별 판매 데이터를 기반으로 선형 회귀 예측
    monthly_sales['month_num'] = np.arange(len(monthly_sales))

    # 선형 회귀 모델을 적용
    model = LinearRegression()
    model.fit(monthly_sales['month_num'].values.reshape(-1, 1), monthly_sales['total_monthly_sales_amount'].values)

    # 향후 12개월 예측
    future_months = np.arange(len(monthly_sales), len(monthly_sales) + 12).reshape(-1, 1)
    forecast_sales = model.predict(future_months)

    # 예측 결과를 데이터프레임에 추가
    future_dates = pd.date_range(start=monthly_sales['month'].max(), periods=13, freq='M')[1:]
    forecast_df = pd.DataFrame({
        'month' : future_dates,
        'predicted_sales' : forecast_sales
    })
    return forecast_df


def get_sales_analysis():
    try:
        # 테이블에서 데이터 불러오기
        sales_df = pd.read_sql("SELECT * FROM sales", engine)
        products_df = pd.read_sql("SELECT * FROM products", engine)
        customers_df = pd.read_sql("SELECT * FROM customers", engine)

        # 상품별 판매 금액 및 판매 수량 집계
        sales_summary = sales_df.groupby("product_id").agg(
            total_sales_amount = ('total_price', 'sum'),
            total_sales_quantity = ('quantity', 'sum')
        ).reset_index()

        # 상품명 결합
        sales_summary = pd.merge(sales_summary, products_df[['product_id', 'name']], on='product_id', how='left')
        print("판매 집계: " , sales_summary)

        # 가장 많이 팔린 상품 5개
        top5_products = sales_summary.sort_values('total_sales_amount', ascending=False).head(5)
        print("가장 많이 팔린 상품 5개: ", top5_products)

        # 가장 안 팔린 상품 5개
        bottom5_products = sales_summary.sort_values('total_sales_amount', ascending=True).head(5)
        print("가장 안 팔린 상품 5개: ", bottom5_products)

        # 월별 판매금액 집계: 판매 데이터 프레임에 월(month) 칼럼을 추가하고 월별 집계
        sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
        sales_df['month'] = sales_df['sale_date'].dt.to_period('M')

        monthly_sales = sales_df.groupby("month").agg(
        total_monthly_sales_amount=('total_price', 'sum'),
        #total_monthly_sales_count=('sale_id', 'count')
        ).reset_index()

        # 차후 1년간 월별 판매 예상 (선형 회귀 예측)
        monthly_sales['month'] = monthly_sales['month'].dt.strftime('%Y-%m')
        forecast_df = def_months_predict(monthly_sales)
        forecast_df['month'] = pd.to_datetime(forecast_df['month'])
        forecast_df['month'] = forecast_df['month'].dt.to_period('M')
        print("예상 판매: ", forecast_df)

        # 데이터 변환
        results = {
            "sales_summary" : sales_summary.to_dict(orient='records'),
            "top5_products" : top5_products.to_dict(orient='records'),
            "bottom5_products" : bottom5_products.to_dict(orient='records'),
            "monthly_sales" : monthly_sales.to_dict(orient='records'),
            "predict_sales" : forecast_df.to_dict(orient='records')
        }

        results = convert_timestamp(results)
        results = convert_periods(results)
        return results
    except Exception as e:
        print(f"Error: {str(e)}")
        raise Exception (f"An error occurred while retrieving data: {str(e)}")
    
def get_marketing_analysis():
    try:
        # 데이터 불러오기
        campaigns_df = pd.read_sql("SELECT * FROM marketing", engine)
        sales_df = pd.read_sql("SELECT * FROM sales", engine)
        customers_df = pd.read_sql("SELECT * FROM customers", engine)
        products_df = pd.read_sql("SELECT * FROM products", engine)

        print(campaigns_df.columns)  # campaigns_df의 모든 컬럼을 출력해 봅니다.

        # 날짜 변환: sales_df의 sale_date를 DATE 타입으로 변환
        sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date']).dt.date

        # 캠페인별 판매 분석: marketing_id로 그룹하고 total_price, quantity의 합을 집계합니다.
        campaign_sales = sales_df.groupby('marketing_id').agg(
            total_sales_amount=('total_price', 'sum'),
            total_sales_quantity=('quantity', 'sum')
        ).reset_index()
        campaign_sales = pd.merge(campaign_sales, campaigns_df[['marketing_id', 'campaign_name']], on='marketing_id', how='left')

        # 캠페인별 참여 고객 수 (마케팅 ID를 통해 참여한 고객 수)
        campaign_participants = sales_df.groupby('marketing_id')['customer_id'].count().reset_index()
        campaign_participants = pd.merge(campaign_participants, 
                                         campaigns_df[['marketing_id', 'campaign_name']], on='marketing_id', how='left')
        campaign_participants.rename(columns={'customer_id': 'participant_count'}, inplace=True)

        # 캠페인별 ROI 분석 (ROI = (판매금액 - 마케팅비용) / 마케팅비용)
        campaigns_df = pd.merge(campaigns_df, campaign_sales[['marketing_id', 'total_sales_amount']], 
                                on='marketing_id', how='left')
        campaigns_df['roi'] = (campaigns_df['total_sales_amount'] - campaigns_df['budget']) / campaigns_df['budget']
        roi_analysis = campaigns_df[['marketing_id', 'campaign_name', 'roi']]

        # 상품별 캠페인 효과 분석
        product_campaign_sales = sales_df.groupby(['marketing_id', 'product_id']).agg(
            total_sales_amount=('total_price', 'sum'),
            total_sales_quantity=('quantity', 'sum')
        ).reset_index()
        product_campaign_sales = pd.merge(product_campaign_sales, 
                                          products_df[['product_id', 'name']], on='product_id', how='left')
        product_campaign_sales = pd.merge(product_campaign_sales, 
                                          campaigns_df[['marketing_id', 'campaign_name']], on='marketing_id', how='left')

        # 고객 세그먼트별 마케팅 분석 (예시: 고객의 연령대별로 분석)
        customers_df['age'] = customers_df['birth_date'].apply(lambda x: (datetime.now() - pd.to_datetime(x)).days // 365)  # 나이 계산
        customers_df['age_group'] = pd.cut(customers_df['age'], bins=[0, 18, 30, 40, 50, 60, 100], 
                                           labels=['18 이하', '19-30', '31-40', '41-50', '51-60', '60 이상'])

        segment_sales = sales_df.groupby(['marketing_id', 'customer_id'], observed=True).agg(
            total_sales_amount=('total_price', 'sum')
        ).reset_index()
        segment_sales = pd.merge(segment_sales, customers_df[['customer_id', 'age_group']], on='customer_id', how='left')
        segment_sales = pd.merge(segment_sales, campaigns_df[['marketing_id', 'campaign_name']], on='marketing_id', how='left')
        segment_sales = segment_sales.groupby(['campaign_name', 'age_group']).agg(
            total_sales_amount=('total_sales_amount', 'sum')
        ).reset_index()

        # 데이터 변환
        results = {
            "campaign_sales": campaign_sales.to_dict(orient='records'),
            "campaign_participants": campaign_participants.to_dict(orient='records'),
            "roi_analysis": roi_analysis.to_dict(orient='records'),
            "product_campaign_sales": product_campaign_sales.to_dict(orient='records'),
            "segment_sales": segment_sales.to_dict(orient='records')
        }

        # return results
        results = convert_timestamp(results)
        results = handle_float_values(results)
        return results

    except Exception as e:
        print(f"Error: {str(e)}")
        raise Exception(f"An error occurred while retrieving data: {str(e)}")