"""CLI for AlphaDom. This is experimental."""


from alpha_dom import cards

list(map(print, map(repr, sorted(cards.load_all()))))
