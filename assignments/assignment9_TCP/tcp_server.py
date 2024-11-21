import socket

# Function to perform calculation
def calculate(num1, num2, operation):
    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '*':
        return num1 * num2
    elif operation == '/':
        return num1 / num2 if num2 != 0 else "Cannot divide by zero"
    else:
        return "Invalid operation"

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = ('localhost', 65432)  # Use 'localhost' and a port number
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print("Server is waiting for a connection...")

while True:
    # Wait for a connection
    connection, client_address = server_socket.accept()
    
    try:
        print(f"Connection established with {client_address}")
        
        # Receive data from the client
        data = connection.recv(1024).decode('utf-8')
        if data:
            print(f"Received: {data}")
            
            # Split the data into numbers and operation
            num1, num2, operation = data.split(',')
            num1, num2 = float(num1), float(num2)
            
            # Perform the calculation
            result = calculate(num1, num2, operation)
            
            # Print the result on the server side
            print(f"Calculated result: {result}")
            
            # Send the result back to the client
            connection.sendall(str(result).encode('utf-8'))
    
    finally:
        # Clean up the connection
        connection.close()

