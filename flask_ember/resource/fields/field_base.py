from abc import ABCMeta, abstractmethod


class FieldBase(metaclass=ABCMeta):
    """Base class for field declaration in resources. The class provides the
    :meth:`prepare_attributes` method in order to alter the attributes of a
    resource class that is to be generated for this field.
    """

    @abstractmethod
    def prepare_attributes(self, field_name, attrs):
        """Prepares the attributes of a resource class that is to be generated
        for this field with the given field name. As an example this method may
        replace the original declarative field with a sqlalchemy column.

        :param field_name: the name of the field to generate
        :type field_name: string
        :param attrs: the attributes of the class that is to be generated
        :type attrs: dict
        """
        pass
