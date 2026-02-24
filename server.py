#!/usr/bin/env python3
 
"""
Simple Test MCP Server - Updated for Azure Container Apps.
"""
 
from fastmcp import FastMCP
import os
from datetime import datetime
import logging
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
 
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
 
# IMPORTANT: Renamed 'mcp' to 'app' so production servers (Gunicorn/Uvicorn)
# can find the entry point automatically.
app = FastMCP("simple-test-server", stateless_http=True, auth=None)
 
@app.tool(
    description="Get the current date and time",
    title="Get Current Time"
)
def get_current_time(format: str = "readable") -> dict:
    logger.info(f"Getting current time in format: {format}")
    now = datetime.now()
   
    if format == "iso":
        time_str = now.isoformat()
    else:
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
   
    return {
        "current_time": time_str,
        "format": format,
        "unix_timestamp": now.timestamp(),
        "timezone": str(now.astimezone().tzinfo)
    }
 
@app.tool(
    description="Calculate the area of a rectangle",
    title="Calculate Rectangle Area"
)
def calculate_rectangle_area(width: float, height: float) -> dict:
    logger.info(f"Calculating rectangle area: {width} x {height}")
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive numbers")
   
    return {
        "width": width,
        "height": height,
        "area": width * height,
        "perimeter": 2 * (width + height),
        "units": "square units"
    }
 
@app.tool(
    description="Reverse a text string",
    title="Reverse String"
)
def reverse_string(text: str) -> dict:
    logger.info(f"Reversing text length: {len(text)}")
    if not text:
        raise ValueError("Text parameter cannot be empty")
   
    reversed_text = text[::-1]
    return {
        "original": text,
        "reversed": reversed_text,
        "length": len(text),
        "palindrome": text.lower() == reversed_text.lower()
    }
 
@app.tool(
    description="Check server health status",
    title="Health Check"
)
def health() -> dict:
    return {
        "status": "ok",
        "server_name": "simple-test-server",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "tools_available": 4
    }
 
# Local execution block
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")
   
    logger.info(f"Starting server on {host}:{port}")
   
    # Using 'streamable-http' as requested for MCP compatibility
    app.run(
        transport="streamable-http",
        port=port,
        host=host,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_methods=["*"],
                allow_headers=["*"],
                allow_credentials=True,
            )
        ]
    )
 
