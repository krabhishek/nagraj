"""Password-related specifications."""

import re

from {{cookiecutter.project_slug}}.common.base.specification import BaseSpecification


class ValidPasswordSpecification(BaseSpecification[str]):
    """Specification for validating password requirements."""

    def __init__(
        self,
        min_length: int = 8,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digit: bool = True,
        require_special: bool = True,
    ):
        """Initialize password validation rules."""
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digit = require_digit
        self.require_special = require_special

    def is_satisfied_by(self, password: str) -> bool:
        """Check if the password meets all requirements."""
        if len(password) < self.min_length:
            return False

        if self.require_uppercase and not any(c.isupper() for c in password):
            return False

        if self.require_lowercase and not any(c.islower() for c in password):
            return False

        if self.require_digit and not any(c.isdigit() for c in password):
            return False

        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False

        return True
