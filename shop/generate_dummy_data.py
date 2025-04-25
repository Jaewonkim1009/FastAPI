# conda install psycopg2 faker
# 고객 30명 생성
# 상품 30개 생성
# 판매 1000건 생성
# 결제 1000건 (판매와 연결)
# 리뷰 900건 (일부 판매된 상품에 연결)

import psycopg2
import random
from faker import Faker
from datetime import datetime, timedelta
import string
import pytz

# 예: 한국 시간대 지정
korea_tz = pytz.timezone("Asia/Seoul")

# DB 연결
DB_NAME = "shop"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"

faker = Faker('ko_KR')

def connect_db():
    return psycopg2.connect(
        dbname = DB_NAME, user = DB_USER, password = DB_PASSWORD, host = DB_HOST
    )

# 영어 + 숫자로 이루어진 아이디 생성 (8글자)
def generate_userid(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# 중복 확인 
def add_user_credentials(customers_df):
    df = customers_df.copy()
    existing_userids = set(df['userid'].dropna())

    def unique_userid():
        while True:
            userid = generate_userid()
            if userid not in existing_userids:
                existing_userids.add(userid)
                return userid



# 고객 데이터 30개 생성
def insert_customers(cursor):
    userids_set = set()
    emails_set = set()
    created_count = 0

    while created_count < 30:
        userid = faker.user_name()
        email = faker.email()

        # 중복된 userid나 email이면 다시 생성
        if userid in userids_set or email in emails_set:
            continue

        userids_set.add(userid)
        emails_set.add(email)

        name = faker.name()
        phone = faker.phone_number()[:15]
        gender = random.choice(["남", "여"])
        passwd = faker.password()[:4]
        birth_date = faker.date_of_birth()
        registration_date = faker.date_time_between(start_date='-2y', end_date='now', tzinfo=korea_tz)

        try:
            cursor.execute(
                """
                INSERT INTO customers (name, email, phone, gender, userid, passwd, birth_date, registration_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (name, email, phone, gender, userid, passwd, birth_date, registration_date)
            )
            created_count += 1
        except Exception as e:
            print(f"오류 발생: {e}")
            
# 상품 데이터 30개 생성
def insert_products(cursor):
    for _ in range(30):
        name = faker.word()
        category = random.choice(["가전제품", "옷", "가구", "책"])
        price = round(random.uniform(10, 1000), 2)
        stock_quantity = random.randint(10, 100)
        created_at = faker.date_time_between(start_date='-2y', end_date='now', tzinfo=korea_tz)

        cursor.execute(
            """
            INSERT INTO products (name, category, price, stock_quantity, created_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (name, category, price, stock_quantity, created_at)
        )

# 판매 1000건 생성
def insert_sales(cursor):
    # customer_id만 조회하여 단일 컬럼 데이터를 처리
    # 리스트 컴프리헨션 ([row[0] for row in cursor.fetchall()])을 사용
    # 튜플에서 값을 추출 (row[0]) 하여 단순한 ID 리스트 생성
    cursor.execute("SELECT customer_id FROM customers")
    customers = [row[0] for row in cursor.fetchall()]

    # product_id와 price를 모두 조회하여 다중 컬럼 데이터를 처리
    # fetchall() 결과를 그래도 사용, 각 행의 튜플을 유지
    cursor.execute("SELECT product_id, price FROM products")
    products = cursor.fetchall()

    sales = []
    for _ in range(1000):
        customers_id = random.choice(customers)
        product_id, price = random.choice(products)
        quantity = random.randint(1, 5)
        total_price = price * quantity
        sale_date = faker.date_time_between(start_date = '-1y', end_date = 'now', tzinfo=korea_tz)
        sales.append((customers_id, product_id, quantity, total_price, sale_date))

    cursor.executemany(
        """
        INSERT INTO sales (customer_id, product_id, quantity, total_price, sale_date)
        VALUES (%s, %s, %s, %s, %s)
        """,
        sales
)
# 결제 1000건 생성
def insert_payments(cursor):
    cursor.execute("SELECT sale_id FROM sales")
    sales = [row[0] for row in cursor.fetchall()]

    payment_method = random.choice(["credit card", "paypal", "cash card"])
    payment_status = random.choice(["success", "pending", "fail"])
    
    payments = []
    for _ in range(1000):
        sale_id = random.choice(sales)
        method = random.choice(payment_method)
        status = random.choice(payment_status)
        payment_date = faker.date_time_between(start_date = '-1y', end_date = 'now')
        payments.append((sale_id, method, status, payment_date))

    cursor.executemany(
        """
        INSERT INTO payments (sale_id, payment_method, payment_status, payment_date)
        VALUES (%s, %s, %s, %s)
        """,
        payments
)

# 리뷰 900건 생성
def insert_reviews(cursor):
    cursor.execute("SELECT sale_id, customer_id, product_id FROM sales ORDER BY RANDOM() LIMIT 900")
    reviews = []
    for sale_id, customer_id, product_id in cursor.fetchall():
        rating = random.randint(1, 5)
        #review_text = faker.text(max_nb_chars=200) if random.random() > 0.2 else None # 20% 확률로 텍스트 없음
        review_text = faker.paragraph(nb_sentences=3, variable_nb_sentences=True)[:200] if random.random() > 0.2 else None # 한글로 나오게 설정
        review_date = faker.date_time_between(start_date="-1y", end_date="now")
        reviews.append((customer_id, product_id, rating, review_text, review_date))

    cursor.executemany(
        """
        INSERT INTO reviews (customer_id, product_id, rating, review_text, review_date)
        VALUES (%s, %s, %s, %s, %s)
        """,
        reviews
    )

def main():
    conn = connect_db()
    cursor = conn.cursor()

    insert_customers(cursor)
    insert_products(cursor)
    insert_sales(cursor)
    insert_payments(cursor)
    insert_reviews(cursor)

    conn.commit()
    cursor.close()
    conn.close()
    print("더미 데이터 생성 완료")

if __name__ == "__main__":
    main()