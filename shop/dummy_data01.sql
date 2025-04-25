-- python generate_dummy_data.py 실행 후 아래 내용 진행

-- 고객 더미 데이터 수정
update customers set name='김기태', userid='danielcoleman', passwd='1234' where customer_id=19;
update customers set name='김나라', userid='tracy95', passwd='1111' where customer_id=20;
update customers set name='김대철', userid='tbaker', passwd='2222' where customer_id=21;
update customers set name='유순복', userid='bryantcraig', passwd='3333' where customer_id=22;
update customers set name='박소영', userid='joanwhite', passwd='4444' where customer_id=23;
update customers set name='이초연', userid='blackwellbrandon', passwd='1212' where customer_id=24;
update customers set name='이정숙', userid='todd97', passwd='1212' where customer_id=25;
update customers set name='함창훈', userid='nmercer', passwd='1004' where customer_id=26;
update customers set name='변영미', userid='laura52', passwd='7979' where customer_id=27;
update customers set name='강수민', userid='jacobpena', passwd='1234' where customer_id=28;
update customers set name='김재우', userid='kevin17', passwd='1255' where customer_id=29;
update customers set name='신예은', userid='lovegarrett', passwd='2848' where customer_id=30;
update customers set name='서지혜', userid='elizabethfreeman', passwd='3434' where customer_id=31;
update customers set name='김계희', userid='jeffreybrown', passwd='2482' where customer_id=32;
update customers set name='장원', userid='akelly', passwd='5678' where customer_id=33;
update customers set name='김슬기', userid='carterjames', passwd='8765' where customer_id=34;
update customers set name='박영점', userid='charles58', passwd='2848' where customer_id=35;
update customers set name='신동진', userid='julie94', passwd='9876' where customer_id=36;
update customers set name='이민호', userid='mburke', passwd='2121' where customer_id=37;
update customers set name='전창우', userid='garciaronald', passwd='4343' where customer_id=38;
update customers set name='송미선', userid='uedwards', passwd='6565' where customer_id=39;
update customers set name='김미리내', userid='raymondpitts', passwd='1414' where customer_id=40;
update customers set name='김문기', userid='lewischad', passwd='8284' where customer_id=41;
update customers set name='조주용', userid='bergeranthony', passwd='2121' where customer_id=42;
update customers set name='윤정호', userid='jorge27', passwd='4248' where customer_id=43;
update customers set name='송기석', userid='markcoffey', passwd='6767' where customer_id=44;
update customers set name='박진성', userid='gregorymaria', passwd='4748' where customer_id=45;
update customers set name='장원영', userid='daniel64', passwd='9876' where customer_id=46;
update customers set name='김명은', userid='victorerickson', passwd='3235' where customer_id=47;
update customers set name='오미란', userid='marshalltyler', passwd='9797' where customer_id=48;

commit;

-- 마케팅 더미 데이터 
-- 마케팅 테이블 더미 데이터 추가
INSERT INTO marketing (campaign_name, target_audience, budget, start_date, end_date)
VALUES
('여름 시즌 세일', '20대 여성', 5000000, '2024-06-01', '2024-06-30'),
('신제품 출시 이벤트', '30대 남성', 3000000, '2024-05-01', '2024-05-15'),
('가을 맞이 할인', '40대 이상', 4000000, '2024-09-01', '2024-09-30'),
('겨울 패션 프로모션', '20대 남성', 3500000, '2024-12-01', '2024-12-15'),
('블랙 프라이데이 특가', '30대 여성', 10000000, '2024-11-25', '2024-11-27'),
('핸드폰 액세서리 세일', '10대 남녀', 2000000, '2024-07-10', '2024-07-20'),
('할로윈 의상 할인', '10대 여성', 1500000, '2024-10-20', '2024-10-31'),
('봄맞이 대세 상품', '20대 남성', 2500000, '2024-04-01', '2024-04-15'),
('추석 특별 기획전', '40대 이상 여성', 3000000, '2024-09-01', '2024-09-10'),
('크리스마스 선물 이벤트', '20대 여성, 남성', 7000000, '2024-12-01', '2024-12-24'),
('재입고 알림 캠페인', '30대 여성', 1200000, '2024-08-10', '2024-08-20'),
('명절 선물 세트', '40대 남성', 3500000, '2024-08-25', '2024-09-05'),
('명품 할인 프로모션', '30대 남성', 8000000, '2024-07-01', '2024-07-15'),
('여름 휴가용 의류 세일', '20대 여성', 4500000, '2024-06-10', '2024-06-25'),
('새해 맞이 대할인', '20대 남성', 6000000, '2024-01-01', '2024-01-07'),
('스타일리시한 봄 의류 할인', '30대 여성', 3000000, '2024-04-10', '2024-04-25'),
('여름 나들이 패션', '20대 여성', 5000000, '2024-06-15', '2024-06-30'),
('겨울철 방한 용품 세일', '40대 이상 남성', 3500000, '2024-12-05', '2024-12-20'),
('겨울 스키 의류 세일', '20대 남성', 4500000, '2024-12-01', '2024-12-10'),
('봄 패션 트렌드 세일', '20대 여성', 2500000, '2024-03-01', '2024-03-15'),
('가을 레이어드 스타일', '30대 남성', 4000000, '2024-09-10', '2024-09-30'),
('피트니스 의류 할인', '30대 여성', 3000000, '2024-05-15', '2024-06-01'),
('가을 컬러 팔레트', '20대 남성', 3500000, '2024-10-01', '2024-10-15'),
('오래된 상품 재고 세일', '40대 이상', 2500000, '2024-08-15', '2024-08-31'),
('여성 명품 가방 세일', '20대 여성', 6000000, '2024-07-01', '2024-07-15'),
('겨울 홈 웨어 세일', '30대 여성', 4000000, '2024-12-10', '2024-12-20'),
('가정용 가전 세일', '40대 이상 남성', 5000000, '2024-11-01', '2024-11-15'),
('봄맞이 화장품 이벤트', '20대 여성', 2000000, '2024-04-05', '2024-04-20'),
('하계 스포츠 용품 세일', '10대 남녀', 3000000, '2024-06-01', '2024-06-15'),
('크리스마스 할인 이벤트', '30대 남성', 8000000, '2024-12-01', '2024-12-24'),
('신상품 출시 할인', '20대 여성', 4000000, '2024-05-01', '2024-05-15'),
('겨울철 필수 아이템 세일', '40대 이상', 3500000, '2024-12-01', '2024-12-10'),
('가을 신상 패션', '30대 여성', 5000000, '2024-09-01', '2024-09-15'),
('봄맞이 새로운 스타일', '20대 남성', 2500000, '2024-04-01', '2024-04-15'),
('주말 한정 특별 할인', '20대 여성, 남성', 3000000, '2024-07-10', '2024-07-12'),
('온라인 쇼핑몰 이벤트', '30대 남성', 6000000, '2024-10-01', '2024-10-10'),
('새해 첫 쇼핑 이벤트', '20대 여성', 4500000, '2024-01-01', '2024-01-07'),
('할로윈 기념 세일', '10대 남녀', 1500000, '2024-10-25', '2024-10-31'),
('여성 패션 아이템 세일', '30대 여성', 5000000, '2024-08-01', '2024-08-15'),
('추석 대세 상품', '40대 이상 남성', 3500000, '2024-09-05', '2024-09-10');

UPDATE sales s
SET marketing_id = (
    SELECT m.marketing_id
    FROM marketing m
    WHERE s.sale_date::DATE BETWEEN m.start_date AND m.end_date
    ORDER BY m.start_date ASC
    LIMIT 1
)
WHERE EXISTS (
    SELECT 1
    FROM marketing m
    WHERE s.sale_date::DATE BETWEEN m.start_date AND m.end_date
);

commit;

select * from customers;
select * from products;
select * from sales;
select * from marketing;
select * from payments;
select * from reviews;