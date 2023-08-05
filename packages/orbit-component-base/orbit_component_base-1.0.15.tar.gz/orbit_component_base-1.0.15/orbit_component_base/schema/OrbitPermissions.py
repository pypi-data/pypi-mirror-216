from orbit_component_base.src.orbit_orm import BaseTable, BaseCollection, register_class, register_method
from orbit_database import SerialiserType, Doc


class PermissionsTable (BaseTable):
    norm_table_name = 'permissions'
    norm_auditing = True
    norm_codec = SerialiserType.UJSON
    norm_ensure = [
        {'index_name': 'by_request', 'duplicates': False , 'func': '{host_id}|{namespace}|{name}|{exec}'},
        {'index_name': 'by_host_id', 'duplicates': True  , 'func': '{host_id}'},
    ]

    def from_request (self, host_id, namespace, name, exec, transaction=None):
        self.set(
            self.norm_tb.seek_one('by_request', Doc(
                {
                    'host_id': host_id,
                    'namespace': namespace,
                    'name': name,
                    'exec': exec,
                })
            , txn=transaction)
        )
        return self


@register_class
class PermissionsCollection (BaseCollection):
    table_class = PermissionsTable
    table_methods = ['get_ids']

    def check (self, host_id, namespace, name, exec):
        return PermissionsTable().from_request (host_id, namespace, name, exec).isValid

    @register_method
    def get_ids_by_host(cls, session, params, transaction=None):
        ids, data = [], []
        limit = Doc({'host_id': params.get('host_id')})
        for result in cls().filter('by_host_id', lower=limit, upper=limit):
            session.append(params, result.oid.decode(), ids, data, result, strip=cls.table_strip)
        session.update(ids, params)
        return {'ok': True, 'ids': ids, 'data': data}
