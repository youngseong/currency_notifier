def threshold_trigger(amount: float, threshold: float, comparator: str, **kwargs):
    if comparator not in {'>', '<', 'gt', 'lt'}:
        raise ValueError(f"Invalid comparator: {comparator!r}. Must be one of '>', '<', 'gt', 'lt'")

    def cmp(a, b): return a > b if comparator == '>' or comparator == 'gt' else a < b
    return cmp(amount, threshold)
