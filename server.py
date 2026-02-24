#!/usr/bin/env python3
 
"""
Simple Test MCP Server - Basic MCP server with simple tools for testing.
 
This server provides basic tools for testing MCP functionality.
Uses FastMCP library for HTTP transport.
"""
 
from fastmcp import FastMCP
import os
from datetime import datetime
import logging
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from typing import Optional
 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.info("Starting Simple Test MCP Server")
 
# Initialize MCP server
mcp = FastMCP("simple-test-server", stateless_http=True, auth=None, host="0.0.0.0")
 
 
@mcp.tool(
    description="Get the current date and time",
    title="Get Current Time"
)
def get_current_time(format: str = "readable") -> dict:
    """
    Get the current date and time.
 
    Parameters:
        format (str): Time format: 'iso' or 'readable' (default: 'readable')
 
    Returns:
        dict: Current time information
    """
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
 
 
@mcp.tool(
    description="Calculate the area of a rectangle",
    title="Calculate Rectangle Area"
)
def calculate_rectangle_area(width: float, height: float) -> dict:
    """
    Calculate the area of a rectangle.
 
    Parameters:
        width (float): Width of the rectangle
        height (float): Height of the rectangle
 
    Returns:
        dict: Rectangle area calculation result
    """
    logger.info(f"Calculating rectangle area: {width} x {height}")
   
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive numbers")
   
    area = width * height
    perimeter = 2 * (width + height)
   
    return {
        "width": width,
        "height": height,
        "area": area,
        "perimeter": perimeter,
        "units": "square units"
    }
 
 
@mcp.tool(
    description="Reverse a text string",
    title="Reverse String"
)
def reverse_string(text: str) -> dict:
    """
    Reverse a text string.
 
    Parameters:
        text (str): Text to reverse
 
    Returns:
        dict: Reversed string result
    """
    logger.info(f"Reversing text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
   
    if not text:
        raise ValueError("Text parameter cannot be empty")
   
    reversed_text = text[::-1]
   
    return {
        "original": text,
        "reversed": reversed_text,
        "length": len(text),
        "palindrome": text.lower() == reversed_text.lower()
    }
 
 
@mcp.tool(
    description="Check server health status",
    title="Health Check"
)
def health() -> dict:
    """
    Perform a health check for the server.
 
    Returns:
        dict: Health status information
    """
    logger.info("Performing health check")
   
    return {
        "status": "ok",
        "server_name": "simple-test-server",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "tools_available": 4
    }
 
 
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")
    logger.info(f"Starting Simple Test MCP server on {host}:{port}")
    logger.info("Transport mode: streamable-http")
 
    mcp.run(
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
