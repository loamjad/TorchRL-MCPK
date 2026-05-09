class DataWatcher:
    def __init__(self, owner):
        self.data_types = {}
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
        elif id in self.watchedObjects:
            # TODO: throw new IllegalArgumentException("Duplicate id value for " + id + "!");
            pass
        else:
            datawatcher_watchableobject = WatchableObject(integer, id, object)
            self.watched_objects[id] = datawatcher_watchableobject
            self.is_blank = False

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

            def get_object():
                return self.watched_object
            
            def get_object_type(self):
                return self.object_type
            
            def is_watched(self):
                return self.watched

            def set_watched(self, watched):
                self.watched = watched
            
