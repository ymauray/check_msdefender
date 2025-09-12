#!/usr/bin/env python3
"""Test script for verbose mode functionality."""

import sys
import logging
from check_msdefender.core.logging_config import get_verbose_logger

def test_verbose_logging():
    """Test verbose logging at different levels."""
    print("Testing verbose logging functionality...")
    
    for level in range(4):
        print(f"\n=== Verbose Level {level} ===")
        logger = get_verbose_logger("test_logger", level)
        
        logger.info("This is an info message")
        logger.debug("This is a debug message") 
        logger.trace("This is a trace message")
        logger.api_call("GET", "https://api.example.com/test", 200, 0.125)
        logger.json_response('{"status": "success", "data": []}')
        logger.method_entry("test_method", param1="value1", param2="value2")
        logger.method_exit("test_method", "return_value")
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    test_verbose_logging()