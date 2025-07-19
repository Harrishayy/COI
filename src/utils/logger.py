#!/usr/bin/env python3
"""
Logging utilities for the cognitive presence pipeline.

This module provides a centralized logging system with consistent formatting
and configuration across all pipeline components.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

def setup_logger(
    name: str,
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
) -> logging.Logger:
    """
    Set up a logger with consistent configuration.
    
    Args:
        name: Logger name (usually __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging to file
        log_format: Log message format string
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_pipeline_logger(config) -> logging.Logger:
    """
    Get a logger configured for the pipeline.
    
    Args:
        config: Configuration object with logging settings
        
    Returns:
        Configured logger for pipeline use
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path(config.logs_dir)
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"pipeline_{timestamp}.log"
    
    return setup_logger(
        name="pipeline",
        level=config.log_level,
        log_file=str(log_file),
        log_format=config.log_format
    )

class PipelineLogger:
    """
    Context manager for pipeline logging with automatic cleanup.
    """
    
    def __init__(self, config, stage_name: str):
        """
        Initialize pipeline logger.
        
        Args:
            config: Configuration object
            stage_name: Name of the pipeline stage
        """
        self.config = config
        self.stage_name = stage_name
        self.logger = None
    
    def __enter__(self):
        """Enter logging context."""
        self.logger = get_pipeline_logger(self.config)
        self.logger.info(f"Starting pipeline stage: {self.stage_name}")
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit logging context."""
        if exc_type:
            self.logger.error(f"Pipeline stage '{self.stage_name}' failed: {exc_val}")
        else:
            self.logger.info(f"Completed pipeline stage: {self.stage_name}")

def log_function_call(logger: logging.Logger, func_name: str, **kwargs):
    """
    Decorator to log function calls with parameters.
    
    Args:
        logger: Logger instance
        func_name: Name of the function being called
        **kwargs: Function parameters to log
    """
    def decorator(func):
        def wrapper(*args, **func_kwargs):
            # Log function call
            params = {**kwargs, **func_kwargs}
            logger.debug(f"Calling {func_name} with parameters: {params}")
            
            try:
                result = func(*args, **func_kwargs)
                logger.debug(f"{func_name} completed successfully")
                return result
            except Exception as e:
                logger.error(f"{func_name} failed: {str(e)}")
                raise
        
        return wrapper
    return decorator

def log_performance(logger: logging.Logger, operation: str):
    """
    Decorator to log operation performance.
    
    Args:
        logger: Logger instance
        operation: Name of the operation being timed
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time
                logger.info(f"{operation} completed in {elapsed_time:.2f}s")
                return result
            except Exception as e:
                elapsed_time = time.time() - start_time
                logger.error(f"{operation} failed after {elapsed_time:.2f}s: {str(e)}")
                raise
        
        return wrapper
    return decorator

def log_progress(logger: logging.Logger, total: int, operation: str):
    """
    Context manager for logging progress of operations.
    
    Args:
        logger: Logger instance
        total: Total number of items to process
        operation: Name of the operation
    """
    class ProgressLogger:
        def __init__(self, logger, total, operation):
            self.logger = logger
            self.total = total
            self.operation = operation
            self.current = 0
        
        def __enter__(self):
            self.logger.info(f"Starting {self.operation} ({self.total} items)")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                self.logger.error(f"{self.operation} failed at {self.current}/{self.total}")
            else:
                self.logger.info(f"Completed {self.operation} ({self.total} items)")
        
        def update(self, count: int = 1):
            """Update progress counter."""
            self.current += count
            if self.current % max(1, self.total // 10) == 0:  # Log every 10%
                progress = (self.current / self.total) * 100
                self.logger.info(f"{self.operation} progress: {self.current}/{self.total} ({progress:.1f}%)")
    
    return ProgressLogger(logger, total, operation) 