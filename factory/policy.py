"""Approved AC13 review policy and AC11/AC12 contract invalidation."""


def latest_non_comment_reviews(reviews):
    """Input is chronological; comments do not withdraw a review decision."""
    return {r['user']['login']: r for r in reviews if r['state'] != 'COMMENTED'}


def contract_change_reason(old_contract, new_contract):
    """Only contract-bound gates consume this reason."""
    return None if old_contract == new_contract else 'STALE_CONTRACT'
