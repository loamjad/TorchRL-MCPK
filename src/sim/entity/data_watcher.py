import numpy as np

from src.sim.util.block_pos import BlockPos


class DataWatcher:
    def __init__(self, owner):
        self.watched_objects = {}

        self.owner = owner

    def add_object(self, id, object):
        integer = self.data_types.get(type(object))

        if integer == None:
            # TODO: throw new IllegalArgumentException("Unknown data type: " + object.getClass());
            pass
        elif id > 31:
            # TODO: throw new IllegalArgumentException("Data value id is too big with " + id + "! (Max is " + 31 + ")");
            pass
        elif id in self.watched_objects:
            # TODO: throw new IllegalArgumentException("Duplicate id value for " + id + "!");
            pass
        else:
            datawatcher_watchableobject = DataWatcher.WatchableObject(integer, id, object)
            self.watched_objects[id] = datawatcher_watchableobject
            self.is_blank = False

    def get_watchable_object_byte(self, id):
        return np.int8(self.get_watched_object(id).get_object())
    
    def get_watched_object(self, id):
        try:
            datawatcher_watchableobject = self.watched_objects.get(id)
        except:
            pass

        return datawatcher_watchableobject
    
    def update_object(self, id, new_data):
        datawatcher_watchableobject = self.get_watched_object(id)

        if new_data != datawatcher_watchableobject.get_object():
            datawatcher_watchableobject.set_object(new_data)
            datawatcher_watchableobject.set_watched(True)
            self.object_changed = True

    
    @classmethod
    def static(cls):
        cls.data_types[np.int8]    = 0
        cls.data_types[np.int16]   = 1
        cls.data_types[np.int32]   = 2
        cls.data_types[np.float32] = 3
        cls.data_types[str]        = 4
        # cls.data_types[ItemStack] = 5
        cls.data_types[BlockPos]   = 6
        # cls.data_types[Rotations] = 7

    class WatchableObject:
        def __init__(self, type, id, object):
            self.data_value_id = id
            self.watched_object = object
            self.object_type = type
            self.watched = True
        def get_data_value_id(self):
            return self.data_value_id
        
        def set_object(self, object):
            self.watched_object = object
        def get_object(self):
            return self.watched_object
        
        def get_object_type(self):
            return self.object_type
        
        def is_watched(self):
            return self.watched
        def set_watched(self, watched):
            self.watched = watched
            
DataWatcher.data_types = {}
DataWatcher.static()