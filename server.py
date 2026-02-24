#!/usr/bin/env python3
 
from fastmcp import FastMCP
import os
from datetime import datetime
import logging
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
 
# 1. Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
 
# 2. Initialize FastMCP
mcp = FastMCP("simple-test-server")
 
# 3. EXPORT THE CALLABLE APP FOR AZURE
# This solves the "Application object must be callable" error by 
# providing the underlying Starlette/ASGI application to Gunicorn.
app = mcp.http_app()
 
@mcp.tool(
    description="Get the current date and time",
    title="Get Current Time"
)
def get_current_time(format: str = "readable") -> dict:
    logger.info(f"Getting current time in format: {format}")
    now = datetime.now()
    time_str = now.isoformat() if format == "iso" else now.strftime("%Y-%m-%d %H:%M:%S")
    return {
        "current_time": time_str,
        "format": format,
        "unix_timestamp": now.timestamp(),
        "timezone": str(now.astimezone().tzinfo)
    }
 
@mcp.tool(
    description="Calculate the area of a rectangle",
    title="Calculate Rectangle Area"
)
def calculate_rectangle_area(width: float, height: float) -> dict:
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive numbers")
    return {
        "width": width,
        "height": height,
        "area": width * height,
        "perimeter": 2 * (width + height)
    }
 
@mcp.tool(
    description="Reverse a text string",
    title="Reverse String"
)
def reverse_string(text: str) -> dict:
    if not text:
        raise ValueError("Text parameter cannot be empty")
    reversed_text = text[::-1]
    return {
        "original": text,
        "reversed": reversed_text,
        "palindrome": text.lower() == reversed_text.lower()
    }
 
@mcp.tool()
def health() -> dict:
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }
 
# 4. Local Execution
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")
    logger.info(f"Starting MCP server locally on {host}:{port}")
    mcp.run(
        transport="streamable-http",
        port=port,
        host=host
    )
