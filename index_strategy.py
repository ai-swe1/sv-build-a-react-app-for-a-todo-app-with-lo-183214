from django.db import models
from models import Todo

class IndexStrategy:
    def __init__(self):
        self.indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['completed']),
        ]

    def create_indexes(self):
        for index in self.indexes:
            Todo._meta.get_field('id').create_index()
            index.create_index()