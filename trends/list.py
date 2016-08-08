empty = 'empty'


def is_link(s):
    return s == empty or (len(s) == 2 and is_link(s[1]))


def link(first, rest):
    assert is_link(rest)
    return [first, rest]


def first(s):
    assert is_link(s), "first only applies to linked lists."
    assert s != empty, "empty linked list has no first element"
    return s[0]


def rest(s):
    assert is_link(s)
    assert s != empty
    return s[1]


def len_link(s):
    length = 0
    while s != empty:
        s, length = rest(s), length + 1
    return length


def getitem_link(s, i):
    while i > 0:
        s, i = rest(s), i - 1
    return first(s)


def len_link_recursive(s):
    if s == empty:
        return 0
    return 1 + len_link_recursive(rest(s))


def getitem_link_recursive(s, i):
    if i == 0:
        return first(s)
    return getitem_link_recursive(rest(s), i - 1)


def extend_link(s, t):
    assert is_link(s) and is_link(t)
    if s == empty:
        return t
    else:
        return link(first(s), extend_link(rest(s), t))


def apply_to_all_link(f, s):
    assert is_link(s)
    if s == empty:
        return s
    else:
        return link(f(first(s)), apply_to_all_link(f, rest(s)))


def join_link(s, separator):
    if s == empty:
        return ""
    elif rest(s) == empty:
        return str(first(s))
    else:
        return str(first(s)+separator+join_link(rest(s), separator))


def sum_linked_list(lst, fn):
    if lst == empty:
        return 0
    else:
        return fn(first(lst)) + sum_linked_list(rest(lst), fn)


def change(lst, s, t):
    if lst == empty:
        return lst
    if first(lst) == s:
        return link(t, change(rest(lst), s, t))
    return link(first(lst), change(rest(lst), s, t))


def link_to_list(linked_lst):
    if linked_lst == empty:
        return []
    return [first(linked_lst)] + link_to_list(rest(linked_lst))


def insert(lst, item, index):
    # Returns a link matching lst but with the given item inserted at the specified index.
    if lst == empty:
        return link(item, empty)
    if index == 0:
        return link(item, lst)
    return link(first(lst), insert(rest(lst), item, index-1))

lst1 = link(1, link(2, link(3, link(4, empty))))


def reverse_iterative(s):
    # lst, s = link(first(s), empty), rest(s)
    lst = empty
    while s != empty:
        lst, s = link(first(s), lst), rest(s)
        print(lst)

    return lst

print(reverse_iterative(lst1))


def reverse_recursive(s):
    def reverse_helper(s, tail):
        if s == empty:
            return tail
        return reverse_helper(rest(s), link(first(s), tail))
    return reverse_helper(s, empty)
