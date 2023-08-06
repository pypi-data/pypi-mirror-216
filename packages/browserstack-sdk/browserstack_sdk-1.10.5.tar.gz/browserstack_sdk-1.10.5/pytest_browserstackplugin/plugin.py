# coding: UTF-8
import sys
bstack1lll1_opy_ = sys.version_info [0] == 2
bstack1_opy_ = 2048
bstack11_opy_ = 7
def bstack1lll_opy_ (bstack1l1l_opy_):
    global bstack1l_opy_
    stringNr = ord (bstack1l1l_opy_ [-1])
    bstack1llll_opy_ = bstack1l1l_opy_ [:-1]
    bstack1111_opy_ = stringNr % len (bstack1llll_opy_)
    bstack1l11_opy_ = bstack1llll_opy_ [:bstack1111_opy_] + bstack1llll_opy_ [bstack1111_opy_:]
    if bstack1lll1_opy_:
        bstack1ll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1_opy_ - (bstack1ll_opy_ + stringNr) % bstack11_opy_) for bstack1ll_opy_, char in enumerate (bstack1l11_opy_)])
    else:
        bstack1ll1l_opy_ = str () .join ([chr (ord (char) - bstack1_opy_ - (bstack1ll_opy_ + stringNr) % bstack11_opy_) for bstack1ll_opy_, char in enumerate (bstack1l11_opy_)])
    return eval (bstack1ll1l_opy_)
import pytest
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
def bstack1ll1_opy_(page, bstack111l_opy_):
  try:
    page.evaluate(bstack1lll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧࠀ"), bstack1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩࠁ")+ json.dumps(bstack111l_opy_) + bstack1lll_opy_ (u"ࠨࡽࡾࠤࠂ"))
  except Exception as e:
    print(bstack1lll_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧࠃ"), e)
def bstack11ll_opy_(page, message, level):
  try:
    page.evaluate(bstack1lll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤࠄ"), bstack1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧࠅ") + json.dumps(message) + bstack1lll_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭ࠆ") + json.dumps(level) + bstack1lll_opy_ (u"ࠫࢂࢃࠧࠇ"))
  except Exception as e:
    print(bstack1lll_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣࠈ"), e)
def bstack11l_opy_(page, status, message = bstack1lll_opy_ (u"ࠨࠢࠉ")):
  try:
    if(status == bstack1lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢࠊ")):
      page.evaluate(bstack1lll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤࠋ"), bstack1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠪࠌ") + json.dumps(bstack1lll_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࠧࠍ") + str(message)) + bstack1lll_opy_ (u"ࠫ࠱ࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠨࠎ") + json.dumps(status) + bstack1lll_opy_ (u"ࠧࢃࡽࠣࠏ"))
    else:
      page.evaluate(bstack1lll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢࠐ"), bstack1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠨࠑ") + json.dumps(status) + bstack1lll_opy_ (u"ࠣࡿࢀࠦࠒ"))
  except Exception as e:
    print(bstack1lll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨࠓ"), e)
@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack11l1_opy_ = item.config.getoption(bstack1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬࠔ"))
    plugins = item.config.getoption(bstack1lll_opy_ (u"ࠦࡵࡲࡵࡨ࡫ࡱࡷࠧࠕ"))
    if(bstack1lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠥࠖ") not in plugins):
        return
    report = outcome.get_result()
    summary = []
    driver = getattr(item, bstack1lll_opy_ (u"ࠨ࡟ࡥࡴ࡬ࡺࡪࡸࠢࠗ"), None)
    page = getattr(item, bstack1lll_opy_ (u"ࠢࡠࡲࡤ࡫ࡪࠨ࠘"), None)
    if(driver is not None):
        bstack111_opy_(item, report, summary, bstack11l1_opy_)
    if(page is not None):
        bstack1l1_opy_(item, report, summary, bstack11l1_opy_)
def bstack111_opy_(item, report, summary, bstack11l1_opy_):
    if report.when in [bstack1lll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ࠙"), bstack1lll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦࠚ")]:
            return
    if(str(bstack11l1_opy_).lower() != bstack1lll_opy_ (u"ࠪࡸࡷࡻࡥࠨࠛ")):
        item._driver.execute_script(bstack1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩࠜ") + json.dumps(report.nodeid) + bstack1lll_opy_ (u"ࠬࢃࡽࠨࠝ"))
    passed = report.passed or (report.failed and hasattr(report, bstack1lll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣࠞ")))
    bstackl_opy_ = bstack1lll_opy_ (u"ࠢࠣࠟ")
    if not passed:
        try:
            bstackl_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1lll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣࠠ").format(e)
            )
    try:
        if passed:
            item._driver.execute_script(
                bstack1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠤࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࠡࡿࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠩࠡ")
            )
        else:
            if bstackl_opy_:
                item._driver.execute_script(
                    bstack1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ࠢ")
                    + json.dumps(str(bstackl_opy_))
                    + bstack1lll_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨࠣ")
                )
                item._driver.execute_script(
                    bstack1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠤࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠥ࠭ࠤ")
                    + json.dumps(str(bstackl_opy_))
                    + bstack1lll_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣࠥ")
                )
            else:
                item._driver.execute_script(
                    bstack1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠣࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡦࡢ࡫࡯ࡩࡩࠨࠠࡾࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠬࠦ")
                )
    except Exception as e:
        summary.append(bstack1lll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽ࠳ࢁࠧࠧ").format(e))
def bstack1l1_opy_(item, report, summary, bstack11l1_opy_):
    if report.when in [bstack1lll_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣࠨ"), bstack1lll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧࠩ")]:
            return
    if(str(bstack11l1_opy_).lower() != bstack1lll_opy_ (u"ࠫࡹࡸࡵࡦࠩࠪ")):
        bstack1ll1_opy_(item._page, report.nodeid)
    passed = report.passed or (report.failed and hasattr(report, bstack1lll_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢࠫ")))
    bstackl_opy_ = bstack1lll_opy_ (u"ࠨࠢࠬ")
    if not passed:
        try:
            bstackl_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1lll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢ࠭").format(e)
            )
    try:
        if passed:
            bstack11l_opy_(item._page, bstack1lll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ࠮"))
        else:
            if bstackl_opy_:
                bstack11ll_opy_(item._page, str(bstackl_opy_), bstack1lll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ࠯"))
                bstack11l_opy_(item._page, bstack1lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰"), str(bstackl_opy_))
            else:
                bstack11l_opy_(item._page, bstack1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ࠱"))
    except Exception as e:
        summary.append(bstack1lll_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁ࠰ࡾࠤ࠲").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1lll_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠳"), default=bstack1lll_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨ࠴"), help=bstack1lll_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢ࠵"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1lll_opy_ (u"ࠤ࠰࠱ࡩࡸࡩࡷࡧࡵࠦ࠶"), action=bstack1lll_opy_ (u"ࠥࡷࡹࡵࡲࡦࠤ࠷"), default=bstack1lll_opy_ (u"ࠦࡨ࡮ࡲࡰ࡯ࡨࠦ࠸"),
                        help=bstack1lll_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶࠦ࠹"))