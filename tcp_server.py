import socket

# Define the server's IP address and port
SERVER_HOST = '0.0.0.0'  # Listen on all available network interfaces
SERVER_PORT = 12345

def handle_client_connection(client_socket):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break  # If no data is received, client has disconnected

        # Process the received command
        # Replace this with your actual command processing logic
        response = f"Received command: {data}"
        
        # Send the response back to the client
        client_socket.send(response.encode('utf-8'))

    # Close the client connection
    client_socket.close()

def start_server():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to the specified address and port
        server_socket.bind((SERVER_HOST, SERVER_PORT))

        # Listen for incoming connections
        server_socket.listen(1)
        print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

            # Handle the client connection in a separate thread or process
            handle_client_connection(client_socket)

    except KeyboardInterrupt:
        # Close the server socket on keyboard interrupt
        server_socket.close()
        print("Server stopped.")

# Start the TCP server
start_server()
