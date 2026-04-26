import os
import logging
from fastmcp import FastMCP

# Initialize professional logging
logging.basicConfig(
    filename="saasw_org/chapter5/logs/market_node.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("MarketNode")

mcp = FastMCP("Market-Intelligence-Pro")

@mcp.tool()
def get_market_sentiment(industry: str) -> dict:
    """
    Retrieves deep market sentiment and risk factors for a specific industry.
    Args:
        industry: The name of the industry (e.g., 'SaaS', 'Fintech', 'AI').
    Returns:
        A structured dictionary containing sentiment score and top risks.
    """
    logger.info(f"Querying sentiment for industry: {industry}")
    
    # In a real production node, this would hit an external API
    mock_data = {
        "SaaS": {"sentiment": 0.85, "status": "Bullish", "risks": ["Churn rate increasing", "Pricing pressure"]},
        "AI": {"sentiment": 0.95, "status": "Hyper-Growth", "risks": ["GPU scarcity", "Regulatory uncertainty"]},
        "Fintech": {"sentiment": 0.65, "status": "Consolidating", "risks": ["Interest rate volatility"]}
    }
    
    result = mock_data.get(industry, {"sentiment": 0.5, "status": "Neutral", "risks": ["Insufficient data"]})
    return {
        "industry": industry,
        "analysis": result,
        "node_metadata": {"version": "1.0.0", "status": "verified"}
    }

if __name__ == "__main__":
    logger.info("Market Intelligence Pro Node starting up...")
    mcp.run()
