from orbit_component_base.src.orbit_shared import world
from orbit_component_base.schema.OrbitGroupPermissions import GroupPermissionsCollection, GroupPermissionsTable
from orbit_component_base.schema.OrbitUsers import UsersCollection, UsersTable
from orbit_component_base.cli.cli_base import CliBase
from rich.console import Console
from rich.table import Table
from orbit_database import Doc
from orbit_database.exceptions import DuplicateKey


class GroupPermissions (CliBase):

    COLLECTIONS = [GroupPermissionsCollection]

    def list_permissions (self):
        table = Table(
            title='Current Group Permissions',
            title_style='bold green',
            caption=f'authentication="{world.conf.authentication}"',
            caption_style='bold magenta'
        )
        rstyle = 'cyan'
        hstyle = 'deep_sky_blue4'
        table.add_column('Id',         style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Group Id',   style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Namespace',  style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Name',       style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Executable', style=rstyle, header_style=hstyle, no_wrap=True)
        for result in GroupPermissionsCollection():
            doc = result.doc
            table.add_row(
                doc.key,
                doc._group_id,
                doc._namespace,
                doc._name,
                doc._exec)
                
        Console().print(table)
        print()

    def list (self):
        table = Table(
            title='Current Groups',
            title_style='bold green',
            caption=f'authentication="{world.conf.authentication}"',
            caption_style='bold magenta'
        )
        rstyle = 'cyan'
        hstyle = 'deep_sky_blue4'
        table.add_column('Group Name',  style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Permissions', style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Users',       style=rstyle, header_style=hstyle, no_wrap=True)
        
        groups = {}
        
        for result in UsersCollection().filter('by_group', suppress_duplicates=True):
            gid = result.key.decode()
            if gid not in groups:
                groups[gid] = {'permissions': 0, 'users': 0}
            groups[gid]['users'] = result.count

        for result in GroupPermissionsCollection().filter('by_group_id', suppress_duplicates=True):
            groups[gid]['permissions'] = result.count
       
        for gid in groups:
            table.add_row(gid, str(groups[gid]['permissions']), str(groups[gid]['users']))
        Console().print(table)
        print()
        
    def add (self, group_id, namespace, name, exec):
        try:
            GroupPermissionsTable().from_doc(Doc({'group_id': group_id, 'namespace': namespace, 'name': name, 'exec': exec})).append()
            print(f'Added permission: for host "{group_id}", namespace "{namespace}" endpoint "{name}" exec "{exec}"')
        except DuplicateKey:
            print(f'Error: permission already exists!')

    def delete (self, group_id, namespace, name, exec):
        doc = GroupPermissionsTable().from_request(group_id, namespace,name, exec)
        if doc.isValid:
            print(f'Removed permission: for host "{group_id}", namespace "{namespace}" endpoint "{name}" exec "{exec}"')
            doc.delete()
        else:
            print(f'Permission does not exist for host "{group_id}", namespace "{namespace}" endpoint "{name}" exec "{exec}"')

    def add_user_group (self, host_id, group_id):
        user = UsersTable().from_key(host_id)
        if not user.isValid:
            print('Error: no such user')
            return
        if not user._groups:
            user._groups = []
        if group_id in user._groups:
            print('Error: user is already a member of that group')
            return
        user._groups.append(group_id)
        user.save()
        print(f'Added group "{group_id}", to user "{host_id}"')

    def del_user_group (self, host_id, group_id):
        user = UsersTable().from_key(host_id)
        if not user.isValid:
            print('Error: no such user')
            return
        if not user._groups:
            user._groups = []
        if group_id not in user._groups:
            print('Error: user not a member of that group')
            return
        user._groups.remove(group_id)
        user.save()
        print(f'Removed group "{group_id}", from user "{host_id}"')
