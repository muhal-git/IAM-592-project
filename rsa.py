def rsa_encipherement(m,e,n):
    return pow(m,e,n)

    
def rsa_decipherment(c,d,n):
    return pow(c,d,n)
