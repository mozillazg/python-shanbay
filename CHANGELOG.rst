Changelog
=========


0.2.1 (2014-mm-dd)
-------------------

- [fix] team.info 无法处理打卡率是 0% 的情况
- [change] 登录成功时， shanbay.login() 返回值改为 True


0.2.0 (2014-06-09)
-------------------

- [delete] ``shanbay.API``, 因为扇贝网不再支持 API v0.8, 并且新的 API 尚未释出
- [change] 各 api 接口移除 @property 装饰器


0.1.1 (2014-05-15)
------------------

- [add] 站内消息 api
- [add] 小组管理 api
- [change] api 接口

具体用法可以参考 tests/ 以及 python-shanbay-team-assistant_

.. _python-shanbay-team-assistant:  https://github.com/mozillazg/python-shanbay-team-assistant/blob/develop/assistant.py


0.1.0 (2014-03-31)
------------------

- 封装 `扇贝网 API v0.8 <http://www.shanbay.com/help/developer/api>`__.
