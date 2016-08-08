def tree(root, branches=[]):
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [root]+list(branches)


def root(tree):
    return tree[0]


def branches(tree):
    return tree[1]


def is_tree(tree):
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True


def is_leaf(tree):
    return not branches(tree)


def make_pytunes(username):
    """Return a pyTunes tree as shown in the diagram with USERNAME as the value
        of the root.

        >>> pytunes = make_pytunes('i_love_music')
        >>> print_tree(pytunes)
        i_love_music
          pop
            justin bieber
              single
                what do you mean?
            2015 pop mashup
          trance
            darude
              sandstorm
    """
    return tree(username,
                [tree('pop',
                      [tree('justin bieber',
                            [tree('single',
                                  [tree('what do you mean?')])]),
                       tree('2015 pop mashup')]),
                 tree('trance',
                      [tree('darude',
                            [tree('sandstorm')])])])


def num_songs(t):
    if is_leaf(t):
        return 1
    leaves = 0
    for b in branches(t):
        leaves += num_songs(b)
    return leaves


