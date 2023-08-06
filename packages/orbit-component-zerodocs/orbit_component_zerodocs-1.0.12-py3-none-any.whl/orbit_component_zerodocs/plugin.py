from orbit_component_base.src.orbit_plugin import PluginBase
from orbit_component_base.src.orbit_decorators import Sentry
from orbit_component_zerodocs.schema.Cache import CacheCollection
from orbit_component_zerodocs.schema.APIs import APIsCollection
from orbit_component_zerodocs.schema.Project import ProjectCollection
from orbit_component_base.schema.OrbitPermissions import PermissionsCollection
from loguru import logger as log

COMPONENT_NAMESPACE = 'zerodocs'


def check_permission (session, name, args):
    log.warning(f'name={name} host={session.get("host_id")} nsp={COMPONENT_NAMESPACE} args={str(args)}')
    key = f'{name}|default'
    if key in session.get('permission_cache', []):
        return True
    if 'permission_cache' not in session:
        session['permission_cache'] = set()
    if PermissionsCollection(args[1]).check(session.get("host_id"), COMPONENT_NAMESPACE, name, 'default'):
        session['permission_cache'].add(key)
        return True
    log.debug(f'Permission denied, user={session.get("host_id")} namespace={COMPONENT_NAMESPACE} name={name}')
    return False


class Plugin (PluginBase):

    NAMESPACE = COMPONENT_NAMESPACE
    COLLECTIONS = [
        CacheCollection,
        APIsCollection,
        ProjectCollection
    ]

    @Sentry()
    async def on_cache_fetch (self, sid, params, force=False):
        return await CacheCollection(sid).fetch(params, force)

    @Sentry()
    async def on_get_project_id (self, sid, params):
        return await CacheCollection(sid).get_project_id(params)

    @Sentry()
    async def on_get_api_remote (self, sid, provider, api, branch, path):
        return APIsCollection(sid).get_api_remote(provider, api, branch, path)

    @Sentry(check_permission)
    async def on_cache_put (self, sid, old_data, new_data):
        return await CacheCollection(sid).put(old_data, new_data)

    @Sentry(check_permission)
    async def on_project_put (self, sid, params):
        return await ProjectCollection(sid).put(params)

    @Sentry(check_permission)
    async def on_project_remove (self, sid, params):
        try:
            await ProjectCollection(sid).remove(params)
            await CacheCollection(sid).remove(params)
            return {'ok': True}
        except Exception as e:
            log.exception(e)
            return {'ok': False, 'error': str(e)}
