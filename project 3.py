import os
import subprocess
import jwt
import httplib
import datetime
from jwt.algorithms import RSAAlgorithm
from jwt import PyJWT
from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import json
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Variables
CXX = "g++"
CXXFLAGS = "-std=c++11 -I./httplib -I./jwt-cpp/include"
LDFLAGS = "-lcrypto -lssl"
TARGET = "jwks_server"
SOURCES = "main.cpp"

# Get the path to the OpenSSL installation from Homebrew
OPENSSL_PREFIX = subprocess.run(["brew", "--prefix", "openssl"], capture_output=True, text=True).stdout.strip()

# Add the path to the OpenSSL headers to the CXXFLAGS variable
CXXFLAGS += f" -I{OPENSSL_PREFIX}/include"
LDFLAGS += f" -L{OPENSSL_PREFIX}/lib"

# Build the C++ program
subprocess.run([CXX, CXXFLAGS, SOURCES, "-o", TARGET, LDFLAGS], check=True)

# Initialize Argon2 password hasher
ph = PasswordHasher()

# Initialize PyJWT
jwt.algorithms.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))

# Database functions (simulated)
def store_user(username, email, password_hash):
    # Simulated function to store user data in the database
    print(f"Storing user: {username}, {email}, {password_hash}")

def store_auth_log(ip_address, timestamp, user_id):
    # Simulated function to store authentication log in the database
    print(f"Storing auth log: {ip_address}, {timestamp}, {user_id}")

# AES Encryption of Private Keys
def encrypt_private_key(private_key, encryption_key):
    # Simulated AES encryption function
    encrypted_key = f"AES_ENCRYPT({private_key}, {encryption_key})"
    return encrypted_key

# User Registration Endpoint
class RegisterHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        user_data = json.loads(post_data)

        # Generate UUIDv4 for password
        password = "generated_uuidv4"

        # Hash the password using Argon2
        hashed_password = ph.hash(password)

        # Store user data and hashed password
        store_user(user_data['username'], user_data['email'], hashed_password)

        # Send response with generated password
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_data = json.dumps({'password': password})
        self.wfile.write(response_data.encode('utf-8'))

# Authentication Endpoint
class AuthHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/auth':
            self.send_response(405)
            self.end_headers()
            self.wfile.write("Method Not Allowed".encode('utf-8'))
            return

        # Simulated IP address
        ip_address = "192.168.1.1"

        # Simulated user ID
        user_id = 123

        # Simulated rate limiter (assuming 10 requests per second)
        # Simulated authentication success
        if True:  # Replace with actual rate limiter and authentication logic
            # Log authentication request
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            store_auth_log(ip_address, timestamp, user_id)

            # Generate JWT token
            token = jwt.encode({'sample': 'test'}, 'secret', algorithm='RS256')

            # Send response with JWT token
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(token.encode('utf-8'))
        else:
            self.send_response(429)  # Too Many Requests
            self.end_headers()
            self.wfile.write("Too Many Requests".encode('utf-8'))

# Initialize HTTP server
httpd = HTTPServer(('localhost', 8080), AuthHandler)
print('Server running at localhost:8080')
httpd.serve_forever()

# Cleanup
os.remove(TARGET)
