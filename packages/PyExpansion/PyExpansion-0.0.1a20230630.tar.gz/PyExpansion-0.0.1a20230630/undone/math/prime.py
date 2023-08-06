def get_list_prime(number, start=2):
    prime_list = [2]
    for x in range(start, number):
        if is_prime(x):
            prime_list.append(x)
    return prime_list
        

def is_prime(number):
    for i in range(2, number):
        if(number % i) == 0:
            return False
    return True
