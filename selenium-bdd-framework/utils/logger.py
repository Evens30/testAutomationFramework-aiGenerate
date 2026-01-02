"""
Logger Utility
Configures logging for the framework
"""

import logging
import colorlog
from config.settings import LogConfig


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Setup logger with color formatting
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LogConfig.LOG_LEVEL))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler with color
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    color_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(color_formatter)
    
    # File handler
    file_handler = logging.FileHandler(LogConfig.LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    
    file_formatter = logging.Formatter(LogConfig.LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
