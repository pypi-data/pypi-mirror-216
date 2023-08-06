import logging
import urllib.parse as parser
from typing import Union

from pydantic import BaseModel
from .rule import RuleHolder

LOGGER = logging.getLogger(__name__)
rule_holder = RuleHolder()


class UrlModel(BaseModel):
    """
    通用基础数据模型
    """
    # 链接序列号（全局唯一）  如：jd:5129155、tmall:576748721316,3985068128611
    link_sn: str = None
    # 网站编码  如：jd
    plat_code: str = None
    # 网站名称  如：京东
    plat_name: str = None
    # 链接商品编码（多编码链接，编码之间逗号分隔）  如：5129155、576748721316,3985068128611
    ec_sku_id: str = None


def parse_url(url) -> Union[UrlModel, None]:
    """
    解析url链接
    """
    plat_code, plat_name, ec_sku_id = _match_url(url)
    if plat_code and ec_sku_id:
        link_sn = _build_link_sn(plat_code, ec_sku_id)
        return UrlModel(link_sn=link_sn, plat_code=plat_code, plat_name=plat_name, ec_sku_id=ec_sku_id)

    return None


def _build_link_sn(plat_code, ec_sku_id):
    """
    构建link_sn编码规则
    """
    if plat_code and ec_sku_id:
        return f'{plat_code}:{ec_sku_id}'

    return None


def _clean_url(url):
    """
    链接非法字符清理
    """
    fix_err = {
        '&amp;': '&',
        '＆': '&'
    }
    _url = url
    if _url:
        for key in fix_err:
            if key in _url:
                _url = _url.replace(key, fix_err.get(key))

    return _url


def _match_url(url):
    plat_code = ''
    plat_name = ''
    ec_sku_id = ''
    _url = _clean_url(url)
    if _url:
        host = parser.urlparse(_url).hostname
        rule = rule_holder.get_rule(host)
        if host and rule:
            plat_code = rule.get('plat_code')
            plat_name = rule.get('plat_name')
            sku_param = rule.get('sku_param', [])
            if sku_param:
                ec_sku_id = _parse_sku_by_param(_url, sku_param)
            patterns = rule.get('patterns', [])
            if patterns and not ec_sku_id:
                ec_sku_id = _parse_sku_by_path(_url, patterns)

    return plat_code, plat_name, ec_sku_id


def _match_plat_code(url, default='*'):
    plat_code = default
    if url:
        host = parser.urlparse(url).hostname
        rule = rule_holder.get_rule(host)
        if host and rule:
            plat_code = rule.get('plat_code')

    return plat_code


def _parse_sku_by_path(url, patterns):
    """
    根据url中path部分解析skuId
    :param url:
    :param patterns:
    :return:
    """
    try:
        for ptn in patterns:
            arr = ptn.findall(url.strip())
            if len(arr):
                return arr[0].strip()
    except Exception as e:
        LOGGER.error('match sku error[parse_sku_by_path]: url=%s, ex=%s' % (url, e))

    return ''


def _parse_sku_by_param(url, sku_param, token=','):
    """
    根据url中param部分解析skuId
    :param url:
    :param sku_param:
    :return:
    """
    try:
        params = parser.parse_qs(parser.urlparse(url).query)

        rs_list = []
        if len(params) and sku_param:
            for param in sku_param:
                if param in params and params.get(param)[0].strip():
                    rs_list.append(str(params.get(param)[0].strip()))

            if token:
                return token.join(rs_list)
            else:
                return rs_list
    except Exception as e:
        LOGGER.error('match sku error[parse_sku_by_param]: url=%s, ex=%s' % (url, e))

    return ''
