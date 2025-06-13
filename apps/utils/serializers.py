from rest_framework.serializers import ChoiceField
from apps.utils.enums import BaseEnum

class EnumChoiceField(ChoiceField):
    def __init__(self, enum: BaseEnum, **kwargs):
        self.enum = enum
        super().__init__(enum.CHOICES, **kwargs)

    def to_representation(self, value):
        return {'id': value, 'name': self.enum.get_name(value)}
