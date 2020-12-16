#!/usr/bin/python
# -*- coding: utf-8 -*-

from message import IntegrationEvent

"""
小程序平台列表
/// <summary>
/// 微信小程序
/// </summary>
WeiXinMini = 1,

/// <summary>
/// 微信公众号
/// </summary>
WeiXinMP = 11,

/// <summary>
/// 微信开放平台
/// </summary>
WeiXinOpen = 12,

/// <summary>
/// 支付宝小程序
/// </summary>
AliPayMini = 2,

/// <summary>
/// 抖音
/// </summary>
Tiktok = 3,

/// <summary>
/// 常规 H5或App
/// </summary>
Normal = 9,

"""


class CMCMiniprogramRelease(IntegrationEvent):
    def __init__(self, deploy, platform, version):
        super(CMCMiniprogramRelease, self).__init__()
        self._deploy = deploy
        self._platform = platform
        self._version = version
        self._event_name = 'CMCMiniprogramReleaseIntegrationEvent'

    @property
    def body(self):
        content = super(CMCMiniprogramRelease, self).body
        content['deploy'] = self._deploy
        content['platform'] = self._platform
        content['version'] = self._version

        return content