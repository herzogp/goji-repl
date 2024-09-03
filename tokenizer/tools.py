import os
# import itertools
# from enum import Enum

def lines_to_process(filepath, should_join = True):
    all_lines = []
    if not os.access(filepath, os.R_OK):
        return all_lines
    fo = open(filepath, "r", encoding="utf-8")
    for x in fo.readlines():
        line = x.rstrip()
        cmp_line = line.lstrip()
        if should_join:
            if not cmp_line.startswith("//"):
                all_lines.append(line)
        else:
            all_lines.append(line)

    fo.close()
    if should_join:
        return ' '.join(all_lines)
    return all_lines


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
            print("GOT:  ", got, type(got))
            print("WANT: ", want, type(want))
            failed = failed + 1
            print('[' + str(idx) + ']', str(got) + ' // ' + str(want))
    return failed
