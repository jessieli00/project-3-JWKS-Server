import subprocess
import os

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

# Default target
def all():
    fetch()
    build()

# Target to build the program
def build():
    subprocess.run([CXX, CXXFLAGS, SOURCES, "-o", TARGET, LDFLAGS], check=True)

# Target to fetch the required libraries
def fetch():
    # Check if httplib directory exists, if not fetch it
    if not os.path.isdir("httplib"):
        subprocess.run(["git", "clone", "https://github.com/yhirose/cpp-httplib.git", "httplib"], check=True)

    # Check if jwt-cpp directory exists, if not fetch it
    if not os.path.isdir("jwt-cpp"):
        subprocess.run(["git", "clone", "https://github.com/Thalhammer/jwt-cpp.git", "jwt-cpp"], check=True)

def clean():
    if os.path.isfile(TARGET):
        os.remove(TARGET)
    if os.path.isdir("httplib"):
        subprocess.run(["rm", "-rf", "httplib"])
    if os.path.isdir("jwt-cpp"):
        subprocess.run(["rm", "-rf", "jwt-cpp"])

if __name__ == "__main__":
    all()
