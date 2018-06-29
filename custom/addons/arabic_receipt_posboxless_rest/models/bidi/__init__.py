#!/usr/bin/env python
VERSION = '0.4.0'


def main():
    import optparse
    import sys
    import codecs
    import locale
    import six
    from .algorithm import get_display

    parser = optparse.OptionParser()

    parser.add_option('-e', '--encoding',
                      dest='encoding',
                      default='utf-8',
                      type='string',
                      help='Text encoding (default: utf-8)')

    parser.add_option('-u', '--upper-is-rtl',
                      dest='upper_is_rtl',
                      default=False,
                      action='store_true',
                      help="Treat upper case chars as strong 'R' "
                      'for debugging (default: False).')

    parser.add_option('-d', '--debug',
                      dest='debug',
                      default=False,
                      action='store_true',
                      help="Output to stderr steps taken with the algorithm")

    parser.add_option('-b', '--base-dir',
                      dest='base_dir',
                      default=None,
                      type='string',
                      help="Override base direction [L|R]")

    options, rest = parser.parse_args()

    if options.base_dir and options.base_dir not in 'LR':
        parser.error('option -b can be L or R')

    # allow unicode in sys.stdout.write
    if six.PY2:
        sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

    if rest:
        lines = rest
    else:
        lines = sys.stdin

    for line in lines:
        display = get_display(line, options.encoding, options.upper_is_rtl,
                              options.base_dir, options.debug)
        # adjust the encoding as unicode, to match the output encoding
        if not isinstance(display, six.text_type):
            display = display.decode(options.encoding)

        six.print_(display, end='')
