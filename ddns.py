#!/usr/bin/env python

# Copyright (c) 2011 Dmitry Alenichev <mitya@rockers.su>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import os
import sys

from subprocess import call
from easyzone import easyzone

def usage():
    progname = os.path.basename(sys.argv[0])
    print 'usage: %s hostname ip' % progname
    sys.exit(1)

def main():
    if len(sys.argv) != 3:
        usage()

    hostname, zonename = sys.argv[1].split('.', 1)
    zonefile = '/srv/ns/zones/%s.zone' % zonename

    z = easyzone.zone_from_file(zonename, zonefile)
    r = '%s.' % sys.argv[1]

    try:
        a = z.names[r].records('A')
    except KeyError:
        print 'error: %s record not found in %s' % (hostname, zonefile)
        exit(1)

    a.delete(a.items[0])
    a.add(sys.argv[2])
    z.save(autoserial=True)

    call('sudo /etc/init.d/nsd3 rebuild', shell=True)
    call('sudo /etc/init.d/nsd3 restart', shell=True)

if __name__ == "__main__":
    main()
