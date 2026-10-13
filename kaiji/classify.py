"""開示タイトルからカテゴリを判定するルールベース分類器。

1件の開示は複数のタグを持ちうる。`primary` は優先順位が最も高いタグ。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .textutil import nfkc


@dataclass(frozen=True)
class Category:
    key: str
    label: str
    include: tuple[str, ...]
    exclude: tuple[str, ...] = ()
    # PDF本文を取得して詳細抽出するか
    deep: bool = False
    # 通知・ハイライト対象としての重要度(0-3)
    importance: int = 1


# 金融取引・資本政策系の「契約」は受注ではない
_FINANCE_WORDS = (
    "借入", "コミットメント", "金銭消費貸借", "当座貸越", "シンジケート", "スワップ",
    "新株予約権", "株式譲渡", "株式交換", "合併", "株式取得", "公開買付", "第三者割当",
    "TOPIX", "指数", "インデックス", "構成銘柄", "上場契約", "賃貸借", "マスターリース",
    "保険契約", "和解", "合弁", "事業譲", "株式売買", "吸収分割", "会社分割",
)
_NEGATIVE_CONTRACT = ("解除", "解約", "終了", "打ち切り", "中止", "破棄")

CATEGORIES: tuple[Category, ...] = (
    Category(
        "order", "受注・契約獲得",
        include=(
            r"受注(?!速報|状況|高|残|実績|動向|概況|・売上|及び売上)",
            r"落札(?!結果)", r"契約(を)?獲得", r"(供給|納入|販売|製造委託|業務委託|導入|ライセンス|採用)契約",
            r"採用(が)?決定", r"に採用", r"業務を?受託", r"受託(に関する|のお知らせ|決定)",
            r"案件(の)?(獲得|受注)", r"契約締結.*(受注|納入|供給)",
            r"発注(を)?受け", r"契約金額.*(増額)", r"選定され", r"取引開始",
        ),
        exclude=_FINANCE_WORDS + _NEGATIVE_CONTRACT + ("TOPIX", "銘柄", "役員", "社外取締役", "受注速報"),
        deep=True, importance=3,
    ),
    Category(
        "monthly", "月次・受注速報",
        include=(r"月次", r"月度", r"受注速報", r"売上速報", r"営業概況", r"販売(状況|実績)", r"契約数の状況",
                 r"\d+月(の)?(売上|営業|受注)", r"(既存店|全店)(売上)?"),
        exclude=("ETF", "上場投信", "分配金"),
        deep=True, importance=1,
    ),
    Category(
        "forecast", "業績予想修正",
        include=(r"業績予想(の|及び|および)?.{0,10}修正", r"業績予想と.{0,6}実績.{0,4}(差異|乖離)", r"上方修正", r"下方修正",
                 r"業績(予想)?の修正", r"通期.*予想.*修正", r"業績予想に関する"),
        deep=True, importance=3,
    ),
    Category(
        "earnings", "決算短信",
        include=(r"決算短信",),
        exclude=("説明資料", "補足"),
        deep=True, importance=2,
    ),
    Category(
        "mtp", "中期経営計画・成長戦略",
        include=(r"中期経営計画", r"中期計画", r"中期ビジョン", r"長期ビジョン", r"成長可能性", r"成長戦略",
                 r"資本コストや株価を意識した経営", r"経営改革", r"構造改革", r"事業ポートフォリオ", r"経営方針"),
        deep=True, importance=2,
    ),
    Category(
        "alliance", "提携・協業",
        include=(r"業務提携", r"資本提携", r"資本業務提携", r"協業", r"パートナー(シップ)?", r"共同開発", r"基本合意",
                 r"OEM", r"戦略的提携", r"連携協定", r"包括連携"),
        exclude=("解消", "解除", "終了", "借入", "金銭消費貸借", "コミットメント", "当座貸越"),
        deep=True, importance=2,
    ),
    Category(
        "new_biz", "新製品・新事業",
        include=(r"新製品", r"新サービス", r"新(たな)?事業", r"事業(を)?開始", r"参入", r"提供開始", r"販売開始", r"発売",
                 r"開発に成功", r"特許(を)?取得", r"承認(を)?取得", r"製造販売承認", r"治験", r"上市", r"新工場",
                 r"量産", r"出店", r"開業", r"ローンチ", r"合弁会社(の)?設立", r"新会社(の)?設立"),
        exclude=("持株会社", "特別目的会社", "持株会", "会社分割"),
        deep=True, importance=2,
    ),
    Category(
        "subsidy", "採択・補助金",
        include=(r"採択", r"補助金", r"助成金", r"交付決定"),
        exclude=("営業外収益", "特別利益"),
        deep=True, importance=2,
    ),
    Category(
        "ma", "M&A・組織再編",
        include=(r"子会社(等)?の異動", r"株式(等)?の取得", r"子会社化", r"事業(の)?譲(渡|受|り受け)", r"経営統合", r"合併",
                 r"株式交換", r"株式移転", r"公開買付", r"TOB", r"会社分割", r"持株会社", r"孫会社化", r"買収",
                 r"MBO"),
        exclude=("自己株式", "自社株", "自己投資口"),
        deep=True, importance=2,
    ),
    Category(
        "extraordinary", "特別損益・減損",
        include=(r"特別損失", r"特別利益", r"減損", r"引当金", r"損失(の|等の)?計上", r"評価損", r"営業外(収益|費用)",
                 r"為替差(損|益)", r"売却益", r"売却損"),
        deep=True, importance=2,
    ),
    Category(
        "shareholder", "配当・株主還元",
        include=(r"配当", r"株主優待", r"株主還元", r"自己株式(の)?取得", r"自己株式の消却", r"自社株"),
        exclude=("分配金",),
        importance=1,
    ),
    Category(
        "capital", "資金調達・資本政策",
        include=(r"新株予約権", r"第三者割当", r"株式分割", r"増資", r"売出し", r"ストック・?オプション", r"借入",
                 r"社債", r"コミットメント", r"当座貸越", r"金銭消費貸借", r"譲渡制限付株式", r"自己株式",
                 r"株式報酬", r"資本金", r"資本準備金", r"ESOP", r"信託", r"シンジケート", r"ローン", r"資金調達"),
        importance=1,
    ),
    Category(
        "presentation", "説明資料・IR",
        include=(r"説明資料", r"説明会", r"補足資料", r"プレゼンテーション", r"決算補足", r"IR", r"統合報告",
                 r"Fact ?Book", r"ファクトブック"),
        importance=1,
    ),
    Category(
        "governance", "人事・ガバナンス",
        include=(r"代表取締役", r"役員", r"人事", r"定款", r"株主総会", r"内部統制", r"調査委員会", r"不適切", r"取締役",
                 r"監査", r"組織変更", r"機構改革", r"商号", r"本店", r"異動"),
        importance=1,
    ),
    Category(
        "fund", "ETF・REIT",
        include=(r"ETF", r"上場投信", r"投資法人", r"基準価額", r"分配金", r"REIT", r"リート", r"ETN", r"受益証券",
                 r"資産の(取得|譲渡)", r"信託財産"),
        importance=0,
    ),
)

CATEGORY_BY_KEY = {c.key: c for c in CATEGORIES}
LABELS = {c.key: c.label for c in CATEGORIES} | {"other": "その他"}

_COMPILED = [
    (c, re.compile("|".join(c.include)), re.compile("|".join(map(re.escape, c.exclude))) if c.exclude else None)
    for c in CATEGORIES
]


@dataclass
class Classification:
    primary: str
    tags: list[str] = field(default_factory=list)
    is_correction: bool = False
    importance: int = 0

    @property
    def deep(self) -> bool:
        return any(CATEGORY_BY_KEY[t].deep for t in self.tags if t in CATEGORY_BY_KEY)


def classify(title: str, name: str = "") -> Classification:
    t = nfkc(title)
    n = nfkc(name)
    tags: list[str] = []
    for cat, inc, exc in _COMPILED:
        if not inc.search(t):
            continue
        if exc and exc.search(t):
            continue
        tags.append(cat.key)

    # 「決算短信の開示が期末後50日を超えることに関するお知らせ」等は短信そのものではない
    if "earnings" in tags and re.search(r"決算短信.*(開示|提出|発表).*(お知らせ|について)|開示予定日", t):
        tags.remove("earnings")
    # 決算短信はタイトルに「配当」等を含まないが、短信優先で処理する
    if "earnings" in tags:
        tags = ["earnings"] + [x for x in tags if x not in ("earnings", "presentation")]
    # 投資法人・ETFは銘柄名からも判定する
    if n.startswith(("R-", "I-")) and "fund" not in tags and re.search(r"投資法人|リート|REIT", t + n):
        tags.append("fund")
    # ETF・REIT の決算短信は「2026年8月期(2026年2月5日~2026年8月4日)決算短信」のように計算期間が入る
    _period = r"[\(（]\s*\d{4}年\d{1,2}月\d{1,2}日\s*[~～〜-]\s*\d{4}年\d{1,2}月\d{1,2}日"
    if "earnings" in tags and (re.search(_period + r"\s*[\)）]\s*決算短信", t) or re.search(r"決算短信\s*" + _period, t)):
        tags = ["fund"] + tags
    if re.search(r"決算短信.*(REIT|リート)|投資法人", t) and "fund" not in tags:
        tags = ["fund"] + tags
    if "fund" in tags:
        # ETF/REIT の開示は事業会社向けタグを外す
        tags = ["fund"] + [x for x in tags if x in ("earnings", "forecast")]

    if not tags:
        tags = ["other"]
    primary = tags[0]
    importance = max((CATEGORY_BY_KEY[x].importance for x in tags if x in CATEGORY_BY_KEY), default=0)
    is_correction = bool(re.match(r"^\s*[\(（\[【]?\s*(訂正|数値データ訂正)", t)) or "一部訂正" in t
    if is_correction:
        importance = min(importance, 1)
    return Classification(primary=primary, tags=tags, is_correction=is_correction, importance=importance)
