import random
from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
#Origin cors
CORS(app)
ma=Marshmallow(app)

#Takes interval, returns every prime number in this interval
def primesInRange(bottom, top):
    top+=1
    prime_list = []
    for n in range(bottom, top):
        isPrime = True
        for num in range(2, n):
            if n % num == 0:
                isPrime = False
        if isPrime:
            prime_list.append(n)
    return prime_list

#Generates random prime number 'p' and 'q' in selected interval for RSA algorithm
def primeGenerator(bottom, top):
    #Maximum is 1000 because of limitations of computing power
    
    #prime_list is list of all prime numbers in range min-max
    prime_list = primesInRange(bottom, top)
    if(len(prime_list)<2):
        return (3,5)
    #Choice of two random prime numbers from prime_list
    p = prime_list[random.randint(0, len(prime_list)-1)]
    q = p
    while q == p:
        q = prime_list[random.randint(0, len(prime_list)-1)]
    return (p, q)

#Classic euclid algorithm. Used for finding Greatest Common Divisor
def euclid(a, b):
    if a<b:
        a,b = b,a
    while(b != 0):
        while(a >= b):
            a -= b
        a,b = b,a
    return a

#Encryption of a message using 'n' and 'e'
def msgEncrypt(msg, n, e):
    msg = int(msg)
    n = int(n)
    e = int(e)
    return {"result": ((msg**e)%n)}

#Decryption of coded message using 'n' and 'd'
def msgDecrypt(msg, n, d):
    msg = int(msg)
    n = int(n)
    d = int(d)
    return {"result": ((msg**d)%n)}

#Generate whole key from interval
def keyGenerator(bottom, top):
    bottom = int(bottom)
    top = int(top)
    #Generating 'p' and 'q' using primeGenerator method
    (p,q) = primeGenerator(bottom, top)
    #Calculating 'n' and 'fiN'
    n = p*q
    fiN = (p-1)*(q-1)
    #Calculating 'e' using 'fiN' and euclid algorithm
    e = fiN
    while(True):
        e = random.randint(2, fiN-1)
        if(euclid(e, fiN) == 1):
            break
    #Calculating 'd'
    d = pow(e, -1, fiN)
    return {'keyGenP': p, 'keyGenQ': q, 'keyGenN': n, 'keyGenE': e, 'keyGenD': d}

#Routing - this section is to handle frontend requests
@app.route('/encrypt/<msg>/<n>/<e>', methods=['GET'])
def encrypt_message(msg, n, e):
    return jsonify(msgEncrypt(msg, n, e))

@app.route('/decrypt/<msg>/<n>/<d>', methods=['GET'])
def decrypt_message(msg, n, d):
    return jsonify(msgDecrypt(msg, n, d))

@app.route('/keyGene/<bottom>/<top>', methods=['GET'])
def keyGene_message(bottom, top):
    return jsonify(keyGenerator(bottom, top))

#Main method
if __name__=='__main__':
    #Server setup
    app.run(debug=False, host='0.0.0.0')