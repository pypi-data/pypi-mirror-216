# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11l_opy_ = 2048
bstack1ll1_opy_ = 7
def bstackl_opy_ (bstack1l1_opy_):
    global bstack1ll_opy_
    stringNr = ord (bstack1l1_opy_ [-1])
    bstack1l_opy_ = bstack1l1_opy_ [:-1]
    bstack11_opy_ = stringNr % len (bstack1l_opy_)
    bstack1lll_opy_ = bstack1l_opy_ [:bstack11_opy_] + bstack1l_opy_ [bstack11_opy_:]
    if bstack1_opy_:
        bstack1l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11l_opy_ - (bstack111_opy_ + stringNr) % bstack1ll1_opy_) for bstack111_opy_, char in enumerate (bstack1lll_opy_)])
    else:
        bstack1l1l_opy_ = str () .join ([chr (ord (char) - bstack11l_opy_ - (bstack111_opy_ + stringNr) % bstack1ll1_opy_) for bstack111_opy_, char in enumerate (bstack1lll_opy_)])
    return eval (bstack1l1l_opy_)
import atexit
import os
import signal
import sys
import time
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
from multiprocessing import Pool
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack111111l1_opy_ = {
	bstackl_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧࠁ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪࠂ"),
  bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪࠃ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫࠄ"),
  bstackl_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬࠅ"): bstackl_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࠆ"),
  bstackl_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫࠇ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬࠈ"),
  bstackl_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࠉ"): bstackl_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨࠊ"),
  bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࠋ"): bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨࠌ"),
  bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࠍ"): bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩࠎ"),
  bstackl_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࠏ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫࠐ"),
  bstackl_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬࠑ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨࠒ"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠓ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠔ"),
  bstackl_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠕ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠖ"),
  bstackl_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬࠗ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬ࠘"),
  bstackl_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ࠙"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠚ"),
  bstackl_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠛ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠜ"),
  bstackl_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠝ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠞ"),
  bstackl_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠟ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠠ"),
  bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࠡ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࠢ"),
  bstackl_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠣ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠤ"),
  bstackl_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠥ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠦ"),
  bstackl_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠧ"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠨ"),
  bstackl_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬࠩ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬࠪ"),
  bstackl_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠫ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠬ"),
  bstackl_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭࠭"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭࠮"),
  bstackl_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪ࠯"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪ࠰"),
  bstackl_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠱"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠲"),
  bstackl_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠳"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠴"),
  bstackl_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ࠵"): bstackl_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ࠶"),
  bstackl_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ࠷"): bstackl_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩ࠸"),
  bstackl_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ࠹"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࠺"),
  bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠻"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠼"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠽"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠾"),
  bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࠿"): bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ࡀ"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡁ"): bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡂ"),
  bstackl_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨࡃ"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨࡄ"),
  bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡅ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡆ"),
  bstackl_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡇ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡈ"),
}
bstack111lll1l_opy_ = [
  bstackl_opy_ (u"ࠧࡰࡵࠪࡉ"),
  bstackl_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࡊ"),
  bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࡋ"),
  bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࡌ"),
  bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨࡍ"),
  bstackl_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩࡎ"),
  bstackl_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࡏ"),
]
bstack1l1l11l1_opy_ = {
  bstackl_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩࡐ"): [bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩࡑ"), bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡎࡂࡏࡈࠫࡒ")],
  bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࡓ"): bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧࡔ"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨࡕ"): bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩࡖ"),
  bstackl_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬࡗ"): bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊ࠭ࡘ"),
  bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࡙ࠫ"): bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࡚ࠬ"),
  bstackl_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰ࡛ࠫ"): bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑ࡙࡟ࡑࡇࡕࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭࡜"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ࡝"): bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ࡞"),
  bstackl_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ࡟"): bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ࡠ"),
  bstackl_opy_ (u"ࠪࡥࡵࡶࠧࡡ"): bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧࡢ"),
  bstackl_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࡣ"): bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࡤࡊࡅࡃࡗࡊࠫࡤ"),
  bstackl_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫࡥ"): bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫࡦ")
}
bstack1l1llllll_opy_ = {
  bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࡧ"): [bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬࡨ"), bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࡩ")],
  bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࡪ"): [bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ࡫"), bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࡬")],
  bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡭"): bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡮"),
  bstackl_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࡯"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨࡰ"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡱ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡲ"),
  bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧࡳ"): [bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫࡴ"), bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࡵ")],
  bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࡶ"): bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩࡷ"),
  bstackl_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡸ"): bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡹ"),
  bstackl_opy_ (u"ࠧࡢࡲࡳࠫࡺ"): bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫࡻ"),
  bstackl_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡼ"): bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡽ"),
  bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡾ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡿ")
}
bstack111lll_opy_ = {
  bstackl_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢀ"): bstackl_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫࢁ"),
  bstackl_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢂ"): [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࢃ"), bstackl_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࢄ")],
  bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢅ"): bstackl_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢆ"),
  bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪࢇ"): bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ࢈"),
  bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ࢉ"): [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪࢊ"), bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩࢋ")],
  bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢌ"): bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢍ"),
  bstackl_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࢎ"): bstackl_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬ࢏"),
  bstackl_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࢐"): [bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࢑"), bstackl_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ࢒")],
  bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࢓"): [bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭࢔"), bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭࢕")]
}
bstack1lll1ll11_opy_ = [
  bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭࢖"),
  bstackl_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫࢗ"),
  bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ࢘"),
  bstackl_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶ࢙ࠪ"),
  bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࢚࠭"),
  bstackl_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻ࢛ࠪ"),
  bstackl_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ࢜"),
  bstackl_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ࢝"),
  bstackl_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭࢞"),
  bstackl_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ࢟"),
  bstackl_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢠ"),
  bstackl_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬࢡ"),
]
bstack1llll111l_opy_ = [
  bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢢ"),
  bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢣ"),
  bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢤ"),
  bstackl_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࢥ"),
  bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢦ"),
  bstackl_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢧ"),
  bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧࢨ"),
  bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩࢩ"),
  bstackl_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩࢪ"),
  bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬࢫ")
]
bstack11l11_opy_ = [
  bstackl_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ࢬ"),
  bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࢭ"),
  bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࢮ"),
  bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢯ"),
  bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫࢰ"),
  bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩࢱ"),
  bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩࢲ"),
  bstackl_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ࢳ"),
  bstackl_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࢴ"),
  bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࢵ"),
  bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢶ"),
  bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫࢷ"),
  bstackl_opy_ (u"࠭࡯ࡴࠩࢸ"),
  bstackl_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࢹ"),
  bstackl_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧࢺ"),
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫࢻ"),
  bstackl_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪࢼ"),
  bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ࢽ"),
  bstackl_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭ࢾ"),
  bstackl_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪࢿ"),
  bstackl_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬࣀ"),
  bstackl_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬࣁ"),
  bstackl_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨࣂ"),
  bstackl_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧࣃ"),
  bstackl_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬࣄ"),
  bstackl_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࣅ"),
  bstackl_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪࣆ"),
  bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨࣇ"),
  bstackl_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬࣈ"),
  bstackl_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭ࣉ"),
  bstackl_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬ࣊"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋"),
  bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬ࣌"),
  bstackl_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬ࣍"),
  bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࣎"),
  bstackl_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࣏"),
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࣐࠭"),
  bstackl_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪ࣑ࠫ"),
  bstackl_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵ࣒ࠪ"),
  bstackl_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴ࣓ࠩ"),
  bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨࣔ"),
  bstackl_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩࣕ"),
  bstackl_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧࣖ"),
  bstackl_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧࣗ"),
  bstackl_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨࣘ"),
  bstackl_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣙ"),
  bstackl_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪࣚ"),
  bstackl_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ࣛ"),
  bstackl_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫࣜ"),
  bstackl_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪࣝ"),
  bstackl_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪࣞ"),
  bstackl_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫࣟ"),
  bstackl_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬ࣠"),
  bstackl_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࣡"),
  bstackl_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫ࣢"),
  bstackl_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࣣࠧ"),
  bstackl_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪࣤ"),
  bstackl_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧࣥ"),
  bstackl_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨࣦ"),
  bstackl_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬࣧ"),
  bstackl_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬࣨ"),
  bstackl_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࣩࠧ"),
  bstackl_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧ࣪"),
  bstackl_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨ࣫"),
  bstackl_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨ࣬"),
  bstackl_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪ࣭ࠪ"),
  bstackl_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸ࣮ࠬ"),
  bstackl_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࣯"),
  bstackl_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࣰࠪ"),
  bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸࣱ࠭"),
  bstackl_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࣲࠫ"),
  bstackl_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ࣳ"),
  bstackl_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪࣴ"),
  bstackl_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬࣵ"),
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࣶࠬ"),
  bstackl_opy_ (u"࠭ࡩࡦࠩࣷ"),
  bstackl_opy_ (u"ࠧࡦࡦࡪࡩࠬࣸ"),
  bstackl_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨࣹ"),
  bstackl_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨࣺ"),
  bstackl_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬࣻ"),
  bstackl_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬࣼ"),
  bstackl_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫࣽ"),
  bstackl_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩࣾ"),
  bstackl_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪࣿ"),
  bstackl_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬऀ"),
  bstackl_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩँ"),
  bstackl_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪं"),
  bstackl_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ः"),
  bstackl_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ऄ"),
  bstackl_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩअ"),
  bstackl_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧआ"),
  bstackl_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩइ"),
  bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪई"),
  bstackl_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨउ"),
  bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ऊ"),
  bstackl_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩऋ"),
  bstackl_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬऌ"),
  bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫऍ"),
  bstackl_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫऎ"),
  bstackl_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ए"),
  bstackl_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨऐ"),
  bstackl_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ऑ"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ"),
  bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨओ"),
  bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭औ"),
  bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪक"),
  bstackl_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬख"),
  bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩग"),
  bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭घ"),
  bstackl_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨङ")
]
bstack1lll1l1l_opy_ = {
  bstackl_opy_ (u"࠭ࡶࠨच"): bstackl_opy_ (u"ࠧࡷࠩछ"),
  bstackl_opy_ (u"ࠨࡨࠪज"): bstackl_opy_ (u"ࠩࡩࠫझ"),
  bstackl_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩञ"): bstackl_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪट"),
  bstackl_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫठ"): bstackl_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬड"),
  bstackl_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫढ"): bstackl_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬण"),
  bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬत"): bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭थ"),
  bstackl_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧद"): bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨध"),
  bstackl_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩन"): bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऩ"),
  bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫप"): bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬफ"),
  bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫब"): bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬभ"),
  bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭म"): bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧय"),
  bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨर"): bstackl_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऱ"),
  bstackl_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫल"): bstackl_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬळ"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬऴ"): bstackl_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧव"),
  bstackl_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨश"): bstackl_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩष"),
  bstackl_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬस"): bstackl_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ह"),
  bstackl_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫऺ"): bstackl_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧऻ"),
  bstackl_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫़ࠧ"): bstackl_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩऽ"),
  bstackl_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪा"): bstackl_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫि"),
  bstackl_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪी"): bstackl_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫु"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू"): bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧृ"),
}
bstack1l111ll11_opy_ = bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧॄ")
bstack1lllllll1_opy_ = bstackl_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪॅ")
bstack1ll1ll11_opy_ = bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬॆ")
bstack1lll1111_opy_ = {
  bstackl_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫे"): 50,
  bstackl_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩै"): 40,
  bstackl_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬॉ"): 30,
  bstackl_opy_ (u"ࠬ࡯࡮ࡧࡱࠪॊ"): 20,
  bstackl_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬो"): 10
}
bstack1ll11111l_opy_ = bstack1lll1111_opy_[bstackl_opy_ (u"ࠧࡪࡰࡩࡳࠬौ")]
bstack11ll1ll1_opy_ = bstackl_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵्ࠧ")
bstack1l1l1ll1l_opy_ = bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧॎ")
bstack1l1111lll_opy_ = bstackl_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩॏ")
bstack1lllll1_opy_ = bstackl_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪॐ")
bstack11ll1ll11_opy_ = [bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭॑"), bstackl_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ॒࠭")]
bstack11l11lll_opy_ = [bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॓"), bstackl_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॔")]
bstack1lll11lll_opy_ = [
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪॕ"),
  bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬॖ"),
  bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨॗ"),
  bstackl_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩक़"),
  bstackl_opy_ (u"࠭ࡡࡱࡲࠪख़"),
  bstackl_opy_ (u"ࠧࡶࡦ࡬ࡨࠬग़"),
  bstackl_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪज़"),
  bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩड़"),
  bstackl_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨढ़"),
  bstackl_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩफ़"),
  bstackl_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭य़"), bstackl_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩॠ"),
  bstackl_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪॡ"),
  bstackl_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧॢ"),
  bstackl_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ॣ"),
  bstackl_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭।"),
  bstackl_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬ॥"),
  bstackl_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ०"), bstackl_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪ१"), bstackl_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ२"), bstackl_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩ३"), bstackl_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫ४"),
  bstackl_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨ५"),
  bstackl_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨ६"),
  bstackl_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧ७"), bstackl_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪ८"),
  bstackl_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬ९"),
  bstackl_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩ॰"),
  bstackl_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨॱ"),
  bstackl_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫॲ"),
  bstackl_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩॳ"),
  bstackl_opy_ (u"ࠬࡧࡶࡥࠩॴ"), bstackl_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩॵ"), bstackl_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩॶ"), bstackl_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩॷ"),
  bstackl_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧॸ"), bstackl_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩॹ"), bstackl_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧॺ"),
  bstackl_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧॻ"), bstackl_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫॼ"),
  bstackl_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩॽ"), bstackl_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫॾ"), bstackl_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧॿ"), bstackl_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬঀ"), bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨঁ"),
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨং"), bstackl_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪঃ"),
  bstackl_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩ঄"),
  bstackl_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭অ"),
  bstackl_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨআ"), bstackl_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫই"), bstackl_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩঈ"), bstackl_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨউ"),
  bstackl_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫঊ"),
  bstackl_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩঋ"), bstackl_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨঌ"),
  bstackl_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩ঍"),
  bstackl_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬ঎"),
  bstackl_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭এ"),
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঐ"),
  bstackl_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧ঑"),
  bstackl_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭঒"),
  bstackl_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩও"),
  bstackl_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨঔ"),
  bstackl_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧক"),
  bstackl_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨখ"),
  bstackl_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭গ"),
  bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬঘ"),
  bstackl_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫঙ"),
  bstackl_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨচ"),
  bstackl_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧছ"),
  bstackl_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧজ"),
  bstackl_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫঝ"),
  bstackl_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩঞ"), bstackl_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪট"), bstackl_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪঠ"),
  bstackl_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬড"),
  bstackl_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ঢ"),
  bstackl_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬণ"),
  bstackl_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭ত"),
  bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩথ"),
  bstackl_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪদ"),
  bstackl_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪধ"), bstackl_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧন"), bstackl_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬ঩"),
  bstackl_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪপ"),
  bstackl_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬফ"),
  bstackl_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧব"),
  bstackl_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ভ"),
  bstackl_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪম"), bstackl_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧয"),
  bstackl_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬর"), bstackl_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧ঱"),
  bstackl_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫল"),
  bstackl_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫ঳"),
  bstackl_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩ঴"), bstackl_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫ঵"), bstackl_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬশ"), bstackl_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩষ"),
  bstackl_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪস"),
  bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬহ"),
  bstackl_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ঺"),
  bstackl_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭঻"),
  bstackl_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪ়ࠫ"),
  bstackl_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪঽ"),
  bstackl_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪা"), bstackl_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫি"),
  bstackl_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧী"),
  bstackl_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬু"),
  bstackl_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧূ"),
  bstackl_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৃ"),
  bstackl_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪৄ"),
  bstackl_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬ৅"),
  bstackl_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫ৆"),
  bstackl_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬে"),
  bstackl_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬৈ"),
  bstackl_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫ৉"),
  bstackl_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬ৊"),
  bstackl_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧো"),
  bstackl_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨৌ"),
  bstackl_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩ্ࠬ"),
  bstackl_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭ৎ"),
  bstackl_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨ৏"),
  bstackl_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧ৐"),
  bstackl_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨ৑"),
  bstackl_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬ৒"),
  bstackl_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨ৓"),
  bstackl_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭৔"),
  bstackl_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ৕"), bstackl_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬ৖"),
  bstackl_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪৗ"), bstackl_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨ৘"),
  bstackl_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭৙"),
  bstackl_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬ৚"),
  bstackl_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬ৛"),
  bstackl_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨড়"), bstackl_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨঢ়"),
  bstackl_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ৞"),
  bstackl_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬয়"),
  bstackl_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨৠ"),
  bstackl_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪৡ"),
  bstackl_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬৢ"),
  bstackl_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧৣ"),
  bstackl_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪ৤"),
  bstackl_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬ৥"),
  bstackl_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩ০"),
  bstackl_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧ১"), bstackl_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭২"),
  bstackl_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪ৩")
]
bstack1llll1111_opy_ = bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ৪")
bstack1l111l1l_opy_ = [bstackl_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ৫"), bstackl_opy_ (u"࠭࠮ࡢࡣࡥࠫ৬"), bstackl_opy_ (u"ࠧ࠯࡫ࡳࡥࠬ৭")]
bstack1111lll_opy_ = [bstackl_opy_ (u"ࠨ࡫ࡧࠫ৮"), bstackl_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৯"), bstackl_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ৰ"), bstackl_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪৱ")]
bstack11l11111_opy_ = {
  bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ৲"): bstackl_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৳"),
  bstackl_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ৴"): bstackl_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭৵"),
  bstackl_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৶"): bstackl_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৷"),
  bstackl_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৸"): bstackl_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৹"),
  bstackl_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭৺"): bstackl_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ৻")
}
bstack111l1ll_opy_ = [
  bstackl_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ৼ"),
  bstackl_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ৽"),
  bstackl_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৾"),
  bstackl_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ৿"),
  bstackl_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭਀"),
]
bstack1ll11lll_opy_ = bstack1llll111l_opy_ + bstack11l11_opy_ + bstack1lll11lll_opy_
bstack1l1ll1ll1_opy_ = [
  bstackl_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫਁ"),
  bstackl_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨਂ"),
  bstackl_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧਃ"),
  bstackl_opy_ (u"ࠩࡡ࠵࠵࠴ࠧ਄"),
  bstackl_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩਅ"),
  bstackl_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪਆ"),
  bstackl_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫਇ"),
  bstackl_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩਈ")
]
bstack1l1llll11_opy_ = bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀࠫਉ")
bstack11l11ll_opy_ = bstackl_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧਊ")
bstack11ll1_opy_ = [ bstackl_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ਋") ]
bstack11lll1_opy_ = [ bstackl_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ਌") ]
bstack11l1ll1l_opy_ = [ bstackl_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ਍") ]
bstack1ll1llll1_opy_ = bstackl_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧ਎")
bstack11lll1ll_opy_ = bstackl_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩਏ")
bstack1lll1lll1_opy_ = bstackl_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫਐ")
bstack1ll1l111l_opy_ = bstackl_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ਑")
bstack11llll1ll_opy_ = [
  bstackl_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭਒"),
  bstackl_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪਓ"),
  bstackl_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬਔ"),
  bstackl_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫਕ"),
  bstackl_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪਖ"),
  bstackl_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨਗ"),
  bstackl_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨਘ"),
  bstackl_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫਙ"),
  bstackl_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬਚ"),
  bstackl_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਛ"),
  bstackl_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ਜ"),
  bstackl_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬਝ"),
  bstackl_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪਞ"),
  bstackl_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩਟ"),
  bstackl_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ਠ"),
  bstackl_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪਡ"),
  bstackl_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧਢ"),
  bstackl_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਣ"),
  bstackl_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧਤ"),
  bstackl_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ਥ"),
  bstackl_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧਦ"),
]
def bstack11l11l1l_opy_():
  global CONFIG
  headers = {
        bstackl_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨਧ"): bstackl_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ਨ"),
      }
  proxy = bstack1llll11ll_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ਩")) or CONFIG.get(bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩਪ")):
    proxies = {
      bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬਫ"): proxy
    }
  try:
    response = requests.get(bstack1ll1ll11_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l111l11l_opy_ = response.json()[bstackl_opy_ (u"ࠧࡩࡷࡥࡷࠬਬ")]
      logger.debug(bstack1ll11ll1l_opy_.format(response.json()))
      return bstack1l111l11l_opy_
    else:
      logger.debug(bstack1l1l1llll_opy_.format(bstackl_opy_ (u"ࠣࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡎࡘࡕࡎࠡࡲࡤࡶࡸ࡫ࠠࡦࡴࡵࡳࡷࠦࠢਭ")))
  except Exception as e:
    logger.debug(bstack1l1l1llll_opy_.format(e))
def bstack1111ll11_opy_(hub_url):
  global CONFIG
  url = bstackl_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦਮ")+  hub_url + bstackl_opy_ (u"ࠥ࠳ࡨ࡮ࡥࡤ࡭ࠥਯ")
  headers = {
        bstackl_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪਰ"): bstackl_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ਱"),
      }
  proxy = bstack1llll11ll_opy_(CONFIG)
  proxies = {}
  if CONFIG.get(bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩਲ")) or CONFIG.get(bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫਲ਼")):
    proxies = {
      bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ਴"): proxy
    }
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11ll11l11_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll111l11_opy_.format(hub_url, e))
def bstack11l1l1ll_opy_():
  try:
    global bstack1l1111_opy_
    bstack1l111l11l_opy_ = bstack11l11l1l_opy_()
    with Pool() as pool:
      results = pool.map(bstack1111ll11_opy_, bstack1l111l11l_opy_)
    bstack1lll1l1ll_opy_ = {}
    for item in results:
      hub_url = item[bstackl_opy_ (u"ࠩ࡫ࡹࡧࡥࡵࡳ࡮ࠪਵ")]
      latency = item[bstackl_opy_ (u"ࠪࡰࡦࡺࡥ࡯ࡥࡼࠫਸ਼")]
      bstack1lll1l1ll_opy_[hub_url] = latency
    bstack1ll1ll1_opy_ = min(bstack1lll1l1ll_opy_, key= lambda x: bstack1lll1l1ll_opy_[x])
    bstack1l1111_opy_ = bstack1ll1ll1_opy_
    logger.debug(bstack1llllll1l_opy_.format(bstack1ll1ll1_opy_))
  except Exception as e:
    logger.debug(bstack11lll1l_opy_.format(e))
bstack1l111ll1l_opy_ = bstackl_opy_ (u"ࠫࡘ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠰ࠥࡻࡳࡪࡰࡪࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠺ࠡࡽࢀࠫ਷")
bstack1l1l11l1l_opy_ = bstackl_opy_ (u"ࠬࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡵࡨࡸࡺࡶࠡࠨਸ")
bstack111l1l11_opy_ = bstackl_opy_ (u"࠭ࡐࡢࡴࡶࡩࡩࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠨਹ")
bstack1ll1ll1l_opy_ = bstackl_opy_ (u"ࠧࡔࡣࡱ࡭ࡹ࡯ࡺࡦࡦࠣࡧࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠬ਺")
bstack1l11l11_opy_ = bstackl_opy_ (u"ࠨࡗࡶ࡭ࡳ࡭ࠠࡩࡷࡥࠤࡺࡸ࡬࠻ࠢࡾࢁࠬ਻")
bstack1l1ll1_opy_ = bstackl_opy_ (u"ࠩࡖࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࡻࡾ਼ࠩ")
bstack11ll1l1ll_opy_ = bstackl_opy_ (u"ࠪࡖࡪࡩࡥࡪࡸࡨࡨࠥ࡯࡮ࡵࡧࡵࡶࡺࡶࡴ࠭ࠢࡨࡼ࡮ࡺࡩ࡯ࡩࠪ਽")
bstack1l1ll_opy_ = bstackl_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡡࠩਾ")
bstack11lll1l1_opy_ = bstackl_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡡ࡯ࡦࠣࡴࡾࡺࡥࡴࡶ࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡢࠪਿ")
bstack1111111_opy_ = bstackl_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡳࡱࡥࡳࡹ࠲ࠠࡱࡣࡥࡳࡹࠦࡡ࡯ࡦࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࡱ࡯ࡢࡳࡣࡵࡽࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹࠠࡵࡱࠣࡶࡺࡴࠠࡳࡱࡥࡳࡹࠦࡴࡦࡵࡷࡷࠥ࡯࡮ࠡࡲࡤࡶࡦࡲ࡬ࡦ࡮࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠲ࡶࡡࡣࡱࡷࠤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡬ࡪࡤࡵࡥࡷࡿࡠࠨੀ")
bstack1l1ll111_opy_ = bstackl_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡤࡨ࡬ࡦࡼࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡣࡧ࡫ࡥࡻ࡫ࡠࠨੁ")
bstack1ll11l11_opy_ = bstackl_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡤࡴࡵ࡯ࡵ࡮࠯ࡦࡰ࡮࡫࡮ࡵࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡃࡳࡴ࡮ࡻ࡭࠮ࡒࡼࡸ࡭ࡵ࡮࠮ࡅ࡯࡭ࡪࡴࡴࡡࠩੂ")
bstack1l1l1ll11_opy_ = bstackl_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡣࠫ੃")
bstack1lll111_opy_ = bstackl_opy_ (u"ࠪࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡦࡪࡰࡧࠤࡪ࡯ࡴࡩࡧࡵࠤࡘ࡫࡬ࡦࡰ࡬ࡹࡲࠦ࡯ࡳࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡶࡤࡰࡱࠦࡴࡩࡧࠣࡶࡪࡲࡥࡷࡣࡱࡸࠥࡶࡡࡤ࡭ࡤ࡫ࡪࡹࠠࡶࡵ࡬ࡲ࡬ࠦࡰࡪࡲࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠪ੄")
bstack11ll1l11l_opy_ = bstackl_opy_ (u"ࠫࡍࡧ࡮ࡥ࡮࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤ࡮ࡲࡷࡪ࠭੅")
bstack11lll1ll1_opy_ = bstackl_opy_ (u"ࠬࡇ࡬࡭ࠢࡧࡳࡳ࡫ࠡࠨ੆")
bstack1lllll11_opy_ = bstackl_opy_ (u"࠭ࡃࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࠥࡧࡴࠡࡣࡱࡽࠥࡶࡡࡳࡧࡱࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡱࡩࠤࠧࢁࡽࠣ࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡩ࡬ࡶࡦࡨࠤࡦࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭࠱ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡤࡱࡱࠦࡦࡪ࡮ࡨࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨࡲࡶࠥࡺࡥࡴࡶࡶ࠲ࠬੇ")
bstack1llll1l_opy_ = bstackl_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤࡳࡵࡴࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡦࡪࡤࠡࡶ࡫ࡩࡲࠦࡩ࡯ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧࠣࡥࡸࠦࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤࠣࡥࡳࡪࠠࠣࡣࡦࡧࡪࡹࡳࡌࡧࡼࠦࠥࡵࡲࠡࡵࡨࡸࠥࡺࡨࡦ࡯ࠣࡥࡸࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࡹ࠺ࠡࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠥࠤࡦࡴࡤࠡࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠧ࠭ੈ")
bstack1lll1_opy_ = bstackl_opy_ (u"ࠨࡏࡤࡰ࡫ࡵࡲ࡮ࡧࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠼ࠥࡿࢂࠨࠧ੉")
bstack1ll111ll1_opy_ = bstackl_opy_ (u"ࠩࡈࡲࡨࡵࡵ࡯ࡶࡨࡶࡪࡪࠠࡦࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡱࠢ࠰ࠤࢀࢃࠧ੊")
bstack11ll1llll_opy_ = bstackl_opy_ (u"ࠪࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡑࡵࡣࡢ࡮ࠪੋ")
bstack111ll1ll_opy_ = bstackl_opy_ (u"ࠫࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯ࠫੌ")
bstack11l1l11_opy_ = bstackl_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡑࡵࡣࡢ࡮ࠣ࡭ࡸࠦ࡮ࡰࡹࠣࡶࡺࡴ࡮ࡪࡰࡪ੍ࠥࠬ")
bstack1lll11ll_opy_ = bstackl_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡶࡸࡦࡸࡴࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱࡀࠠࡼࡿࠪ੎")
bstack1l111111_opy_ = bstackl_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡯࡮ࡨࠢ࡯ࡳࡨࡧ࡬ࠡࡤ࡬ࡲࡦࡸࡹࠡࡹ࡬ࡸ࡭ࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࡽࢀࠫ੏")
bstack11ll1l_opy_ = bstackl_opy_ (u"ࠨࡗࡳࡨࡦࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠩ੐")
bstack1lll111l_opy_ = bstackl_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠨੑ")
bstack1lll11l1l_opy_ = bstackl_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣࡴࡷࡵࡶࡪࡦࡨࠤࡦࡴࠠࡢࡲࡳࡶࡴࡶࡲࡪࡣࡷࡩࠥࡌࡗࠡࠪࡵࡳࡧࡵࡴ࠰ࡲࡤࡦࡴࡺࠩࠡ࡫ࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠮ࠣࡷࡰ࡯ࡰࠡࡶ࡫ࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡭ࡨࡽࠥ࡯࡮ࠡࡥࡲࡲ࡫࡯ࡧࠡ࡫ࡩࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡹࡩ࡮ࡲ࡯ࡩࠥࡶࡹࡵࡪࡲࡲࠥࡹࡣࡳ࡫ࡳࡸࠥࡽࡩࡵࡪࡲࡹࡹࠦࡡ࡯ࡻࠣࡊ࡜࠴ࠧ੒")
bstack1l11l1l11_opy_ = bstackl_opy_ (u"ࠫࡘ࡫ࡴࡵ࡫ࡱ࡫ࠥ࡮ࡴࡵࡲࡓࡶࡴࡾࡹ࠰ࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡱࡱࠤࡨࡻࡲࡳࡧࡱࡸࡱࡿࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠣࡺࡪࡸࡳࡪࡱࡱࠤࡴ࡬ࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࠫࡿࢂ࠯ࠬࠡࡲ࡯ࡩࡦࡹࡥࠡࡷࡳ࡫ࡷࡧࡤࡦࠢࡷࡳ࡙ࠥࡥ࡭ࡧࡱ࡭ࡺࡳ࠾࠾࠶࠱࠴࠳࠶ࠠࡰࡴࠣࡶࡪ࡬ࡥࡳࠢࡷࡳࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠰ࡴࡸࡲ࠲ࡺࡥࡴࡶࡶ࠱ࡧ࡫ࡨࡪࡰࡧ࠱ࡵࡸ࡯ࡹࡻࠦࡴࡾࡺࡨࡰࡰࠣࡪࡴࡸࠠࡢࠢࡺࡳࡷࡱࡡࡳࡱࡸࡲࡩ࠴ࠧ੓")
bstack1l1l11111_opy_ = bstackl_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡻࡰࡰࠥ࡬ࡩ࡭ࡧ࠱࠲ࠬ੔")
bstack1l111_opy_ = bstackl_opy_ (u"࠭ࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡶ࡫ࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠤࠫ੕")
bstack111l1l1l_opy_ = bstackl_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪ࠴ࠠࡼࡿࠪ੖")
bstack1l1ll111l_opy_ = bstackl_opy_ (u"ࠨࡇࡻࡴࡪࡩࡴࡦࡦࠣࡥࡹࠦ࡬ࡦࡣࡶࡸࠥ࠷ࠠࡪࡰࡳࡹࡹ࠲ࠠࡳࡧࡦࡩ࡮ࡼࡥࡥࠢ࠳ࠫ੗")
bstack1l111l1l1_opy_ = bstackl_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡦࡸࡶ࡮ࡴࡧࠡࡃࡳࡴࠥࡻࡰ࡭ࡱࡤࡨ࠳ࠦࡻࡾࠩ੘")
bstack11lll11_opy_ = bstackl_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱ࡮ࡲࡥࡩࠦࡁࡱࡲ࠱ࠤࡎࡴࡶࡢ࡮࡬ࡨࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡿࢂ࠴ࠧਖ਼")
bstack111l1l1_opy_ = bstackl_opy_ (u"ࠫࡐ࡫ࡹࡴࠢࡦࡥࡳࡴ࡯ࡵࠢࡦࡳ࠲࡫ࡸࡪࡵࡷࠤࡦࡹࠠࡢࡲࡳࠤࡻࡧ࡬ࡶࡧࡶ࠰ࠥࡻࡳࡦࠢࡤࡲࡾࠦ࡯࡯ࡧࠣࡴࡷࡵࡰࡦࡴࡷࡽࠥ࡬ࡲࡰ࡯ࠣࡿ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡳࡥࡹ࡮࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡴࡪࡤࡶࡪࡧࡢ࡭ࡧࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࡽ࠭ࠢࡲࡲࡱࡿࠠࠣࡲࡤࡸ࡭ࠨࠠࡢࡰࡧࠤࠧࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠣࠢࡦࡥࡳࠦࡣࡰ࠯ࡨࡼ࡮ࡹࡴࠡࡶࡲ࡫ࡪࡺࡨࡦࡴ࠱ࠫਗ਼")
bstack11ll11l1_opy_ = bstackl_opy_ (u"ࠬࡡࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡢࡲࡳࠤࡵࡸ࡯ࡱࡧࡵࡸࡾࡣࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠠࡢࡴࡨࠤࢀ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡴࡦࡺࡨ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡵ࡫ࡥࡷ࡫ࡡࡣ࡮ࡨࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾ࡾ࠰ࠣࡊࡴࡸࠠ࡮ࡱࡵࡩࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡰ࡭ࡧࡤࡷࡪࠦࡶࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵࡶࡩࡶ࡯࠲ࡷࡪࡺ࠭ࡶࡲ࠰ࡸࡪࡹࡴࡴ࠱ࡶࡴࡪࡩࡩࡧࡻ࠰ࡥࡵࡶࠧਜ਼")
bstack111ll1_opy_ = bstackl_opy_ (u"࡛࠭ࡊࡰࡹࡥࡱ࡯ࡤࠡࡣࡳࡴࠥࡶࡲࡰࡲࡨࡶࡹࡿ࡝ࠡࡕࡸࡴࡵࡵࡲࡵࡧࡧࠤࡻࡧ࡬ࡶࡧࡶࠤࡴ࡬ࠠࡢࡲࡳࠤࡦࡸࡥࠡࡱࡩࠤࢀ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡴࡦࡺࡨ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡵ࡫ࡥࡷ࡫ࡡࡣ࡮ࡨࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾ࡾ࠰ࠣࡊࡴࡸࠠ࡮ࡱࡵࡩࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡰ࡭ࡧࡤࡷࡪࠦࡶࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵࡶࡩࡶ࡯࠲ࡷࡪࡺ࠭ࡶࡲ࠰ࡸࡪࡹࡴࡴ࠱ࡶࡴࡪࡩࡩࡧࡻ࠰ࡥࡵࡶࠧੜ")
bstack11111ll1_opy_ = bstackl_opy_ (u"ࠧࡖࡵ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡣࡳࡴࠥ࡯ࡤࠡࡽࢀࠤ࡫ࡵࡲࠡࡪࡤࡷ࡭ࠦ࠺ࠡࡽࢀ࠲ࠬ੝")
bstack11l1llll_opy_ = bstackl_opy_ (u"ࠨࡃࡳࡴ࡛ࠥࡰ࡭ࡱࡤࡨࡪࡪࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾ࠴ࠠࡊࡆࠣ࠾ࠥࢁࡽࠨਫ਼")
bstack1l1l1lll1_opy_ = bstackl_opy_ (u"ࠩࡘࡷ࡮ࡴࡧࠡࡃࡳࡴࠥࡀࠠࡼࡿ࠱ࠫ੟")
bstack1l11ll11_opy_ = bstackl_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡰࡴࠣࡺࡦࡴࡩ࡭࡮ࡤࠤࡵࡿࡴࡩࡱࡱࠤࡹ࡫ࡳࡵࡵ࠯ࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡽࡩࡵࡪࠣࡴࡦࡸࡡ࡭࡮ࡨࡰࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡀࠤ࠶࠭੠")
bstack11111l_opy_ = bstackl_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࠽ࠤࢀࢃࠧ੡")
bstack1l1l1l1_opy_ = bstackl_opy_ (u"ࠬࡉ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡥ࡯ࡳࡸ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲ࠻ࠢࡾࢁࠬ੢")
bstack1ll1l1ll1_opy_ = bstackl_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡪࡩࡹࠦࡲࡦࡣࡶࡳࡳࠦࡦࡰࡴࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡪࡧࡴࡶࡴࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩ࠳ࠦࡻࡾࠩ੣")
bstack11ll1ll1l_opy_ = bstackl_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡨࡵࡳࡲࠦࡡࡱ࡫ࠣࡧࡦࡲ࡬࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ੤")
bstack1ll1111ll_opy_ = bstackl_opy_ (u"ࠨࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡮࡯ࡸࠢࡥࡹ࡮ࡲࡤࠡࡗࡕࡐ࠱ࠦࡡࡴࠢࡥࡹ࡮ࡲࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠥ࡯ࡳࠡࡰࡲࡸࠥࡻࡳࡦࡦ࠱ࠫ੥")
bstack1ll1l1_opy_ = bstackl_opy_ (u"ࠩࡖࡩࡷࡼࡥࡳࠢࡶ࡭ࡩ࡫ࠠࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠫࡿࢂ࠯ࠠࡪࡵࠣࡲࡴࡺࠠࡴࡣࡰࡩࠥࡧࡳࠡࡥ࡯࡭ࡪࡴࡴࠡࡵ࡬ࡨࡪࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠪࡾࢁ࠮࠭੦")
bstack1ll1l11l1_opy_ = bstackl_opy_ (u"࡚ࠪ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡰࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡧࡥࡸ࡮ࡢࡰࡣࡵࡨ࠿ࠦࡻࡾࠩ੧")
bstack11l1lll_opy_ = bstackl_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡢࡥࡦࡩࡸࡹࠠࡢࠢࡳࡶ࡮ࡼࡡࡵࡧࠣࡨࡴࡳࡡࡪࡰ࠽ࠤࢀࢃࠠ࠯ࠢࡖࡩࡹࠦࡴࡩࡧࠣࡪࡴࡲ࡬ࡰࡹ࡬ࡲ࡬ࠦࡣࡰࡰࡩ࡭࡬ࠦࡩ࡯ࠢࡼࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥ࠻ࠢ࡟ࡲ࠲࠳࠭࠮࠯࠰࠱࠲࠳࠭࠮ࠢ࡟ࡲࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭࠼ࠣࡸࡷࡻࡥࠡ࡞ࡱ࠱࠲࠳࠭࠮࠯࠰࠱࠲࠳࠭ࠨ੨")
bstack11lllll1_opy_ = bstackl_opy_ (u"࡙ࠬ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࡡࡨࡶࡷࡵࡲࠡ࠼ࠣࡿࢂ࠭੩")
bstack1l1111l_opy_ = bstackl_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡲࡩࡥࡡ࡮ࡲ࡯࡭ࡹࡻࡤࡦࡡࡨࡺࡪࡴࡴࠡࡨࡲࡶ࡙ࠥࡄࡌࡕࡨࡸࡺࡶࠠࡼࡿࠥ੪")
bstack11ll11lll_opy_ = bstackl_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡳࡪ࡟ࡢ࡯ࡳࡰ࡮ࡺࡵࡥࡧࡢࡩࡻ࡫࡮ࡵࠢࡩࡳࡷࠦࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠢࡾࢁࠧ੫")
bstack1ll11_opy_ = bstackl_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠࡣࡰࡴࡱ࡯ࡴࡶࡦࡨࡣࡪࡼࡥ࡯ࡶࠣࡪࡴࡸࠠࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠤࢀࢃࠢ੬")
bstack11l1l1l_opy_ = bstackl_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡫࡯ࡲࡦࡡࡵࡩࡶࡻࡥࡴࡶࠣࡿࢂࠨ੭")
bstack111ll111_opy_ = bstackl_opy_ (u"ࠥࡔࡔ࡙ࡔࠡࡇࡹࡩࡳࡺࠠࡼࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࠥࡀࠠࡼࡿࠥ੮")
bstack1lll1ll_opy_ = bstackl_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࠣࡴࡷࡵࡸࡺࠢࡶࡩࡹࡺࡩ࡯ࡩࡶ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ੯")
bstack1ll11ll1l_opy_ = bstackl_opy_ (u"ࠬࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥ࠵࡮ࡦࡺࡷࡣ࡭ࡻࡢࡴࠢࡾࢁࠬੰ")
bstack1l1l1llll_opy_ = bstackl_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢ࠲ࡲࡪࡾࡴࡠࡪࡸࡦࡸࡀࠠࡼࡿࠪੱ")
bstack1llllll1l_opy_ = bstackl_opy_ (u"ࠧࡏࡧࡤࡶࡪࡹࡴࠡࡪࡸࡦࠥࡧ࡬࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡶ࠾ࠥࢁࡽࠨੲ")
bstack11lll1l_opy_ = bstackl_opy_ (u"ࠨࡇࡕࡖࡔࡘࠠࡊࡐࠣࡅࡑࡒࡏࡄࡃࡗࡉࠥࡎࡕࡃࠢࡾࢁࠬੳ")
bstack11ll11l11_opy_ = bstackl_opy_ (u"ࠩࡏࡥࡹ࡫࡮ࡤࡻࠣࡳ࡫ࠦࡨࡶࡤ࠽ࠤࢀࢃࠠࡪࡵ࠽ࠤࢀࢃࠧੴ")
bstack1ll111l11_opy_ = bstackl_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦ࡬ࡢࡶࡨࡲࡨࡿࠠࡧࡱࡵࠤࢀࢃࠠࡩࡷࡥ࠾ࠥࢁࡽࠨੵ")
bstack1llll1l11_opy_ = bstackl_opy_ (u"ࠫࡍࡻࡢࠡࡷࡵࡰࠥࡩࡨࡢࡰࡪࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦ࡯ࡱࡶ࡬ࡱࡦࡲࠠࡩࡷࡥ࠾ࠥࢁࡽࠨ੶")
bstack1lll1111l_opy_ = bstackl_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡹ࡮ࡥࠡࡱࡳࡸ࡮ࡳࡡ࡭ࠢ࡫ࡹࡧࠦࡵࡳ࡮࠽ࠤࢀࢃࠧ੷")
bstack11ll11ll_opy_ = bstackl_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭੸")
bstack1l1l1111_opy_ = bstackl_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭੹")
from ._version import __version__
bstack11ll1lll1_opy_ = None
CONFIG = {}
bstack11l11ll1_opy_ = {}
bstack1ll11l1l1_opy_ = {}
bstack1lllll111_opy_ = None
bstack1ll1l1l_opy_ = None
bstack1l1l11_opy_ = None
bstack1lll111l1_opy_ = -1
bstack1111l11_opy_ = bstack1ll11111l_opy_
bstack1lll11l11_opy_ = 1
bstack11ll1l111_opy_ = False
bstack1ll1l1111_opy_ = bstackl_opy_ (u"ࠨࠩ੺")
bstack11111l11_opy_ = bstackl_opy_ (u"ࠩࠪ੻")
bstack11l111_opy_ = False
bstack11l1lllll_opy_ = True
bstack1l11l1l_opy_ = bstackl_opy_ (u"ࠪࠫ੼")
bstack1ll1111_opy_ = []
bstack1l1111_opy_ = bstackl_opy_ (u"ࠫࠬ੽")
bstack1l11lll11_opy_ = False
bstack1l11111l_opy_ = None
bstack1l1l111ll_opy_ = -1
bstack1l1lll1l_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠬࢄࠧ੾")), bstackl_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭੿"), bstackl_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ઀"))
bstack11ll_opy_ = False
bstack11ll11ll1_opy_ = None
bstack1l11ll11l_opy_ = None
bstack111l111_opy_ = None
bstack11111ll_opy_ = None
bstack1ll1lll11_opy_ = None
bstack1lll1l1_opy_ = None
bstack111ll11l_opy_ = None
bstack111ll1l_opy_ = None
bstack1llllll1_opy_ = None
bstack1l1l1l11_opy_ = None
bstack1l11111l1_opy_ = None
bstack111l1lll_opy_ = None
bstack1ll1lllll_opy_ = None
bstack111llll1_opy_ = None
bstack11lll11l1_opy_ = None
bstack1l11llll_opy_ = bstackl_opy_ (u"ࠣࠤઁ")
class bstack1l11ll1ll_opy_(threading.Thread):
  def run(self):
    self.exc = None
    try:
      self.ret = self._target(*self._args, **self._kwargs)
    except Exception as e:
      self.exc = e
  def join(self, timeout=None):
    super(bstack1l11ll1ll_opy_, self).join(timeout)
    if self.exc:
      raise self.exc
    return self.ret
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1111l11_opy_,
                    format=bstackl_opy_ (u"ࠩ࡟ࡲࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧં"),
                    datefmt=bstackl_opy_ (u"ࠪࠩࡍࡀࠥࡎ࠼ࠨࡗࠬઃ"))
def bstack11l1ll1_opy_():
  global CONFIG
  global bstack1111l11_opy_
  if bstackl_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭઄") in CONFIG:
    bstack1111l11_opy_ = bstack1lll1111_opy_[CONFIG[bstackl_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧઅ")]]
    logging.getLogger().setLevel(bstack1111l11_opy_)
def bstack1ll1111l1_opy_():
  global CONFIG
  global bstack11ll_opy_
  bstack1lll1l11_opy_ = bstack1ll11l11l_opy_(CONFIG)
  if(bstackl_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨઆ") in bstack1lll1l11_opy_ and str(bstack1lll1l11_opy_[bstackl_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩઇ")]).lower() == bstackl_opy_ (u"ࠨࡶࡵࡹࡪ࠭ઈ")):
    bstack11ll_opy_ = True
def bstack11ll111ll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l11111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1l11l_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstackl_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡦࡳࡳ࡬ࡩࡨࡨ࡬ࡰࡪࠨઉ") == args[i].lower() or bstackl_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡧ࡫ࡪࠦઊ") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l11l1l_opy_
      bstack1l11l1l_opy_ += bstackl_opy_ (u"ࠫ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡈࡵ࡮ࡧ࡫ࡪࡊ࡮ࡲࡥࠡࠩઋ") + path
      return path
  return None
def bstack111lll1_opy_():
  bstack1l1lllll_opy_ = bstack1l1l11l_opy_()
  if bstack1l1lllll_opy_ and os.path.exists(os.path.abspath(bstack1l1lllll_opy_)):
    fileName = bstack1l1lllll_opy_
  if bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆࠩઌ") in os.environ and os.path.exists(os.path.abspath(os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪઍ")])) and not bstackl_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩ઎") in locals():
    fileName = os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬએ")]
  if bstackl_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫઐ") in locals():
    bstack1ll1l11ll_opy_ = os.path.abspath(fileName)
  else:
    bstack1ll1l11ll_opy_ = bstackl_opy_ (u"ࠪࠫઑ")
  bstack1ll111l1_opy_ = os.getcwd()
  bstack1ll1ll1l1_opy_ = bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧ઒")
  bstack1l1ll11ll_opy_ = bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡧ࡭࡭ࠩઓ")
  while (not os.path.exists(bstack1ll1l11ll_opy_)) and bstack1ll111l1_opy_ != bstackl_opy_ (u"ࠨࠢઔ"):
    bstack1ll1l11ll_opy_ = os.path.join(bstack1ll111l1_opy_, bstack1ll1ll1l1_opy_)
    if not os.path.exists(bstack1ll1l11ll_opy_):
      bstack1ll1l11ll_opy_ = os.path.join(bstack1ll111l1_opy_, bstack1l1ll11ll_opy_)
    if bstack1ll111l1_opy_ != os.path.dirname(bstack1ll111l1_opy_):
      bstack1ll111l1_opy_ = os.path.dirname(bstack1ll111l1_opy_)
    else:
      bstack1ll111l1_opy_ = bstackl_opy_ (u"ࠢࠣક")
  if not os.path.exists(bstack1ll1l11ll_opy_):
    bstack1l1l11ll1_opy_(
      bstack1lllll11_opy_.format(os.getcwd()))
  with open(bstack1ll1l11ll_opy_, bstackl_opy_ (u"ࠨࡴࠪખ")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack1l1l11ll1_opy_(bstack1lll1_opy_.format(str(exc)))
def bstack111l111l_opy_(config):
  bstack1l11l1111_opy_ = bstack1l111ll1_opy_(config)
  for option in list(bstack1l11l1111_opy_):
    if option.lower() in bstack1lll1l1l_opy_ and option != bstack1lll1l1l_opy_[option.lower()]:
      bstack1l11l1111_opy_[bstack1lll1l1l_opy_[option.lower()]] = bstack1l11l1111_opy_[option]
      del bstack1l11l1111_opy_[option]
  return config
def bstack11ll1ll_opy_():
  global bstack1ll11l1l1_opy_
  for key, bstack11l1l1l1_opy_ in bstack1l1l11l1_opy_.items():
    if isinstance(bstack11l1l1l1_opy_, list):
      for var in bstack11l1l1l1_opy_:
        if var in os.environ:
          bstack1ll11l1l1_opy_[key] = os.environ[var]
          break
    elif bstack11l1l1l1_opy_ in os.environ:
      bstack1ll11l1l1_opy_[key] = os.environ[bstack11l1l1l1_opy_]
  if bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫગ") in os.environ:
    bstack1ll11l1l1_opy_[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧઘ")] = {}
    bstack1ll11l1l1_opy_[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨઙ")][bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧચ")] = os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨછ")]
def bstack1ll1llll_opy_():
  global bstack11l11ll1_opy_
  global bstack1l11l1l_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstackl_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪજ").lower() == val.lower():
      bstack11l11ll1_opy_[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬઝ")] = {}
      bstack11l11ll1_opy_[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ઞ")][bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬટ")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack1llll11_opy_ in bstack1l1llllll_opy_.items():
    if isinstance(bstack1llll11_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1llll11_opy_:
          if idx<len(sys.argv) and bstackl_opy_ (u"ࠫ࠲࠳ࠧઠ") + var.lower() == val.lower() and not key in bstack11l11ll1_opy_:
            bstack11l11ll1_opy_[key] = sys.argv[idx+1]
            bstack1l11l1l_opy_ += bstackl_opy_ (u"ࠬࠦ࠭࠮ࠩડ") + var + bstackl_opy_ (u"࠭ࠠࠨઢ") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstackl_opy_ (u"ࠧ࠮࠯ࠪણ") + bstack1llll11_opy_.lower() == val.lower() and not key in bstack11l11ll1_opy_:
          bstack11l11ll1_opy_[key] = sys.argv[idx+1]
          bstack1l11l1l_opy_ += bstackl_opy_ (u"ࠨࠢ࠰࠱ࠬત") + bstack1llll11_opy_ + bstackl_opy_ (u"ࠩࠣࠫથ") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack1111ll1l_opy_(config):
  bstack1l1ll1l11_opy_ = config.keys()
  for bstack11llll11_opy_, bstack1l1ll1ll_opy_ in bstack111111l1_opy_.items():
    if bstack1l1ll1ll_opy_ in bstack1l1ll1l11_opy_:
      config[bstack11llll11_opy_] = config[bstack1l1ll1ll_opy_]
      del config[bstack1l1ll1ll_opy_]
  for bstack11llll11_opy_, bstack1l1ll1ll_opy_ in bstack111lll_opy_.items():
    if isinstance(bstack1l1ll1ll_opy_, list):
      for bstack1llllll_opy_ in bstack1l1ll1ll_opy_:
        if bstack1llllll_opy_ in bstack1l1ll1l11_opy_:
          config[bstack11llll11_opy_] = config[bstack1llllll_opy_]
          del config[bstack1llllll_opy_]
          break
    elif bstack1l1ll1ll_opy_ in bstack1l1ll1l11_opy_:
        config[bstack11llll11_opy_] = config[bstack1l1ll1ll_opy_]
        del config[bstack1l1ll1ll_opy_]
  for bstack1llllll_opy_ in list(config):
    for bstack1llll111_opy_ in bstack1ll11lll_opy_:
      if bstack1llllll_opy_.lower() == bstack1llll111_opy_.lower() and bstack1llllll_opy_ != bstack1llll111_opy_:
        config[bstack1llll111_opy_] = config[bstack1llllll_opy_]
        del config[bstack1llllll_opy_]
  bstack11111l1l_opy_ = []
  if bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭દ") in config:
    bstack11111l1l_opy_ = config[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧધ")]
  for platform in bstack11111l1l_opy_:
    for bstack1llllll_opy_ in list(platform):
      for bstack1llll111_opy_ in bstack1ll11lll_opy_:
        if bstack1llllll_opy_.lower() == bstack1llll111_opy_.lower() and bstack1llllll_opy_ != bstack1llll111_opy_:
          platform[bstack1llll111_opy_] = platform[bstack1llllll_opy_]
          del platform[bstack1llllll_opy_]
  for bstack11llll11_opy_, bstack1l1ll1ll_opy_ in bstack111lll_opy_.items():
    for platform in bstack11111l1l_opy_:
      if isinstance(bstack1l1ll1ll_opy_, list):
        for bstack1llllll_opy_ in bstack1l1ll1ll_opy_:
          if bstack1llllll_opy_ in platform:
            platform[bstack11llll11_opy_] = platform[bstack1llllll_opy_]
            del platform[bstack1llllll_opy_]
            break
      elif bstack1l1ll1ll_opy_ in platform:
        platform[bstack11llll11_opy_] = platform[bstack1l1ll1ll_opy_]
        del platform[bstack1l1ll1ll_opy_]
  for bstack1l11lll1_opy_ in bstack11l11111_opy_:
    if bstack1l11lll1_opy_ in config:
      if not bstack11l11111_opy_[bstack1l11lll1_opy_] in config:
        config[bstack11l11111_opy_[bstack1l11lll1_opy_]] = {}
      config[bstack11l11111_opy_[bstack1l11lll1_opy_]].update(config[bstack1l11lll1_opy_])
      del config[bstack1l11lll1_opy_]
  for platform in bstack11111l1l_opy_:
    for bstack1l11lll1_opy_ in bstack11l11111_opy_:
      if bstack1l11lll1_opy_ in list(platform):
        if not bstack11l11111_opy_[bstack1l11lll1_opy_] in platform:
          platform[bstack11l11111_opy_[bstack1l11lll1_opy_]] = {}
        platform[bstack11l11111_opy_[bstack1l11lll1_opy_]].update(platform[bstack1l11lll1_opy_])
        del platform[bstack1l11lll1_opy_]
  config = bstack111l111l_opy_(config)
  return config
def bstack11lll111_opy_(config):
  global bstack11111l11_opy_
  if bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩન") in config and str(config[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ઩")]).lower() != bstackl_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭પ"):
    if not bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬફ") in config:
      config[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭બ")] = {}
    if not bstackl_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬભ") in config[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨમ")]:
      bstack11ll1l1l_opy_ = datetime.datetime.now()
      bstack11l1111_opy_ = bstack11ll1l1l_opy_.strftime(bstackl_opy_ (u"ࠬࠫࡤࡠࠧࡥࡣࠪࡎࠥࡎࠩય"))
      hostname = socket.gethostname()
      bstack111l1l_opy_ = bstackl_opy_ (u"࠭ࠧર").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstackl_opy_ (u"ࠧࡼࡿࡢࡿࢂࡥࡻࡾࠩ઱").format(bstack11l1111_opy_, hostname, bstack111l1l_opy_)
      config[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬલ")][bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫળ")] = identifier
    bstack11111l11_opy_ = config[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ઴")][bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭વ")]
  return config
def bstack1lll1l11l_opy_():
  if (
    isinstance(os.getenv(bstackl_opy_ (u"ࠬࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠪશ")), str) and len(os.getenv(bstackl_opy_ (u"࠭ࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠫષ"))) > 0
  ) or (
    isinstance(os.getenv(bstackl_opy_ (u"ࠧࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊ࠭સ")), str) and len(os.getenv(bstackl_opy_ (u"ࠨࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠧહ"))) > 0
  ):
    return os.getenv(bstackl_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨ઺"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠪࡇࡎ࠭઻"))).lower() == bstackl_opy_ (u"ࠫࡹࡸࡵࡦ઼ࠩ") and str(os.getenv(bstackl_opy_ (u"ࠬࡉࡉࡓࡅࡏࡉࡈࡏࠧઽ"))).lower() == bstackl_opy_ (u"࠭ࡴࡳࡷࡨࠫા"):
    return os.getenv(bstackl_opy_ (u"ࠧࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠪિ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠨࡅࡌࠫી"))).lower() == bstackl_opy_ (u"ࠩࡷࡶࡺ࡫ࠧુ") and str(os.getenv(bstackl_opy_ (u"ࠪࡘࡗࡇࡖࡊࡕࠪૂ"))).lower() == bstackl_opy_ (u"ࠫࡹࡸࡵࡦࠩૃ"):
    return os.getenv(bstackl_opy_ (u"࡚ࠬࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫૄ"), 0)
  if str(os.getenv(bstackl_opy_ (u"࠭ࡃࡊࠩૅ"))).lower() == bstackl_opy_ (u"ࠧࡵࡴࡸࡩࠬ૆") and str(os.getenv(bstackl_opy_ (u"ࠨࡅࡌࡣࡓࡇࡍࡆࠩે"))).lower() == bstackl_opy_ (u"ࠩࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠫૈ"):
    return 0 # bstack1l1l11ll_opy_ bstack11ll11l_opy_ not set build number env
  if os.getenv(bstackl_opy_ (u"ࠪࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡓࡃࡑࡇࡍ࠭ૉ")) and os.getenv(bstackl_opy_ (u"ࠫࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠧ૊")):
    return os.getenv(bstackl_opy_ (u"ࠬࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧો"), 0)
  if str(os.getenv(bstackl_opy_ (u"࠭ࡃࡊࠩૌ"))).lower() == bstackl_opy_ (u"ࠧࡵࡴࡸࡩ્ࠬ") and str(os.getenv(bstackl_opy_ (u"ࠨࡆࡕࡓࡓࡋࠧ૎"))).lower() == bstackl_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ૏"):
    return os.getenv(bstackl_opy_ (u"ࠪࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨૐ"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠫࡈࡏࠧ૑"))).lower() == bstackl_opy_ (u"ࠬࡺࡲࡶࡧࠪ૒") and str(os.getenv(bstackl_opy_ (u"࠭ࡓࡆࡏࡄࡔࡍࡕࡒࡆࠩ૓"))).lower() == bstackl_opy_ (u"ࠧࡵࡴࡸࡩࠬ૔"):
    return os.getenv(bstackl_opy_ (u"ࠨࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠫ૕"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠩࡆࡍࠬ૖"))).lower() == bstackl_opy_ (u"ࠪࡸࡷࡻࡥࠨ૗") and str(os.getenv(bstackl_opy_ (u"ࠫࡌࡏࡔࡍࡃࡅࡣࡈࡏࠧ૘"))).lower() == bstackl_opy_ (u"ࠬࡺࡲࡶࡧࠪ૙"):
    return os.getenv(bstackl_opy_ (u"࠭ࡃࡊࡡࡍࡓࡇࡥࡉࡅࠩ૚"), 0)
  if str(os.getenv(bstackl_opy_ (u"ࠧࡄࡋࠪ૛"))).lower() == bstackl_opy_ (u"ࠨࡶࡵࡹࡪ࠭૜") and str(os.getenv(bstackl_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠬ૝"))).lower() == bstackl_opy_ (u"ࠪࡸࡷࡻࡥࠨ૞"):
    return os.getenv(bstackl_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗ࠭૟"), 0)
  if str(os.getenv(bstackl_opy_ (u"࡚ࠬࡆࡠࡄࡘࡍࡑࡊࠧૠ"))).lower() == bstackl_opy_ (u"࠭ࡴࡳࡷࡨࠫૡ"):
    return os.getenv(bstackl_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠧૢ"), 0)
  return -1
def bstack1l1l11lll_opy_(bstack1lllll11l_opy_):
  global CONFIG
  if not bstackl_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪૣ") in CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૤")]:
    return
  CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૥")] = CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૦")].replace(
    bstackl_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧ૧"),
    str(bstack1lllll11l_opy_)
  )
def bstack11ll1l11_opy_():
  global CONFIG
  if not bstackl_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬ૨") in CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૩")]:
    return
  bstack11ll1l1l_opy_ = datetime.datetime.now()
  bstack11l1111_opy_ = bstack11ll1l1l_opy_.strftime(bstackl_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࠭૪"))
  CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૫")] = CONFIG[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૬")].replace(
    bstackl_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪ૭"),
    bstack11l1111_opy_
  )
def bstack1l1l1l1l_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૮") in CONFIG and not bool(CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૯")]):
    del CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૰")]
    return
  if not bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૱") in CONFIG:
    CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૲")] = bstackl_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭૳")
  if bstackl_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪ૴") in CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૵")]:
    bstack11ll1l11_opy_()
    os.environ[bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ૶")] = CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૷")]
  if not bstackl_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪ૸") in CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫૹ")]:
    return
  bstack1lllll11l_opy_ = bstackl_opy_ (u"ࠪࠫૺ")
  bstack1ll11ll_opy_ = bstack1lll1l11l_opy_()
  if bstack1ll11ll_opy_ != -1:
    bstack1lllll11l_opy_ = bstackl_opy_ (u"ࠫࡈࡏࠠࠨૻ") + str(bstack1ll11ll_opy_)
  if bstack1lllll11l_opy_ == bstackl_opy_ (u"ࠬ࠭ૼ"):
    bstack1ll11l_opy_ = bstack1lll1llll_opy_(CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ૽")])
    if bstack1ll11l_opy_ != -1:
      bstack1lllll11l_opy_ = str(bstack1ll11l_opy_)
  if bstack1lllll11l_opy_:
    bstack1l1l11lll_opy_(bstack1lllll11l_opy_)
    os.environ[bstackl_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ૾")] = CONFIG[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૿")]
def bstack11lll11l_opy_(bstack11lll1l11_opy_, bstack11llll1l1_opy_, path):
  bstack1l1l1lll_opy_ = {
    bstackl_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭଀"): bstack11llll1l1_opy_
  }
  if os.path.exists(path):
    bstack1111llll_opy_ = json.load(open(path, bstackl_opy_ (u"ࠪࡶࡧ࠭ଁ")))
  else:
    bstack1111llll_opy_ = {}
  bstack1111llll_opy_[bstack11lll1l11_opy_] = bstack1l1l1lll_opy_
  with open(path, bstackl_opy_ (u"ࠦࡼ࠱ࠢଂ")) as outfile:
    json.dump(bstack1111llll_opy_, outfile)
def bstack1lll1llll_opy_(bstack11lll1l11_opy_):
  bstack11lll1l11_opy_ = str(bstack11lll1l11_opy_)
  bstack111ll11_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠬࢄࠧଃ")), bstackl_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭଄"))
  try:
    if not os.path.exists(bstack111ll11_opy_):
      os.makedirs(bstack111ll11_opy_)
    file_path = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠧࡿࠩଅ")), bstackl_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨଆ"), bstackl_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫଇ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstackl_opy_ (u"ࠪࡻࠬଈ")):
        pass
      with open(file_path, bstackl_opy_ (u"ࠦࡼ࠱ࠢଉ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstackl_opy_ (u"ࠬࡸࠧଊ")) as bstack1lllll_opy_:
      bstack11ll1lll_opy_ = json.load(bstack1lllll_opy_)
    if bstack11lll1l11_opy_ in bstack11ll1lll_opy_:
      bstack1111l_opy_ = bstack11ll1lll_opy_[bstack11lll1l11_opy_][bstackl_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪଋ")]
      bstack1lll1lll_opy_ = int(bstack1111l_opy_) + 1
      bstack11lll11l_opy_(bstack11lll1l11_opy_, bstack1lll1lll_opy_, file_path)
      return bstack1lll1lll_opy_
    else:
      bstack11lll11l_opy_(bstack11lll1l11_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11111l_opy_.format(str(e)))
    return -1
def bstack1lllll1ll_opy_(config):
  if not config[bstackl_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩଌ")] or not config[bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ଍")]:
    return True
  else:
    return False
def bstack1l111111l_opy_(config):
  if bstackl_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨ଎") in config:
    del(config[bstackl_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩଏ")])
    return False
  if bstack1l11111_opy_() < version.parse(bstackl_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪଐ")):
    return False
  if bstack1l11111_opy_() >= version.parse(bstackl_opy_ (u"ࠬ࠺࠮࠲࠰࠸ࠫ଑")):
    return True
  if bstackl_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭଒") in config and config[bstackl_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧଓ")] == False:
    return False
  else:
    return True
def bstack111l11_opy_(config, index = 0):
  global bstack11l111_opy_
  bstack1l1111ll1_opy_ = {}
  caps = bstack1llll111l_opy_ + bstack1lll1ll11_opy_
  if bstack11l111_opy_:
    caps += bstack1lll11lll_opy_
  for key in config:
    if key in caps + [bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଔ")]:
      continue
    bstack1l1111ll1_opy_[key] = config[key]
  if bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬକ") in config:
    for bstack11lll1111_opy_ in config[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଖ")][index]:
      if bstack11lll1111_opy_ in caps + [bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଗ"), bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ଘ")]:
        continue
      bstack1l1111ll1_opy_[bstack11lll1111_opy_] = config[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଙ")][index][bstack11lll1111_opy_]
  bstack1l1111ll1_opy_[bstackl_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩଚ")] = socket.gethostname()
  if bstackl_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩଛ") in bstack1l1111ll1_opy_:
    del(bstack1l1111ll1_opy_[bstackl_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪଜ")])
  return bstack1l1111ll1_opy_
def bstack1ll1ll1ll_opy_(config):
  global bstack11l111_opy_
  bstack111111l_opy_ = {}
  caps = bstack1lll1ll11_opy_
  if bstack11l111_opy_:
    caps+= bstack1lll11lll_opy_
  for key in caps:
    if key in config:
      bstack111111l_opy_[key] = config[key]
  return bstack111111l_opy_
def bstack1llll1_opy_(bstack1l1111ll1_opy_, bstack111111l_opy_):
  bstack11l111l1_opy_ = {}
  for key in bstack1l1111ll1_opy_.keys():
    if key in bstack111111l1_opy_:
      bstack11l111l1_opy_[bstack111111l1_opy_[key]] = bstack1l1111ll1_opy_[key]
    else:
      bstack11l111l1_opy_[key] = bstack1l1111ll1_opy_[key]
  for key in bstack111111l_opy_:
    if key in bstack111111l1_opy_:
      bstack11l111l1_opy_[bstack111111l1_opy_[key]] = bstack111111l_opy_[key]
    else:
      bstack11l111l1_opy_[key] = bstack111111l_opy_[key]
  return bstack11l111l1_opy_
def bstack1lll111ll_opy_(config, index = 0):
  global bstack11l111_opy_
  caps = {}
  bstack111111l_opy_ = bstack1ll1ll1ll_opy_(config)
  bstack1l1111ll_opy_ = bstack1lll1ll11_opy_
  bstack1l1111ll_opy_ += bstack111l1ll_opy_
  if bstack11l111_opy_:
    bstack1l1111ll_opy_ += bstack1lll11lll_opy_
  if bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଝ") in config:
    if bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଞ") in config[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଟ")][index]:
      caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫଠ")] = config[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଡ")][index][bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ଢ")]
    if bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪଣ") in config[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ତ")][index]:
      caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬଥ")] = str(config[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଦ")][index][bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧଧ")])
    bstack111ll1l1_opy_ = {}
    for bstack1l11l111_opy_ in bstack1l1111ll_opy_:
      if bstack1l11l111_opy_ in config[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪନ")][index]:
        if bstack1l11l111_opy_ == bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ଩"):
          bstack111ll1l1_opy_[bstack1l11l111_opy_] = str(config[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬପ")][index][bstack1l11l111_opy_] * 1.0)
        else:
          bstack111ll1l1_opy_[bstack1l11l111_opy_] = config[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଫ")][index][bstack1l11l111_opy_]
        del(config[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧବ")][index][bstack1l11l111_opy_])
    bstack111111l_opy_ = update(bstack111111l_opy_, bstack111ll1l1_opy_)
  bstack1l1111ll1_opy_ = bstack111l11_opy_(config, index)
  for bstack1llllll_opy_ in bstack1lll1ll11_opy_ + [bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪଭ"), bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧମ")]:
    if bstack1llllll_opy_ in bstack1l1111ll1_opy_:
      bstack111111l_opy_[bstack1llllll_opy_] = bstack1l1111ll1_opy_[bstack1llllll_opy_]
      del(bstack1l1111ll1_opy_[bstack1llllll_opy_])
  if bstack1l111111l_opy_(config):
    bstack1l1111ll1_opy_[bstackl_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧଯ")] = True
    caps.update(bstack111111l_opy_)
    caps[bstackl_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩର")] = bstack1l1111ll1_opy_
  else:
    bstack1l1111ll1_opy_[bstackl_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ଱")] = False
    caps.update(bstack1llll1_opy_(bstack1l1111ll1_opy_, bstack111111l_opy_))
    if bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଲ") in caps:
      caps[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬଳ")] = caps[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ଴")]
      del(caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫଵ")])
    if bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨଶ") in caps:
      caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪଷ")] = caps[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪସ")]
      del(caps[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫହ")])
  return caps
def bstack1lll11111_opy_():
  global bstack1l1111_opy_
  if bstack1l11111_opy_() <= version.parse(bstackl_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ଺")):
    if bstack1l1111_opy_ != bstackl_opy_ (u"ࠬ࠭଻"):
      return bstackl_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵଼ࠢ") + bstack1l1111_opy_ + bstackl_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦଽ")
    return bstack1lllllll1_opy_
  if  bstack1l1111_opy_ != bstackl_opy_ (u"ࠨࠩା"):
    return bstackl_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦି") + bstack1l1111_opy_ + bstackl_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦୀ")
  return bstack1l111ll11_opy_
def bstack1l11ll1l1_opy_(options):
  return hasattr(options, bstackl_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬୁ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l11l1ll_opy_(options, bstack1111l1l_opy_):
  for bstack111111ll_opy_ in bstack1111l1l_opy_:
    if bstack111111ll_opy_ in [bstackl_opy_ (u"ࠬࡧࡲࡨࡵࠪୂ"), bstackl_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪୃ")]:
      next
    if bstack111111ll_opy_ in options._experimental_options:
      options._experimental_options[bstack111111ll_opy_]= update(options._experimental_options[bstack111111ll_opy_], bstack1111l1l_opy_[bstack111111ll_opy_])
    else:
      options.add_experimental_option(bstack111111ll_opy_, bstack1111l1l_opy_[bstack111111ll_opy_])
  if bstackl_opy_ (u"ࠧࡢࡴࡪࡷࠬୄ") in bstack1111l1l_opy_:
    for arg in bstack1111l1l_opy_[bstackl_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୅")]:
      options.add_argument(arg)
    del(bstack1111l1l_opy_[bstackl_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ୆")])
  if bstackl_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧେ") in bstack1111l1l_opy_:
    for ext in bstack1111l1l_opy_[bstackl_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨୈ")]:
      options.add_extension(ext)
    del(bstack1111l1l_opy_[bstackl_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ୉")])
def bstack1ll111ll_opy_(options, bstack11llll1_opy_):
  if bstackl_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ୊") in bstack11llll1_opy_:
    for bstack1l111ll_opy_ in bstack11llll1_opy_[bstackl_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ୋ")]:
      if bstack1l111ll_opy_ in options._preferences:
        options._preferences[bstack1l111ll_opy_] = update(options._preferences[bstack1l111ll_opy_], bstack11llll1_opy_[bstackl_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧୌ")][bstack1l111ll_opy_])
      else:
        options.set_preference(bstack1l111ll_opy_, bstack11llll1_opy_[bstackl_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ୍")][bstack1l111ll_opy_])
  if bstackl_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ୎") in bstack11llll1_opy_:
    for arg in bstack11llll1_opy_[bstackl_opy_ (u"ࠫࡦࡸࡧࡴࠩ୏")]:
      options.add_argument(arg)
def bstack11ll111l1_opy_(options, bstack111l11l1_opy_):
  if bstackl_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭୐") in bstack111l11l1_opy_:
    options.use_webview(bool(bstack111l11l1_opy_[bstackl_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧ୑")]))
  bstack1l11l1ll_opy_(options, bstack111l11l1_opy_)
def bstack1ll11ll11_opy_(options, bstack1111l1_opy_):
  for bstack1ll1l_opy_ in bstack1111l1_opy_:
    if bstack1ll1l_opy_ in [bstackl_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫ୒"), bstackl_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୓")]:
      next
    options.set_capability(bstack1ll1l_opy_, bstack1111l1_opy_[bstack1ll1l_opy_])
  if bstackl_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ୔") in bstack1111l1_opy_:
    for arg in bstack1111l1_opy_[bstackl_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ୕")]:
      options.add_argument(arg)
  if bstackl_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨୖ") in bstack1111l1_opy_:
    options.use_technology_preview(bool(bstack1111l1_opy_[bstackl_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩୗ")]))
def bstack1llll1lll_opy_(options, bstack1l1llll_opy_):
  for bstack11l1l111_opy_ in bstack1l1llll_opy_:
    if bstack11l1l111_opy_ in [bstackl_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ୘"), bstackl_opy_ (u"ࠧࡢࡴࡪࡷࠬ୙")]:
      next
    options._options[bstack11l1l111_opy_] = bstack1l1llll_opy_[bstack11l1l111_opy_]
  if bstackl_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ୚") in bstack1l1llll_opy_:
    for bstack1l11l11l1_opy_ in bstack1l1llll_opy_[bstackl_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭୛")]:
      options.add_additional_option(
          bstack1l11l11l1_opy_, bstack1l1llll_opy_[bstackl_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧଡ଼")][bstack1l11l11l1_opy_])
  if bstackl_opy_ (u"ࠫࡦࡸࡧࡴࠩଢ଼") in bstack1l1llll_opy_:
    for arg in bstack1l1llll_opy_[bstackl_opy_ (u"ࠬࡧࡲࡨࡵࠪ୞")]:
      options.add_argument(arg)
def bstack1l1ll1lll_opy_(options, caps):
  if not hasattr(options, bstackl_opy_ (u"࠭ࡋࡆ࡛ࠪୟ")):
    return
  if options.KEY == bstackl_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬୠ") and options.KEY in caps:
    bstack1l11l1ll_opy_(options, caps[bstackl_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ୡ")])
  elif options.KEY == bstackl_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧୢ") and options.KEY in caps:
    bstack1ll111ll_opy_(options, caps[bstackl_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨୣ")])
  elif options.KEY == bstackl_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬ୤") and options.KEY in caps:
    bstack1ll11ll11_opy_(options, caps[bstackl_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭୥")])
  elif options.KEY == bstackl_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ୦") and options.KEY in caps:
    bstack11ll111l1_opy_(options, caps[bstackl_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ୧")])
  elif options.KEY == bstackl_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ୨") and options.KEY in caps:
    bstack1llll1lll_opy_(options, caps[bstackl_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ୩")])
def bstack11l1l1_opy_(caps):
  global bstack11l111_opy_
  if bstack11l111_opy_:
    if bstack11ll111ll_opy_() < version.parse(bstackl_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩ୪")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ୫")
    if bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ୬") in caps:
      browser = caps[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ୭")]
    elif bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ୮") in caps:
      browser = caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ୯")]
    browser = str(browser).lower()
    if browser == bstackl_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩ୰") or browser == bstackl_opy_ (u"ࠪ࡭ࡵࡧࡤࠨୱ"):
      browser = bstackl_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫ୲")
    if browser == bstackl_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭୳"):
      browser = bstackl_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭୴")
    if browser not in [bstackl_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ୵"), bstackl_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭୶"), bstackl_opy_ (u"ࠩ࡬ࡩࠬ୷"), bstackl_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪ୸"), bstackl_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬ୹")]:
      return None
    try:
      package = bstackl_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ୺").format(browser)
      name = bstackl_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧ୻")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l11ll1l1_opy_(options):
        return None
      for bstack1llllll_opy_ in caps.keys():
        options.set_capability(bstack1llllll_opy_, caps[bstack1llllll_opy_])
      bstack1l1ll1lll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1ll1l1l1_opy_(options, bstack11111_opy_):
  if not bstack1l11ll1l1_opy_(options):
    return
  for bstack1llllll_opy_ in bstack11111_opy_.keys():
    if bstack1llllll_opy_ in bstack111l1ll_opy_:
      next
    if bstack1llllll_opy_ in options._caps and type(options._caps[bstack1llllll_opy_]) in [dict, list]:
      options._caps[bstack1llllll_opy_] = update(options._caps[bstack1llllll_opy_], bstack11111_opy_[bstack1llllll_opy_])
    else:
      options.set_capability(bstack1llllll_opy_, bstack11111_opy_[bstack1llllll_opy_])
  bstack1l1ll1lll_opy_(options, bstack11111_opy_)
  if bstackl_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭୼") in options._caps:
    if options._caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭୽")] and options._caps[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ୾")].lower() != bstackl_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ୿"):
      del options._caps[bstackl_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪ஀")]
def bstack11l11l1_opy_(proxy_config):
  if bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ஁") in proxy_config:
    proxy_config[bstackl_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨஂ")] = proxy_config[bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫஃ")]
    del(proxy_config[bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ஄")])
  if bstackl_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬஅ") in proxy_config and proxy_config[bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭ஆ")].lower() != bstackl_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫஇ"):
    proxy_config[bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨஈ")] = bstackl_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭உ")
  if bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬஊ") in proxy_config:
    proxy_config[bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ஋")] = bstackl_opy_ (u"ࠩࡳࡥࡨ࠭஌")
  return proxy_config
def bstack11111l1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ஍") in config:
    return proxy
  config[bstackl_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪஎ")] = bstack11l11l1_opy_(config[bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫஏ")])
  if proxy == None:
    proxy = Proxy(config[bstackl_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬஐ")])
  return proxy
def bstack1l11l1l1_opy_(self):
  global CONFIG
  global bstack1llllll1_opy_
  if bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ஑") in CONFIG:
    return CONFIG[bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫஒ")]
  elif bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ஓ") in CONFIG:
    return CONFIG[bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧஔ")]
  else:
    return bstack1llllll1_opy_(self)
def bstack1l11ll_opy_():
  global CONFIG
  return bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧக") in CONFIG or bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ஖") in CONFIG
def bstack1llll11ll_opy_(config):
  if not bstack1l11ll_opy_():
    return
  if config.get(bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ஗")):
    return config.get(bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ஘"))
  if config.get(bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬங")):
    return config.get(bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ச"))
def bstack11l1111l_opy_():
  return bstack1l11ll_opy_() and bstack1l11111_opy_() >= version.parse(bstack1ll1l111l_opy_)
def bstack1l111ll1_opy_(config):
  if bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ஛") in config:
    return config[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨஜ")]
  if bstackl_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ஝") in config:
    return config[bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬஞ")]
  return {}
def bstack1ll11l11l_opy_(config):
  if bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬட") in config:
    return config[bstackl_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭஠")]
  return {}
def bstack11ll1111l_opy_(caps):
  global bstack11111l11_opy_
  if bstackl_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ஡") in caps:
    caps[bstackl_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ஢")][bstackl_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪண")] = True
    if bstack11111l11_opy_:
      caps[bstackl_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭த")][bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ஥")] = bstack11111l11_opy_
  else:
    caps[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬ஦")] = True
    if bstack11111l11_opy_:
      caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ஧")] = bstack11111l11_opy_
def bstack1lll1ll1l_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ந") in CONFIG and CONFIG[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧன")]:
    bstack1l11l1111_opy_ = bstack1l111ll1_opy_(CONFIG)
    bstack11lll_opy_(CONFIG[bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧப")], bstack1l11l1111_opy_)
def bstack11lll_opy_(key, bstack1l11l1111_opy_):
  global bstack11ll1lll1_opy_
  logger.info(bstack11ll1llll_opy_)
  try:
    bstack11ll1lll1_opy_ = Local()
    bstack1llll1l1l_opy_ = {bstackl_opy_ (u"ࠬࡱࡥࡺࠩ஫"): key}
    bstack1llll1l1l_opy_.update(bstack1l11l1111_opy_)
    logger.debug(bstack1l111111_opy_.format(str(bstack1llll1l1l_opy_)))
    bstack11ll1lll1_opy_.start(**bstack1llll1l1l_opy_)
    if bstack11ll1lll1_opy_.isRunning():
      logger.info(bstack11l1l11_opy_)
  except Exception as e:
    bstack1l1l11ll1_opy_(bstack1lll11ll_opy_.format(str(e)))
def bstack1l11l1lll_opy_():
  global bstack11ll1lll1_opy_
  if bstack11ll1lll1_opy_.isRunning():
    logger.info(bstack111ll1ll_opy_)
    bstack11ll1lll1_opy_.stop()
  bstack11ll1lll1_opy_ = None
def bstack1l11_opy_():
  global bstack1l11llll_opy_
  global bstack1ll1111_opy_
  if bstack1l11llll_opy_:
    logger.warning(bstack11l1lll_opy_.format(str(bstack1l11llll_opy_)))
  logger.info(bstack11ll1l11l_opy_)
  global bstack11ll1lll1_opy_
  if bstack11ll1lll1_opy_:
    bstack1l11l1lll_opy_()
  try:
    for driver in bstack1ll1111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11lll1ll1_opy_)
  bstack111llll_opy_()
def bstack1ll11l111_opy_(self, *args):
  logger.error(bstack11ll1l1ll_opy_)
  bstack1l11_opy_()
  sys.exit(1)
def bstack1l1l11ll1_opy_(err):
  logger.critical(bstack1ll111ll1_opy_.format(str(err)))
  bstack111llll_opy_(bstack1ll111ll1_opy_.format(str(err)))
  atexit.unregister(bstack1l11_opy_)
  sys.exit(1)
def bstack1ll1l1l1l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack111llll_opy_(message)
  atexit.unregister(bstack1l11_opy_)
  sys.exit(1)
def bstack111l1111_opy_():
  global CONFIG
  global bstack11l11ll1_opy_
  global bstack1ll11l1l1_opy_
  global bstack11l1lllll_opy_
  CONFIG = bstack111lll1_opy_()
  bstack11ll1ll_opy_()
  bstack1ll1llll_opy_()
  CONFIG = bstack1111ll1l_opy_(CONFIG)
  update(CONFIG, bstack1ll11l1l1_opy_)
  update(CONFIG, bstack11l11ll1_opy_)
  CONFIG = bstack11lll111_opy_(CONFIG)
  if bstackl_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ஬") in CONFIG and str(CONFIG[bstackl_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ஭")]).lower() == bstackl_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧம"):
    bstack11l1lllll_opy_ = False
  if (bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬய") in CONFIG and bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ர") in bstack11l11ll1_opy_) or (bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧற") in CONFIG and bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨல") not in bstack1ll11l1l1_opy_):
    if os.getenv(bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪள")):
      CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩழ")] = os.getenv(bstackl_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬவ"))
    else:
      bstack1l1l1l1l_opy_()
  elif (bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬஶ") not in CONFIG and bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬஷ") in CONFIG) or (bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧஸ") in bstack1ll11l1l1_opy_ and bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨஹ") not in bstack11l11ll1_opy_):
    del(CONFIG[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ஺")])
  if bstack1lllll1ll_opy_(CONFIG):
    bstack1l1l11ll1_opy_(bstack1llll1l_opy_)
  bstack11111111_opy_()
  bstack1ll1ll11l_opy_()
  if bstack11l111_opy_:
    CONFIG[bstackl_opy_ (u"ࠧࡢࡲࡳࠫ஻")] = bstack1l11l1l1l_opy_(CONFIG)
    logger.info(bstack1l1l1lll1_opy_.format(CONFIG[bstackl_opy_ (u"ࠨࡣࡳࡴࠬ஼")]))
def bstack1ll1ll11l_opy_():
  global CONFIG
  global bstack11l111_opy_
  if bstackl_opy_ (u"ࠩࡤࡴࡵ࠭஽") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll1l1l1l_opy_(e, bstack1ll11l11_opy_)
    bstack11l111_opy_ = True
def bstack1l11l1l1l_opy_(config):
  bstack1ll1l111_opy_ = bstackl_opy_ (u"ࠪࠫா")
  app = config[bstackl_opy_ (u"ࠫࡦࡶࡰࠨி")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l111l1l_opy_:
      if os.path.exists(app):
        bstack1ll1l111_opy_ = bstack1l11111ll_opy_(config, app)
      elif bstack1l1l1l1l1_opy_(app):
        bstack1ll1l111_opy_ = app
      else:
        bstack1l1l11ll1_opy_(bstack11lll11_opy_.format(app))
    else:
      if bstack1l1l1l1l1_opy_(app):
        bstack1ll1l111_opy_ = app
      elif os.path.exists(app):
        bstack1ll1l111_opy_ = bstack1l11111ll_opy_(app)
      else:
        bstack1l1l11ll1_opy_(bstack111ll1_opy_)
  else:
    if len(app) > 2:
      bstack1l1l11ll1_opy_(bstack111l1l1_opy_)
    elif len(app) == 2:
      if bstackl_opy_ (u"ࠬࡶࡡࡵࡪࠪீ") in app and bstackl_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩு") in app:
        if os.path.exists(app[bstackl_opy_ (u"ࠧࡱࡣࡷ࡬ࠬூ")]):
          bstack1ll1l111_opy_ = bstack1l11111ll_opy_(config, app[bstackl_opy_ (u"ࠨࡲࡤࡸ࡭࠭௃")], app[bstackl_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ௄")])
        else:
          bstack1l1l11ll1_opy_(bstack11lll11_opy_.format(app))
      else:
        bstack1l1l11ll1_opy_(bstack111l1l1_opy_)
    else:
      for key in app:
        if key in bstack1111lll_opy_:
          if key == bstackl_opy_ (u"ࠪࡴࡦࡺࡨࠨ௅"):
            if os.path.exists(app[key]):
              bstack1ll1l111_opy_ = bstack1l11111ll_opy_(config, app[key])
            else:
              bstack1l1l11ll1_opy_(bstack11lll11_opy_.format(app))
          else:
            bstack1ll1l111_opy_ = app[key]
        else:
          bstack1l1l11ll1_opy_(bstack11ll11l1_opy_)
  return bstack1ll1l111_opy_
def bstack1l1l1l1l1_opy_(bstack1ll1l111_opy_):
  import re
  bstack1llll1l1_opy_ = re.compile(bstackl_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦெ"))
  bstack11lll1lll_opy_ = re.compile(bstackl_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤே"))
  if bstackl_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬை") in bstack1ll1l111_opy_ or re.fullmatch(bstack1llll1l1_opy_, bstack1ll1l111_opy_) or re.fullmatch(bstack11lll1lll_opy_, bstack1ll1l111_opy_):
    return True
  else:
    return False
def bstack1l11111ll_opy_(config, path, bstack1l1111l11_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstackl_opy_ (u"ࠧࡳࡤࠪ௉")).read()).hexdigest()
  bstack1ll11111_opy_ = bstack1ll11l1ll_opy_(md5_hash)
  bstack1ll1l111_opy_ = None
  if bstack1ll11111_opy_:
    logger.info(bstack11111ll1_opy_.format(bstack1ll11111_opy_, md5_hash))
    return bstack1ll11111_opy_
  bstack1ll1l1ll_opy_ = MultipartEncoder(
    fields={
        bstackl_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭ொ"): (os.path.basename(path), open(os.path.abspath(path), bstackl_opy_ (u"ࠩࡵࡦࠬோ")), bstackl_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴࠧௌ")),
        bstackl_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪ்ࠧ"): bstack1l1111l11_opy_
    }
  )
  response = requests.post(bstack1llll1111_opy_, data=bstack1ll1l1ll_opy_,
                         headers={bstackl_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ௎"): bstack1ll1l1ll_opy_.content_type}, auth=(config[bstackl_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ௏")], config[bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪௐ")]))
  try:
    res = json.loads(response.text)
    bstack1ll1l111_opy_ = res[bstackl_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩ௑")]
    logger.info(bstack11l1llll_opy_.format(bstack1ll1l111_opy_))
    bstack1111_opy_(md5_hash, bstack1ll1l111_opy_)
  except ValueError as err:
    bstack1l1l11ll1_opy_(bstack1l111l1l1_opy_.format(str(err)))
  return bstack1ll1l111_opy_
def bstack11111111_opy_():
  global CONFIG
  global bstack1lll11l11_opy_
  bstack1l1l1l_opy_ = 0
  bstack1l1l1ll1_opy_ = 1
  if bstackl_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ௒") in CONFIG:
    bstack1l1l1ll1_opy_ = CONFIG[bstackl_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ௓")]
  if bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ௔") in CONFIG:
    bstack1l1l1l_opy_ = len(CONFIG[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௕")])
  bstack1lll11l11_opy_ = int(bstack1l1l1ll1_opy_) * int(bstack1l1l1l_opy_)
def bstack1ll11l1ll_opy_(md5_hash):
  bstack1llllll11_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"࠭ࡾࠨ௖")), bstackl_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧௗ"), bstackl_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩ௘"))
  if os.path.exists(bstack1llllll11_opy_):
    bstack1lll1l_opy_ = json.load(open(bstack1llllll11_opy_,bstackl_opy_ (u"ࠩࡵࡦࠬ௙")))
    if md5_hash in bstack1lll1l_opy_:
      bstack1l11l1_opy_ = bstack1lll1l_opy_[md5_hash]
      bstack1l1lll1l1_opy_ = datetime.datetime.now()
      bstack1l1ll11l_opy_ = datetime.datetime.strptime(bstack1l11l1_opy_[bstackl_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭௚")], bstackl_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ௛"))
      if (bstack1l1lll1l1_opy_ - bstack1l1ll11l_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l11l1_opy_[bstackl_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ௜")]):
        return None
      return bstack1l11l1_opy_[bstackl_opy_ (u"࠭ࡩࡥࠩ௝")]
  else:
    return None
def bstack1111_opy_(md5_hash, bstack1ll1l111_opy_):
  bstack111ll11_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠧࡿࠩ௞")), bstackl_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ௟"))
  if not os.path.exists(bstack111ll11_opy_):
    os.makedirs(bstack111ll11_opy_)
  bstack1llllll11_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠩࢁࠫ௠")), bstackl_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ௡"), bstackl_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬ௢"))
  bstack1l1111111_opy_ = {
    bstackl_opy_ (u"ࠬ࡯ࡤࠨ௣"): bstack1ll1l111_opy_,
    bstackl_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ௤"): datetime.datetime.strftime(datetime.datetime.now(), bstackl_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫ௥")),
    bstackl_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭௦"): str(__version__)
  }
  if os.path.exists(bstack1llllll11_opy_):
    bstack1lll1l_opy_ = json.load(open(bstack1llllll11_opy_,bstackl_opy_ (u"ࠩࡵࡦࠬ௧")))
  else:
    bstack1lll1l_opy_ = {}
  bstack1lll1l_opy_[md5_hash] = bstack1l1111111_opy_
  with open(bstack1llllll11_opy_, bstackl_opy_ (u"ࠥࡻ࠰ࠨ௨")) as outfile:
    json.dump(bstack1lll1l_opy_, outfile)
def bstack11l1lll1_opy_(self):
  return
def bstack1l11ll1l_opy_(self):
  return
def bstack11ll11_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1111ll1_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1lllll111_opy_
  global bstack1lll111l1_opy_
  global bstack1l1l11_opy_
  global bstack11ll1l111_opy_
  global bstack1ll1l1111_opy_
  global bstack11ll11ll1_opy_
  global bstack1ll1111_opy_
  global bstack1l1l111ll_opy_
  CONFIG[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭௩")] = str(bstack1ll1l1111_opy_) + str(__version__)
  command_executor = bstack1lll11111_opy_()
  logger.debug(bstack1l11l11_opy_.format(command_executor))
  proxy = bstack11111l1_opy_(CONFIG, proxy)
  bstack1llll11l_opy_ = 0 if bstack1lll111l1_opy_ < 0 else bstack1lll111l1_opy_
  if bstack11ll1l111_opy_ is True:
    bstack1llll11l_opy_ = int(threading.current_thread().getName())
  bstack11111_opy_ = bstack1lll111ll_opy_(CONFIG, bstack1llll11l_opy_)
  logger.debug(bstack111l1l11_opy_.format(str(bstack11111_opy_)))
  if bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ௪") in CONFIG and CONFIG[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ௫")]:
    bstack11ll1111l_opy_(bstack11111_opy_)
  if desired_capabilities:
    bstack11l1l11l_opy_ = bstack1111ll1l_opy_(desired_capabilities)
    bstack11l1l11l_opy_[bstackl_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ௬")] = bstack1l111111l_opy_(CONFIG)
    bstack11llll11l_opy_ = bstack1lll111ll_opy_(bstack11l1l11l_opy_)
    if bstack11llll11l_opy_:
      bstack11111_opy_ = update(bstack11llll11l_opy_, bstack11111_opy_)
    desired_capabilities = None
  if options:
    bstack1ll1l1l1_opy_(options, bstack11111_opy_)
  if not options:
    options = bstack11l1l1_opy_(bstack11111_opy_)
  if proxy and bstack1l11111_opy_() >= version.parse(bstackl_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ௭")):
    options.proxy(proxy)
  if options and bstack1l11111_opy_() >= version.parse(bstackl_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ௮")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack1l11111_opy_() < version.parse(bstackl_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ௯")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11111_opy_)
  logger.info(bstack1l1l11l1l_opy_)
  if bstack1l11111_opy_() >= version.parse(bstackl_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫ௰")):
    bstack11ll11ll1_opy_(self, command_executor=command_executor,
          options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l11111_opy_() >= version.parse(bstackl_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ௱")):
    bstack11ll11ll1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l11111_opy_() >= version.parse(bstackl_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭௲")):
    bstack11ll11ll1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11ll11ll1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  try:
    bstack11l111l_opy_ = bstackl_opy_ (u"ࠧࠨ௳")
    if bstack1l11111_opy_() >= version.parse(bstackl_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩ௴")):
      bstack11l111l_opy_ = self.caps.get(bstackl_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ௵"))
    else:
      bstack11l111l_opy_ = self.capabilities.get(bstackl_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥ௶"))
    if bstack11l111l_opy_:
      if bstack1l11111_opy_() <= version.parse(bstackl_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ௷")):
        self.command_executor._url = bstackl_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ௸") + bstack1l1111_opy_ + bstackl_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥ௹")
      else:
        self.command_executor._url = bstackl_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ௺") + bstack11l111l_opy_ + bstackl_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤ௻")
      logger.debug(bstack1llll1l11_opy_.format(bstack11l111l_opy_))
    else:
      logger.debug(bstack1lll1111l_opy_.format(bstackl_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥ௼")))
  except Exception as e:
    logger.debug(bstack1lll1111l_opy_.format(e))
  bstack1l1l111_opy_(bstack1lll111l1_opy_, bstack1l1l111ll_opy_)
  bstack1lllll111_opy_ = self.session_id
  bstack1ll1111_opy_.append(self)
  if bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௽") in CONFIG and bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ௾") in CONFIG[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௿")][bstack1llll11l_opy_]:
    bstack1l1l11_opy_ = CONFIG[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩఀ")][bstack1llll11l_opy_][bstackl_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬఁ")]
  logger.debug(bstack1l1ll1_opy_.format(bstack1lllll111_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1l1llll1l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l11lll11_opy_
      if(bstackl_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥం") in args[1]):
        with open(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠩࢁࠫః")), bstackl_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪఄ"), bstackl_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭అ")), bstackl_opy_ (u"ࠬࡽࠧఆ")) as fp:
          fp.write(bstackl_opy_ (u"ࠨࠢఇ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤఈ")))):
          with open(args[1], bstackl_opy_ (u"ࠨࡴࠪఉ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstackl_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨఊ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11ll11ll_opy_)
            lines.insert(1, bstack1l1l1111_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧఋ")), bstackl_opy_ (u"ࠫࡼ࠭ఌ")) as bstack1l1lll111_opy_:
              bstack1l1lll111_opy_.writelines(lines)
        CONFIG[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ఍")] = str(bstack1ll1l1111_opy_) + str(__version__)
        bstack1llll11l_opy_ = 0 if bstack1lll111l1_opy_ < 0 else bstack1lll111l1_opy_
        if bstack11ll1l111_opy_ is True:
          bstack1llll11l_opy_ = int(threading.current_thread().getName())
        CONFIG[bstackl_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨఎ")] = False
        CONFIG[bstackl_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨఏ")] = True
        bstack11111_opy_ = bstack1lll111ll_opy_(CONFIG, bstack1llll11l_opy_)
        logger.debug(bstack111l1l11_opy_.format(str(bstack11111_opy_)))
        if CONFIG[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬఐ")]:
          bstack11ll1111l_opy_(bstack11111_opy_)
        if bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ఑") in CONFIG and bstackl_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨఒ") in CONFIG[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧఓ")][bstack1llll11l_opy_]:
          bstack1l1l11_opy_ = CONFIG[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨఔ")][bstack1llll11l_opy_][bstackl_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫక")]
        args.append(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠧࡿࠩఖ")), bstackl_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨగ"), bstackl_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫఘ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11111_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstackl_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧఙ"))
      bstack1l11lll11_opy_ = True
      return bstack111l1lll_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1lll1l1l1_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1lllll111_opy_
    global bstack1lll111l1_opy_
    global bstack1l1l11_opy_
    global bstack11ll1l111_opy_
    global bstack1ll1l1111_opy_
    global bstack11ll11ll1_opy_
    CONFIG[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭చ")] = str(bstack1ll1l1111_opy_) + str(__version__)
    bstack1llll11l_opy_ = 0 if bstack1lll111l1_opy_ < 0 else bstack1lll111l1_opy_
    if bstack11ll1l111_opy_ is True:
      bstack1llll11l_opy_ = int(threading.current_thread().getName())
    CONFIG[bstackl_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦఛ")] = True
    bstack11111_opy_ = bstack1lll111ll_opy_(CONFIG, bstack1llll11l_opy_)
    logger.debug(bstack111l1l11_opy_.format(str(bstack11111_opy_)))
    if CONFIG[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪజ")]:
      bstack11ll1111l_opy_(bstack11111_opy_)
    if bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪఝ") in CONFIG and bstackl_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ఞ") in CONFIG[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬట")][bstack1llll11l_opy_]:
      bstack1l1l11_opy_ = CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ఠ")][bstack1llll11l_opy_][bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩడ")]
    import urllib
    import json
    bstack1lllllll_opy_ = bstackl_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧఢ") + urllib.parse.quote(json.dumps(bstack11111_opy_))
    browser = self.connect(bstack1lllllll_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1l111l_opy_():
    global bstack1l11lll11_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1lll1l1l1_opy_
        bstack1l11lll11_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l1llll1l_opy_
      bstack1l11lll11_opy_ = True
    except Exception as e:
      pass
def bstack1111l1l1_opy_(context, bstack11l1ll_opy_):
  try:
    context.page.evaluate(bstackl_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢణ"), bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫత")+ json.dumps(bstack11l1ll_opy_) + bstackl_opy_ (u"ࠣࡿࢀࠦథ"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢద"), e)
def bstack1ll1ll111_opy_(context, message, level):
  try:
    context.page.evaluate(bstackl_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦధ"), bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩన") + json.dumps(message) + bstackl_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨ఩") + json.dumps(level) + bstackl_opy_ (u"࠭ࡽࡾࠩప"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥఫ"), e)
def bstack1lll11l_opy_(context, status, message = bstackl_opy_ (u"ࠣࠤబ")):
  try:
    if(status == bstackl_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤభ")):
      context.page.evaluate(bstackl_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦమ"), bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠬయ") + json.dumps(bstackl_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦࠢర") + str(message)) + bstackl_opy_ (u"࠭ࠬࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠪఱ") + json.dumps(status) + bstackl_opy_ (u"ࠢࡾࡿࠥల"))
    else:
      context.page.evaluate(bstackl_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤళ"), bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠪఴ") + json.dumps(status) + bstackl_opy_ (u"ࠥࢁࢂࠨవ"))
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠣశ"), e)
def bstack1ll1l11l_opy_(self, url):
  global bstack1l11111l1_opy_
  try:
    bstack1ll111l_opy_(url)
  except Exception as err:
    logger.debug(bstack11lllll1_opy_.format(str(err)))
  try:
    bstack1l11111l1_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1l11l11_opy_ = str(e)
      if any(err_msg in bstack1l1l11l11_opy_ for err_msg in bstack11llll1ll_opy_):
        bstack1ll111l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11lllll1_opy_.format(str(err)))
    raise e
def bstack111ll_opy_(self):
  global bstack1l11111l_opy_
  bstack1l11111l_opy_ = self
  return
def bstack11llll_opy_(self, test):
  global CONFIG
  global bstack1l11111l_opy_
  global bstack1lllll111_opy_
  global bstack1ll1l1l_opy_
  global bstack1l1l11_opy_
  global bstack1l11ll11l_opy_
  global bstack111l111_opy_
  global bstack1ll1111_opy_
  try:
    if not bstack1lllll111_opy_:
      with open(os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠬࢄࠧష")), bstackl_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭స"), bstackl_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩహ"))) as f:
        bstack1l11lllll_opy_ = json.loads(bstackl_opy_ (u"ࠣࡽࠥ఺") + f.read().strip() + bstackl_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫ఻") + bstackl_opy_ (u"ࠥࢁ఼ࠧ"))
        bstack1lllll111_opy_ = bstack1l11lllll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1ll1111_opy_:
    for driver in bstack1ll1111_opy_:
      if bstack1lllll111_opy_ == driver.session_id:
        if test:
          bstack1l1ll11_opy_ = str(test.data)
        if not bstack11ll_opy_ and bstack1l1ll11_opy_:
          bstack111l1_opy_ = {
            bstackl_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫఽ"): bstackl_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ా"),
            bstackl_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩి"): {
              bstackl_opy_ (u"ࠧ࡯ࡣࡰࡩࠬీ"): bstack1l1ll11_opy_
            }
          }
          bstack11lll11ll_opy_ = bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ు").format(json.dumps(bstack111l1_opy_))
          driver.execute_script(bstack11lll11ll_opy_)
        if bstack1ll1l1l_opy_:
          bstack11lll111l_opy_ = {
            bstackl_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩూ"): bstackl_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬృ"),
            bstackl_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧౄ"): {
              bstackl_opy_ (u"ࠬࡪࡡࡵࡣࠪ౅"): bstack1l1ll11_opy_ + bstackl_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨె"),
              bstackl_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ే"): bstackl_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ై")
            }
          }
          bstack111l1_opy_ = {
            bstackl_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ౉"): bstackl_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ొ"),
            bstackl_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧో"): {
              bstackl_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬౌ"): bstackl_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ్࠭")
            }
          }
          if bstack1ll1l1l_opy_.status == bstackl_opy_ (u"ࠧࡑࡃࡖࡗࠬ౎"):
            bstack11lllll_opy_ = bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭౏").format(json.dumps(bstack11lll111l_opy_))
            driver.execute_script(bstack11lllll_opy_)
            bstack11lll11ll_opy_ = bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ౐").format(json.dumps(bstack111l1_opy_))
            driver.execute_script(bstack11lll11ll_opy_)
          elif bstack1ll1l1l_opy_.status == bstackl_opy_ (u"ࠪࡊࡆࡏࡌࠨ౑"):
            reason = bstackl_opy_ (u"ࠦࠧ౒")
            bstack1ll1l11_opy_ = bstack1l1ll11_opy_ + bstackl_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩ࠭౓")
            if bstack1ll1l1l_opy_.message:
              reason = str(bstack1ll1l1l_opy_.message)
              bstack1ll1l11_opy_ = bstack1ll1l11_opy_ + bstackl_opy_ (u"࠭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥ࠭౔") + reason
            bstack11lll111l_opy_[bstackl_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵౕࠪ")] = {
              bstackl_opy_ (u"ࠨ࡮ࡨࡺࡪࡲౖࠧ"): bstackl_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ౗"),
              bstackl_opy_ (u"ࠪࡨࡦࡺࡡࠨౘ"): bstack1ll1l11_opy_
            }
            bstack111l1_opy_[bstackl_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧౙ")] = {
              bstackl_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬౚ"): bstackl_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭౛"),
              bstackl_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ౜"): reason
            }
            bstack11lllll_opy_ = bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ౝ").format(json.dumps(bstack11lll111l_opy_))
            driver.execute_script(bstack11lllll_opy_)
            bstack11lll11ll_opy_ = bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ౞").format(json.dumps(bstack111l1_opy_))
            driver.execute_script(bstack11lll11ll_opy_)
  elif bstack1lllll111_opy_:
    try:
      data = {}
      bstack1l1ll11_opy_ = None
      if test:
        bstack1l1ll11_opy_ = str(test.data)
      if not bstack11ll_opy_ and bstack1l1ll11_opy_:
        data[bstackl_opy_ (u"ࠪࡲࡦࡳࡥࠨ౟")] = bstack1l1ll11_opy_
      if bstack1ll1l1l_opy_:
        if bstack1ll1l1l_opy_.status == bstackl_opy_ (u"ࠫࡕࡇࡓࡔࠩౠ"):
          data[bstackl_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬౡ")] = bstackl_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ౢ")
        elif bstack1ll1l1l_opy_.status == bstackl_opy_ (u"ࠧࡇࡃࡌࡐࠬౣ"):
          data[bstackl_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ౤")] = bstackl_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ౥")
          if bstack1ll1l1l_opy_.message:
            data[bstackl_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ౦")] = str(bstack1ll1l1l_opy_.message)
      user = CONFIG[bstackl_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭౧")]
      key = CONFIG[bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ౨")]
      url = bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠲ࡿࢂ࠴ࡪࡴࡱࡱࠫ౩").format(user, key, bstack1lllll111_opy_)
      headers = {
        bstackl_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭౪"): bstackl_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ౫"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1lll111l_opy_.format(str(e)))
  if bstack1l11111l_opy_:
    bstack111l111_opy_(bstack1l11111l_opy_)
  bstack1l11ll11l_opy_(self, test)
def bstack1ll1l1lll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11111ll_opy_
  bstack11111ll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1ll1l1l_opy_
  bstack1ll1l1l_opy_ = self._test
def bstack111l_opy_():
  global bstack1l1lll1l_opy_
  if os.path.exists(bstack1l1lll1l_opy_):
    os.remove(bstack1l1lll1l_opy_)
def bstack1ll1lll1l_opy_():
  global bstack1l1lll1l_opy_
  if not os.path.isfile(bstack1l1lll1l_opy_):
    with open(bstack1l1lll1l_opy_, bstackl_opy_ (u"ࠩࡺࠫ౬")):
      pass
    with open(bstack1l1lll1l_opy_, bstackl_opy_ (u"ࠥࡻ࠰ࠨ౭")) as outfile:
      json.dump({}, outfile)
  bstack1111llll_opy_ = {}
  if os.path.exists(bstack1l1lll1l_opy_):
    bstack1111llll_opy_ = json.load(open(bstack1l1lll1l_opy_, bstackl_opy_ (u"ࠫࡷࡨࠧ౮")))
  return bstack1111llll_opy_
def bstack1l1l111_opy_(platform_index, item_index):
  global bstack1l1lll1l_opy_
  bstack1111llll_opy_ = bstack1ll1lll1l_opy_()
  bstack1111llll_opy_[item_index] = platform_index
  with open(bstack1l1lll1l_opy_, bstackl_opy_ (u"ࠧࡽࠫࠣ౯")) as outfile:
    json.dump(bstack1111llll_opy_, outfile)
def bstack11lll1l1l_opy_(bstack111l11l_opy_):
  global CONFIG
  bstack1l1l1l11l_opy_ = bstackl_opy_ (u"࠭ࠧ౰")
  if not bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౱") in CONFIG:
    logger.info(bstackl_opy_ (u"ࠨࡐࡲࠤࡵࡲࡡࡵࡨࡲࡶࡲࡹࠠࡱࡣࡶࡷࡪࡪࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡸࡥࡱࡱࡵࡸࠥ࡬࡯ࡳࠢࡕࡳࡧࡵࡴࠡࡴࡸࡲࠬ౲"))
  try:
    platform = CONFIG[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౳")][bstack111l11l_opy_]
    if bstackl_opy_ (u"ࠪࡳࡸ࠭౴") in platform:
      bstack1l1l1l11l_opy_ += str(platform[bstackl_opy_ (u"ࠫࡴࡹࠧ౵")]) + bstackl_opy_ (u"ࠬ࠲ࠠࠨ౶")
    if bstackl_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ౷") in platform:
      bstack1l1l1l11l_opy_ += str(platform[bstackl_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ౸")]) + bstackl_opy_ (u"ࠨ࠮ࠣࠫ౹")
    if bstackl_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭౺") in platform:
      bstack1l1l1l11l_opy_ += str(platform[bstackl_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ౻")]) + bstackl_opy_ (u"ࠫ࠱ࠦࠧ౼")
    if bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ౽") in platform:
      bstack1l1l1l11l_opy_ += str(platform[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ౾")]) + bstackl_opy_ (u"ࠧ࠭ࠢࠪ౿")
    if bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ಀ") in platform:
      bstack1l1l1l11l_opy_ += str(platform[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧಁ")]) + bstackl_opy_ (u"ࠪ࠰ࠥ࠭ಂ")
    if bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬಃ") in platform:
      bstack1l1l1l11l_opy_ += str(platform[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭಄")]) + bstackl_opy_ (u"࠭ࠬࠡࠩಅ")
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠧࡔࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡶࡪࡶ࡯ࡳࡶࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡴࡴࠧಆ") + str(e))
  finally:
    if bstack1l1l1l11l_opy_[len(bstack1l1l1l11l_opy_) - 2:] == bstackl_opy_ (u"ࠨ࠮ࠣࠫಇ"):
      bstack1l1l1l11l_opy_ = bstack1l1l1l11l_opy_[:-2]
    return bstack1l1l1l11l_opy_
def bstack11l11l_opy_(path, bstack1l1l1l11l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1lll1l111_opy_ = ET.parse(path)
    bstack1l11l111l_opy_ = bstack1lll1l111_opy_.getroot()
    bstack11l1ll11_opy_ = None
    for suite in bstack1l11l111l_opy_.iter(bstackl_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨಈ")):
      if bstackl_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪಉ") in suite.attrib:
        suite.attrib[bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩಊ")] += bstackl_opy_ (u"ࠬࠦࠧಋ") + bstack1l1l1l11l_opy_
        bstack11l1ll11_opy_ = suite
    bstack111l1ll1_opy_ = None
    for robot in bstack1l11l111l_opy_.iter(bstackl_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬಌ")):
      bstack111l1ll1_opy_ = robot
    bstack1ll11l1l_opy_ = len(bstack111l1ll1_opy_.findall(bstackl_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭಍")))
    if bstack1ll11l1l_opy_ == 1:
      bstack111l1ll1_opy_.remove(bstack111l1ll1_opy_.findall(bstackl_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧಎ"))[0])
      bstack11ll1l1_opy_ = ET.Element(bstackl_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨಏ"), attrib={bstackl_opy_ (u"ࠪࡲࡦࡳࡥࠨಐ"):bstackl_opy_ (u"ࠫࡘࡻࡩࡵࡧࡶࠫ಑"), bstackl_opy_ (u"ࠬ࡯ࡤࠨಒ"):bstackl_opy_ (u"࠭ࡳ࠱ࠩಓ")})
      bstack111l1ll1_opy_.insert(1, bstack11ll1l1_opy_)
      bstack11ll11111_opy_ = None
      for suite in bstack111l1ll1_opy_.iter(bstackl_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ಔ")):
        bstack11ll11111_opy_ = suite
      bstack11ll11111_opy_.append(bstack11l1ll11_opy_)
      bstack1l1l1_opy_ = None
      for status in bstack11l1ll11_opy_.iter(bstackl_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨಕ")):
        bstack1l1l1_opy_ = status
      bstack11ll11111_opy_.append(bstack1l1l1_opy_)
    bstack1lll1l111_opy_.write(path)
  except Exception as e:
    logger.debug(bstackl_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠧಖ") + str(e))
def bstack1ll1l1l11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11lll11l1_opy_
  global CONFIG
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstackl_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢಗ") in options:
    del options[bstackl_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣಘ")]
  if ROBOT_VERSION < bstackl_opy_ (u"ࠧ࠺࠮࠱ࠤಙ"):
    stats = {
      bstackl_opy_ (u"ࠨࡣࡳ࡫ࡷ࡭ࡨࡧ࡬ࠣಚ"): {bstackl_opy_ (u"ࠢࡵࡱࡷࡥࡱࠨಛ"): 0, bstackl_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣಜ"): 0, bstackl_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤಝ"): 0},
      bstackl_opy_ (u"ࠥࡥࡱࡲࠢಞ"): {bstackl_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࠥಟ"): 0, bstackl_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧಠ"): 0, bstackl_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨಡ"): 0},
    }
  else:
    stats = {
      bstackl_opy_ (u"ࠢࡵࡱࡷࡥࡱࠨಢ"): 0,
      bstackl_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣಣ"): 0,
      bstackl_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤತ"): 0,
      bstackl_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦಥ"): 0,
    }
  bstack1l1l1lll_opy_ = bstack1ll1lll1l_opy_()
  for bstack1l11l11ll_opy_ in bstack1l1l1lll_opy_.keys():
    path = os.path.join(os.getcwd(), bstackl_opy_ (u"ࠫࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠫದ"), str(bstack1l11l11ll_opy_), bstackl_opy_ (u"ࠬࡵࡵࡵࡲࡸࡸ࠳ࡾ࡭࡭ࠩಧ"))
    bstack11l11l_opy_(path, bstack11lll1l1l_opy_(bstack1l1l1lll_opy_[bstack1l11l11ll_opy_]))
  bstack111l_opy_()
  return bstack11lll11l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1lll11ll1_opy_(self, ff_profile_dir):
  global bstack1ll1lll11_opy_
  if not ff_profile_dir:
    return None
  return bstack1ll1lll11_opy_(self, ff_profile_dir)
def bstack1llll11l1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11111l11_opy_
  bstack11ll1l1l1_opy_ = []
  if bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩನ") in CONFIG:
    bstack11ll1l1l1_opy_ = CONFIG[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ಩")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstackl_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤಪ")],
      pabot_args[bstackl_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥಫ")],
      argfile,
      pabot_args.get(bstackl_opy_ (u"ࠥ࡬࡮ࡼࡥࠣಬ")),
      pabot_args[bstackl_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢಭ")],
      platform[0],
      bstack11111l11_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstackl_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧಮ")] or [(bstackl_opy_ (u"ࠨࠢಯ"), None)]
    for platform in enumerate(bstack11ll1l1l1_opy_)
  ]
def bstack11llllll_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack11ll1111_opy_=bstackl_opy_ (u"ࠧࠨರ")):
  global bstack111ll11l_opy_
  self.platform_index = platform_index
  self.bstack11llll1l_opy_ = bstack11ll1111_opy_
  bstack111ll11l_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1ll111lll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack111ll1l_opy_
  global bstack1l11l1l_opy_
  if not bstackl_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪಱ") in item.options:
    item.options[bstackl_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫಲ")] = []
  for v in item.options[bstackl_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬಳ")]:
    if bstackl_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪ಴") in v:
      item.options[bstackl_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧವ")].remove(v)
    if bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ಶ") in v:
      item.options[bstackl_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩಷ")].remove(v)
  item.options[bstackl_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪಸ")].insert(0, bstackl_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫಹ").format(item.platform_index))
  item.options[bstackl_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ಺")].insert(0, bstackl_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫ಻").format(item.bstack11llll1l_opy_))
  if bstack1l11l1l_opy_:
    item.options[bstackl_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫಼ࠧ")].insert(0, bstackl_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩಽ").format(bstack1l11l1l_opy_))
  return bstack111ll1l_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1111l111_opy_(command, item_index):
  global bstack1l11l1l_opy_
  if bstack1l11l1l_opy_:
    command[0] = command[0].replace(bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ಾ"), bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬಿ") + str(item_index) + bstack1l11l1l_opy_, 1)
  else:
    command[0] = command[0].replace(bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨೀ"), bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧು") + str(item_index), 1)
def bstack1l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1lll1l1_opy_
  bstack1111l111_opy_(command, item_index)
  return bstack1lll1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11lllll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1lll1l1_opy_
  bstack1111l111_opy_(command, item_index)
  return bstack1lll1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack11l11l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1lll1l1_opy_
  bstack1111l111_opy_(command, item_index)
  return bstack1lll1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1ll1lll_opy_(self, runner, quiet=False, capture=True):
  global bstack1l1lll11l_opy_
  bstack111l11ll_opy_ = bstack1l1lll11l_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstackl_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫೂ")):
      runner.exception_arr = []
    if not hasattr(runner, bstackl_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳࠩೃ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack111l11ll_opy_
def bstack1l1lll1ll_opy_(self, name, context, *args):
  global bstack1l1l1l111_opy_
  if name in [bstackl_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧೄ"), bstackl_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ೅")]:
    bstack1l1l1l111_opy_(self, name, context, *args)
  if name == bstackl_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩೆ"):
    try:
      if(not bstack11ll_opy_):
        bstack11l1ll_opy_ = str(self.feature.name)
        bstack1111l1l1_opy_(context, bstack11l1ll_opy_)
        context.browser.execute_script(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧೇ") + json.dumps(bstack11l1ll_opy_) + bstackl_opy_ (u"ࠪࢁࢂ࠭ೈ"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ೉").format(str(e)))
  if name == bstackl_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧೊ"):
    try:
      if not hasattr(self, bstackl_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨೋ")):
        self.driver_before_scenario = True
      if(not bstack11ll_opy_):
        bstack11l1l_opy_ = args[0].name
        bstack1l1ll1l1l_opy_ = bstack11l1ll_opy_ = str(self.feature.name)
        bstack11l1ll_opy_ = bstack1l1ll1l1l_opy_ + bstackl_opy_ (u"ࠧࠡ࠯ࠣࠫೌ") + bstack11l1l_opy_
        if self.driver_before_scenario:
          bstack1111l1l1_opy_(context, bstack11l1ll_opy_)
          context.browser.execute_script(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾್ࠥ࠭") + json.dumps(bstack11l1ll_opy_) + bstackl_opy_ (u"ࠩࢀࢁࠬ೎"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫ೏").format(str(e)))
  if name == bstackl_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ೐"):
    try:
      bstack1llllllll_opy_ = args[0].status.name
      if str(bstack1llllllll_opy_).lower() == bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ೑"):
        bstack11llllll1_opy_ = bstackl_opy_ (u"࠭ࠧ೒")
        bstack1l11l11l_opy_ = bstackl_opy_ (u"ࠧࠨ೓")
        bstack1ll111111_opy_ = bstackl_opy_ (u"ࠨࠩ೔")
        try:
          import traceback
          bstack11llllll1_opy_ = self.exception.__class__.__name__
          bstack1l11lll_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1l11l11l_opy_ = bstackl_opy_ (u"ࠩࠣࠫೕ").join(bstack1l11lll_opy_)
          bstack1ll111111_opy_ = bstack1l11lll_opy_[-1]
        except Exception as e:
          logger.debug(bstack1ll1l1ll1_opy_.format(str(e)))
        bstack11llllll1_opy_ += bstack1ll111111_opy_
        bstack1ll1ll111_opy_(context, json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤೖ") + str(bstack1l11l11l_opy_)), bstackl_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ೗"))
        if self.driver_before_scenario:
          bstack1lll11l_opy_(context, bstackl_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ೘"), bstack11llllll1_opy_)
        context.browser.execute_script(bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ೙") + json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ೚") + str(bstack1l11l11l_opy_)) + bstackl_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ೛"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩ೜") + json.dumps(bstackl_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢೝ") + str(bstack11llllll1_opy_)) + bstackl_opy_ (u"ࠫࢂࢃࠧೞ"))
      else:
        bstack1ll1ll111_opy_(context, bstackl_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨ೟"), bstackl_opy_ (u"ࠨࡩ࡯ࡨࡲࠦೠ"))
        if self.driver_before_scenario:
          bstack1lll11l_opy_(context, bstackl_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢೡ"))
        context.browser.execute_script(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ೢ") + json.dumps(str(args[0].name) + bstackl_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨೣ")) + bstackl_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩ೤"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧࡶࡡࡴࡵࡨࡨࠧࢃࡽࠨ೥"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ೦").format(str(e)))
  if name == bstackl_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭೧"):
    try:
      if context.failed is True:
        bstack1ll1ll_opy_ = []
        bstack1l111l11_opy_ = []
        bstack1111l1ll_opy_ = []
        bstack1l1ll11l1_opy_ = bstackl_opy_ (u"ࠧࠨ೨")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1ll1ll_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1l11lll_opy_ = traceback.format_tb(exc_tb)
            bstack111lllll_opy_ = bstackl_opy_ (u"ࠨࠢࠪ೩").join(bstack1l11lll_opy_)
            bstack1l111l11_opy_.append(bstack111lllll_opy_)
            bstack1111l1ll_opy_.append(bstack1l11lll_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll1l1ll1_opy_.format(str(e)))
        bstack11llllll1_opy_ = bstackl_opy_ (u"ࠩࠪ೪")
        for i in range(len(bstack1ll1ll_opy_)):
          bstack11llllll1_opy_ += bstack1ll1ll_opy_[i] + bstack1111l1ll_opy_[i] + bstackl_opy_ (u"ࠪࡠࡳ࠭೫")
        bstack1l1ll11l1_opy_ = bstackl_opy_ (u"ࠫࠥ࠭೬").join(bstack1l111l11_opy_)
        if not self.driver_before_scenario:
          bstack1ll1ll111_opy_(context, bstack1l1ll11l1_opy_, bstackl_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ೭"))
          bstack1lll11l_opy_(context, bstackl_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ೮"), bstack11llllll1_opy_)
          context.browser.execute_script(bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ೯") + json.dumps(bstack1l1ll11l1_opy_) + bstackl_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ೰"))
          context.browser.execute_script(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩೱ") + json.dumps(bstackl_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣೲ") + str(bstack11llllll1_opy_)) + bstackl_opy_ (u"ࠫࢂࢃࠧೳ"))
      else:
        if not self.driver_before_scenario:
          bstack1ll1ll111_opy_(context, bstackl_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣ೴") + str(self.feature.name) + bstackl_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣ೵"), bstackl_opy_ (u"ࠢࡪࡰࡩࡳࠧ೶"))
          bstack1lll11l_opy_(context, bstackl_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ೷"))
          context.browser.execute_script(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ೸") + json.dumps(bstackl_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨ೹") + str(self.feature.name) + bstackl_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨ೺")) + bstackl_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ೻"))
          context.browser.execute_script(bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࡾࡿࠪ೼"))
    except Exception as e:
      logger.debug(bstackl_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ೽").format(str(e)))
  if name in [bstackl_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ೾"), bstackl_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ೿")]:
    bstack1l1l1l111_opy_(self, name, context, *args)
    if (name == bstackl_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫഀ") and self.driver_before_scenario) or (name == bstackl_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫഁ") and not self.driver_before_scenario):
      try:
        context.browser.quit()
      except Exception:
        pass
def bstack11llll111_opy_(config, startdir):
  return bstackl_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥം").format(bstackl_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧഃ"))
class Notset:
  def __repr__(self):
    return bstackl_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤഄ")
notset = Notset()
def bstack1llll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll1lllll_opy_
  if str(name).lower() == bstackl_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨഅ"):
    return bstackl_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣആ")
  else:
    return bstack1ll1lllll_opy_(self, name, default, skip)
def bstack1l111l1ll_opy_(item, when):
  global bstack111llll1_opy_
  try:
    bstack111llll1_opy_(item, when)
  except Exception as e:
    pass
def bstack1l11ll111_opy_():
  return
def bstack1lllll1l_opy_(bstack1l1l1111l_opy_):
  global bstack1ll1l1111_opy_
  global bstack1l11lll11_opy_
  bstack1ll1l1111_opy_ = bstack1l1l1111l_opy_
  logger.info(bstack1l111ll1l_opy_.format(bstack1ll1l1111_opy_.split(bstackl_opy_ (u"ࠪ࠱ࠬഇ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    Service.start = bstack11l1lll1_opy_
    Service.stop = bstack1l11ll1l_opy_
    webdriver.Remote.__init__ = bstack1111ll1_opy_
    webdriver.Remote.get = bstack1ll1l11l_opy_
    WebDriver.close = bstack11ll11_opy_
    bstack1l11lll11_opy_ = True
  except Exception as e:
    pass
  bstack1l1l111l_opy_()
  if not bstack1l11lll11_opy_:
    bstack1ll1l1l1l_opy_(bstackl_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨഈ"), bstack1lll111_opy_)
  if bstack11l1111l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l11l1l1_opy_
    except Exception as e:
      logger.error(bstack1lll1ll_opy_.format(str(e)))
  if (bstackl_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫഉ") in str(bstack1l1l1111l_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1lll11ll1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack111ll_opy_
      except Exception as e:
        logger.warn(bstack1111111_opy_ + str(e))
    except Exception as e:
      bstack1ll1l1l1l_opy_(e, bstack1111111_opy_)
    Output.end_test = bstack11llll_opy_
    TestStatus.__init__ = bstack1ll1l1lll_opy_
    QueueItem.__init__ = bstack11llllll_opy_
    pabot._create_items = bstack1llll11l1_opy_
    try:
      from pabot import __version__ as bstack1llll1ll_opy_
      if version.parse(bstack1llll1ll_opy_) >= version.parse(bstackl_opy_ (u"࠭࠲࠯࠳࠸࠲࠵࠭ഊ")):
        pabot._run = bstack11l11l11_opy_
      elif version.parse(bstack1llll1ll_opy_) >= version.parse(bstackl_opy_ (u"ࠧ࠳࠰࠴࠷࠳࠶ࠧഋ")):
        pabot._run = bstack11lllll1l_opy_
      else:
        pabot._run = bstack1l11l_opy_
    except Exception as e:
      pabot._run = bstack1l11l_opy_
    pabot._create_command_for_execution = bstack1ll111lll_opy_
    pabot._report_results = bstack1ll1l1l11_opy_
  if bstackl_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨഌ") in str(bstack1l1l1111l_opy_).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l1l1l_opy_(e, bstack1l1ll111_opy_)
    Runner.run_hook = bstack1l1lll1ll_opy_
    Step.run = bstack1ll1lll_opy_
  if bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ഍") in str(bstack1l1l1111l_opy_).lower():
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      from _pytest import runner
      pytest_selenium.pytest_report_header = bstack11llll111_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l11ll111_opy_
      Config.getoption = bstack1llll_opy_
      runner._update_current_test_var = bstack1l111l1ll_opy_
    except Exception as e:
      pass
def bstack1l11ll1_opy_():
  global CONFIG
  if bstackl_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪഎ") in CONFIG and int(CONFIG[bstackl_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫഏ")]) > 1:
    logger.warn(bstack1l11ll11_opy_)
def bstack1l1lll1_opy_(bstack1l111llll_opy_, index):
  bstack1lllll1l_opy_(bstack11ll1ll1_opy_)
  exec(open(bstack1l111llll_opy_).read())
def bstack1ll11l1_opy_(arg):
  arg.append(bstackl_opy_ (u"ࠧ࠳࠭ࡤࡣࡳࡸࡺࡸࡥ࠾ࡵࡼࡷࠧഐ"))
  arg.append(bstackl_opy_ (u"ࠨ࠭ࡘࠤ഑"))
  arg.append(bstackl_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡎࡱࡧࡹࡱ࡫ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡰࡴࡴࡸࡴࡦࡦ࠽ࡴࡾࡺࡥࡴࡶ࠱ࡔࡾࡺࡥࡴࡶ࡚ࡥࡷࡴࡩ࡯ࡩࠥഒ"))
  global CONFIG
  bstack1lllll1l_opy_(bstack1lllll1_opy_)
  os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩഓ")] = CONFIG[bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫഔ")]
  os.environ[bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ക")] = CONFIG[bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧഖ")]
  from _pytest.config import main as bstack11lllll11_opy_
  bstack11lllll11_opy_(arg)
def bstack11ll11l1l_opy_(arg):
  bstack1lllll1l_opy_(bstack1l1111lll_opy_)
  from behave.__main__ import main as bstack1111111l_opy_
  bstack1111111l_opy_(arg)
def bstack1l111l111_opy_():
  logger.info(bstack1l1l11111_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstackl_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫഗ"), help=bstackl_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧഘ"))
  parser.add_argument(bstackl_opy_ (u"ࠧ࠮ࡷࠪങ"), bstackl_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬച"), help=bstackl_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨഛ"))
  parser.add_argument(bstackl_opy_ (u"ࠪ࠱ࡰ࠭ജ"), bstackl_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪഝ"), help=bstackl_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ࠭ഞ"))
  parser.add_argument(bstackl_opy_ (u"࠭࠭ࡧࠩട"), bstackl_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬഠ"), help=bstackl_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഡ"))
  bstack1lll11_opy_ = parser.parse_args()
  try:
    bstack1ll11llll_opy_ = bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ഢ")
    if bstack1lll11_opy_.framework and bstack1lll11_opy_.framework not in (bstackl_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪണ"), bstackl_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬത")):
      bstack1ll11llll_opy_ = bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫഥ")
    bstack111lll11_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll11llll_opy_)
    bstack1111l11l_opy_ = open(bstack111lll11_opy_, bstackl_opy_ (u"࠭ࡲࠨദ"))
    bstack1ll1lll1_opy_ = bstack1111l11l_opy_.read()
    bstack1111l11l_opy_.close()
    if bstack1lll11_opy_.username:
      bstack1ll1lll1_opy_ = bstack1ll1lll1_opy_.replace(bstackl_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧധ"), bstack1lll11_opy_.username)
    if bstack1lll11_opy_.key:
      bstack1ll1lll1_opy_ = bstack1ll1lll1_opy_.replace(bstackl_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪന"), bstack1lll11_opy_.key)
    if bstack1lll11_opy_.framework:
      bstack1ll1lll1_opy_ = bstack1ll1lll1_opy_.replace(bstackl_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪഩ"), bstack1lll11_opy_.framework)
    file_name = bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭പ")
    file_path = os.path.abspath(file_name)
    bstack11lllllll_opy_ = open(file_path, bstackl_opy_ (u"ࠫࡼ࠭ഫ"))
    bstack11lllllll_opy_.write(bstack1ll1lll1_opy_)
    bstack11lllllll_opy_.close()
    logger.info(bstack1l111_opy_)
    try:
      os.environ[bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧബ")] = bstack1lll11_opy_.framework if bstack1lll11_opy_.framework != None else bstackl_opy_ (u"ࠨࠢഭ")
      config = yaml.safe_load(bstack1ll1lll1_opy_)
      config[bstackl_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧമ")] = bstackl_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡵࡨࡸࡺࡶࠧയ")
      bstack1lll11l1_opy_(bstack1ll1llll1_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1111l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack111l1l1l_opy_.format(str(e)))
def bstack1lll11l1_opy_(bstack11ll111l_opy_, config, bstack1l111l_opy_ = {}):
  global bstack11l1lllll_opy_
  if not config:
    return
  bstack1ll111_opy_ = bstack11l1ll1l_opy_ if not bstack11l1lllll_opy_ else ( bstack11lll1_opy_ if bstackl_opy_ (u"ࠩࡤࡴࡵ࠭ര") in config else bstack11ll1_opy_ )
  data = {
    bstackl_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬറ"): config[bstackl_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ല")],
    bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨള"): config[bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩഴ")],
    bstackl_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫവ"): bstack11ll111l_opy_,
    bstackl_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫശ"): {
      bstackl_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഷ"): str(config[bstackl_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪസ")]) if bstackl_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫഹ") in config else bstackl_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨഺ"),
      bstackl_opy_ (u"࠭ࡲࡦࡨࡨࡶࡷ࡫ࡲࠨ഻"): bstack1l1111l1l_opy_(os.getenv(bstackl_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠤ഼"), bstackl_opy_ (u"ࠣࠤഽ"))),
      bstackl_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫാ"): bstackl_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪി"),
      bstackl_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬീ"): bstack1ll111_opy_,
      bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨു"): config[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩൂ")]if config[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪൃ")] else bstackl_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤൄ"),
      bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൅"): str(config[bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬെ")]) if bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭േ") in config else bstackl_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨൈ"),
      bstackl_opy_ (u"࠭࡯ࡴࠩ൉"): sys.platform,
      bstackl_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩൊ"): socket.gethostname()
    }
  }
  update(data[bstackl_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫോ")], bstack1l111l_opy_)
  try:
    response = bstack1l1ll1l_opy_(bstackl_opy_ (u"ࠩࡓࡓࡘ࡚ࠧൌ"), bstack11l11ll_opy_, data, config)
    if response:
      logger.debug(bstack111ll111_opy_.format(bstack11ll111l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11l1l1l_opy_.format(str(e)))
def bstack1l1ll1l_opy_(type, url, data, config):
  bstack1l1l1l1ll_opy_ = bstack1l1llll11_opy_.format(url)
  proxy = bstack1llll11ll_opy_(config)
  proxies = {}
  response = {}
  if config.get(bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ്࠭")) or config.get(bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨൎ")):
    proxies = {
      bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ൏"): proxy
    }
  if type == bstackl_opy_ (u"࠭ࡐࡐࡕࡗࠫ൐"):
    response = requests.post(bstack1l1l1l1ll_opy_, json=data,
                    headers={bstackl_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭൑"): bstackl_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ൒")}, auth=(config[bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ൓")], config[bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ൔ")]), proxies=proxies)
  return response
def bstack1l1111l1l_opy_(framework):
  return bstackl_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣൕ").format(str(framework), __version__) if framework else bstackl_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨൖ").format(__version__)
def bstack11ll111_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack111l1111_opy_()
    logger.debug(bstack1ll1ll1l_opy_.format(str(CONFIG)))
    bstack11l1ll1_opy_()
    bstack1ll1111l1_opy_()
  except Exception as e:
    logger.error(bstackl_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥൗ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1lll1ll1_opy_
  atexit.register(bstack1l11_opy_)
  signal.signal(signal.SIGINT, bstack1ll11l111_opy_)
  signal.signal(signal.SIGTERM, bstack1ll11l111_opy_)
def bstack1lll1ll1_opy_(exctype, value, traceback):
  global bstack1ll1111_opy_
  try:
    for driver in bstack1ll1111_opy_:
      driver.execute_script(
        bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ࠮ࠣࠦࡷ࡫ࡡࡴࡱࡱࠦ࠿ࠦࠧ൘") + json.dumps(bstackl_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦ൙") + str(value)) + bstackl_opy_ (u"ࠩࢀࢁࠬ൚"))
  except Exception:
    pass
  bstack111llll_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack111llll_opy_(message = bstackl_opy_ (u"ࠪࠫ൛")):
  global CONFIG
  try:
    if message:
      bstack1l111l_opy_ = {
        bstackl_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ൜"): str(message)
      }
      bstack1lll11l1_opy_(bstack1lll1lll1_opy_, CONFIG, bstack1l111l_opy_)
    else:
      bstack1lll11l1_opy_(bstack1lll1lll1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1ll11_opy_.format(str(e)))
def bstack11111lll_opy_(bstack1ll11lll1_opy_, size):
  bstack11l111ll_opy_ = []
  while len(bstack1ll11lll1_opy_) > size:
    bstack1l111lll1_opy_ = bstack1ll11lll1_opy_[:size]
    bstack11l111ll_opy_.append(bstack1l111lll1_opy_)
    bstack1ll11lll1_opy_   = bstack1ll11lll1_opy_[size:]
  bstack11l111ll_opy_.append(bstack1ll11lll1_opy_)
  return bstack11l111ll_opy_
def run_on_browserstack():
  if len(sys.argv) <= 1:
    logger.critical(bstack1l1ll111l_opy_)
    return
  if sys.argv[1] == bstackl_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ൝")  or sys.argv[1] == bstackl_opy_ (u"࠭࠭ࡷࠩ൞"):
    logger.info(bstackl_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧൟ").format(__version__))
    return
  if sys.argv[1] == bstackl_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧൠ"):
    bstack1l111l111_opy_()
    return
  args = sys.argv
  bstack11ll111_opy_()
  global CONFIG
  global bstack1lll11l11_opy_
  global bstack11ll1l111_opy_
  global bstack1lll111l1_opy_
  global bstack11111l11_opy_
  global bstack1l11l1l_opy_
  bstack1l1l1ll_opy_ = bstackl_opy_ (u"ࠩࠪൡ")
  if args[1] == bstackl_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪൢ") or args[1] == bstackl_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬൣ"):
    bstack1l1l1ll_opy_ = bstackl_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ൤")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ൥"):
    bstack1l1l1ll_opy_ = bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭൦")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ൧"):
    bstack1l1l1ll_opy_ = bstackl_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ൨")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ൩"):
    bstack1l1l1ll_opy_ = bstackl_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ൪")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ൫"):
    bstack1l1l1ll_opy_ = bstackl_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭൬")
    args = args[2:]
  elif args[1] == bstackl_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ൭"):
    bstack1l1l1ll_opy_ = bstackl_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ൮")
    args = args[2:]
  else:
    if not bstackl_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ൯") in CONFIG or str(CONFIG[bstackl_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭൰")]).lower() in [bstackl_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ൱"), bstackl_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭൲")]:
      bstack1l1l1ll_opy_ = bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൳")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ൴")]).lower() == bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ൵"):
      bstack1l1l1ll_opy_ = bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ൶")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭൷")]).lower() == bstackl_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ൸"):
      bstack1l1l1ll_opy_ = bstackl_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ൹")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩൺ")]).lower() == bstackl_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧൻ"):
      bstack1l1l1ll_opy_ = bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨർ")
      args = args[1:]
    elif str(CONFIG[bstackl_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬൽ")]).lower() == bstackl_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪൾ"):
      bstack1l1l1ll_opy_ = bstackl_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫൿ")
      args = args[1:]
    else:
      os.environ[bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ඀")] = bstack1l1l1ll_opy_
      bstack1l1l11ll1_opy_(bstack1lll11l1l_opy_)
  global bstack111l1lll_opy_
  try:
    os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨඁ")] = bstack1l1l1ll_opy_
    bstack1lll11l1_opy_(bstack11lll1ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1ll11_opy_.format(str(e)))
  global bstack11ll11ll1_opy_
  global bstack1l11ll11l_opy_
  global bstack111l111_opy_
  global bstack11111ll_opy_
  global bstack1ll1lll11_opy_
  global bstack1lll1l1_opy_
  global bstack111ll11l_opy_
  global bstack111ll1l_opy_
  global bstack1l1l1l11_opy_
  global bstack1l1l1l111_opy_
  global bstack1l1lll11l_opy_
  global bstack1l11111l1_opy_
  global bstack1llllll1_opy_
  global bstack1ll1lllll_opy_
  global bstack111llll1_opy_
  global bstack11lll11l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11ll11ll1_opy_ = webdriver.Remote.__init__
    bstack1l1l1l11_opy_ = WebDriver.close
    bstack1l11111l1_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack111l1lll_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack1l11ll_opy_():
    if bstack1l11111_opy_() < version.parse(bstack1ll1l111l_opy_):
      logger.error(bstack1l11l1l11_opy_.format(bstack1l11111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1llllll1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1lll1ll_opy_.format(str(e)))
  bstack11l1l1ll_opy_()
  if (bstack1l1l1ll_opy_ in [bstackl_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ං"), bstackl_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧඃ"), bstackl_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ඄")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1lll11ll1_opy_
        bstack111l111_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1111111_opy_ + str(e))
    except Exception as e:
      bstack1ll1l1l1l_opy_(e, bstack1111111_opy_)
    if bstack1l1l1ll_opy_ != bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫඅ"):
      bstack111l_opy_()
    bstack1l11ll11l_opy_ = Output.end_test
    bstack11111ll_opy_ = TestStatus.__init__
    bstack1lll1l1_opy_ = pabot._run
    bstack111ll11l_opy_ = QueueItem.__init__
    bstack111ll1l_opy_ = pabot._create_command_for_execution
    bstack11lll11l1_opy_ = pabot._report_results
  if bstack1l1l1ll_opy_ == bstackl_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫආ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1l1l1l_opy_(e, bstack1l1ll111_opy_)
    bstack1l1l1l111_opy_ = Runner.run_hook
    bstack1l1lll11l_opy_ = Step.run
  if bstack1l1l1ll_opy_ == bstackl_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬඇ"):
    try:
      from _pytest.config import Config
      bstack1ll1lllll_opy_ = Config.getoption
      from _pytest import runner
      bstack111llll1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11lll1l1_opy_)
  if bstack1l1l1ll_opy_ == bstackl_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ඈ"):
    bstack1lll1ll1l_opy_()
    bstack1l11ll1_opy_()
    if bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪඉ") in CONFIG:
      bstack11ll1l111_opy_ = True
      bstack1ll1111l_opy_ = []
      for index, platform in enumerate(CONFIG[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫඊ")]):
        bstack1ll1111l_opy_.append(bstack1l11ll1ll_opy_(name=str(index),
                                      target=bstack1l1lll1_opy_, args=(args[0], index)))
      for t in bstack1ll1111l_opy_:
        t.start()
      for t in bstack1ll1111l_opy_:
        t.join()
    else:
      bstack1lllll1l_opy_(bstack11ll1ll1_opy_)
      exec(open(args[0]).read())
  elif bstack1l1l1ll_opy_ == bstackl_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨඋ") or bstack1l1l1ll_opy_ == bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩඌ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll1l1l1l_opy_(e, bstack1111111_opy_)
    bstack1lll1ll1l_opy_()
    bstack1lllll1l_opy_(bstack1l1l1ll1l_opy_)
    if bstackl_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩඍ") in args:
      i = args.index(bstackl_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪඎ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1lll11l11_opy_))
    args.insert(0, str(bstackl_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫඏ")))
    pabot.main(args)
  elif bstack1l1l1ll_opy_ == bstackl_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨඐ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll1l1l1l_opy_(e, bstack1111111_opy_)
    for a in args:
      if bstackl_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧඑ") in a:
        bstack1lll111l1_opy_ = int(a.split(bstackl_opy_ (u"ࠩ࠽ࠫඒ"))[1])
      if bstackl_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧඓ") in a:
        bstack11111l11_opy_ = str(a.split(bstackl_opy_ (u"ࠫ࠿࠭ඔ"))[1])
      if bstackl_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬඕ") in a:
        bstack1l11l1l_opy_ = str(a.split(bstackl_opy_ (u"࠭࠺ࠨඖ"))[1])
    bstack1l1l111l1_opy_ = None
    if bstackl_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭඗") in args:
      i = args.index(bstackl_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧ඘"))
      args.pop(i)
      bstack1l1l111l1_opy_ = args.pop(i)
    if bstack1l1l111l1_opy_ is not None:
      global bstack1l1l111ll_opy_
      bstack1l1l111ll_opy_ = bstack1l1l111l1_opy_
    bstack1lllll1l_opy_(bstack1l1l1ll1l_opy_)
    run_cli(args)
  elif bstack1l1l1ll_opy_ == bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ඙"):
    try:
      from _pytest.config import _prepareconfig
      from _pytest.config import Config
      from _pytest import runner
      import importlib
      bstack1l1llll1_opy_ = importlib.find_loader(bstackl_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬක"))
    except Exception as e:
      logger.warn(e, bstack11lll1l1_opy_)
    bstack1lll1ll1l_opy_()
    try:
      if bstackl_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ඛ") in args:
        i = args.index(bstackl_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧග"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩඝ") in args:
        i = args.index(bstackl_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪඞ"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠨ࠯ࡳࠫඟ") in args:
        i = args.index(bstackl_opy_ (u"ࠩ࠰ࡴࠬච"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫඡ") in args:
        i = args.index(bstackl_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬජ"))
        args.pop(i+1)
        args.pop(i)
      if bstackl_opy_ (u"ࠬ࠳࡮ࠨඣ") in args:
        i = args.index(bstackl_opy_ (u"࠭࠭࡯ࠩඤ"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack1l1ll1111_opy_ = config.args
    bstack1l1ll1l1_opy_ = config.invocation_params.args
    bstack1l1ll1l1_opy_ = list(bstack1l1ll1l1_opy_)
    bstack1l1lll_opy_ = []
    for arg in bstack1l1ll1l1_opy_:
      for spec in bstack1l1ll1111_opy_:
        if os.path.normpath(arg) != os.path.normpath(spec):
          bstack1l1lll_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstackl_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨඥ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l1ll1111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1111lll1_opy_)))
                    for bstack1111lll1_opy_ in bstack1l1ll1111_opy_]
    if (bstack11ll_opy_):
      bstack1l1lll_opy_.append(bstackl_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬඦ"))
      bstack1l1lll_opy_.append(bstackl_opy_ (u"ࠩࡗࡶࡺ࡫ࠧට"))
    bstack1l1lll_opy_.append(bstackl_opy_ (u"ࠪ࠱ࡵ࠭ඨ"))
    bstack1l1lll_opy_.append(bstackl_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩඩ"))
    bstack1l1lll_opy_.append(bstackl_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧඪ"))
    bstack1l1lll_opy_.append(bstackl_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ණ"))
    bstack111111_opy_ = []
    for spec in bstack1l1ll1111_opy_:
      bstack1ll111l1l_opy_ = []
      bstack1ll111l1l_opy_.append(spec)
      bstack1ll111l1l_opy_ += bstack1l1lll_opy_
      bstack111111_opy_.append(bstack1ll111l1l_opy_)
    bstack11ll1l111_opy_ = True
    bstack1l1lllll1_opy_ = 1
    if bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧඬ") in CONFIG:
      bstack1l1lllll1_opy_ = CONFIG[bstackl_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨත")]
    bstack1l11l1ll1_opy_ = int(bstack1l1lllll1_opy_)*int(len(CONFIG[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬථ")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ද")]):
      for bstack1ll111l1l_opy_ in bstack111111_opy_:
        item = {}
        item[bstackl_opy_ (u"ࠫࡦࡸࡧࠨධ")] = bstack1ll111l1l_opy_
        item[bstackl_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫන")] = index
        execution_items.append(item)
    bstack1l1111l1_opy_ = bstack11111lll_opy_(execution_items, bstack1l11l1ll1_opy_)
    for execution_item in bstack1l1111l1_opy_:
      bstack1ll1111l_opy_ = []
      for item in execution_item:
        bstack1ll1111l_opy_.append(bstack1l11ll1ll_opy_(name=str(item[bstackl_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ඲")]),
                                            target=bstack1ll11l1_opy_,
                                            args=(item[bstackl_opy_ (u"ࠧࡢࡴࡪࠫඳ")],)))
      for t in bstack1ll1111l_opy_:
        t.start()
      for t in bstack1ll1111l_opy_:
        t.join()
  elif bstack1l1l1ll_opy_ == bstackl_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨප"):
    try:
      from behave.__main__ import main as bstack1111111l_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll1l1l1l_opy_(e, bstack1l1ll111_opy_)
    bstack1lll1ll1l_opy_()
    bstack11ll1l111_opy_ = True
    bstack1l1lllll1_opy_ = 1
    if bstackl_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩඵ") in CONFIG:
      bstack1l1lllll1_opy_ = CONFIG[bstackl_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪබ")]
    bstack1l11l1ll1_opy_ = int(bstack1l1lllll1_opy_)*int(len(CONFIG[bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧභ")]))
    config = Configuration(args)
    bstack1l1ll1111_opy_ = config.paths
    bstack1111ll_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack1l1ll1111_opy_:
        bstack1111ll_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstackl_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭ම"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l1ll1111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1111lll1_opy_)))
                    for bstack1111lll1_opy_ in bstack1l1ll1111_opy_]
    bstack111111_opy_ = []
    for spec in bstack1l1ll1111_opy_:
      bstack1ll111l1l_opy_ = []
      bstack1ll111l1l_opy_ += bstack1111ll_opy_
      bstack1ll111l1l_opy_.append(spec)
      bstack111111_opy_.append(bstack1ll111l1l_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩඹ")]):
      for bstack1ll111l1l_opy_ in bstack111111_opy_:
        item = {}
        item[bstackl_opy_ (u"ࠧࡢࡴࡪࠫය")] = bstackl_opy_ (u"ࠨࠢࠪර").join(bstack1ll111l1l_opy_)
        item[bstackl_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ඼")] = index
        execution_items.append(item)
    bstack1l1111l1_opy_ = bstack11111lll_opy_(execution_items, bstack1l11l1ll1_opy_)
    for execution_item in bstack1l1111l1_opy_:
      bstack1ll1111l_opy_ = []
      for item in execution_item:
        bstack1ll1111l_opy_.append(bstack1l11ll1ll_opy_(name=str(item[bstackl_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩල")]),
                                            target=bstack11ll11l1l_opy_,
                                            args=(item[bstackl_opy_ (u"ࠫࡦࡸࡧࠨ඾")],)))
      for t in bstack1ll1111l_opy_:
        t.start()
      for t in bstack1ll1111l_opy_:
        t.join()
  else:
    bstack1l1l11ll1_opy_(bstack1lll11l1l_opy_)
  bstack1l1lll11_opy_()
def bstack1l1lll11_opy_():
  global CONFIG
  try:
    if bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ඿") in CONFIG:
      host = bstackl_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩව") if bstackl_opy_ (u"ࠧࡢࡲࡳࠫශ") in CONFIG else bstackl_opy_ (u"ࠨࡣࡳ࡭ࠬෂ")
      user = CONFIG[bstackl_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫස")]
      key = CONFIG[bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭හ")]
      bstack1l11lll1l_opy_ = bstackl_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪළ") if bstackl_opy_ (u"ࠬࡧࡰࡱࠩෆ") in CONFIG else bstackl_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ෇")
      url = bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠰࡭ࡷࡴࡴࠧ෈").format(user, key, host, bstack1l11lll1l_opy_)
      headers = {
        bstackl_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧ෉"): bstackl_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲ්ࠬ"),
      }
      if bstackl_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ෋") in CONFIG:
        params = {bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ෌"):CONFIG[bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ෍")], bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ෎"):CONFIG[bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩා")]}
      else:
        params = {bstackl_opy_ (u"ࠨࡰࡤࡱࡪ࠭ැ"):CONFIG[bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬෑ")]}
      response = requests.get(url, params=params, headers=headers)
      if response.json():
        bstack11l1_opy_ = response.json()[0][bstackl_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡣࡷ࡬ࡰࡩ࠭ි")]
        if bstack11l1_opy_:
          bstack1llll1ll1_opy_ = bstack11l1_opy_[bstackl_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨී")].split(bstackl_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧ࠲ࡨࡵࡪ࡮ࡧࠫු"))[0] + bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠵ࠧ෕") + bstack11l1_opy_[bstackl_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪූ")]
          logger.info(bstack1ll1l11l1_opy_.format(bstack1llll1ll1_opy_))
          bstack1l11llll1_opy_ = CONFIG[bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ෗")]
          if bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫෘ") in CONFIG:
            bstack1l11llll1_opy_ += bstackl_opy_ (u"ࠪࠤࠬෙ") + CONFIG[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ේ")]
          if bstack1l11llll1_opy_!= bstack11l1_opy_[bstackl_opy_ (u"ࠬࡴࡡ࡮ࡧࠪෛ")]:
            logger.debug(bstack1ll1l1_opy_.format(bstack11l1_opy_[bstackl_opy_ (u"࠭࡮ࡢ࡯ࡨࠫො")], bstack1l11llll1_opy_))
    else:
      logger.warn(bstack1ll1111ll_opy_)
  except Exception as e:
    logger.debug(bstack11ll1ll1l_opy_.format(str(e)))
def bstack1ll111l_opy_(url, bstack1lllll1l1_opy_=False):
  global CONFIG
  global bstack1l11llll_opy_
  if not bstack1l11llll_opy_:
    hostname = bstack1l111lll_opy_(url)
    is_private = bstack1ll11ll1_opy_(hostname)
    if (bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫෝ") in CONFIG and not CONFIG[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬෞ")]) and (is_private or bstack1lllll1l1_opy_):
      bstack1l11llll_opy_ = hostname
def bstack1l111lll_opy_(url):
  return urlparse(url).hostname
def bstack1ll11ll1_opy_(hostname):
  for bstack1l111l1_opy_ in bstack1l1ll1ll1_opy_:
    regex = re.compile(bstack1l111l1_opy_)
    if regex.match(hostname):
      return True
  return False