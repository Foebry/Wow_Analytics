from objects import Object



class Mount(Object):
    """Mount"""
    def __init__(self, operation=None, request=None, id_=None, test=False, **kwargs):
        """
            Initialization of Item object.
        """
        super().__init__(operation, request, id_, test, **kwargs)


    def prepareData(self, operation, request, data, dummy: bool=False):

        data["id_"] = self.id
        if data["source"]: data["source"] = data["source"]["name"]
        else: data["source"] = "Unknown"

        if data["faction"]: data["faction"] = data["faction"]["name"]
        else: data["faction"] = "Factionless"

        return data
