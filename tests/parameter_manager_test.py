import unittest

from happy_python import ParameterManager

ARG_FLAG_USER_NAME = 1 << 0
ARG_FLAG_USER_ID = 2 << 0
ARG_FLAG_ROLE_ID = 3 << 0


def check_user_name(user_name):
    return user_name


def check_user_id(user_id):
    return user_id


def check_role_id(role_id):
    return role_id


class TestParameterManager(unittest.TestCase):
    pm = None

    def setUp(self):
        self.pm = ParameterManager()

    def test_get_register_paras(self):
        self.pm.reset()
        self.pm.register_para(ARG_FLAG_USER_NAME, 'userName', check_user_name)

        reg_paras = self.pm.get_register_paras()
        assert_reg_paras = {ARG_FLAG_USER_NAME: ['userName', check_user_name]}
        self.assertDictEqual(assert_reg_paras, reg_paras)

    def test_register_para(self):
        self.pm.register_para(ARG_FLAG_ROLE_ID, 'roleId', check_role_id)
        self.pm.register_para(ARG_FLAG_USER_NAME, 'userName', check_user_name)
        self.pm.register_para(ARG_FLAG_USER_ID, 'userId', check_user_id)

    def test_set_para(self):
        self.pm.set_para(ARG_FLAG_USER_NAME)

    def test_enable_paras(self):
        self.pm.enable_paras(ARG_FLAG_USER_NAME | ARG_FLAG_USER_ID | ARG_FLAG_ROLE_ID)

    def test_is_enable_paras(self):
        self.pm.enable_paras(ARG_FLAG_USER_NAME | ARG_FLAG_USER_ID | ARG_FLAG_ROLE_ID)
        self.assertTrue(self.pm.is_enable_paras(ARG_FLAG_USER_NAME))
        self.assertTrue(self.pm.is_enable_paras(ARG_FLAG_USER_ID))
        self.assertTrue(self.pm.is_enable_paras(ARG_FLAG_ROLE_ID))

    def test_disable_paras(self):
        self.pm.enable_paras(ARG_FLAG_USER_NAME | ARG_FLAG_USER_ID | ARG_FLAG_ROLE_ID)
        self.pm.disable_paras(ARG_FLAG_USER_NAME)

        self.assertFalse(self.pm.is_enable_paras(ARG_FLAG_USER_NAME))
        self.assertTrue(self.pm.is_enable_paras(ARG_FLAG_USER_ID))
        self.assertTrue(self.pm.is_enable_paras(ARG_FLAG_ROLE_ID))

    def test_get_enable_paras(self):
        self.pm.reset()
        self.pm.register_para(ARG_FLAG_ROLE_ID, 'roleId', check_role_id)
        self.pm.register_para(ARG_FLAG_USER_NAME, 'userName', check_user_name)
        self.pm.register_para(ARG_FLAG_USER_ID, 'userId', check_user_id)

        self.pm.enable_paras(ARG_FLAG_USER_NAME | ARG_FLAG_USER_ID | ARG_FLAG_ROLE_ID)
        paras = self.pm.get_enable_paras()

        self.assertListEqual(['roleId', check_role_id], paras[ARG_FLAG_ROLE_ID])
        self.assertListEqual(['userName', check_user_name], paras[ARG_FLAG_USER_NAME])
        self.assertListEqual(['userId', check_user_id], paras[ARG_FLAG_USER_ID])

    def test_validate_paras(self):
        pm = ParameterManager()
        pm.reset()
        pm.register_para(ARG_FLAG_USER_NAME, 'userName', check_user_name)

        pm.set_para(ARG_FLAG_USER_NAME)
        result = pm.validate_paras({'userName': 'foo'})

        self.assertTrue(result[0])
        self.assertEqual('', result[1])


if __name__ == '__main__':
    unittest.main()
