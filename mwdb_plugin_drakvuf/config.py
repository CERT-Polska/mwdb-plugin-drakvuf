from mwdb.core.config import AppConfig, app_config
from mwdb.core.typedconfig import Config, group_key, key, section


@section("drakvuf")
class DrakvufPluginConfig(Config):
    drakvuf_url = key(cast=str, required=True)
    timeout = key(cast=int, required=False, default=600)


class DrakvufPluginAppConfig(AppConfig):
    drakvuf = group_key(DrakvufPluginConfig)


config = DrakvufPluginAppConfig(provider=app_config.provider)
