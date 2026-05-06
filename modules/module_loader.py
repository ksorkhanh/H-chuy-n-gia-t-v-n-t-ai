"""
Module Loader - Dynamically discovers and loads business modules.
Uses registry pattern for plugin management.
"""
import os
import importlib
import logging
from config.settings import MODULES_DIR
from modules.base_module import BaseModule

logger = logging.getLogger(__name__)


class ModuleLoader:
    """
    Dynamic module loader and registry.
    Scans modules/ directory for valid modules implementing BaseModule.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._modules = {}

    def discover_modules(self):
        """Scan and load all modules from the modules directory."""
        self._modules = {}

        if not os.path.exists(MODULES_DIR):
            logger.warning(f"Modules directory not found: {MODULES_DIR}")
            return

        for item in os.listdir(MODULES_DIR):
            module_path = os.path.join(MODULES_DIR, item)
            if os.path.isdir(module_path) and item != "__pycache__":
                module_file = os.path.join(module_path, "module.py")
                if os.path.exists(module_file):
                    try:
                        mod = importlib.import_module(f"modules.{item}.module")
                        # Find class that inherits BaseModule
                        for attr_name in dir(mod):
                            attr = getattr(mod, attr_name)
                            if (isinstance(attr, type) and issubclass(attr, BaseModule)
                                    and attr is not BaseModule):
                                instance = attr()
                                self._modules[instance.get_name()] = instance
                                logger.info(f"Loaded module: {instance.get_display_name()}")
                                break
                    except Exception as e:
                        logger.error(f"Error loading module '{item}': {e}")

    def get_module(self, name):
        """Get a specific module by name."""
        return self._modules.get(name)

    def get_all_modules(self):
        """Get all loaded modules."""
        return self._modules

    def get_module_names(self):
        """Get list of module names."""
        return list(self._modules.keys())

    def get_module_list(self):
        """Get list of module info for UI display."""
        return [
            {
                "name": m.get_name(),
                "display_name": m.get_display_name(),
                "description": m.get_description(),
                "icon": m.get_icon()
            }
            for m in self._modules.values()
        ]
