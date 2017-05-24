import random
import string

SCHEMES = ['', 'http://', 'https://', 'ftp://', 'file://', 'mailto:', 'irc://',
           'irc6://', 'ircs://']
VALID_CHARS = string.ascii_lowercase + string.digits


def random_chars(count, chars=VALID_CHARS):
    """ Generate string of length `count` random chars """
    return ''.join(random.choice(chars) for _ in range(count))


def random_urls(count):
    """ Generate `count` random urls """
    for _ in range(count):
        scheme = random.choice(SCHEMES)

        part_lengths = [
            random.randint(1, 16) for _ in range(random.randint(2, 6))]
        host = '.'.join([random_chars(c) for c in part_lengths])

        part_lengths = [
            random.randint(1, 16) for _ in range(random.randint(0, 8))]
        path = '/'.join([random_chars(c) for c in part_lengths])
        if len(path) > 0:
            path = '/' + path

        query_lengths = [(random.randint(1, 10), random.randint(1, 10))
                         for _ in range(random.randint(0, 6))]
        queries = '&'.join(['{0}={1}'.format(random_chars(i), random_chars(j))
                            for i, j in query_lengths])
        if len(queries) > 0:
            queries = '?' + queries

        fragment = random_chars(random.randint(0, 8))
        if len(fragment) > 0:
            fragment = '#' + fragment

        yield '{0}{1}{2}{3}{4}'.format(
            scheme, host, path, queries, fragment)
