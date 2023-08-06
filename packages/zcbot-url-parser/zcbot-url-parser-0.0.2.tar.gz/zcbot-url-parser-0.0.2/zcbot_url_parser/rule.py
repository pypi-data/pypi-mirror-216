import logging
import re
import requests
from .utils import singleton

LOGGER = logging.getLogger(__name__)


@singleton
class RuleHolder(object):
    """
    常见电商平台商品编码解析规则
    """
    rule_map = {}

    def __init__(self):
        self.reload()

    def get_rule(self, host):
        return self.rule_map.get(host)

    def reload(self):
        """
        加载最新规则，可挂到定时任务上定期更新
        :return:
        """
        plats = self._fetch_platforms()
        plat_map = {}
        for plat in plats:
            plat_map[plat.get('_id')] = plat.get('name')

        rows = self._fetch_url_rules()
        for row in rows:
            regex_list = row.get('regex', [])
            patterns = []
            for regex in regex_list:
                try:
                    patterns.append(re.compile(regex))
                except re.error:
                    LOGGER.error(f'错误规则: regex={regex}, row={row}')

            plat_code = row.get('plat_code')
            plat_name = row.get('plat_name', None) or plat_map.get(plat_code) or plat_code
            self.rule_map[row.get('_id')] = {
                'plat_code': plat_code,
                'plat_name': plat_name,
                'sku_param': row.get('params', []),
                'patterns': [
                    re.compile(x) for x in row.get('regex', [])
                ],
            }
        LOGGER.info(f'更新链接分拣规则: {len(self.rule_map)}条')

    def _fetch_platforms(self):
        platforms = []
        # TODO 待优化
        rs = requests.get('http://www.zcbot.cn/zcbot-api/api/meta/platforms', timeout=15)
        if rs:
            platforms = rs.json().get('data', []) or []

        return platforms

    def _fetch_url_rules(self):
        rules = []
        # TODO 待优化
        rs = requests.get('http://www.zcbot.cn/zcbot-api/api/meta/url-rules', timeout=15)
        if rs:
            rules = rs.json().get('data', []) or []

        return rules
