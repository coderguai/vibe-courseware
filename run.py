"""Entry point for the application."""

import uvicorn
from src.vibe_courseware.db.session import init_db

def main() -> None:
    """Run the application."""
    # Initialize the database
    init_db()
    
    # Run the application
    uvicorn.run(
        "src.vibe_courseware.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

if __name__ == "__main__":
    main()