def string_to_slug(string: str) -> str:
    """
    Replace a string into a URL slug.

    - Lowercase all characters.
    - strip all leading, trailing whitespaces.
    - Replace all consecutive whitespaces with "-".
    - Do something about CJK characters.
    """

    return string.strip().lower().replace(" ", "-")
