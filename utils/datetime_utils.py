import datetime

class DateTimeUtils:
    @staticmethod
    def current_date_str() -> str:
        return datetime.date.today().isoformat()

    @staticmethod
    def current_datetime_str() -> str:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def format_date(date_str: str, fmt: str = '%b %d, %Y') -> str:
        if not date_str:
            return ''
        try:
            dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return dt.strftime(fmt)
        except Exception:
            return date_str

    @staticmethod
    def days_between(date1_str: str, date2_str: str) -> int:
        try:
            d1 = datetime.datetime.strptime(date1_str, '%Y-%m-%d').date()
            d2 = datetime.datetime.strptime(date2_str, '%Y-%m-%d').date()
            return (d2 - d1).days
        except Exception:
            return 0
