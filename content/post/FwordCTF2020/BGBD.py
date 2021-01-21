from Crypto.Util.number import *
import math
from sympy import lcm 
import random
from fractions import gcd 
from sympy import nextprime
from pwn import xor
from secret import p_1,q_1,flag

def verify_keys(a,b):
	while True:
		if a%4==3:
			while b%4!=3:
				b=nextprime(b)
			return a,b
		if b%4==3:
			while a%4!=3:
				a=nextprime(a)
			return a,b
		a,b=nextprime(a),nextprime(b)
	
def enc1(n,e,msg):
	m=int(msg.encode('hex'),16)
	return pow(m,e,n)

def encode(msg):
	enc_msg=""
	for i in msg:
		enc_msg+=bin(ord(i))[2:].zfill(8)
	return enc_msg

def enc2(msg,bs,mds):
	while len(msg)%bs!=0:
		msg='0'+msg
	ll=len(msg)/bs
	r=3945132
	x=pow(r,2,mds)
	c = ''
	for i in range(ll):
		x=pow(x,2,mds)
		p=(bin(x)[2:])[-bs:]
		c_i=int(p,2)^int(msg[i*bs:(i+1)*bs],2)
		ci_bin = format(c_i, '0' + str(bs) + 'b')
		c+=ci_bin
	return c,pow(x,2,mds)



n=p_1*q_1
e=17742461742896634972201474241931685701682825423273435469196581493593083245061146905518481601646582623355393811189032402488804067701439209191772750727581718922909269638936474927145555944487152988216781157681122522177270474504549932191814852246849976334482284151493985991827502940015843682072459462031659332887

part1=flag[:len(flag)/2]
part2=flag[len(flag)/2:]

cipher1=enc1(n,e,part1)
print (cipher1)

p_2,q_2=verify_keys(p_1,q_1)
N=p_2*q_2

block_size=int(math.log(int(math.log(N,2)),2))

cipher2,xt=(enc2(encode(part2),block_size,N))

print (cipher2,xt)


#n : 136925867715334350539351541819374303153581861883077425871381479619256902280896182751175418274848819117804106313526390171733172646719203781502341411544996240718046559322020330755493739123717974336861438650061159088512867158495809372652057009979517497499951599965613535967213529497308200114836792389883404448987
#Cipher 1 : 46282600628982824130530839707152802257095678655388901777970530297126873677669029302844975736419114037407828011895452774978714646752289839556387176301641119447701609034322702222708553203047498652811019927150942380861621605039714510498733535604972160616786208389979609391313009722848684563568437967800442928084
#(cipher2,xt) : ('101110100011010000110010100100000011001110110001010101100101000000100111011010010010110101000101000110000100011001001100111011111011101001110111100001100011101010101111101100001000010111111000110110110010110100000001001011100010011000110100111100001100111001101110001111001100010001001111100110110110100001011100011100110101001000011100100011011110011000010100110010100111000010101101110101011100010110000100001101101101001111000101011100101100100110110011101000100010101000010001010010110110101011111101110011101110010000101001000111000000100100001010110111001011110001010100100001101111010010111101111001001001111010001100000111000010000100110101100010001111100011111100100100001010010100111010100010000101110000110101000101100', 99938901144293305318474508248429453175561082362898230514299720558762394911631823304146558717537729838080951066313213321374755623652896593453644503184122276925455269140340267427068200657877772040554093186417385902385500879519631051754226252925525926019109245833691317900888626583890623823019289563531254979763)

