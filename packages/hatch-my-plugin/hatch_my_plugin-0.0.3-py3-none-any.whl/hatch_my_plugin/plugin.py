from hatch.env.collectors.plugin.interface import EnvironmentCollectorInterface


class SpecialEnvironmentCollector(EnvironmentCollectorInterface):
    PLUGIN_NAME = 'myplug'
    print('-------------------------------------------マイプラグ')

    def config(self):
        print('configのプリント----------')
        print(self.__config)
        print('--------------------------')
