"""Server runner for the ERP application."""

import uvicorn

from core import settings


def run_server():
    """Run the FastAPI server."""
    uvicorn.run(
        "dario_app.api:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info",
    )


if __name__ == "__main__":
    run_server()
