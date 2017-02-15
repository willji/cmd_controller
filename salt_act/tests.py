from django.test import TestCase
from act import ExecCmdSalt


# Create your tests here.
class ActTestCase(TestCase):
    def setUp(self):
        self.host = '172.16.100.80'
        self.module_name = 'get_package'
        self.args = (u'iis', u'production/m2c/haiwai.ymatou.com/T2', u'172.16.100.81,wdeployadmin,wdeployadmin')

    def test_cmd(self):
        self.salt_cmd()

    def salt_cmd(self):
        print ExecCmdSalt(self.host, self.module_name, self.args).run

    def tearDown(self):
        pass
