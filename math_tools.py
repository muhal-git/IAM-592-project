import secrets #for generating cryptographically! secure random integers
import random  #for generating random numbers(not cryptographically secure)

'''
egcd(..,..) recursively calculates greatest common divisor(gcd) of integers a and b
Also it caluculates x&y such that gcd(a,b) = x*a + y*b
This function also can be use for finding inverse of a in modulo b

input: a, b
output:gcd(a,b), x, y (such that gcd(a,b) = x*a + y*b)
'''
def egcd(a, b):

    # handling base Case
    if a == 0 :
        return b, 0, 1

    gcd, x1, y1 = egcd(b%a, a)

    # updating x and y recursively
    x = y1 - (b//a) * x1
    y = x1

    return gcd, x, y

'''
Using egcd(..,..),inverse_mod(..,..) calculates and returns inverse of a in mod b

input: a, b
output:inverse(say it is inv) of a in modulo b ( so that (a*inv)%b=1 )
'''
def inverse_mod(a,b):

    #handles the case gcd(a,b)=1, since if not there is no inverse of a in mod b
    if egcd(a,b)[0]!=1:
        print("inverse of",a,"in modulo",b,"does not exist !")
        return False

    inverse_of_a_in_mod_b = egcd(a,b)[1]

    if inverse_of_a_in_mod_b < 0:
        inverse_of_a_in_mod_b+=b
    return inverse_of_a_in_mod_b

'''
miiller_rabin_test(d,n) makes Miller-Rabin primality test, it is a probabilistic
primality test, miillerTest(d,n) function looks for primality of integr n,
such that n - 1 = (2^d)*k

input: d, n ( so that n-1 = 2^(d)*k for some odd k )
output:False(if n is not prime) or True(if n is (probably) prime)
'''
def miiller_rabin_test(d, n):

    # take a random number from [2,...,n-2]
    a = 2 + secrets.randbelow(n-4)

    # applying Miller-Rabin primality test
    x = pow(a, d, n);
    if (x == 1 or x == n - 1):
        return True;

    while (d != n - 1):
        x = (x * x) % n;
        d *= 2;

        if (x == 1):
            return False;
        if (x == n - 1):
            return True;

    return False;



'''
isPrime(n,k) looks for primality of n using miiller_rabin_test() function k-times
greater k means greater accuracy of the test--->Error of this test is E(k)= 1/(4^k) 

input: n, k(number of tests, equals to 64 as default)
output:False(if n is not prime) or True(if n is (probably) prime)
'''
def isPrime( n, k=64):
	
    if (n <= 1 or n%2 == 0):
        return False;
    if (n <= 3):
        return True;

    # finding d such that n = n-1 = 2^(d)*k
    d = n - 1;
    while (d % 2 == 0):
        d //= 2;
	
	
    for i in range(k):
        if (miiller_rabin_test(d, n) == False):
            return False;
    return True;


#generating 1024 bit primes and looking for primality of them
'''
k=7
i=0
while True:
	if k<=10:
		#print("number generated.")
		p=secrets.randbits(1024)
		if(p%2==0):
			p=p-1
		i+=1
		if isPrime(p,10):
			print("found at ",i,"th try",k,"th prime:",p)
			k=k+1
			if k==11:
				break

'''
