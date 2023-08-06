from orbit_component_base.src.orbit_plugin import PluginBase, ArgsBase
from orbit_component_base.schema.OrbitSessions import SessionsCollection
from orbit_component_base.schema.OrbitUsers import UsersCollection
from orbit_component_base.schema.OrbitPermissions import PermissionsCollection
from orbit_component_base.cli.users import Users
from orbit_component_base.cli.sessions import Sessions
from orbit_component_base.cli.permissions import Permissions


class Plugin (PluginBase):

    NAMESPACE = 'orbit'
    COLLECTIONS = [
        UsersCollection,
        SessionsCollection,
        PermissionsCollection
    ]


class Args (ArgsBase):
        
    def setup (self):
        self._parser.add_argument("--dev", action='store_true', default=False, help='Start the Orbit server in development mode')
        self._parser.add_argument("--run", action='store_true', default=False, help='Start the Orbit server and run in the background')
        self._parser.add_argument("--users", action='store_true', help="List users")
        self._parser.add_argument("--sessions", action='store_true', help="List sessions")
        self._parser.add_argument("--permissions", action='store_true', help="List permissions table")
        self._parser.add_argument("--permission", type=str, metavar="<perm>", help='Set permission [user|admin] for a given host id')
        self._parser.add_argument("--permission-add", type=str, metavar="<endpoint>", help='Allow access to a specified endpoint')
        self._parser.add_argument("--permission-del", type=str, metavar="<endpoint>", help='Remove access to a specified endpoint')
        self._parser.add_argument("--hostid", type=str, metavar="<host>", help='The host_id for a "permission" operation')
        self._parser.add_argument("--namespace", type=str, metavar="<namespace>", help='The namespace for a "permission" operation')
        self._parser.add_argument("--exec", type=str, metavar="<exec>", help='The executable to give access to')
        return super().process()
    
    def process (self):
        if self._args.users:
            return Users(self._odb).setup().list()
        if self._args.sessions:
            return Sessions(self._odb).setup().list()
        if self._args.permissions:
            return Permissions(self._odb).setup().list()
        if self._args.permission_add:
            return Permissions(self._odb).setup().add(self._args.hostid, self._args.namespace, self._args.permission_add, self._args.exec)
        if self._args.permission_del:
            return Permissions(self._odb).setup().delete(self._args.hostid, self._args.namespace, self._args.permission_del, self._args.exec)

        if self._args.permission:
            if not self._args.hostid:
                self._parser.error('You need to specify a host (hostid) argument to authorize a user')
                exit()
            return Users(self._odb).setup().auth(self._args.permission, self._args.hostid)
