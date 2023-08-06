from peewee import ModelSelect
from peewee import Field, IntegerField
from peewee import ModelSelect
from typing import Any, List

__version__ = '0.0.1'
VERSION = __version__


def operator_in_func(field: Field, filter_value: str) -> List[str]:
    if isinstance(field, IntegerField):
        filter_value_list = [int(i) for i in filter_value.split(',')]
        return field.in_(filter_value_list)
    else:
        return field.in_(filter_value.split(','))


def operator_not_in_func(field: Field, filter_value: str) -> List[str]:
    if isinstance(field, IntegerField):
        filter_value_list = [int(i) for i in filter_value.split(',')]
        return (~field.in_(filter_value_list))
    else:
        return (~field.in_(filter_value.split(',')))


class BaseFilter:
    def filter(self) -> ModelSelect:
        operators = self._Meta.operators
        model_class = self.Meta.model_class

        fields: dict[str, Field] = model_class._meta.fields

        q: ModelSelect = model_class.select()

        conditions = []
        for field_name, field in fields.items():
            for operator_name, operator_function in operators.items():
                field_key = (field_name+'_' +
                             operator_name) if operator_name else field_name
                if field_key in self.__dict__:
                    filter_value = self.__dict__[field_key]
                    if filter_value == None:
                        continue

                    conditions.append(
                        operator_function(
                            getattr(model_class, field_name), filter_value)
                    )

        if conditions:
            q = q.where(*conditions)
        return q

    class _Meta:
        operators = {
            '': lambda l, r: l == r,
            'neq': lambda l, r: l != r,
            'gt': lambda l, r: l > r,
            'gte': lambda l, r: l >= r,
            'isnull': lambda l, r: l == None,
            'lt': lambda l, r: l < r,
            'lte': lambda l, r: l <= r,
            'not': lambda l, r: l != r,
            'ne': lambda l, r: l != r,
            'in': operator_in_func,
            'not_in': operator_not_in_func,
            'nin': operator_not_in_func,
        }
