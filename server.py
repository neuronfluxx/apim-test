#!/usr/bin/env python3
 
from fastmcp import FastMCP
import os
from datetime import datetime
import logging
import asyncio
from contextlib import asynccontextmanager
from a2wsgi import ASGIMiddleware  # Required for Azure Sync Worker compatibility
 
# 1. Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
 
# 2. Initialize FastMCP
mcp = FastMCP("simple-test-server")
 
# 3. FIX: Lifespan Management
# This manually starts the internal MCP task groups that would 
# otherwise only start during mcp.run()
@asynccontextmanager
async def lifespan(app_instance):
    # mcp._app is the underlying Starlette instance
    async with mcp._app.lifespan_context(mcp._app):
        yield
 
# 4. EXPORT AND WRAP THE APP
# Get the base ASGI app
base_asgi_app = mcp.http_app()
 
# Attach the custom lifespan to the base app
base_asgi_app.lifespan_context = lifespan
 
# Wrap the ASGI app in WSGI middleware so Azure's 'sync' worker can call it
# This solves the "missing 1 required positional argument: 'send'" error
app = ASGIMiddleware(base_asgi_app)
 
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
 
# 5. Local Execution
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")
 
    logger.info(f"Starting MCP server locally on {host}:{port}")
 
    mcp.run(
        transport="streamable-http",
        port=port,
        host=host
    )
