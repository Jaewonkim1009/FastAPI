# PostgreSQL 드라이버
import psycopg
import psycopg_pool
from config import config

# psycopg-pool로 PostgreSQL DB pool 생성
pool_default = psycopg_pool.ConnectionPool(
    config.PGSQL_TEST_DATABASE_STRING,
    min_size = config.PGSQL_TEST_POLL_MIN_SIZE,
    max_size = config.PGSQL_TEST_POLL_MAX_SIZE,
    max_idle = config.PGSQL_TEST_POLL_MAX_IDLE,
)

# procedure 사용하기
# 쿼리문으로 목록 가져오기
def list_admin():
    with pool_default.connection() as conn:
        cur = conn.cursor(row_factory=psycopg.rows.dict_row)

        try:
            # cur.execute("call sp_l_admin('out1)")
            # results = cur.execute("fetch all from out1").fetchall()
            # conn.commit()
            results = cur.execute("select * from tb_admin").fetchall()
        except psycopg.OperationalError as e:
            print(f"An error occurred: {e}")
            results = False
        except psycopg.ProgrammingError as e:
            print(f"Programming error occurred: {e}")
            results = False
    return results
