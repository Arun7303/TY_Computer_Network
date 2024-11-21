import socket

# Function to get user input
def get_input():
    # Take two numbers and an operation from the user
    num1 = input("Enter the first number: ")
    num2 = input("Enter the second number: ")
    print("Choose operation: +, -, *, /")
    operation = input("Enter the operation: ")
    
    # Combine the inputs into a single string to send to the server
    return f"{num1},{num2},{operation}"

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define server address and port
server_address = ('localhost', 65432)

# Connect to the server
client_socket.connect(server_address)

try:
    # Get the input from the user
    message = get_input()
    
    # Send the input to the server
    client_socket.sendall(message.encode('utf-8'))
    
    # Wait for the result from the server
    data = client_socket.recv(1024)
    
    # Print the result on the client side
    result = data.decode('utf-8')
    print(f"Result from server: {result}")
    
finally:
    # Close the socket
    client_socket.close()

