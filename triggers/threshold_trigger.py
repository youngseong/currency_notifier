def threshold_trigger(amount: float, threshold: float, comparator: str, **kwargs):
    assert comparator in set(['>', '<', 'gt', 'lt'])

    def cmp(a, b): return a > b if comparator == '>' or comparator == 'gt' else a < b
    return cmp(amount, threshold)
