from apps.utils.enums import BaseEnum


class OrderStatus(BaseEnum):
    Pending = 1
    Success = 2
    Failed = 3
    Cancel = 4

    CHOICES = (
        (Pending, 'Pending'),
        (Success, 'Success'),
        (Failed, 'Failed'),
        (Cancel, 'Cancel'),
    )