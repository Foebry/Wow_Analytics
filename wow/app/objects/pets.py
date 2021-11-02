#!/usr/bin/env python3

from objects import Object



class Pet(Object):
    """Pet"""
    def __init__(self, operation=None, request=None, id_=None, test=False, **kwargs):
        """
            Initialization of Item object.
        """
        super().__init__(operation, request, id_, test, **kwargs)


    def prepareData(self, operation, request, data, dummy: bool=False):

        data["id_"] = self.id
        data["type"] = data["battle_pet_type"]["name"]
        data["source"] = data["source"]["name"]
        data["faction"] = "Factionless"

        if data["is_alliance_only"]: data["faction"] = "Alliance"
        elif data["is_horde_only"]: data["faction"] = "Horde"

        return data
