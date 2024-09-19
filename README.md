
# Caching Proxy Server

A simple CLI tool that starts a caching proxy server, it will forward requests to the actual server and cache the responses. If the same request is made again, it will return the cached response instead of forwarding the request to the server.

## Features

- Forwards requests to an origin server and caches the responses.
- Cache "HIT" and "MISS" are indicated in the response headers.
- Simple command-line interface (CLI) with options to start the server and clear the cache.
- Supports custom origin servers.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/julieboysen/caching_proxy.git
   ```

2. Navigate to the project directory:

   ```bash
   cd caching_proxy
   ```

3. Ensure you have Python 3.x installed on your machine. You can verify by running:

   ```bash
   python3 --version
   ```

4. No additional dependencies are required since the project uses Python's standard libraries.

## Usage

### Starting the Proxy Server

To start the caching proxy, run the following command:

```bash
python3 caching_proxy.py --port <PORT> --origin <ORIGIN_URL>
```

- `<PORT>`: The port number on which the proxy server will listen.
- `<ORIGIN_URL>`: The origin server URL to which requests will be forwarded.

Example:

```bash
python3 caching_proxy.py --port 8001 --origin https://dummyjson.com
```

This starts the proxy on port `8001` and forwards requests to `https://dummyjson.com`.

### Clearing the Cache

To clear the cached files, use the `--clear-cache` option:

```bash
python3 caching_proxy.py --clear-cache
```

This clears all cached files without starting the server.s

## Testing

Once the proxy is running, you can use `curl` or a browser to send requests to the proxy, and it will forward them to the origin server and cache the responses.

Example:

```bash
curl http://localhost:8001/products
```

This will fetch the `/products` endpoint from the origin server and cache the response.

A bash script to test has also been provided in the `test_proxy.sh` file.

Make the script executable: 
```bash
chmod +x test_proxy.sh
```

And run the script:
```bash
./test_proxy.sh
```

## Project Link
For more details about this project, visit the [Caching Proxy Project](https://roadmap.sh/projects/caching-server).

