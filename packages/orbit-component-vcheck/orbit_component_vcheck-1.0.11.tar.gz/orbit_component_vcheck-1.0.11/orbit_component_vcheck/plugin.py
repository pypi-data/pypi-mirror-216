from orbit_component_base.src.orbit_plugin import PluginBase, ArgsBase
from orbit_component_vcheck.schema.Versions import VersionsCollection
from orbit_component_vcheck.src.versions import Versions
from loguru import logger as log


class Plugin (PluginBase):

    NAMESPACE = 'vcheck'
    COLLECTIONS = [VersionsCollection]

    async def on_get_version (self, sid, product, version):
        log.debug(f"NS={self.ns} product={product} version={version}")
        return await VersionsCollection(sid=sid, session=await self.get_session(sid), ns=self.ns).get_version(product, version)


class Args (ArgsBase):
        
    def setup (self):
        self._parser.add_argument("--vc-versions", action='store_true', help="List version check versions")
        self._parser.add_argument("--vc-add", type=str, help='Set the version for a given product string', metavar="<product>")
        self._parser.add_argument("--vc-del", type=str, help='Delete the specified product record', metavar="<product>")
        self._parser.add_argument("--vc-ver", type=str, help='The version for set-version', metavar="<version>")
        return self
    
    def process (self):
        if self._args.vc_versions:
            return Versions(self._odb).setup().list()
        if self._args.vc_add:
            if not self._args.vc_ver:
                self._parser.error('You need to specify a version (vc-ver) argument to add a new product')
                exit()
            return Versions(self._odb).setup().add(self._args.vc_add, self._args.vc_ver)
        if self._args.vc_del:
            return Versions(self._odb).setup().delete(self._args.vc_del)
