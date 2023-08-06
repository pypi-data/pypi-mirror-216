from orbit_component_base.src.orbit_plugin import ArgsBase
from orbit_component_base.src.orbit_shells import PluginXTerm
from orbit_component_base.src.orbit_decorators import Sentry
from orbit_component_base.schema.OrbitPermissions import PermissionsCollection
from loguru import logger as log

COMPONENT_NAMESPACE = 'dbshell'

def check_permission (args, session, name, exec):
    key = f'{name}|{exec}'
    if key in session.get('permission_cache', []):
        return True
    if 'permission_cache' not in session:
        session['permission_cache'] = set()
    if PermissionsCollection(args[1]).check(session.get("host_id"), COMPONENT_NAMESPACE, name, exec):
        session['permission_cache'].add(key)
        return True
    log.debug(f'Permission denied, user={session.get("host_id")} namespace={COMPONENT_NAMESPACE} name={name} exec={exec}')
    return False


class Plugin (PluginXTerm):

    NAMESPACE = COMPONENT_NAMESPACE
    EXECUTABLE = 'orbit_database_shell'

    @Sentry(check_permission)
    async def on_mount (self, *args, **kwargs):
        return await super().mount(*args, **kwargs)


class Args (ArgsBase):
    pass
