# Import all API namespaces here for easy access
from .books import books_ns
from .members import members_ns
from .loans import loans_ns
from .returns import returns_ns

__all__ = ['books_ns', 'members_ns', 'loans_ns', 'returns_ns']
