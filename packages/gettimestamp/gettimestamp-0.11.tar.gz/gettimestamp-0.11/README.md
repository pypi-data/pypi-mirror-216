# A function to get a Timestamp string in the format YYYY_MM_DD_HH_MM_SS_microseconds ('_' can be defined) 

## pip install gettimestamp

### Tested against Windows 10 / Python 3.10 / Anaconda 

The function takes an optional sep argument,
which represents the separator character used in the timestamp string.
By default, the separator is set to "_".

The function utilizes the datetime module to retrieve the current date and time.
It formats the timestamp using the provided separator and
includes the year, month, day, hour, minute, second, and microseconds.

The resulting timestamp string is returned by the function.
However, if the separator is set to "ÇÇÇÇSXÇX",
a ValueError is raised to prevent the use of that specific separator.


```python
        Args:
            sep (str, optional): Separator character to use in the timestamp string. Defaults to "_".

        Returns:
            str: Timestamp string in the format "YYYY_MM_DD_HH_MM_SS_microseconds".

        Raises:
            ValueError: Raised when the separator is set to "ÇÇÇÇSXÇX".

        Example:
            from gettimestamp import get_timestamp
            >>> get_timestamp()
            '2023_06_26_15_30_45_123456'
            >>> get_timestamp("-")
            '2023-06-26-15-30-45-123456'
```

