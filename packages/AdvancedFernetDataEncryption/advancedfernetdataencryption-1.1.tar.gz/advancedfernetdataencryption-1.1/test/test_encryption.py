from AdvancedFernetDataEncryption import *
import json

# Generates the Token and stores the random token into the Token.json file 
def writeJson():
    with open("Token.json", "w") as outfile:
        outfile.write(json.dumps({"GenerateToken":passwordToken()}))

# Encrypts any plain text and uses the token that is stored to generate an encrypted text
def BasicDataEncryption():
    plainText = input("Plan text: ")
    print("Encrypted Text: ", dataEncrpytion(plainText))

# Encrypts any encrypted text and generates the plain text with the token stored
def BasicDataDecryption():
    encryptedText = input("Encrypted Text: ")
    print("Decrypted Text: ", dataDecryption(encryptedText))

# Generates a unique sessionToken and Key for user sessions (For Web Servers)
def WebSession():
    UsernameToken = input("User Session: ")
    SessionToken, SessionKey = generateSessionToken(UsernameToken)
    print ("Session Token: ", SessionToken)
    print("Session Key: ", SessionKey)
    plaintext = decryption(SessionToken, SessionKey)
