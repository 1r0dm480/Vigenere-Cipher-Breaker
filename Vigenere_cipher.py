MAX_KEY_LENGTH_GUESS = 20
alphabet = 'abcdefghijklmnopqrstuvwxyz'

# Array containing the relative frequency of each letter in the English language
english_frequences = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
					  0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
					  0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
					  0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

# Returns the Index of Councidence for the "section" of ciphertext given
def get_index_c(ciphertext):
	
	N = float(len(ciphertext))
	frequency_sum = 0.0

	# Using Index of Coincidence formula
	for letter in alphabet:
		frequency_sum+= ciphertext.count(letter) * (ciphertext.count(letter)-1)

	# Using Index of Coincidence formula
	ic = frequency_sum/(N*(N-1))
	return ic

# Returns the key length with the highest average Index of Coincidence
def get_key_length(ciphertext):
	ic_table=[]

	# Splits the ciphertext into sequences based on the guessed key length from 0 until the max key length guess (20)
	# Ex. guessing a key length of 2 splits the "12345678" into "1357" and "2468"
	# This procedure of breaking ciphertext into sequences and sorting it by the Index of Coincidence
	# The guessed key length with the highest IC is the most porbable key length
	for guess_len in range(MAX_KEY_LENGTH_GUESS):
		ic_sum=0.0
		avg_ic=0.0
		for i in range(guess_len):
			sequence=""
			# breaks the ciphertext into sequences
			for j in range(0, len(ciphertext[i:]), guess_len):
				sequence += ciphertext[i+j]
			ic_sum+=get_index_c(sequence)
		# obviously don't want to divide by zero
		if not guess_len==0:
			avg_ic=ic_sum/guess_len
		ic_table.append(avg_ic)

	# returns the index of the highest Index of Coincidence (most probable key length)
	best_guess = ic_table.index(sorted(ic_table, reverse = True)[0])
	second_best_guess = ic_table.index(sorted(ic_table, reverse = True)[1])

	# Since this program can sometimes think that a key is literally twice itself, or three times itself, 
	# it's best to return the smaller amount.
	# Ex. the actual key is "dog", but the program thinks the key is "dogdog" or "dogdogdog"
	# (The reason for this error is that the frequency distribution for the key "dog" vs "dogdog" would be nearly identical)
	if best_guess % second_best_guess == 0:
		return second_best_guess
	else:
		return best_guess

# Performs frequency analysis on the "sequence" of the ciphertext to return the letter for that part of the key
# Uses the Chi-Squared Statistic to measure how similar two probability distributions are. 
# (The two being the ciphertext and regular english distribution)
def freq_analysis(sequence):
	all_chi_squareds = [0] * 26

	for i in range(26):

		chi_squared_sum = 0.0

		#sequence_offset = [(((seq_ascii[j]-97-i)%26)+97) for j in range(len(seq_ascii))]
		sequence_offset = [chr(((ord(sequence[j])-97-i)%26)+97) for j in range(len(sequence))]
		v = [0] * 26
		# count the numbers of each letter in the sequence_offset already in ascii
		for l in sequence_offset:
			v[ord(l) - ord('a')] += 1
		# divide the array by the length of the sequence to get the frequency percentages
		for j in range(26):
			v[j] *= (1.0/float(len(sequence)))

		# now you can compare to the english frequencies
		for j in range(26):
			chi_squared_sum+=((v[j] - float(english_frequences[j]))**2)/float(english_frequences[j])

		# add it to the big table of chi squareds
		all_chi_squareds[i] = chi_squared_sum

	# return the letter of the key that it needs to be shifted by
	# this is found by the smallest chi-squared statistic (smallest different between sequence distribution and 
	# english distribution)
	shift = all_chi_squareds.index(min(all_chi_squareds))

	# return the letter
	return chr(shift+97)

def get_key(ciphertext, key_length):
	key = ''

	# Calculate letter frequency table for each letter of the key
	for i in range(key_length):
		sequence=""
		# breaks the ciphertext into sequences
		for j in range(0,len(ciphertext[i:]), key_length):
			sequence+=ciphertext[i+j]
		key+=freq_analysis(sequence)

	return key

# Returns the plaintext given the ciphertext and a key
def decrypt(ciphertext, key):
	# Creates an array of the ascii values of the ciphertext and the key
	cipher_ascii = [ord(letter) for letter in ciphertext]
	key_ascii = [ord(letter) for letter in key]
	plain_ascii = []

	# Turns each ascii value of the ciphertext into the ascii value of the plaintext
	for i in range(len(cipher_ascii)):
		plain_ascii.append(((cipher_ascii[i]-key_ascii[i % len(key)]) % 26) +97)

	# Turns the array of ascii values into characters
	plaintext = ''.join(chr(i) for i in plain_ascii)
	return plaintext

def encrypt(plaintext, key):
	# Creates an array of the ascii values of the plaintext and the key
	plain_ascii = [ord(letter) for letter in plaintext]
	key_ascii = [ord(letter) for letter in key]
	cipher_ascii = []

	# Turns each ascii value of the plaintext into the ascii value of the ciphertext
	for i in range(len(plain_ascii)):

		temp = plain_ascii[i]+key_ascii[i % len(key)]-97
		if temp>122:
			# Loop back to the beginning of the alphabet
			cipher_ascii.append(temp-26)
		else:
			cipher_ascii.append(temp)

	# Turns the array of ascii values into characters
	ciphertext = ''.join(chr(i) for i in cipher_ascii)
	return ciphertext

def main():
	ask = True
	while ask:
		text = raw_input("Enter e to encrypt, or d to decrypt: ")
		if text =='e':
			plaintext_unfiltered = raw_input("Enter plaintext to encrypt: ")
			key_unfiltered = raw_input("Enter key to encrypt with: ")
			
			# Filters the text so it is only alphanumeric characters, and lowercase
			plaintext = ''.join(x.lower() for x in plaintext_unfiltered if x.isalpha())	
			key = ''.join(x.lower() for x in key_unfiltered if x.isalpha())	
			print(key)

			ciphertext = encrypt(plaintext, key)	
			print("Ciphertext: {}".format(ciphertext))

			ask = False	
		elif text == 'd':
			ciphertext_unfiltered = raw_input("Enter ciphertext to decrypt: ")

			# Filters the text so it is only alphanumeric characters, and lowercase
			ciphertext = ''.join(x.lower() for x in ciphertext_unfiltered if x.isalpha())	

			askkey = True
			while askkey:
				torf = raw_input("Do you know the key to decrypt with? Enter y or n: ")
				if torf == 'n':

					key_length=get_key_length(ciphertext)
					print("Key length is most likely {}".format(key_length))

					key = get_key(ciphertext, key_length)
					plaintext = decrypt(ciphertext, key)

					print("Key: {}".format(key))
					print("Plaintext: {}".format(plaintext))

					askkey = False
				elif torf == 'y':

					key_unfiltered = raw_input("Enter key to decrypt with: ")
					key = ''.join(x.lower() for x in key_unfiltered if x.isalpha())	
					plaintext = decrypt(ciphertext, key)

					print("Plaintext: {}".format(plaintext))

					askkey = False
				else:
					print("Not a valid input")
	
			ask = False	
		else:
			print("Not a valid input")

if __name__ == '__main__':
	main()
