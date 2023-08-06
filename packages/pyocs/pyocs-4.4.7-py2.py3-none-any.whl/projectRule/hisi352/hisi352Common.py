import abc
from pyocs.pyocs_interface import UniteInterface
from customers.customer_common.common_database import commonDataBase
from pyocs.pyocs_exception import *


class Hisi352Common(UniteInterface):

    def get_code_branch(self):
        region_name_list = self.request_dict[self.ocs_demand.region_name]
        if not region_name_list:
            raise NoRegionError('此单无区域')
        self._code_branch = 'fae'
        return self._code_branch

    @abc.abstractmethod
    def get_ocs_modelid(self):
        pass

    @abc.abstractmethod
    def get_ocs_require(self):
        pass