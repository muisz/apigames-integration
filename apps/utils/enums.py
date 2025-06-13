class BaseEnum:
    CHOICES = ()

    @classmethod
    def get_name(self, value):
        for enum in self.CHOICES:
            if enum[0] == value:
                return enum[1]
        return None
