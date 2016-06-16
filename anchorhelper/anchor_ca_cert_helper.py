#!/usr/bin/python2 -E

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


#
# Authors:
#   Guang Yee <guang.yee@hpe.com>
#

# This is a certmonger CA helper script for Anchor CA subsystem cert renewal.
# See https://git.fedorahosted.org/cgit/certmonger.git/tree/doc/helpers.txt
# for more information on certmonger CA helper scripts.

import argparse
import os
import requests
import sys
import syslog
import traceback

import six


# Return codes. Names of the constants are taken from
# https://git.fedorahosted.org/cgit/certmonger.git/tree/src/submit-e.h
ISSUED = 0
WAIT = 1
REJECTED = 2
UNREACHABLE = 3
UNCONFIGURED = 4
WAIT_WITH_DELAY = 5
OPERATION_NOT_SUPPORTED_BY_HELPER = 6

if six.PY3:
    unicode = str


def main():
    operation = os.environ.get('CERTMONGER_OPERATION')
    if operation not in ('SUBMIT'):
        return OPERATION_NOT_SUPPORTED_BY_HELPER

    parser = argparse.ArgumentParser()
    # TODO(gyee): need to add the client and trust cert options for https
    parser.add_argument('-l', '--url', dest='url', required=True,
        help='Anchor signing request URL. '
             'i.e. https://myhost:5016/v1/sign/MyCA')
    # TODO(gyee): need to add other auth options as Anchor also supports LDAP
    # and Keystone auth. For now, lets use its static account.
    parser.add_argument('-u', '--user', dest='user', required=True,
        help='Anchor user for authentication')
    parser.add_argument('-s', '--secret', dest='secret', required=True,
        help='User secret/password')
    parser.add_argument('--csr', dest='csr', help='CSR file')
    args = parser.parse_args()

    if args.csr:
        csr_file = open(args.csr, 'r')
        csr = csr_file.read()
        csr_file.close()
    else:
        csr = os.environ['CERTMONGER_CSR']

    form_data = {'encoding': 'pem',
                 'user': args.user,
                 'secret': args.secret,
                 'csr': csr}
    resp = requests.post(args.url, data=form_data)
    pem = resp.text
    pem = pem.replace('#012', '\n')
    syslog.syslog(syslog.LOG_ERR, "%s" % (pem))
    print(pem)
    return 0

try:
    sys.exit(main())
except Exception as e:
    syslog.syslog(syslog.LOG_ERR, traceback.format_exc())
    print("Internal error")
    sys.exit(UNREACHABLE)
