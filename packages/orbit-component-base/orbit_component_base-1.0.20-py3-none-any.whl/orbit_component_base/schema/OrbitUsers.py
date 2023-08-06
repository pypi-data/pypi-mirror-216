from orbit_component_base.src.orbit_orm import BaseTable, BaseCollection
from orbit_database import SerialiserType
from datetime import datetime


class UsersTable (BaseTable):

    norm_table_name = 'users'
    norm_auditing = True
    norm_codec = SerialiserType.UJSON

    @property
    def last_seen (self):
        return datetime.utcfromtimestamp(self._when).strftime('%Y-%m-%d %H:%M:%S')
    
    @property
    def code (self):
        return self._code if self._code else "Activated"


class UsersCollection (BaseCollection):

    table_class = UsersTable
    table_strip = ['user_id']
    table_methods = ['get_ids']
