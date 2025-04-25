def calculate(operation, x, y):
    '''
    operation  - takes the string [add, sub, mul, div]
    x & y - two numbers
    '''
    if operation == '더하기':
        return x + y
    
    elif operation == '빼기':
        if x > y:
            return x - y
        else:
            return y - x
        
    elif operation == '곱하기':
        return x * y
    
    elif operation == '나누기':
        return x / y