from orbit_component_base.src.orbit_orm import BaseTable, BaseCollection, register_class, register_method
from orbit_database import SerialiserType, Doc


class GroupPermissionsTable (BaseTable):
    norm_table_name = 'group_permissions'
    norm_auditing = True
    norm_codec = SerialiserType.UJSON
    norm_ensure = [
        {'index_name': 'by_request', 'duplicates': False , 'func': '{group_id}|{namespace}|{name}|{exec}'},
        {'index_name': 'by_group_id', 'duplicates': True  , 'func': '{group_id}'},
    ]

    def from_request (self, group_id, namespace, name, exec, transaction=None):
        self.set(self.norm_tb.seek_one('by_request', Doc({
                'group_id': group_id,
                'namespace': namespace,
                'name': name,
                'exec': exec,
            }), txn=transaction)
        )
        return self


@register_class
class GroupPermissionsCollection (BaseCollection):
    table_class = GroupPermissionsTable
    table_methods = ['get_ids']

    def check (self, group_id, namespace, name, exec):
        return GroupPermissionsTable().from_request (group_id, namespace, name, exec).isValid

    @register_method
    def get_ids_by_group(cls, session, params, transaction=None):
        ids, data = [], []
        limit = Doc({'group_id': params.get('group_id')})
        for result in cls().filter('by_group_id', lower=limit, upper=limit):
            session.append(params, result.oid.decode(), ids, data, result, strip=cls.table_strip)
        session.update(ids, params)
        return {'ok': True, 'ids': ids, 'data': data}
