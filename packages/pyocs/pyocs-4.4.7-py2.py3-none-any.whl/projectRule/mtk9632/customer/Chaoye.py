from projectRule.mtk9632.Mtk9632Common import Mtk9632Common
import re
from customers.customer_common.common_database import commonDataBase


class Ruler(Mtk9632Common):

    # Customer_ID
    _customer_id = 'CUSTOMER_CHAOYE'

    # 代码分支
    _code_branch = ""

    # 测试类型
    _test_type = 'F'

    def get_ocs_modelid(self):
        project = self.request_dict[self.ocs_demand.product_name].replace('.', '_')
        region_name_list = self.request_dict[self.ocs_demand.region_name]
        map_list = commonDataBase().get_region_mapping_info_by_country(region_name_list)
        country = map_list[2]
        if not country:
            country = 'NONE'
        modelid = 'CP' + self.ocs_number + '_AC_CY_' + project + '_' + country + '_PT430CT03_1_43DN4B_2200_EDR0_LOGO_BLACK_SAMPLE'
        return modelid

    def get_tv_system(self):
        ret = ''
        tv_system_str = self.request_dict[self.ocs_demand.tv_system]
        if 'ATV' in tv_system_str and 'DVB' not in tv_system_str:
            ret += self.get_macro_line("CVT_EN_ONLY_ATV_SOURCE", "1")
        return ret

    def get_ocs_require(self):
        """获取ocs上的配置，生成配置代码
        Args:
            ocs_number：OCS订单号
        Returns:
             返回配置代码
        """
        ret = ''
        _space = 60
        ret += '#elif ( IsModelID('+ self.get_ocs_modelid() + ') )' + '\n'
        ret += '//-------------------------------------- Board ----------------------------------------------' + '\n'
        ret += self.get_board_macro()
        ret += self.get_chip_macro()
        ret += self.get_ddr_macro()
        ret += self.get_flash_size_macro()
        ret += self.get_ci_macro()
        ret += self.get_tuner_macro()
        ret += self.get_pwm_macro()
        ret += self.get_eshare_or_maxhubshare_macro()
        ret += self.get_tv_system()

        if 'fae_9632_an11' in self.get_code_branch():
            macro_str = self.ocs_demand.get_wifi_bluetooth()
            other_app_list = self.request_dict[self.ocs_demand.other_app_soft]
            if 'WB7638U' in macro_str:
                ret += self.get_macro_line("CVT_DEF_JPE_BLUETOOTH_TYPE", "ID_CUSTOMER_BUILD_IN_BLUETOOTH")
                if 'Gaia AI' in other_app_list:
                    ret += self.get_macro_line("CVT_DEF_JPE_BLUETOOTH_CONFIG", "ID_CUSTOMER_BLUETOOTH_VOICE")
                else:
                    ret += self.get_macro_line("CVT_DEF_JPE_BLUETOOTH_CONFIG", "ID_CUSTOMER_BLUETOOTH")
            elif 'WB8723DU' in macro_str:
                ret += self.get_macro_line("CVT_DEF_JPE_BLUETOOTH_TYPE", "ID_CUSTOMER_HANG_OUT_BLUETOOTH")
                if 'Gaia AI' in other_app_list:
                    ret += self.get_macro_line("CVT_DEF_JPE_BLUETOOTH_CONFIG", "ID_CUSTOMER_BLUETOOTH_VOICE")
                else:
                    ret += self.get_macro_line("CVT_DEF_JPE_BLUETOOTH_CONFIG", "ID_CUSTOMER_BLUETOOTH")

            ret += '// ir & keypad & logo' + '\n'
            ret += self.get_macro_line("CVT_DEF_IR_TYPE", "ID_IR_JP_IPTV_AP_81_53338W_0003")
            ret += self.get_macro_line("CVT_DEF_LOGO_TYPE", "ID_LOGO_JPE_BLUE")
            ret += self.get_macro_line("CVT_DEF_LAUNCHER_SKIN_LOGO", "ID_LAUNCHER_SKIN_LOGO_NONE")
            ret += '// panel id' + '\n'
            ret += self.get_macro_line("CVT_DEF_PANEL_TYPE", "ID_PNL_GENERAL_3840_2160_2Division")
            ret += self.get_macro_line("CVT_DEF_PQ_TYPE", "ID_PQ_JPE_COMMON")
            ret += '// customer' + '\n'
            if any(ct in self.get_ocs_country() for ct in \
                   ['PANAMA', 'COLOMBIA', 'PHILIPPINES', 'FRENCH_GUIANA', 'GUYANA', 'DOMINICAN', 'PERU', ]):
                ret += self.get_macro_line("CUSTOMER_MODE", "CUSTOMER_MODE_PANAMA_DAICE")
            elif any(ct in self.get_ocs_country() for ct in
                     ['CHILE', 'JAMAICA', 'URUGUAY', 'PERU', 'COSTA_RICA', 'VENEZUELA']):
                ret += self.get_macro_line("CUSTOMER_MODE", "CUSTOMER_MODE_CHILE_DAICE")
            else:
                ret += self.get_macro_line("CUSTOMER_MODE", "CUSTOMER_MODE_UAE_DAICE")
            ret += '// end\n'

        elif 'fae_9632' in self.get_code_branch():
            macro_str = self.ocs_demand.get_wifi_bluetooth()
            other_app_list = self.request_dict[self.ocs_demand.other_app_soft]
            if 'WB7638U' in macro_str:
                ret += self.get_macro_line("CVT_DEF_JPE_BLUETOOTH_TYPE", "ID_CUSTOMER_BUILD_IN_BLUETOOTH")
                if 'Gaia AI' in other_app_list:
                    ret += self.get_macro_line("CVT_DEF_JPE_BLUETOOTH_CONFIG", "ID_CUSTOMER_BLUETOOTH_VOICE")
                else:
                    ret += self.get_macro_line("CVT_DEF_JPE_BLUETOOTH_CONFIG", "ID_CUSTOMER_BLUETOOTH")
            elif 'WB8723DU' in macro_str:
                ret += self.get_macro_line("CVT_DEF_JPE_BLUETOOTH_TYPE", "ID_CUSTOMER_HANG_OUT_BLUETOOTH")
                if 'Gaia AI' in other_app_list:
                    ret += self.get_macro_line("CVT_DEF_JPE_BLUETOOTH_CONFIG", "ID_CUSTOMER_BLUETOOTH_VOICE")
                else:
                    ret += self.get_macro_line("CVT_DEF_JPE_BLUETOOTH_CONFIG", "ID_CUSTOMER_BLUETOOTH")

            ret += '// ir & keypad & logo' + '\n'
            ret += self.get_macro_line("CVT_DEF_IR_TYPE", "ID_IR_JP_IPTV_AP_81_53338W_0003")
            ret += self.get_macro_line("CVT_DEF_LOGO_TYPE", "ID_LOGO_JPE_BLUE_48")
            ret += self.get_macro_line("CVT_DEF_LAUNCHER_SKIN_LOGO", "ID_LAUNCHER_SKIN_LOGO_NONE")
            ret += '// panel id' + '\n'
            ret += self.get_macro_line("CVT_DEF_JPE_PANEL_CONFIG", "ID_CUSTOMER_PANEL_T650QVR09_4")
            ret += '// customer' + '\n'
            if any(ct in self.get_ocs_country() for ct in \
                   ['PANAMA', 'JAMAICA', 'COLOMBIA', 'PHILIPPINES', 'FRENCH_GUIANA', 'GUYANA', 'DOMINICAN', 'PERU', \
                    'VENEZUELA']):
                ret += self.get_macro_line("CUSTOMER_MODE", "CUSTOMER_MODE_PANAMA_DAICE")
            else:
                ret += self.get_macro_line("CUSTOMER_MODE", "CUSTOMER_MODE_DUBAI_DAICE")
            ret += '// end\n'

        elif 'fae_6681' in self.get_code_branch():
            macro_str = self.ocs_demand.get_wifi_bluetooth()
            other_app_list = self.request_dict[self.ocs_demand.other_app_soft]
            if 'WB8723DU' in macro_str:
                if 'Gaia AI' in other_app_list:
                    ret += self.get_macro_line("CHAOYE_LAUNCHER_MODE", "ID_CHAOYE_LAUNCHER_FOR_GAIA20_LAUNCHER40_AI")
                else:
                    ret += self.get_macro_line("CVT_EN_BLUETOOTH_ON_BOARD", "1")
            ret += '//-------------------------------------- panel pq -------------------------------------------' + '\n'
            ret += self.get_macro_line("PANEL_CONFIG_GROUP", "ID_PT430CT03_1")
            ret += '//-------------------------------------- ir logo --------------------------------------------' + '\n'
            ret += self.get_macro_line("CVT_DEF_IR_TYPE", "ID_IR_CHAOYE_IPTV_AM_2200_EDR0")
            ret += self.get_macro_line("CVT_DEF_LOGO_TYPE", "ID_LOGO_CHAOYE_BLACK")
            ret += '//-------------------------------------- Sound ----------------------------------------------' + '\n'
            ret += '//-------------------------------------- country --------------------------------------------' + '\n'
            if any(ct in self.get_ocs_country() for ct in \
                   ['PANAMA', 'JAMAICA', 'COLOMBIA', 'PHILIPPINES', 'FRENCH_GUIANA', 'GUYANA', 'DOMINICAN', 'PERU',\
                    'VENEZUELA']):
                ret += self.get_macro_line("CVT_DEF_COUNTRY_SELECT", "ID_COUNTRY_PANAMA")
            else:
                ret += self.get_macro_line("CVT_DEF_COUNTRY_SELECT", "ID_COUNTRY_UAE")
            ret += '//-------------------------------------- Language -------------------------------------------' + '\n'
            ret += self.get_macro_line("LANGUAGE_CONFIG_GROUP", "ID_US_FR_DE_RU_EG__DEF_US")
            ret += '// END\n'
        return ret

    def get_android_system(self):
        requirement = self.get_customer_special_requirement()
        if "安卓11" in requirement:
            return "an11"
        return None

    def get_ocs_country(self):
        ret = ''
        db = commonDataBase()
        region_name_str = self.request_dict[self.ocs_demand.region_name]
        if region_name_str != '':
            country = db.get_region_mapping_info_by_country(region_name_str)[3]
            # 国家补丁
            if country == None:
                country = 'DUBAI'
            ret += self.get_macro_line("CVT_DEF_COUNTRY_SELECT", "ID_COUNTRY_" + country)
        return ret


















