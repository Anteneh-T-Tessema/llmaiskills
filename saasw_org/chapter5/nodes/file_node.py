import os
from fastmcp import FastMCP

mcp = FastMCP("File-Operations-Pro")

@mcp.tool()
def secure_list_files(directory: str = ".") -> list:
    """
    Lists files in a directory with production safety checks.
    """
    # Production Safety: Prevent path traversal
    if ".." in directory or directory.startswith("/"):
        return ["Error: Access denied. Only relative paths within the project are allowed."]
    
    try:
        items = os.listdir(directory)
        return [f for f in items if os.path.isfile(os.path.join(directory, f))]
    except Exception as e:
        return [f"Error reading directory: {str(e)}"]

@mcp.tool()
def get_node_status() -> str:
    """Returns the health status of the File Node."""
    return "Node is Healthy and Operational."

if __name__ == "__main__":
    mcp.run()
