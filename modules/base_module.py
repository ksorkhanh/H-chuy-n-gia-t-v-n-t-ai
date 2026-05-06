"""
Base Module - Abstract base class for all business modules.
New modules must inherit from this class.
"""
from abc import ABC, abstractmethod


class BaseModule(ABC):
    """
    Abstract base class for plugin-based business modules.
    Each module represents a legal consultation domain.
    """

    @abstractmethod
    def get_name(self):
        """Return module identifier (e.g., 'transfer')."""
        pass

    @abstractmethod
    def get_display_name(self):
        """Return display name in Vietnamese."""
        pass

    @abstractmethod
    def get_description(self):
        """Return module description."""
        pass

    @abstractmethod
    def get_icon(self):
        """Return icon name/emoji for the module."""
        pass

    @abstractmethod
    def get_config(self):
        """
        Return fuzzy configuration dict.
        Must include: input_variables, output_variable
        """
        pass

    @abstractmethod
    def get_input_fields(self):
        """
        Return list of input field definitions for UI form.
        Each field: {name, label, type, range, step, default, description}
        """
        pass

    @abstractmethod
    def interpret_result(self, score, conclusion):
        """
        Interpret the fuzzy result for this specific domain.
        Returns dict with: level, title, description, recommendations
        """
        pass

    def get_domain(self):
        """Return legal domain for this module (default: dat_dai)."""
        return "dat_dai"
