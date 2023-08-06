# -*- coding: utf-8 -*-

"""
todo: doc string
"""


class TagKey:
    """
    枚举了跟项目相关的所有的 AWS Resource Tag Key.

    :param SERVER_ID: **重要** 这个 tag 用来标注 EC2 和 RDS 是属于哪个逻辑 Server.
        它的值需满足如下格式: ``{env_name}-{server_name}``, 例如 ``sbx-blue``.
    :param SERVER_LIFECYCLE: 这个 tag 用来标注 EC2 和 RDS 的生命周期. 例如是否保持
        一直在线, 一直关机, 一直删除等等. 它的值必须是 :class:`ServerLifeCycle` 中的一个.
    :param WOW_STATUS: 这个 tag 用来记录 WOW 服务器的在线状态, 如果不在线则显示
        "stopped", 如果在线, 则显示 "N players" 其中 N 是一个整数. 注意这个 value
        的格式也很重要, 他会被其他项目的代码解析.
    :param WOW_STATUS_MEASURE_TIME: 这个 tag 用来记录 WOW_STATUS 的测量时间. 值为
        ISO 格式的 datetime.
    """

    SERVER_ID = "wserver:server_id"
    SERVER_LIFECYCLE = "wserver:server_lifecycle"
    WOW_STATUS = "wserver:wow_status"
    WOW_STATUS_MEASURE_TIME = "wserver:wow_status_measure_time"


class ServerLifeCycle:
    """
    服务器可能的几种生命周期状态定义. 我们会有一个 Lambda Function 对这些服务器进行管理,
    每隔一段时间就检查一次服务器的状态, 将它们保持在指定的 LifeCycle 状态.

    - running: 永远保持运行状态.
    - smart_running: 智能运行状态, 如果服务器内的玩家持续 4 小时为 0, 那么就会关闭服务器.
        又或是 EC2 和 DB 只有一个在运行的状态, 说明服务器不完整, 我们也将其关闭.
    - stopped: 保持服务器关闭状态.
    - deleted: 将服务器的 EC2 和 RDS 删除, 删除 RDS 之前创建一个 (AWS managed) 备份.
    """

    running = "running"
    smart_running = "smart_running"
    stopped = "stopped"
    deleted = "deleted"
