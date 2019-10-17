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

