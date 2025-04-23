#config/config.py
PGSQL_TEST_DATABASE_STRING = "host=127.0.0.1 dbname=testdb user=prostgres password=1234 port=5432"

# connection pool (일정 수의 연결을 만들어 두고 재사용)
PGSQL_TEST_POLL_MIN_SIZE = 10 # 커넥션 풀에서 유지할 최소 연결수
PGSQL_TEST_POLL_MAX_SIZE = 10 # 동시에 사용 할 수 있는 최대 연결수
PGSQL_TEST_POLL_MAX_IDLE = 60 # 최대 유휴시간 / 사용되지 않은 커넥션이 60초이상 유휴 상태 일 경우 제거 대상이 됨