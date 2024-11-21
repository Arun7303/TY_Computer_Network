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

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define server address and port
server_address = ('localhost', 65432)

# Get the input from the user
message = get_input()

try:
    # Send the input to the server
    client_socket.sendto(message.encode('utf-8'), server_address)
    
    # Wait for the result from the server
    data, server = client_socket.recvfrom(1024)
    
    # Print the result on the client side
    result = data.decode('utf-8')
    print(f"Result from server: {result}")
    
finally:
    # Close the socket
    client_socket.close()
