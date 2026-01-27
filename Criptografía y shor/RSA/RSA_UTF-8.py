import math
from numpy.random import randint, choice

#--------------------------
#   Functions
#--------------------------

# Convert a string into a list of numbers using UTF-8 coding
def string_to_numbers(text):
    """Converts a string into a list of integer values using UTF-8 encoding."""
    return list(text.encode("utf-8"))

def numbers_to_string(numbers):
    """Converts a list of integer values back into a string using UTF-8 decoding."""
    return bytes(numbers).decode("utf-8")

# Encrypt and decrypt each character separately
def encrypt(text, e, N):
    """Encrypts a string using RSA (character by character)."""
    ascii_values = string_to_numbers(text)
    encrypted_values = [pow(char, e, N) for char in ascii_values]
    return encrypted_values

def decrypt(encrypted_values, d, N):
    """Decrypts a list of encrypted numbers back to a string."""
    decrypted_values = [pow(char, d, N) for char in encrypted_values]
    return numbers_to_string(decrypted_values)

def prime_number(n):
    """Check if a number n is primer or not"""
    if n < 2:
        return False
    for i in range (2, int(math.sqrt(n) + 1)):
        if n % i ==0:
            return False
    return True


def modular_inverse(e, phi):
    """Computes the modular inverse of e mod phi."""
    try:
        return pow(e, -1, phi)
    except ValueError:
        return None
    
# Function obtaining e and d
def get_e_and_d(phi):
    """Finds a valid prime e < phi and its modular inverse d, ensuring e ≠ d.
    
    Returns:
        (e, d): Tuple with valid values or (None, None) if no valid pair is found.
    """
    primes = [i for i in range(2, phi) if prime_number(i) and math.gcd(i, phi) == 1]
    
    if not primes:
        return None, None
    
    while primes:
        e = int(choice(primes))
        d = modular_inverse(e, phi)
        
        if d is not None and d != e:
            return e, d
        primes.remove(e)
    
    return None, None

#------------------------------
#       Encrypt
#------------------------------

restar = "y"
while restar == "y":
    # Acquire input values
    print("\n______________________________________________________\n",
          "\nThis first part is to acquire the information. \n")
    print("\nExamples of prime numbers: [11, 13, 17, 19, 41, 67, 71, 89, 97, 101, 919, 997, ...] \n")

    while True:
        try:
            p = int(input("\nGive the first prime number (2-3 digits): "))
            if p > 10 and p < 1000 and prime_number(p):
                break
            print("\nGive me a correct prime number.")
        except ValueError:
            print("\nError: write a number")

    while True:
        try:
            q = int(input("Give me a second prime number (2-3 digits): "))
            if q > 10 and q < 1000 and prime_number(q):
                break
            print("Give me a correct prime number.")
        except ValueError:
            print("Error: write a number")

    N = p * q
    phi = (p - 1) * (q - 1)

    e, d = get_e_and_d(phi)
    if e is None or d is None:
            print("\nError: Could not find suitable values for e and d. Please choose new values for p and q.\n")
            continue  # Reiniciar la elección de p y q
    
    # Define keys
    public = (e, N)
    private = (d, N)
    print("\nThe public key is:", public)
    print("The private key is:", private)
    
    #-------------------
    #   Other message
    #-------------------
    Other_message = "y"
    while Other_message == "y":
        # Get user input
        message = input("Write a small word: ")

        # Encrypt and decrypt
        encrypted_message = encrypt(message, e, N)
        decrypted_message = decrypt(encrypted_message, d, N)

        print("\nOriginal Message:", message)
        print("Encrypted Message (as numbers):", encrypted_message)
        print("Decrypted Message:", decrypted_message)

        # Check if decryption was successful
        if decrypted_message == message:
            print("The message was correctly decrypted!")
        else:
            print("Something went wrong.")

        Other_message = input("Do you want to try with other message (y,n)?: ").lower()
    restar = input("\nDo you want change the keys (y,n)?: ").lower()
    print("\nThank you for your time!")


'''
Observaciones:
1. Con 5, 11 3 tenemos resultados flotantes
2. Con primos pequeños tenemos varios errores
3. El error aparce cuando el 3er primo es menor a los primeros 2

Posible motivos de los errores: 
1. Distinto numero de cifras en lo primeros primos


'''