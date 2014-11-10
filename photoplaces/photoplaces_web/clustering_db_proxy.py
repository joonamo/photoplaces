from django.forms.models import model_to_dict
from copy import copy

class ClusteringDBProxy:
    fields_to_save = []
    one_to_one_relationships_to_save = []

    def __init__(self, db_entry):
        self.db_entry = db_entry
        self.values = model_to_dict(db_entry)

    def set_up_relations(self, **kwargs):
        pass

    def save_to_db(self):
        for field in fields_to_save:
            setattr(self.db_entry, field, self.values[field])
        for rel in one_to_one_relationships_to_save:
            setattr(self.db_entry, rel, self.values[rel]["id"])
        self.db_entry.save()

class RunProxy(ClusteringDBProxy):
    def set_up_relations(self, **kwargs):
        normalized_centers = kwargs["normalized_centers"]
        self.values["normalized_set"] = normalized_centers[self.values["normalized_set"]]

class ClusterProxy(ClusteringDBProxy):
    def set_up_relations(self, **kwargs):
        normalized_entries = kwargs["normalized_entries"]
        relations = []
        for e in self.values["normalized_entries"]:
            relations.append(normalized_entries[e])
        self.values["normalized_entries"] = copy(relations)

        photos = kwargs["photos"]
        relations = []
        for e in self.values["photos"]:
            relations.append(photos[e])
        self.values["photos"] = copy(relations)

        self.values["normalized_centers"] = kwargs["normalized_centers"][self.values["normalized_centers"]]

    def save_to_db(self):
        super.save_to_db()
        self.db_entry.clear_normalized_entries()
        self.add_normalized_entries_from_keys(
            [e.id for e in self.values["normalized_entries"]],
            [e.id for e in self.values["photos"]])

class PhotoProxy(ClusteringDBProxy):
    pass

class NormalizedEntryProxy(ClusteringDBProxy):
    def set_up_relations(self, **kwargs):
        photos = kwargs["photos"]
        self.values["actual_photo"] = photos[self.values["actual_photo"]]

class NormalizedSetProxy(ClusteringDBProxy):
    pass