
def caesar_encrypt(text, shift): #shift each letter
    result = ''
    for char in text:

            shifted = ord(char) + shift #ascii+shift
            if char.islower(): #if char is lowcase
                if shifted > ord('z'): #mode 26
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper(): #if char is uppercase
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            result += chr(shifted) #chipertext #convert ascii to char

    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


def j_i(text):
    text = text.upper().replace("J", "I") #convert to uppercase and replace I
    return text

def playfair_matrix(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key = j_i(key)
    key = key + alphabet  # add remaining alphapet to become 25 letters
    matrix = []
    for char in key:
        if char not in matrix:
            matrix.append(char)   # add unique letter to matrix
    matrix = ''.join(matrix)  # convert to string
    matrix = [matrix[i:i+5] for i in range(0, 25, 5)]  # 5x5 matrix
    return matrix

def playfair_encrypt(text, key):
    matrix = playfair_matrix(key)
    text = j_i(text)
    if len(text) % 2 != 0: #if text is odd add X
        text += 'X'
    ciphertext = ''
    for i in range(0, len(text), 2): #steps 2
        pair1 = text[i]
        pair2 = text[i+1]
        row1, col1 = 0, 0
        row2, col2 = 0, 0
        for row in range(5): # iterate over row to find row and column of pair 1,2
            if pair1 in matrix[row]:
                row1 = row
                col1 = matrix[row].index(pair1)
            if pair2 in matrix[row]:
                row2 = row
                col2 = matrix[row].index(pair2)
        if row1 == row2: #if pair 1,2 are in same row
            ciphertext += matrix[row1][(col1 + 1) % 5] #replace letter to its right
            ciphertext += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2: #if pair 1,2 in the same column
            ciphertext += matrix[(row1 + 1) % 5][col1] #replace letter to its dowsn
            ciphertext += matrix[(row2 + 1) % 5][col2]
        else:
            ciphertext += matrix[row1][col2] #first row second column
            ciphertext += matrix[row2][col1] #second row first column
    return ciphertext

def playfair_decrypt(text, key):
    matrix = playfair_matrix(key)
    plaintext = ''
    for i in range(0, len(text), 2):
        pair1 = text[i]
        pair2 = text[i+1]
        row1, col1 = 0, 0
        row2, col2 = 0, 0
        for row in range(5):
            if pair1 in matrix[row]:
                row1 = row
                col1 = matrix[row].index(pair1)
            if pair2 in matrix[row]:
                row2 = row
                col2 = matrix[row].index(pair2)
        if row1 == row2: #if both same row
            plaintext += matrix[row1][(col1 - 1) % 5] #replace letter to its left
            plaintext += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plaintext += matrix[(row1 - 1) % 5][col1] #replace letter to its up
            plaintext += matrix[(row2 - 1) % 5][col2]
        else:
            plaintext += matrix[row1][col2] #first row second column
            plaintext += matrix[row2][col1] #second row first column
    return plaintext


def railfence_encrypt(text, row):
    fence = [[] for _ in range(row)] #list
    rail = 0
    direction = 1
    for char in text:
        fence[rail].append(char) #for each row, add character
        rail += direction #next row
        if rail == row - 1 or rail == 0: #reach top or bottom
            direction = -direction #reverse directiom
    ciphertext = ''.join([''.join(rail) for rail in fence]) #join characters in each row
    return ciphertext

def railfence_decrypt(text, row):
    fence = [[] for _ in range(row)] #list
    rail = 0
    direction = 1
    for char in text:
        fence[rail].append('') #calc length of row
        rail += direction
        if rail == row - 1 or rail == 0: #reach top or bottom
            direction = -direction #reverse directiom
    index = 0
    for rail in range(row): #iterate every row
        for i in range(len(fence[rail])): #iterate evry position in row
            fence[rail][i] = text[index] #row(rail) and column(i) of character
            index += 1 #move to next character
    rail = 0
    direction = 1
    plaintext = ''
    for _ in range(len(text)):
        plaintext += fence[rail].pop(0) #first letter in each rail
        rail += direction #next row
        if rail == row - 1 or rail == 0: #if reach top or button
            direction = -direction #reverse direction
    return plaintext


def encrypt(plaintext, caesar_shift, playfair_key, railfence_rails):
    caesar_encrypted = caesar_encrypt(plaintext, caesar_shift) #encrypt caeser

    playfair_encrypted = playfair_encrypt(caesar_encrypted, playfair_key) #encrypt playfair+caesar

    railfence_encrypted = railfence_encrypt(playfair_encrypted, railfence_rails) #encrypt railfence+playfair+caeser
    return railfence_encrypted

def decrypt(ciphertext, caesar_shift, playfair_key, railfence_rails):

    railfence_decrypted = railfence_decrypt(ciphertext, railfence_rails) # Decrypt  railfence

    playfair_decrypted = playfair_decrypt(railfence_decrypted, playfair_key) # decrypt with playfair

    caesar_decrypted = caesar_decrypt(playfair_decrypted, caesar_shift)  # decrypt with caeser
    return caesar_decrypted
plaintext=input("Enter plaintext")
caesar_shift=int(input("Enter caesar shift"))
playfair_key=input("Enter playfair Keyword")
rail=int(input("Enter rows"))
#plaintext = "random"
#caesar_shift = 4
#playfair_key = "sad"
#rail = 2


encrypted_message = encrypt(plaintext, caesar_shift, playfair_key, rail)
print("Encrypted message:", encrypted_message)


decrypted_message = decrypt(encrypted_message, caesar_shift, playfair_key, rail)
print("Decrypted message:", decrypted_message)
