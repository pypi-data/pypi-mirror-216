from typing import List, Tuple

from django.db import models


class OnChangeModel(models.Model):
    """
    Handle a field edition.

    on_change_fields -- a list of field for processing by this model.
    Create a method with name like 'on_change_<field_name>' for handling its edition.
    """

    # It would be nice to make decorator @on_change(field1, field2...)

    on_change_fields = ()
    pre_save_prefix = 'on_change_'

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        for name in self.get_on_change_fields():
            setattr(self, f'__origin_{name}', getattr(self, name, None))
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        for name, origin_value, value in self.get_changed_fields():
            method = self._get_method(name)
            method(origin_value, value)
        super().save(*args, **kwargs)
        self.after_save()

    def after_save(self):
        """Customize it on your taste"""
        pass

    def get_on_change_fields(self):
        return self.on_change_fields

    def get_changed_fields(self) -> List[Tuple]:
        fields = []
        for name in self.get_on_change_fields():
            origin_name = f'__origin_{name}'
            origin_value = getattr(self, origin_name)
            value = getattr(self, name)
            if value != origin_value:
                fields.append((name, origin_value, value))
        return fields

    def _get_method(self, field_name: str):
        method_name = f'{self.pre_save_prefix}{field_name}'
        try:
            return getattr(self, method_name)
        except AttributeError:
            raise Exception(f'OnChangeModel has no method {method_name}')
