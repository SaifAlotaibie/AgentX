"""Storage module for persistent data management."""

from .resume_storage import resume_storage
from .ticket_storage import ticket_storage
from .contract_storage import contract_storage
from .certificate_storage import certificate_storage
from .work_permit_storage import work_permit_storage
from .reminder_storage import reminder_storage

__all__ = [
    'resume_storage',
    'ticket_storage',
    'contract_storage',
    'certificate_storage',
    'work_permit_storage',
    'reminder_storage'
]
