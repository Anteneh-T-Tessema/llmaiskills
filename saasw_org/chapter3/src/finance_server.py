from fastmcp import FastMCP

mcp = FastMCP("Finance-Node")

@mcp.tool()
def convert_currency(amount: float, from_curr: str, to_curr: str) -> str:
    """Converts currency based on mock exchange rates."""
    rates = {"USD": 1.0, "EUR": 0.92, "GBP": 0.78, "JPY": 156.0}
    
    if from_curr not in rates or to_curr not in rates:
        return "Unsupported currency."
    
    usd_amount = amount / rates[from_curr]
    final_amount = usd_amount * rates[to_curr]
    return f"{amount} {from_curr} is approximately {final_amount:.2f} {to_curr}"

@mcp.tool()
def calculate_roi(initial: float, final: float) -> str:
    """Calculates the Return on Investment percentage."""
    roi = ((final - initial) / initial) * 100
    return f"The ROI is {roi:.2f}%"

if __name__ == "__main__":
    mcp.run()
