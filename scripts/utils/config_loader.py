# Copyright (c) 2026 [Assisted Evolution Pty Ltd]
# Licensed under MIT License (see LICENSE file)
# or Commercial License (see LICENSE.COMMERCIAL file)

"""
Configuration Loader Module

This module provides utilities for loading and managing configuration files
used throughout the grant research website project.

Configuration files are stored in the config/ directory and include:
- grants_sources.json: Grant data organized by funding source
- theme.json: Visual theme and styling configuration
- filters.json: Filter options and searchable fields
"""

import json
from pathlib import Path
from typing import Dict, Any, List


class ConfigLoader:
    """
    Load and manage configuration files for the grant research website.
    
    This class provides a centralized way to access configuration data,
    with caching to avoid repeated file I/O operations.
    
    Attributes:
        config_dir (Path): Directory containing configuration files
        _cache (Dict): Cache for loaded configuration data
    """
    
    def __init__(self, config_dir: str = 'config') -> None:
        """
        Initialize the ConfigLoader.
        
        Args:
            config_dir (str): Path to the configuration directory.
                            Defaults to 'config' in the current directory.
        
        Raises:
            FileNotFoundError: If the configuration directory does not exist.
        """
        self.config_dir = Path(config_dir)
        self._cache: Dict[str, Any] = {}
        
        if not self.config_dir.exists():
            raise FileNotFoundError(
                f"Configuration directory not found: {self.config_dir}"
            )
    
    def _load_json_file(self, filename: str) -> Dict[str, Any]:
        """
        Load a JSON configuration file.
        
        Args:
            filename (str): Name of the JSON file to load (without path).
        
        Returns:
            Dict[str, Any]: Parsed JSON content.
        
        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file is not valid JSON.
        """
        filepath = self.config_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Configuration file not found: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in {filepath}: {e.msg}",
                e.doc,
                e.pos
            )
    
    def load_grants_sources(self) -> Dict[str, Any]:
        """
        Load grant sources configuration.
        
        Returns:
            Dict[str, Any]: Grant sources data with all funding sources and grants.
        
        Example:
            >>> loader = ConfigLoader()
            >>> sources = loader.load_grants_sources()
            >>> for source in sources['sources']:
            ...     print(f"{source['name']}: {len(source['grants'])} grants")
        """
        if 'grants_sources' not in self._cache:
            self._cache['grants_sources'] = self._load_json_file('grants_sources.json')
        return self._cache['grants_sources']
    
    def load_theme(self) -> Dict[str, Any]:
        """
        Load theme configuration.
        
        Returns:
            Dict[str, Any]: Theme data including colors, typography, and spacing.
        
        Example:
            >>> loader = ConfigLoader()
            >>> theme = loader.load_theme()
            >>> primary_color = theme['theme']['colors']['primary_gradient_start']
        """
        if 'theme' not in self._cache:
            self._cache['theme'] = self._load_json_file('theme.json')
        return self._cache['theme']
    
    def load_filters(self) -> Dict[str, Any]:
        """
        Load filter configuration.
        
        Returns:
            Dict[str, Any]: Filter options including amount thresholds and searchable fields.
        
        Example:
            >>> loader = ConfigLoader()
            >>> filters = loader.load_filters()
            >>> thresholds = filters['filters']['amount_thresholds']
        """
        if 'filters' not in self._cache:
            self._cache['filters'] = self._load_json_file('filters.json')
        return self._cache['filters']
    
    def get_all_grants(self) -> List[Dict[str, Any]]:
        """
        Get all grants from all sources as a flat list.
        
        Returns:
            List[Dict[str, Any]]: List of all grant dictionaries with source information.
        
        Example:
            >>> loader = ConfigLoader()
            >>> all_grants = loader.get_all_grants()
            >>> print(f"Total grants: {len(all_grants)}")
        """
        sources = self.load_grants_sources()
        all_grants = []
        
        for source in sources['sources']:
            source_name = source['name']
            source_id = source['id']
            
            for grant in source.get('grants', []):
                grant_copy = grant.copy()
                grant_copy['source'] = source_name
                grant_copy['source_id'] = source_id
                all_grants.append(grant_copy)
        
        return all_grants
    
    def clear_cache(self) -> None:
        """
        Clear the configuration cache.
        
        Useful for testing or when configuration files are updated
        and you want to reload them without creating a new ConfigLoader instance.
        """
        self._cache.clear()
