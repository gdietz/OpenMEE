##############################################################################                   
#                                          
# Author: George Dietz                     
#                                          
# Description: Abstract implementation of a managed collection. This is
#              meant to be subclassed to suit particular requirements. All we
#              do here is manage a set of objects and a pool of ids of those
#              objects.
#
##############################################################################

from sets import Set
from ome_globals import *

class ManagedCollection(object):
    # Holds a collection of items that all have unique ids within the collection
    # The items are not ordered in any way
    #
    # The items stored must provide the following API:
    # First two arguments to constructor must be: id, label in that order
    # get_label()
    # get_id()
    #
    # Subclasses must implement data_item_name(bool plural) # wich gives
    
    def __init__(self, item_class):
        
        self.item_class = item_class
        #self.items = Set()
        #self.item_ids = Set()  # for now just simple integers
    
        self.ids_to_items = {}
    
    def data_item_name(self, plural=False):    # Abstract method, defined by convention only
        ''' gives the name of an item i.e. a 'study', a 'variable' etc '''
        raise NotImplementedError("Subclass must implement abstract method")
        
    def _acquire_unique_id(self):
        ''' Returns next available item id
        '''
        
        item_ids = self.ids_to_items.keys()
    
        if len(item_ids) == 0:    
            new_id = 0
        else:
            max_id = max(item_ids)
            new_id = max_id + 1
        
        # Should never be raised but is a good check to make sure the ids are
        # uniquely assigned
        if new_id in item_ids:
            err_msg = "The id '%s' is already in the set of used ids for this collection of %s" % (str(new_id), self.data_item_name(plural=True))
            raise DuplicateItemError(err_msg)
            
        return new_id
        
    def get_ids(self):
        return self.ids_to_items.keys()
    
    def get_item_by_id(self, item_id):
        ''' Returns a single item since item ids are always unique '''
    
        for item in self.ids_to_items.values():
            if item.get_id() == item_id:
                return item
        err_msg = "%s with id: '%s' not found" % (self.data_item_name(), str(item_id))
        return KeyError(err_msg)
    
    def get_items_by_label(self, label):
        ''' Returns a list of items since items MAY not have unique labels '''
        
        itemlist = []
        for item in self.ids_to_items.values():
            if item.get_label() == label:
                itemlist.append(item)
        return itemlist
    
    def get_items(self):
        ''' Returns set of all the items in the collection '''
        return self.ids_to_items.values()
    
    def get_labels(self):
        # Exclude None labels
        labels = Set()
        for item in self.ids_to_items.values():
            label = item.get_label()
            if label is not None:
                labels.add(label)
        return labels

    def make_item(self, label=None):
        ''' Makes a new study and returns reference to newly created study.
        Also updates the set of used item ids'''
        
        # creates new study_id and add it to the set of used study_ids
        new_item_id = self._acquire_unique_id()
        
        # Create the new item
        item = self.item_class(new_item_id, label)
            
        # Add the study to the collection
        self.ids_to_items[new_item_id] = item
        
        return item
    
    
    def add_existing_item(self, item):
        ''' Adds an self.item_class object that was created elsewhere to the
        collection (i.e. from an Undo Command) '''
        
        item_id = item.get_id()
        # verification
        item_name_singular = self.data_item_name()
        item_name_plural = self.data_item_name(plural=True)
        if item is None:
            raise Exception("%s is None!" % item_name_singular)
        if item_id is None:
            raise Exception("%s must have an id!" % item_name_singular)
        if item in self.ids_to_items.values():
            raise Exception("%s already in collection of %s!" % (item_name_singular, item_name_plural))
        if item_id in self.ids_to_items.keys():
            raise Exception("%s id already in collection of ids!" % item_name_singular)
        
        # add the item and map it to its id
        self.ids_to_items[item_id] = item
        return item
        
        
    def remove_item(self, item):
        # verification
        if item not in self.ids_to_items.values():
            raise ValueError("Attempted to delete non-existent %s" % self.data_item_name())
        
        # Removes item and frees id
        item_id = item.get_id()
        del self.ids_to_items[item_id]
        
