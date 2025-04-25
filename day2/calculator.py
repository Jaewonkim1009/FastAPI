def calculate_sale(items, x, y):
    '''
    items - 상품 구매/환불 여부
    x - 상품 가격
    y - 구매 수량
    '''
    if items == "상품 구매":
        return x * y  # 총 구매 금액 계산
    
    elif items == "상품 환불":
        return -(x * y)
    
    else:
        return 0