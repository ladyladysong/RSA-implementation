# -*- coding: utf-8 -*- 
import math  
import random
class RSA:
	def __init__(self):
		self.p = self.prime()
		self.q = self.prime()
		self.n = self.p*self.q
		#print "p:",self.p
		#print "q:",self.q
		self.pub_key,self.pri_key= self.genKey(self.p,self.q)


	def primeTest(self,n):
		q = n - 1
		k = 0
		while q % 2 == 0:
			k += 1;
			q /= 2
		a = random.randint(2, n-2);
		if self.squareMultiplyMod(a, q, n) == 1:
			return True 
		for j in range(0, k):
			if self.squareMultiplyMod(a, (2**j)* q, n) == n - 1:
				return True 
		return False 

	def prime(self): # generate a prime number of 64 bits
		testP = random.randrange(2**63+1, 2**64, 2)
		while(not self.primeTest(testP)):
			testP = random.randrange(2**63+1, 2**64, 2)
		return testP


	def gcd(self, a, b):
		if b == 0:
			return a
		else:
			return self.gcd(b, a%b)

	def genKey(self, p, q):
		n = p*q
		s = (p-1)*(q-1)
		while 1:
			e = random.choice(range(2**16))
			x = self.gcd(e, s)
			if x == 1:
				break
		d= self.inverseElement(s, e)
		if d < 0:
			while 1:
				d = d+s
				if d >= 0:
					break
		#print "e:", e
		#print "d:", d
		return ((n, e), (n, d))

	def inverseElement(self, a, b):#求逆元
		t0 = 0
		t1 = 1
		if a < b:
			while True:
				b = b-a
				if a > b:
					break
		while True:
			q = a / b
			r = a % b
			a = b
			b = r
			if r == 0:
				break
			t = t0 - q*t1
			t0 = t1
			t1 = t
		return t
	def squareMultiplyMod(self, x, e, n): #(x^e)mod n
		s=x
		b=bin(e).replace('0b','')
		len_b=len(b)
		for i in range(1,len_b):
			s=(s*s)%n
			if b[i]=='1':
				s=(s*x)%n
		return s

	def encrypt(self,plain):
		cipher = []
		n,e = self.pub_key
		len_plain = len(plain)
		for i in range(0,len_plain):
			a = self.squareMultiplyMod( ord(plain[i]), e, n)
			cipher.append(a)
		self.cipherInList = cipher
		self.cipher_string = str(cipher).replace('[','').replace(']','').replace(',','')
		#print self.cipher_string
		f = open('encrypt.txt','w')
		f.write(self.cipher_string)

	def decrypt(self):
		plain =[]
		cipher = self.cipherInList
		n,d = self.pri_key
		len_cipher = len(cipher)
		for i in range(0, len_cipher):
			yp = long(cipher[i]) % self.p
			yq = long(cipher[i]) % self.q
			dp = d % (self.p-1)
			dq = d % (self.q-1)
			xp = self.squareMultiplyMod(yp, dp, self.p)
			xq = self.squareMultiplyMod(yq, dq, self.q)
			cp = self.inverseElement(self.p, self.q)
			cq = self.inverseElement(self.q, self.p)
			plain.append(chr((self.q*cp*xp + self.p*cq*xq) % n))
		self.plain_string = ''.join(plain)
		
rsa = RSA()