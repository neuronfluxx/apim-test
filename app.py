#!/usr/bin/env python3
"""
Simple Test MCP Server - Configured for Azure Container Apps.
"""

from fastmcp import FastMCP
import os
import json
from datetime import datetime
import logging
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastMCP
mcp = FastMCP("simple-test-server")

# --- REST health endpoint (for Docker & Azure healthchecks) ---
async def health_endpoint(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok", "server": "simple-test-server"})


# Export the ASGI callable for production servers (Gunicorn / Uvicorn).
# This solves the "Application object must be callable" error on Azure.
app = mcp.http_app()

# Mount the /health route onto the Starlette app
app.routes.insert(0, Route("/health", health_endpoint, methods=["GET"]))


@mcp.tool(
    description="Get the current date and time",
    title="Get Current Time",
)
def get_current_time(format: str = "readable") -> dict:
    """Return the current date/time in the requested format."""
    logger.info(f"Getting current time in format: {format}")
    now = datetime.now()
    time_str = now.isoformat() if format == "iso" else now.strftime("%Y-%m-%d %H:%M:%S")
    return {
        "current_time": time_str,
        "format": format,
        "unix_timestamp": now.timestamp(),
        "timezone": str(now.astimezone().tzinfo),
    }


@mcp.tool(
    description="Calculate the area of a rectangle",
    title="Calculate Rectangle Area",
)
def calculate_rectangle_area(width: float, height: float) -> dict:
    """Calculate area and perimeter of a rectangle."""
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive numbers")
    return {
        "width": width,
        "height": height,
        "area": width * height,
        "perimeter": 2 * (width + height),
    }


@mcp.tool(
    description="Reverse a text string",
    title="Reverse String",
)
def reverse_string(text: str) -> dict:
    """Reverse the given text and check if it is a palindrome."""
    if not text:
        raise ValueError("Text parameter cannot be empty")
    reversed_text = text[::-1]
    return {
        "original": text,
        "reversed": reversed_text,
        "palindrome": text.lower() == reversed_text.lower(),
    }


@mcp.tool(
    description="Check server health status",
    title="Health Check",
)
def health() -> dict:
    """Return basic health information."""
    return {
        "status": "ok",
        "server_name": "simple-test-server",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    }


# -- Local execution --
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")
    logger.info(f"Starting MCP server locally on {host}:{port}")
    mcp.run(
        transport="streamable-http",
        port=port,
        host=host,
    )
