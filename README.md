# Vigenere-Cipher-Breaker
A Python script that recovers the encryption key and plaintext from Vigenere cipher-text by performing frequency analysis and comparing categorical probability distributions.

## What is a Vigenere Cipher?
A Vigenere cipher is a polyalphabetic substitution.  It is a method of encrypting alphabetic text by using a series of interwoven Caesar ciphers, based on the letters of a keyword. 

The Caesar cipher is a type of substitution cipher in which each letter in the plaintext is 'shifted' a certain number of places down the alphabet.

Example: The text 'defend the east wall of the castle' is encrypted with a shift of 1 (key of 'a')
```
plaintext:  defend the east wall of the castle
ciphertext: efgfoe uif fbtu xbmm pg uif dbtumf
```
Decryption is just as easy, it's simply a shift in the opposite direction.

So a Vigenere is a series of interwoven Caesar ciphers.  Each cipher has a key that is used to encrypt and decrypt it.  For generating a key, the given keyword is repeated in a circular manner until it matches the length of the plain text.  Each letter in the key corresponds to the shift that the letter in the plaintext should recieve.

Example: The text 'defend the east wall of the castle' (without spaces) is encrypted with a keyword of "fortify"
```
plaintext:  defend the east wall of the castle
key:        fortif yfo rtif yfor ti fyf ortify 
ciphertext: iswxvi rms vtay ufzc hn yfj qrlbqc
```

## Determining the unknown key:
This program uses a two part method to determining the unknown key.  The first part uses the Index of Coincidence to find the key length, and the second part uses the Chi-squared statistic for finding the actual key.

# 1) Finding the key length:
The Vigenere cipher applies different Caesar ciphers to consecutive letters.  If we have a key of "dog", this ends up repeating in a circular manner until it matches the length of the ciphertext.  Since our key length is 3, the 1st letter of the ciphertext is decrypted with the same letter as the 4th letter of the ciphertext ('d'). Same goes for the 2nd letter and the 5th letter ('o'). With a key length guess of 3, you get the sequences of the letter (1,4,7,10... & 2,5,8,10... & 3,6,9,12...).  So the idea is to split up our ciphertext into difference sequences, and compare these frequencies using the Index of Coincidence.  

The Index of Coincidence (I.C.) is a statistical technique that gives an indication of how English-like a piece of text is.  Since I.C. is based on letter frequencies, its result doesn't change if you apply a substitution cipher to the text.   If text is similar to English it will have an I.C. of around 0.06, if the characters are uniformly distributed the I.C. is closer to 0.03-0.04.  We repeat this proceduce of guess the key length and calculating its I.C.

Example: this ciphertext has a key length of 7, since it has the highest I.C. (14 is also high but that makes sense since the key is repeated in a cyclic manner).

```
length         avg I.C.
-----------------------
1 :     0.0449443523561
2 :     0.0457833618884
3 :     0.0435885364312
4 :     0.0474962292609
5 :     0.0393612078978
6 :     0.0471437059672
7 :     0.0909922589726 <--
8 :     0.0461858974359
9 :     0.0407804755631
10:     0.0361152882206
11:     0.0491603339901
12:     0.0512663398693
13:     0.0446886446886
14:     0.0988487702773 <--
15:     0.0334554334554
```

# 2) Finding the key:

