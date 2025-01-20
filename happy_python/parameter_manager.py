"""
启用或禁用参数，以及相关管理函数
"""


class ParameterManager:
    """
    使用位操作符简化参数校验代码
    """

    def __init__(self):
        # 已经启用的 Mask 形式参数列表
        self.flags = 0

        # 注册参数字典及其对应的回调校验函数
        self.reg_para_dict = dict()

    def reset(self):
        """
        清空重置注册参数和启用参数
        :return:
        """
        self.reg_para_dict = dict()
        self.flags = 0

    def set_para(self, flags):
        """
        重新设置启用参数列表
        :param flags: flag mask 形式参数列表，比如 org_id|token|user_id
        :return:
        """
        self.flags = flags

    def enable_paras(self, flags):
        """
        添加一个或多个参数到启用参数列表
        :param flags: flag mask 形式参数列表，比如 org_id|token|user_id
        :return:
        """
        self.flags |= flags

    def is_enable_paras(self, flag):
        """
        检查参数是否启用
        :param flag: flag mask 形式参数，比如 org_id
        :return:
        """
        return (self.flags & flag) > 0

    def disable_paras(self, flags):
        """
        禁用一个或多个参数
        :param flags: flag mask 形式参数列表，比如 org_id|token|user_id
        :return:
        """
        self.flags &= ~flags

    def get_enable_paras(self):
        """
        获取已经启用的参数列表
        :return: dict
        """

        para_dict = dict()

        for k, v in self.reg_para_dict.items():
            if (self.flags & k) > 0:
                para_dict[k] = v

        return para_dict

    def register_para(self, key: int, value: str, callback_func):
        """
        注册参数、名称、回调函数（校验参数）

        :param key: 参数
        :param value: 参数名称
        :param callback_func: 校验参数的回调函数
        """

        self.reg_para_dict[key] = [value, callback_func]

    def get_register_paras(self):
        """
        获取注册参数列表
        :return: dict
        """
        return self.reg_para_dict

    def validate_paras(self, paras: dict):
        """
        校验注册并启用的参数

        :param paras:
        :return: bool, message
        """
        enable_paras = self.get_enable_paras()

        for k, v in enable_paras.items():
            para_name = v[0]
            callback_func = v[1]

            if para_name not in paras:
                return False, ('缺少请求参数：%s' % para_name)

            arg_value = paras[para_name]

            if not callback_func:
                return False, ('回调函数错误：%s' % callback_func)

            if not callback_func(arg_value):
                return False, ('参数校验失败：%s => %s' % (para_name, arg_value))

        return True, ''
