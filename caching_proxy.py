import socket
from urllib.request import Request, urlopen, HTTPError
import argparse
import os, shutil

def fetch_file(filename, origin):
    # Try to read the file locally first
    file_from_cache = fetch_from_cache(filename)

    if file_from_cache:
        print('Fetched successfully from cache.')
        return file_from_cache, 'HIT'
    else:
        print('Not in cache. Fetching from server.')
        file_from_server = fetch_from_server(filename, origin)

        if file_from_server:
            save_in_cache(filename, file_from_server)
            return file_from_server, 'MISS'
        else:
            return None
        
def fetch_from_cache(filename):
    try:
        # Check if we have this file locally
        fin = open('cache' + filename)
        content = fin.read()
        fin.close()
        # If we have it, send it
        return content
    except IOError:
        return None
    
def fetch_from_server(filename, origin):
    url = origin + filename
    q = Request(url)

    try:
        response = urlopen(q)
        # Grab the header and content from the server req
        response_headers = response.info()
        content = response.read().decode('utf-8')
        return content
    except HTTPError:
        return None
    
def save_in_cache(filename, content):
    print('Saving a copy of {} in the cache'.format(filename))
    ensure_cache_directory()
    cached_file = open('cache' + filename, 'w')
    cached_file.write(content)
    cached_file.close()

def clear_cache():
    folder = 'cache'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    print('Cached cleared')

def ensure_cache_directory():
    if not os.path.exists('cache'):
        os.makedirs('cache')
        print('Created cache directory.')

def main():
    # Get port and url command line argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='Port for proxy server')
    parser.add_argument('--origin', type=str, help='Origin server URL')
    parser.add_argument('--clear-cache', action='store_true', help="Clear the cache")
    args = parser.parse_args()

    # Clear cache if the --clear-cache flag is used
    if args.clear_cache:
        clear_cache()
        return

    if not args.port or not args.origin:
        print("Error: --port and --origin are required")
        return

    print("Starting the cache proxy...")

    # Define socket host and port
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = args.port

    origin = args.origin

    # Initialize socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    server_socket.listen(1)

    print(f'Cache proxy is listening on port {SERVER_PORT} and forwarding requests to {origin} ...')

    while True:
        # Wait for client connection
        client_connection, client_address = server_socket.accept()

        # Get the client request
        request = client_connection.recv(1024).decode()
        print(request)

        # Parse HTTP headers
        headers = request.split('\n')

        top_header = headers[0].split()
        method = top_header[0]
        filename = top_header[1]

        # Index check
        if filename == '/':
            filename = '/index.html'

        # Get the file
        content, cache_status = fetch_file(filename, origin)

        # If we have the file, return it, otherwise 404
        if content:
            response = f'HTTP/1.0 200 OK\nX-Cache: {cache_status}\n\n' + content
        else:
            response = 'HTTP/1.0 404 NOT FOUND\n\n File Not Found'

        # Send the response and close the connection
        client_connection.sendall(response.encode())
        client_connection.close()

    # Close socket
    server_socket.close()

if __name__ == '__main__':
    main()