#!/bin/bash

# Run the caching proxy on port 8001 with dummyjson.com as the origin server
python3 caching_proxy.py --port 8001 --origin https://dummyjson.com &  # Run in the background
PROXY_PID=$!  # Capture the process ID of the background process

# Give the proxy some time to start up
sleep 2

# Test the proxy using curl to request a product list
echo "Fetching /products from caching proxy..."
curl http://localhost:8001/products
sleep 2  # Wait for 2 seconds before making the next request

# Test the cache hit by fetching the same resource again
echo "Fetching /products again (should hit cache)..."
curl http://localhost:8001/products
sleep 2

# Test another endpoint, e.g., single product
echo "Fetching /products/1 from caching proxy..."
curl http://localhost:8001/posts
sleep 2

# Fetching the same product again to test cache hit
echo "Fetching /products/1 again (should hit cache)..."
curl http://localhost:8001/posts
sleep 2

# Stop the caching proxy by killing the background process
echo "Stopping the caching proxy..."
kill $PROXY_PID
