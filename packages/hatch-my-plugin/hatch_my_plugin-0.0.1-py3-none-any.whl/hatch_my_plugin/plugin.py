from hatch.env.collectors.plugin.interface import EnvironmentCollectorInterface


class SpecialEnvironmentCollector(EnvironmentCollectorInterface):
    PLUGIN_NAME = 'myplug'
    print('-------------------------------------------マイプラグ')
