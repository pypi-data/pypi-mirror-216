from orbit_component_base.src.orbit_shared import world
from orbit_component_base.schema.OrbitPermissions import PermissionsCollection, PermissionsTable
from orbit_component_base.cli.cli_base import CliBase
from rich.console import Console
from rich.table import Table
from orbit_database import Doc
from orbit_database.exceptions import DuplicateKey
from orbit_component_base.src.orbit_decorators import permissions


class Permissions (CliBase):

    COLLECTIONS = [PermissionsCollection]

    def list (self):
        table = Table(
            title='Current Permissions',
            title_style='bold green',
            caption=f'authentication="{world.conf.authentication}"',
            caption_style='bold magenta'
        )
        rstyle = 'cyan'
        hstyle = 'deep_sky_blue4'
        table.add_column('Id',         style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Host Id',    style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Namespace',  style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Name',       style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Executable', style=rstyle, header_style=hstyle, no_wrap=True)
        for result in PermissionsCollection():
            doc = result.doc
            table.add_row(
                doc.key,
                doc._host_id,
                doc._namespace,
                doc._name,
                doc._exec)
                
        Console().print(table)
        print()
        
    def list_perms (self):
        table = Table(
            title='Available Permissions',
            title_style='bold green',
            caption=f'authentication="{world.conf.authentication}"',
            caption_style='bold magenta'
        )
        rstyle = 'cyan'
        hstyle = 'deep_sky_blue4'
        table.add_column('Package',     style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Namespace',   style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Permission',  style=rstyle, header_style=hstyle, no_wrap=True)
        table.add_column('Description', style=rstyle, header_style=hstyle, no_wrap=True)
        for p in permissions:
            table.add_row(*p)
        Console().print(table)
        print()
        
    def add (self, hostid, namespace, name, exec):
        try:
            PermissionsTable().from_doc(Doc({'host_id': hostid, 'namespace': namespace, 'name': name, 'exec': exec})).append()
            print(f'Added permission: for host "{hostid}", namespace "{namespace}" endpoint "{name}" exec "{exec}"')
        except DuplicateKey:
            print(f'Error: permission already exists!')

    def delete (self, hostid, namespace, name, exec):
        doc = PermissionsTable().from_request(hostid, namespace,name, exec)
        if doc.isValid:
            print(f'Removed permission: for host "{hostid}", namespace "{namespace}" endpoint "{name}" exec "{exec}"')
            doc.delete()
        else:
            print(f'Permission does not exist for host "{hostid}", namespace "{namespace}" endpoint "{name}" exec "{exec}"')

