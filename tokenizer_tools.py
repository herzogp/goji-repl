import os
# import itertools
# from enum import Enum

def lines_to_process(filepath):
    all_lines = []
    if not os.access(filepath, os.R_OK):
        return all_lines
    fo = open(filepath, "r", encoding="utf-8")
    for x in fo.readlines():
        line = x.rstrip().lstrip()
        if not line.startswith(";"):
            all_lines.append(line)
    joined_lines = ' '.join(all_lines)
    fo.close()
    return joined_lines


def show_tokens(heading, tks):
    print(heading + ':')
    for idx, t in enumerate(tks):
        print('[' + str(idx) +']', t)
    print('\n%i %s' % (len(tks), heading))
    print('\n')


def show_token_diff(actual, expected):
    z_results = zip(actual, expected)
    failed = 0
    for idx,pair in enumerate(z_results):
        got = pair[0]
        want = pair[1]
        if got == want:
            print('[' + str(idx) +']', got)
        else:
            failed = failed + 1
            print('[' + str(idx) + ']', str(got) + ' // ' + str(want))
    return failed
