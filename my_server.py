from fastmcp import FastMCP

mcp = FastMCP(
    name="legacy-api-mcp-server",
    host="127.0.0.1",
    port=9000
)

@mcp.tool()
def greet(name: str) -> str:
    """Greet a user by name."""
    print(f"Greeting {name}")
    return f"Hello, langcode {name}!"

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    print(f"Adding {a} and {b}")
    return a + b


if __name__ == "__main__":
    # This runs the server, defaulting to STDIO transport
    mcp.run(
        transport="streamable-http"
    )