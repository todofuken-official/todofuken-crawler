import re
from datetime import date, datetime

TUN_MAPPING = {
    "上旬": 5,
    "中旬": 15,
    "下旬": 25,
}

def clean_period_text(text):
    """不要 단어 제거"""
    remove_words = ["終了間近", "間もなく終了", "開催終了"]
    for word in remove_words:
        text = text.replace(word, "")
    return text.strip()

def safe_parse(date_str):
    """YYYY年MM月DD日 형태 정확히 있는 경우만 파싱"""
    try:
        y_match = re.search(r"(\d{4})年", date_str)
        m_match = re.search(r"(\d{1,2})月", date_str)
        d_match = re.search(r"(\d{1,2})日", date_str)

        if not y_match or not m_match:
            return None

        y = int(y_match.group(1))
        m = int(m_match.group(1))
        d = int(d_match.group(1)) if d_match else 1

        return date(y, m, d)
    except:
        return None

def parse_date_without_year(text, base_year):
    """연도 없는 경우 처리 (월/旬/일 있는 경우)"""
    for key, day in TUN_MAPPING.items():
        if key in text:
            m = int(re.search(r"(\d{1,2})月", text).group(1))
            return date(base_year, m, day)

    # 월 있는 경우
    m_match = re.search(r"(\d{1,2})月", text)
    if not m_match:
        return None

    m = int(m_match.group(1))

    d_match = re.search(r"(\d{1,2})日", text)
    d = int(d_match.group(1)) if d_match else 1

    return date(base_year, m, d)

def parse_day_only(text, base_year, base_month):
    """오른쪽에 '15日' 만 있는 경우 (월/년 둘 다 없음)"""
    d_match = re.search(r"(\d{1,2})日", text)
    if not d_match:
        return None

    d = int(d_match.group(1))
    return date(base_year, base_month, d)

def parse_period(period_raw):
    """WalkerPlus 기간 전체 파싱"""
    if not period_raw:
        return None, None

    text = clean_period_text(period_raw)

    # 常設
    if text == "常設":
        return None, None

    # 開催中～
    if text.startswith("開催中～"):
        right = text.replace("開催中～", "")
        this_year = datetime.now().year
        end = safe_parse(right) or parse_date_without_year(right, this_year)
        return None, end

    # 단일 일자
    if "～" not in text:
        this_year = datetime.now().year
        start = safe_parse(text) or parse_date_without_year(text, this_year)
        return start, start

    # 기간
    left, right = text.split("～", 1)
    this_year = datetime.now().year

    # 왼쪽 날짜
    start = safe_parse(left)
    if not start:
        start = parse_date_without_year(left, this_year)

    if not start:
        return None, None

    # 오른쪽 1) 완전한 날짜
    end = safe_parse(right)
    if end:
        return start, end

    # 오른쪽 2) 월/일 있는 경우
    end = parse_date_without_year(right, start.year)
    if end:
        # 월이 작다면 → 다음 년도
        if end.month < start.month:
            end = date(start.year + 1, end.month, end.day)
        return start, end

    # 오른쪽 3) 일만 있는 경우 ("15日")
    end = parse_day_only(right, start.year, start.month)
    if end:
        return start, end

    # 실패
    return start, None