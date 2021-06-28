import secrets
import numpy as np
import math_tools
from sympy import Matrix
import sympy
import time

def rand_matrix_gen(dimension):

    char_sequence=[]
    for i in range(255):
        char_sequence.append(i+1)


    flag=True
    k=0
    while flag:
        flag_1=False
        flag_2=False
        flag_3=True

        k+=1
        if k%20000==0:
            print("We are at",k,"th trying...")

        rand_nums=[] #an array for keeping entries of matrix for encryption
        for i in range(dimension*dimension):
            # randomly generating entries of encryption matrix
            rand_nums.append(secrets.choice(char_sequence))

        A=np.zeros(shape=(dimension,dimension))
        pivot=0
        for i in range(dimension):
            for j in range(dimension):
                A[i][j]=int(rand_nums[pivot])
                pivot=pivot+1


        det=np.linalg.det(A)
        '''
        if int(det)!=det:
            continue'''
        if math_tools.egcd(det,256)[0]!=1:
            continue

        return A

def gen_key(A):
    k=10
    for i in range(k):
        k=k-1
        try:
            block_size=A.shape[1]
            dimension=block_size
            #A=rand_matrix_gen(dimension)
            A=np.round(A).astype(int)

            mod_matrix=Matrix()

            for i in range(dimension):
                mod_matrix=mod_matrix.row_insert(i,Matrix([A[i]]))
            try:
                A_inv=mod_matrix.inv_mod(256)
            except:
                continue
                k=10
            t=np.dot(mod_matrix,mod_matrix.inv_mod(256))%256


        except:
            print("sell")
            continue
    return A_inv

def gen_hill_matrices(dimension):
    i=0
    while(True):
        i+=1
        try:
            A_1=rand_matrix_gen(dimension)
            B_1=gen_key(A_1)
            print("Hill Cipher Matrix Generation Completed !",i)
            break
        except:
            #print("smthng gone wrong")
            continue
    return A_1,B_1

def hill_cipher(A,A_inverse,mode,message,head_padding=0,tail_padding=0):

    block_size=A.shape[1]


    try:

        if mode=="encrypt":

            if ((len(message))%(block_size))!=0:
                message = "\n--------NEW MESSAGE--------\n\n" + message + "\n\n-----END OF THE MESSAGE-----\nRandom Padding ignore this part:"
                padding_size = block_size - len(message)%block_size
                for i in range(padding_size):
                    padding = chr(secrets.randbits(8))
                    message = message + padding

            cipher_text=""
            pivot=0
            for i in range(int(len(message)/block_size)):
                B=Matrix()
                for j in range(block_size):
                    B = B.row_insert(j,Matrix([ord(message[pivot])]))
                    pivot+=1
                C = np.dot(A,B).astype(int)%256
                #print(C)
                for k in range(block_size):
                    cipher_text = cipher_text + chr(C[k][0])
            try:
                return cipher_text
            except:
                return cipher_text

        elif mode=="decrypt":
            plain_text=""
            pivot=0

            for i in range(int(len(message)/block_size)):
                cipher_matrix=Matrix()
                for j in range(block_size):
                    cipher_matrix = cipher_matrix.row_insert(j,Matrix([ord(message[pivot])]))
                    pivot+=1
                plain_matrix = np.dot(A_inverse,cipher_matrix).astype(int)%256
                for k in range(block_size):
                    plain_text = plain_text + chr(plain_matrix[k][0])
                #print("inside function",plain_text)
            return plain_text

        else:
            raise Exception("Cipher mode is not right!")

    except:
        raise Exception("Something gone wrong while making encryption/decryption !")
