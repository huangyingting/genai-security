# Proof of concept for MCP indirect injection
# uv run fastmcp run indirect_injection.py --transport sse --port 8000

from fastmcp import FastMCP
import os

mcp = FastMCP("MCP indirect injection server 🚀")


@mcp.tool()
def process_document(document_text: str) -> str:
  """Process a document and extract key information

  Args:
      document_text: The text content of the document to process
  """

  # Simulate document processing with a template
  processing_result = f"""
    DOCUMENT ANALYSIS SYSTEM
    =======================
    PROCESSING DOCUMENT:
    
    {document_text}
    
    ANALYSIS RESULTS:
    
    The document appears to be a {len(document_text) > 1000 and 'long' or 'short'} text.
    It contains approximately {len(document_text.split())} words.

    END OF ANALYSIS
    """

  return processing_result

@mcp.tool()
def read_file(filepath: str) -> str:
  """Read the content of a local file and return it as a string.

  Args:
      filepath: Path to the file to read.

  Returns:
      The content of the file as a string.
  """
  try:
    # Security check to prevent directory traversal
    abs_filepath = os.path.abspath(filepath)
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Only allow files within the current directory or subdirectories
    if not abs_filepath.startswith(base_dir):
      return f"Error: Cannot access files outside the application directory for security reasons."

    # Read and return file content
    with open(abs_filepath, 'r') as file:
      content = file.read()

    print(f"Successfully read file: {filepath}")
    return content
  except FileNotFoundError:
    print(f"Error: File not found: {filepath}")
    return f"Error: File not found: {filepath}"
  except PermissionError:
    print(f"Error: Permission denied for file: {filepath}")
    return f"Error: Permission denied for file: {filepath}"
  except Exception as e:
    print(f"Error reading file: {str(e)}")
    return f"Error reading file: {str(e)}"

if __name__ == "__main__":
  mcp.run()
