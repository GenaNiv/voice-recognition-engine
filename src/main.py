import sys
from cli import main as cli_main  # Import the CLI entry point
from web_gui import app as web_app  # Import the Flask app for the Web GUI
import logging
import json

def load_config():
    """Load configuration settings (e.g., port, logging settings)."""
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging is set up.")

def main():
    """Main entry point for the system."""
    # Load config and set up logging
    config = load_config()
    setup_logging()

    # Determine execution mode (CLI or Web GUI)
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        logging.info("Starting CLI interface...")
        cli_main()  # Run the CLI
    else:
        logging.info("Starting Web GUI...")
        web_app.run(host='0.0.0.0', port=config.get("port", 5000), debug=True)

if __name__ == "__main__":
    main()
