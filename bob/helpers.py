def month_string_to_number(month):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }

    if isinstance(month, str) == False:
        raise TypeError('Not a string')
    try:
        s = month.strip()[:3].lower()
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')