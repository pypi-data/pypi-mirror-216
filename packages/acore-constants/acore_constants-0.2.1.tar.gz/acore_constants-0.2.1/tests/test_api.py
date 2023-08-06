# -*- coding: utf-8 -*-

import os
import pytest


def test():
    from acore_constants import api

    _ = api.TagKey
    _ = api.TagKey.SERVER_ID
    _ = api.TagKey.SERVER_LIFECYCLE
    _ = api.TagKey.WOW_STATUS
    _ = api.TagKey.WOW_STATUS_MEASURE_TIME

    _ = api.ServerLifeCycle
    _ = api.ServerLifeCycle.running
    _ = api.ServerLifeCycle.smart_running
    _ = api.ServerLifeCycle.stopped
    _ = api.ServerLifeCycle.deleted


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
