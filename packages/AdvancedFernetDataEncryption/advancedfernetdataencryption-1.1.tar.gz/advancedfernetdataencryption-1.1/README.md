# **AdvancedFernetDataEncryption**

An encryption that uses the Fernet symetric key generator and random values to create a secure token and key that can be stored and still be unreadable to any user. 

## **Methods Supported**
- generateSessionToken(<AnyString>): Generates a random 120 length string and encrypts with fernet symetric algorithm. Used for Web Sessions `return Token, Key`
- dataEncryption(<PlainTxt>): Generates a random 120 length string and shoves it randomly in the PlainTxt and shoves the token randomly in the 120 length string generated. Then all of this information is encrypted with the fernet algorithm. `return <string>`
- dataDecrpytion(<EncyptedTxt>): Decodes the giant encrypted text generated and creates a plain text version `return <String>`
- decryption(<EncryptedTxt>): Decodes the basic encrypted text generated and creates a plain text version `return <String>` Recommended to use only this method for the generated session token
  
## **Package Installation**
  pip install AdvancedFernetDataEncryption
More Info can be found on pypi.org [here](https://pypi.org/project/AdvancedFernetDataEncryption/)

## **Basic Usage Example**
```python
from Encryption.AdvancedFernetDataEncryption import *

text = "Hello I would like to be encrypted
encryptedText = dataEncryption(text, MinLength=20, MaxLength=100)
unencryptedText = dataDecrpytion(encryptedText)
```

When run these following lines the text will be encrypted and would be unecryptable without the usage of the Token generated, which is randomly generated for each encrypted text.

## **Example of Encryption Result**
<img width="848" alt="image" src="https://user-images.githubusercontent.com/34069094/199623092-733cfb1f-a78d-43d5-add9-47c879c6e06a.png">
