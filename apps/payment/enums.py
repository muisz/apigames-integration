from apps.utils.enums import BaseEnum


class PaymentMethod(BaseEnum):
    VA_BNI = 1
    VA_BCA = 2
    
    CHOICES = (
        (VA_BNI, 'BNI Virtual Account'),
        (VA_BCA, 'BCA Virtual Account'),
    )
