


class Object:

    def __init__(self, operation=None, request=None, id_: int=None, test: bool=False, *args, **kwargs):
        from classes import Subclass
        from items import Item
        build_object = kwargs
        new_object = operation is not None and not kwargs

        self.id = id_

        if test:
            self.kwargs = self.setData(operation, request, test=True)

        elif new_object:
            self.setData(operation, request, test, *args)
            self.insert(operation)

        elif build_object:
            self.setAttributes(**kwargs)


    def setAttributes(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])


    def setData(self, operation, request, test=False, *args):
        from items import Item
        from classes import Class, Subclass
        from mounts import Mount
        from pets import Pet

        API_calls = {
            Item: request.getItemData,
            Class: request.getClassData,
            Subclass: request.getSubclassData,
            Pet: request.getPetData,
            Mount: request.getMountData,
        }

        data = None
        for key in API_calls:
            if isinstance(self, key):
                data = API_calls[key](self, *args)
                break

        if data:
            data = self.prepareData(operation, request, data)
            delete = [key for key in data if key not in ["id", "name", "subclasses", "pet_id", "mount_id", "level", "quality", "item_class", "item_subclass", "type", "subtype", "sold", "price", "mean_price", "class_id", "subclass_id", "source", "faction"]]

            for key in delete: del data[key]

            if test: return data

            self.__init__(operation, request, **data)
            return

        data = self.prepareData(dummy=True)
        super().__init__(operation, request, **data)


    def insert(self, operation):
        from items import Item
        from classes import Class, Subclass
        from mounts import Mount
        from pets import Pet

        sections = {
            Item: "items",
            Class: "classes",
            Subclass: "subclasses",
            Pet: "pets",
            Mount: "mounts"
        }

        section = None
        for key in sections:
            if isinstance(self, key):
                section = sections[key]
                break

        set_section_insert_data = section in operation.insert_data
        unset_section_insert_data = section not in operation.insert_data

        if set_section_insert_data: operation.insert_data[section].append(self)

        elif unset_section_insert_data: operation.insert_data[section] = [self]


    def update(self, operation, existing, realm_id: int=None, test: bool=False):
        from items import Item
        from realms import Realm
        from auctions import Auction

        sections = {
            Item: "items"
        }

        section = None
        for key in sections:
            if isinstance(self, key):
                section = sections[key]
                break

        unset_section_update_data = section not in operation.update_data
        new_object_to_update = not unset_section_update_data and self not in operation.update_data[section]

        if unset_section_update_data: operation.update_data[section] = [self]

        elif new_object_to_update: operation.update_data[section].append(self)
