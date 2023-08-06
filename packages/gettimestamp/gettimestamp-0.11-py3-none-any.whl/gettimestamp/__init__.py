import datetime


def get_timestamp(sep: str = "_") -> str:
    """
    The function takes an optional sep argument,
    which represents the separator character used in the timestamp string.
    By default, the separator is set to "_".

    The function utilizes the datetime module to retrieve the current date and time.
    It formats the timestamp using the provided separator and
    includes the year, month, day, hour, minute, second, and microseconds.

    The resulting timestamp string is returned by the function.
    However, if the separator is set to "ÇÇÇÇSXÇX",
    a ValueError is raised to prevent the use of that specific separator.

        Args:
            sep (str, optional): Separator character to use in the timestamp string. Defaults to "_".

        Returns:
            str: Timestamp string in the format "YYYY_MM_DD_HH_MM_SS_microseconds".

        Raises:
            ValueError: Raised when the separator is set to "ÇÇÇÇSXÇX".

        Example:
            >>> get_timestamp()
            '2023_06_26_15_30_45_123456'
            >>> get_timestamp("-")
            '2023-06-26-15-30-45-123456'
    """
    if sep == "ÇÇÇÇSXÇX":
        raise ValueError("ÇÇÇÇSXÇX not allowed")
    titi = datetime.datetime.now().strftime(
        f"%Y{sep}%m{sep}%d{sep}%H{sep}%M{sep}%SÇÇÇÇSXÇX%f"
    )
    t1, t2 = titi.split("ÇÇÇÇSXÇX")
    t2 = (t2 + "0" * 10)[:6]
    return t1 + str(sep) + t2
