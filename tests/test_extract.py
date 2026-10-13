from pathlib import Path

import pytest

from kaiji.extract import best_yen, extract, extract_kv, format_yen, parse_amounts
from kaiji.textutil import clean_text, join_wrapped_lines

FIX = Path(__file__).parent / "fixtures"


def load(name: str) -> str:
    return (FIX / name).read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "text,yen",
    [
        ("約45億円", 4.5e9),
        ("受注金額：147,000,000円", 1.47e8),
        ("20.4百万USドル（3,212百万円）", 3.212e9),
        ("1億2,000万円", 1.2e8),
        ("約7.7億円", 7.7e8),
        ("年額49百万円", 4.9e7),
        ("15百万ポンド(税抜、31.2億円※1)", 3.12e9),
        ("非開示", None),
    ],
)
def test_best_yen(text, yen):
    v, _ = best_yen(text)
    assert v == pytest.approx(yen) if yen else v is None


def test_parse_amounts_foreign():
    a = parse_amounts("年間175.2百万米ドル")
    assert a[0].currency == "USD" and a[0].value == pytest.approx(175.2e6)


def test_format_yen():
    assert format_yen(4.5e9) == "45.0億円"
    assert format_yen(4.9e7) == "49百万円"
    assert format_yen(None) == ""


def test_clean_text_removes_cjk_spaces_and_page_numbers():
    raw = "会 社 名 株式会社テスト\n- 1 -\n受 注 金 額 約10億円"
    assert clean_text(raw) == "会社名 株式会社テスト\n受注金額 約10億円"


def test_join_wrapped_lines():
    text = "当社は、このたび大型案件を受注いたしましたので、下記のとおりお\n知らせいたします。\n記\n1. 受注案件"
    assert join_wrapped_lines(text).splitlines()[0].endswith("お知らせいたします。")


def test_extract_kv_without_separator():
    kv = extract_kv(["受注製品 NASストレージ製品(Dell)、", "周辺機器、および保守サービス", "受注金額約38億円(注1)", "受注先 国内大手企業"])
    assert kv["amount"].startswith("約38億円")
    assert kv["counterparty"] == "国内大手企業"
    assert "周辺機器" in kv["item"]


def test_order_bbtower():
    ex = extract(load("order_bbtower.txt"), "大口受注に関するお知らせ", ["order"])
    assert ex.amount_yen == pytest.approx(3.8e9)
    assert ex.order["amount_approx"] is True
    assert "NASストレージ" in ex.order["item"]
    assert "IPコンテンツ" in ex.order["counterparty"]
    assert "2027年12月期" in ex.order["revenue_timing"]
    assert "業績予想に影響はございません" in ex.outlook.replace(" ", "")
    assert ex.lead.startswith("2026年9月28日付で")


def test_order_nagaoka():
    ex = extract(load("order_nagaoka.txt"), "大口受注に関するお知らせ", ["order"])
    assert ex.amount_yen == pytest.approx(7.7e8)
    assert ex.order["item"] == "スクリーン・インターナル"
    assert "分納" in ex.order["period"]
    assert "約7.7億円" in ex.summary


def test_order_undisclosed_amount():
    ex = extract(load("order_flight.txt"), "大口受注に関するお知らせ", ["order"])
    assert ex.amount_yen is None
    assert ex.order["amount_undisclosed"] is True
    assert ex.order["sales_ratio"] == "売上高の10%以上"
    assert "非開示" in ex.summary


def test_order_foreign_currency_uses_yen_note():
    ex = extract(load("order_datasection.txt"), "大口受注(予定)に関するお知らせ", ["order"])
    assert ex.order["amount_foreign"]["currency"] == "USD"
    assert ex.amount_yen == pytest.approx(27_984e6)  # 注記の年間円換算額
    assert "(注)" not in ex.order["period"]


def test_forecast_down():
    ex = extract(load("forecast_oi.txt"), "2027年3月期第2四半期(中間期)連結業績予想の修正に関するお知らせ", ["forecast"])
    assert ex.direction == "down"
    assert "ずれ込んだ" in ex.reason
    assert ex.summary.startswith("【下方】")
    assert any(s["polarity"] == "neg" for s in ex.signals)


def test_earnings_qualitative_and_order_mentions():
    ex = extract(load("earnings_takeuchi.txt"), "2027年2月期第2四半期(中間期)決算短信〔日本基準〕(連結)", ["earnings"])
    assert ex.qualitative.startswith("当社グループは第四次中期経営計画") or "経営成績" in ex.qualitative[:200] or len(ex.qualitative) > 500
    assert "…" not in ex.qualitative[:100]  # 目次は除去済み
    assert any("受注高" in s for s in ex.order_mentions)
    assert ex.summary


def test_is_readable():
    from kaiji.pdftext import is_readable

    assert not is_readable("")
    assert not is_readable("(cid:12)(cid:345)" * 50)
    assert is_readable("当社は、大口受注をいたしましたのでお知らせいたします。" * 3)


@pytest.mark.parametrize(
    "title,text,expected",
    [
        ("業績予想の修正(上方修正)に関するお知らせ", "売上高は前回予想を下回る見込み", "up"),
        ("業績予想の修正に関するお知らせ", "売上高は前回予想を上回りましたが、営業利益は前回予想を下回る見込みです。", "down"),
        ("業績予想の修正に関するお知らせ", "利益面は前回発表予想を上回る見込みとなりました。", "up"),
        ("業績予想の修正に関するお知らせ", "未定に変更します", ""),
    ],
)
def test_forecast_direction(title, text, expected):
    from kaiji.extract import forecast_direction

    assert forecast_direction(title, text) == expected
