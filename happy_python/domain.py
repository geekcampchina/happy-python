"""
域名相关
"""

# 2.3.4. Size limits https://tools.ietf.org/html/rfc1035
# 域名最大长度
from pathlib import PurePath

from happy_python import HappyLog, is_ascii_str

DOMAIN_NAME_MAX_SIZE = 253

# 字段最大长度
FEILD_MAX_SIZE = 63

# 顶级域最小长度(点+两个字母)
TLD_MIN_SIZE = 3

# 域名分隔符
DOMAIN_SEPARATOR = '.'

hlog = HappyLog.get_instance()

# 顶级域列表
TLDs = []


def _top_level_domain_feild_builder(feild: str) -> str:
    assert bool(feild)
    return DOMAIN_SEPARATOR + feild


def _load_tlds_db() -> None:
    """
    从指定顶级域数据文件载入顶级域数据
    :return:
    """
    tlds_resource_file = str(PurePath(__file__).parent / 'resource' / 'tlds.txt')

    try:
        with open(tlds_resource_file, encoding='UTF-8') as f:
            for line in f.readlines():
                TLDs.append(line.strip())
    except FileNotFoundError:
        hlog.err('TLDs数据文件不存在：%s' % tlds_resource_file)
    except FileExistsError:
        hlog.err('无法打开TLDs数据文件：%s' % tlds_resource_file)


# 载入顶级域列表
_load_tlds_db()


class Domain:
    def __init__(self, domain: str):
        # 域名字符串
        self.name = domain
        # 主机字段数组
        self.feild_hosts = []
        # 域名字段
        self.feild_domain_name = ''
        # 顶级域字段数组
        self.feild_top_level_domains = []

    def add_feild_host(self, value: str):
        self.feild_hosts.append(value)

    def add_feild_top_level_domain(self, value):
        self.feild_top_level_domains.append(value)

    def get_domain_name(self):
        """
        域名字符串，比如 foo.com，foo.com.cn
        :return:
        """
        return '%s%s' % (self.feild_domain_name, ''.join(self.feild_top_level_domains))

    def get_host_name(self):
        """
        主机字符串，比如 www，www.test
        :return:
        """
        return DOMAIN_SEPARATOR.join(self.feild_hosts)


def _is_valid_tld(s: str) -> bool:
    """
    验证顶级域字段是否有效，在载入的顶级域数据数组中，查找存在的顶级域
    :param s:
    :return:
    """

    tld = _top_level_domain_feild_builder(s)
    tld_len = len(tld)

    if tld_len < TLD_MIN_SIZE or tld_len > FEILD_MAX_SIZE:
        return False

    # tld是否在顶级域列表中
    return tld in TLDs


def _is_valid_host(s: str) -> bool:
    """
    验证主机字段，主机字段由字母、数字、下划线以及中横线（“-”）组成，但不能为空或中横线（“-”），不能以中横线（“-”）开头或结尾
    :param s:
    :return:
    """
    s_len = len(s)

    if s_len == 0 or s_len > FEILD_MAX_SIZE:
        return False

    if s == '-':
        return False

    if s_len >= 2 and (s[0] == '-' or s[-1] == '-'):
        return False

    # 只对标准代码做正则匹配，忽略类似中文编码
    if is_ascii_str(s):
        import re

        return bool(re.match(r'[a-z0-9-_]+', s))

    return True


def _is_valid_dn(s: str) -> bool:
    """
    验证域名字段，域名字段由字母、数字、下划线以及中横线（“-”）组成，但长度不能为1，不能以中横线（“-”）开头或结尾
    :param s:
    :return:
    """
    s_len = len(s)

    if s_len <= 1 or s_len > FEILD_MAX_SIZE:
        return False

    if s == '-':
        return False

    if s[0] == '-' or s[-1] == '-':
        return False

    # 只对标准代码做正则匹配，忽略类似中文编码
    if is_ascii_str(s):
        import re

        return bool(re.match(r'^[a-z0-9-]+$', s))

    return True


def to_domain_obj(domain: str):
    """
    转换域名字符串为Domain对象
    :param domain:
    :return:
    """
    if not domain or len(domain) > DOMAIN_NAME_MAX_SIZE or domain[0] == DOMAIN_SEPARATOR:
        return None

    domain_obj = Domain(domain)
    feilds = domain.split(DOMAIN_SEPARATOR)
    feilds_len = len(feilds)

    if feilds_len < 2:
        hlog.error('无效的域名（%s）' % domain)
        return None

    # foo.com
    if feilds_len == 2:
        if _is_valid_dn(feilds[0]) and _is_valid_tld(feilds[1]):
            domain_obj.feild_domain_name = feilds[0]
            domain_obj.add_feild_top_level_domain(_top_level_domain_feild_builder(feilds[1]))

            return domain_obj

    # www.foo.com foo.com.cn

    tmp = feilds[-1]
    if not _is_valid_tld(tmp):
        hlog.error('无效的域名（%s）：%s' % (domain, tmp))
        return None

    tmp = feilds[-2]
    if _is_valid_tld(tmp):
        # foo.com.cn

        # .com
        domain_obj.add_feild_top_level_domain(_top_level_domain_feild_builder(tmp))
        host_index = 3
    else:
        # www.foo.com
        host_index = 2

    # .cn
    tmp = feilds[-1]
    domain_obj.add_feild_top_level_domain(_top_level_domain_feild_builder(tmp))

    # 检查域名字段
    # foo
    tmp = feilds[feilds_len - host_index]

    if _is_valid_dn(tmp):
        domain_obj.feild_domain_name = tmp
    else:
        hlog.error('无效的域名（%s）：%s' % (domain, tmp))
        return None

    host_len = feilds_len - host_index

    for i in range(0, host_len):
        tmp = feilds[i]

        if _is_valid_host(tmp):
            domain_obj.add_feild_host(tmp)
        else:
            hlog.error('无效的域名（%s）：%s' % (domain, tmp))
            return None

    return domain_obj
