from hatch.env.collectors.plugin.interface import EnvironmentCollectorInterface


class SpecialEnvironmentCollector(EnvironmentCollectorInterface):
    PLUGIN_NAME = 'myplug'
    print('-------------------------------------------マイプラグ')
    print('更新')
    def get_initial_config(self):

        print('config表示')
        print(self.__config)
        config = {}
        return {'myplug': config}
