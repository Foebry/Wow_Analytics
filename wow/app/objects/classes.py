from objects import Object



class Class(Object):
    """Class"""
    def __init__(self, operation=None, request=None, id_=None, test=False, **kwargs):
        """
            Initialization of Class object.
        """
        super().__init__(operation, request, id_, **kwargs)


    def prepareData(self, operation, request, data, dummy: bool=False):

        data["id_"] = data["class_id"]
        data["subclasses"] = {}

        return data



class Subclass(Object):
    """Subclass"""
    def __init__(self, operation=None, request=None, class_id=None, test=False, *args, **kwargs):
        """
            Initialization of Class object.
        """
        super().__init__(operation, request, class_id, test, *args, **kwargs)


    def prepareData(self, operation, request, data, dummy: bool=False):
        delattr(self, "id")
        data["name"] = data["display_name"]
        return data
