import os
from fastmcp import FastMCP

mcp = FastMCP("System-Node")

@mcp.tool()
def list_workspace_folders(path: str = ".") -> str:
    """Lists the top-level folders in a given path."""
    try:
        # Get absolute path relative to the project root
        items = os.listdir(path)
        folders = [f for f in items if os.path.isdir(os.path.join(path, f))]
        return f"Folders in '{path}': {', '.join(folders)}"
    except Exception as e:
        return f"Error reading path: {str(e)}"

@mcp.tool()
def get_file_count(path: str = ".") -> str:
    """Counts the number of files in a directory."""
    try:
        items = os.listdir(path)
        files = [f for f in items if os.path.isfile(os.path.join(path, f))]
        return f"There are {len(files)} files in '{path}'."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
