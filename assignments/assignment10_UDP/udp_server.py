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

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the address and port
server_address = ('localhost', 65432)  # Use 'localhost' and a port number
server_socket.bind(server_address)

print("Server is waiting for data...")

while True:
    # Wait for data from the client
    data, client_address = server_socket.recvfrom(1024)
    
    if data:
        # Decode the received data
        received_message = data.decode('utf-8')
        print(f"Received from {client_address}: {received_message}")
        
        # Split the data into numbers and operation
        num1, num2, operation = received_message.split(',')
        num1, num2 = float(num1), float(num2)
        
        # Perform the calculation
        result = calculate(num1, num2, operation)
        
        # Print the result on the server side
        print(f"Calculated result: {result}")
        
        # Send the result back to the client
        server_socket.sendto(str(result).encode('utf-8'), client_address)

