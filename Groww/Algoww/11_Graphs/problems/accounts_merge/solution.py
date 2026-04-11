# Accounts Merge
# Link: https://leetcode.com/problems/accounts-merge/
#
# Given a list of accounts where each element accounts[i] is a list of strings,
# where accounts[i][0] is a name and the rest are emails belonging to that account.
#
# Two accounts belong to the same person if there is some common email address.
# Note that even if two accounts have the same name, they may belong to different people
# (names could be non-unique). However, all accounts with the same email definitely
# belong to the same person.
#
# Return the merged accounts in the following format:
# The first element of each account is the name, and the rest are emails in sorted order.
# The accounts themselves can be returned in any order.
#
# Example 1:
#   Input: [["John","johnsmith@mail.com","john00@mail.com"],
#            ["John","johnnybravo@mail.com"],
#            ["John","johnsmith@mail.com","john_newyork@mail.com"],
#            ["Mary","mary@mail.com"]]
#   Output: [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],
#             ["John","johnnybravo@mail.com"],
#             ["Mary","mary@mail.com"]]
#   (Account 0 and 2 are merged because they share johnsmith@mail.com)
#
# Constraints:
# - 1 <= accounts.length <= 1000
# - 2 <= accounts[i].length <= 10
# - 1 <= accounts[i][j].length <= 30
# - accounts[i][0] consists of English letters
# - accounts[i][j] (for j > 0) is a valid email
#
# Key insight: This is a graph/Union Find problem in disguise.
# Each email is a node. Emails in the same account are connected (same person).
# Merge = find connected components.
# Union Find approach: union all emails within the same account together.
# Then group emails by their root, sort, and prepend the account name.

from typing import List
from collections import defaultdict


def accountsMerge(accounts: List[List[str]]) -> List[List[str]]:
    pass


if __name__ == "__main__":
    # Test 1: standard merge
    accounts = [
        ["John", "johnsmith@mail.com", "john00@mail.com"],
        ["John", "johnnybravo@mail.com"],
        ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
        ["Mary", "mary@mail.com"]
    ]
    result = accountsMerge(accounts)
    result_sorted = [sorted(acc[1:]) for acc in result]
    assert ["john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"] in result_sorted
    assert ["johnnybravo@mail.com"] in result_sorted
    assert ["mary@mail.com"] in result_sorted
    assert len(result) == 3

    # Test 2: no merges needed (all unique emails)
    accounts = [["Alice", "alice@mail.com"], ["Bob", "bob@mail.com"]]
    result = accountsMerge(accounts)
    assert len(result) == 2

    # Test 3: all same account (chain of shared emails)
    accounts = [
        ["A", "a@m.com", "b@m.com"],
        ["A", "b@m.com", "c@m.com"],
        ["A", "c@m.com", "d@m.com"]
    ]
    result = accountsMerge(accounts)
    assert len(result) == 1
    assert sorted(result[0][1:]) == ["a@m.com", "b@m.com", "c@m.com", "d@m.com"]

    print("✅ All tests passed!")
