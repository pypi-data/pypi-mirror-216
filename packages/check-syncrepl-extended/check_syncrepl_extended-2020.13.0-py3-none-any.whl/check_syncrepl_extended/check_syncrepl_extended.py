#!/usr/bin/env python3

#
# Script to check LDAP syncrepl replication state between two servers.
# One server is consider as provider and the other as consumer.
#
# This script can check replication state with two method :
#  - by the fisrt, entryCSN of all entries of LDAP directory will be
#    compare between two servers
#  - by the second, all values of all atributes of all entries will
#    be compare between two servers.
#
# In all case, contextCSN of servers will be compare and entries not
# present in consumer or in provider will be notice. You can decide to
# disable contextCSN verification by using argument --no-check-contextCSN.
#
# This script is also able to "touch" LDAP object on provider to force
# synchronisation of this object. This mechanism consist to add '%%TOUCH%%'
# value to an attribute of this object and remove it just after. The
# touched attribute is specify by parameter --touch. Of course, couple of
# DN and password provided, must have write right on this attribute.
#
# If your prefer, you can use --replace-touch parameter to replace value
# of touched attribute instead of adding the touched value. Use-ful in
# case of single-value attribute.
#
# This script could be use as Nagios plugin (-n argument)
#
# Requirement:
# One or two couples of DN and password able to connect to both server
# and without restriction to retrieve objects from servers.
#
# Author: Benjamin Renard <brenard@easter-eggs.com>
# Source: https://gogs.zionetrix.net/bn8/check_syncrepl_extended
#

import argparse
import logging
import sys
import datetime
import getpass
import ldap
from ldap import LDAPError  # pylint: disable=no-name-in-module
from ldap.controls import SimplePagedResultsControl
import ldap.modlist as modlist

TOUCH_VALUE = "%%TOUCH%%"


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Script to check LDAP syncrepl replication state between " + "two servers."
        ),
        epilog=(
            "Author: Benjamin Renard <brenard@easter-eggs.com>, "
            + "Source: https://gogs.zionetrix.net/bn8/check_syncrepl_extended"
        ),
    )

    parser.add_argument(
        "-p",
        "--provider",
        dest="provider",
        action="store",
        type=str,
        help="LDAP provider URI (example: ldaps://ldapmaster.foo:636)",
    )

    parser.add_argument(
        "-c",
        "--consumer",
        dest="consumer",
        action="store",
        type=str,
        help="LDAP consumer URI (example: ldaps://ldapslave.foo:636)",
    )

    parser.add_argument(
        "-i",
        "--serverID",
        dest="serverid",
        action="store",
        type=int,
        help=(
            "Compare contextCSN of a specific master. Useful in MultiMaster "
            + "setups where each master has a unique ID and a contextCSN for "
            + "each replicated master exists. A valid serverID is a integer "
            + "value from 0 to 4095 (limited to 3 hex digits, example: '12' "
            + "compares the contextCSN matching '#00C#')"
        ),
        default=False,
    )

    parser.add_argument(
        "-T",
        "--starttls",
        dest="starttls",
        action="store_true",
        help="Start TLS on LDAP provider/consumers connections",
        default=False,
    )

    parser.add_argument(
        "-D",
        "--dn",
        dest="dn",
        action="store",
        type=str,
        help="LDAP bind DN (example: uid=nagios,ou=sysaccounts,o=example)",
    )

    parser.add_argument(
        "-P",
        "--pwd",
        dest="pwd",
        action="store",
        type=str,
        help="LDAP bind password",
        default=None,
    )

    parser.add_argument(
        "--dn2",
        dest="dn2",
        action="store",
        type=str,
        help="LDAP bind DN for provider (if it differs from consumer)",
        default=None,
    )

    parser.add_argument(
        "--pwd2",
        dest="pwd2",
        action="store",
        type=str,
        help="LDAP bind password for provider (if it differs from consumer)",
        default="",
    )

    parser.add_argument(
        "-b",
        "--basedn",
        dest="basedn",
        action="store",
        type=str,
        help="LDAP base DN (example: o=example)",
    )

    parser.add_argument(
        "-f",
        "--filter",
        dest="filterstr",
        action="store",
        type=str,
        help="LDAP filter (default: (objectClass=*))",
        default="(objectClass=*)",
    )

    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        help="Debug mode",
        default=False,
    )

    parser.add_argument(
        "-n",
        "--nagios",
        dest="nagios",
        action="store_true",
        help="Nagios check plugin mode",
        default=False,
    )

    parser.add_argument(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        help="Quiet mode",
        default=False,
    )

    parser.add_argument(
        "--no-check-certificate",
        dest="nocheckcert",
        action="store_true",
        help="Don't check the server certificate (Default: False)",
        default=False,
    )

    parser.add_argument(
        "--no-check-contextCSN",
        dest="nocheckcontextcsn",
        action="store_true",
        help="Don't check servers contextCSN (Default: False)",
        default=False,
    )

    parser.add_argument(
        "--only-check-contextCSN",
        dest="onlycheckcontextcsn",
        action="store_true",
        help=(
            "Only check servers root contextCSN (objects check disabled, "
            + "default : False)"
        ),
        default=False,
    )

    parser.add_argument(
        "-a",
        "--attributes",
        dest="attrs",
        action="store_true",
        help="Check attributes values (Default: check only entryCSN)",
        default=False,
    )

    parser.add_argument(
        "--exclude-attributes",
        dest="excl_attrs",
        action="store",
        type=str,
        help="Don't check this attribut (only in attribute check mode)",
        default=None,
    )

    parser.add_argument(
        "--touch",
        dest="touch",
        action="store",
        type=str,
        help=(
            "Touch attribute giving in parameter to force resync a this LDAP "
            + "object from provider. A value '{}' will be add to this attribute "
            + "and remove after. The user use to connect to the LDAP directory "
            + "must have write permission on this attribute on each object."
        ).format(TOUCH_VALUE),
        default=None,
    )

    parser.add_argument(
        "--replace-touch",
        dest="replacetouch",
        action="store_true",
        help="In touch mode, replace value instead of adding.",
        default=False,
    )

    parser.add_argument(
        "--remove-touch-value",
        dest="removetouchvalue",
        action="store_true",
        help="In touch mode, remove touch value if present.",
        default=False,
    )

    parser.add_argument(
        "--page-size",
        dest="page_size",
        action="store",
        type=int,
        help=(
            "Page size: if defined, paging control using LDAP v3 extended "
            + "control will be enabled."
        ),
        default=None,
    )

    parser.add_argument(
        "-W",
        "--warning",
        dest="warning",
        action="store",
        type=int,
        help=(
            "Exit with WARNING status if difference is greater than INTEGER seconds."
        ),
        default=None,
    )

    parser.add_argument(
        "-C",
        "--critical",
        dest="critical",
        action="store",
        type=int,
        help=(
            "Exit with CRITICAL status if difference is greater than INTEGER seconds."
        ),
        default=0,
    )

    options = parser.parse_args()

    if options.nocheckcontextcsn and options.onlycheckcontextcsn:
        parser.error(
            "You can't use both --no-check-contextCSN and "
            + "--only-check-contextCSN parameters and the same time"
        )
        if options.nagios:
            sys.exit(3)
        sys.exit(1)

    if not options.provider or not options.consumer:
        parser.error("You must provide provider and customer URI")
        if options.nagios:
            sys.exit(3)
        sys.exit(1)

    if not options.basedn:
        parser.error("You must provide base DN of connection to LDAP servers")
        if options.nagios:
            sys.exit(3)
        sys.exit(1)

    if not 0 <= options.serverid <= 4095:
        parser.error(
            "ServerID should be a integer value from 0 to 4095 "
            + "(limited to 3 hexadecimal digits)."
        )
        if options.nagios:
            sys.exit(3)
        sys.exit(1)

    if options.touch and not options.attrs:
        logging.info("Force option attrs on touch mode")
        options.attrs = True

    if options.dn and options.pwd is None:
        options.pwd = getpass.getpass()

    if options.dn and options.pwd2 is None:
        options.pwd2 = getpass.getpass()
    elif options.dn and options.pwd and options.pwd2 == "":
        options.pwd2 = options.pwd

    excl_attrs = []
    if options.excl_attrs:
        for ex in options.excl_attrs.split(","):
            excl_attrs.append(ex.strip())

    FORMAT = "%(asctime)s - %(levelname)s: %(message)s"

    if options.debug:
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
        ldap.set_option(ldap.OPT_DEBUG_LEVEL, 0)  # pylint: disable=no-member
    elif options.nagios:
        logging.basicConfig(level=logging.ERROR, format=FORMAT)
    elif options.quiet:
        logging.basicConfig(level=logging.WARNING, format=FORMAT)
    else:
        logging.basicConfig(level=logging.INFO, format=FORMAT)
    return options, excl_attrs


class LdapServer(object):
    uri = ""
    dn = ""
    pwd = ""
    start_tls = False
    dn2 = ""
    pwd2 = ""

    con = 0

    def __init__(
        self, uri, dn, pwd, start_tls=False, page_size=None, dn2=None, pwd2=None
    ):
        self.uri = uri
        self.dn = dn
        self.pwd = pwd
        self.start_tls = start_tls
        self.page_size = page_size
        self.dn2 = dn2
        self.pwd2 = pwd2

    def connect(self):
        if self.con == 0:
            try:
                con = ldap.initialize(self.uri)
                con.protocol_version = ldap.VERSION3  # pylint: disable=no-member
                if self.start_tls:
                    con.start_tls_s()
                if self.dn:
                    con.simple_bind_s(self.dn, self.pwd)
                self.con = con
            except LDAPError:
                logging.error("LDAP Error", exc_info=True)
                return False
        return True

    def getContextCSN(self, basedn=False, serverid=False):
        if not basedn:
            basedn = self.dn
        data = self.search(
            basedn, "(objectclass=*)", attrs=["contextCSN"], scope="base"
        )
        if data:
            contextCSNs = data[0][0][1]["contextCSN"]
            logging.debug("Found contextCSNs %s", contextCSNs)
            if serverid is False:
                return contextCSNs[0]
            csnid = str(format(serverid, "X")).zfill(3)
            sub = str.encode("#%s#" % csnid, encoding="ascii", errors="replace")
            CSN = [s for s in contextCSNs if sub in s]
            if not CSN:
                logging.error(
                    "No contextCSN matching with ServerID %s (=%s) could be found.",
                    serverid,
                    sub,
                )
                return False
            return CSN[0]
        return False

    @staticmethod
    def get_scope(scope):
        if scope == "base":
            return ldap.SCOPE_BASE  # pylint: disable=no-member
        if scope == "one":
            return ldap.SCOPE_ONELEVEL  # pylint: disable=no-member
        if scope == "sub":
            return ldap.SCOPE_SUBTREE  # pylint: disable=no-member
        raise Exception("Unknown LDAP scope '%s'" % scope)

    def search(self, basedn, filterstr, attrs=None, scope=None):
        if self.page_size:
            return self.paged_search(basedn, filterstr, attrs=attrs, scope=scope)
        res_id = self.con.search(
            basedn,
            self.get_scope(scope if scope else "sub"),
            filterstr,
            attrs if attrs else [],
        )
        ret = []
        while 1:
            res_type, res_data = self.con.result(res_id, 0)
            if res_data == []:
                break
            if res_type == ldap.RES_SEARCH_ENTRY:  # pylint: disable=no-member
                ret.append(res_data)
        return ret

    def paged_search(self, basedn, filterstr, attrs=None, scope=None):
        ret = []
        page = 0
        pg_ctrl = SimplePagedResultsControl(True, self.page_size, "")
        while page == 0 or pg_ctrl.cookie:
            page += 1
            logging.debug("Page search: loading page %d", page)
            res_id = self.con.search_ext(
                basedn,
                self.get_scope(scope if scope else "sub"),
                filterstr,
                attrs if attrs else [],
                serverctrls=[pg_ctrl],
            )
            res_type, res_data, res_id, serverctrls = self.con.result3(
                res_id
            )  # pylint: disable=unused-variable
            for serverctrl in serverctrls:
                if serverctrl.controlType == SimplePagedResultsControl.controlType:
                    pg_ctrl.cookie = serverctrl.cookie
                    break
            for item in res_data:
                ret.append([item])
        return ret

    def update_object(self, dn, old, new):
        ldif = modlist.modifyModlist(old, new)
        if ldif == []:
            return True
        try:
            logging.debug("Update object %s: %s", dn, ldif)
            self.con.modify_s(dn, ldif)
            return True
        except LDAPError:
            logging.error("Error updating object %s", dn, exc_info=True)
        return False

    @staticmethod
    def get_attr(obj, attr):
        if attr in obj[0][1]:
            return obj[0][1][attr]
        return []

    def touch_object(self, dn, attr, orig_value, options):
        old = {}
        if orig_value:
            old[attr] = orig_value
        new = {}

        if options.replacetouch:
            if not orig_value or TOUCH_VALUE not in orig_value:
                new[attr] = [TOUCH_VALUE]
        else:
            new[attr] = list(orig_value)
            if orig_value or TOUCH_VALUE in orig_value:
                new[attr].remove(TOUCH_VALUE)
            else:
                new[attr].append(TOUCH_VALUE)
        try:
            logging.info(
                'Touch object "%s" on attribute "%s": %s => %s', dn, attr, old, new
            )
            if self.update_object(dn, old, new):
                logging.info(
                    'Restore original value of attribute "%s" of object "%s"', attr, dn
                )
                if options.removetouchvalue and TOUCH_VALUE in old[attr]:
                    old[attr].remove(TOUCH_VALUE)
                self.update_object(dn=dn, old=new, new=old)
                return True
        except LDAPError:
            logging.error('Error touching object "%s"', dn, exc_info=True)
        return False


def main():
    options, excl_attrs = parse_args()
    if options.nocheckcert:
        ldap.set_option(
            ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER
        )  # pylint: disable=no-member

    servers = [
        (options.provider, options.dn, options.pwd),
        (options.consumer, options.dn2 or options.dn, options.pwd2 or options.pwd),
    ]

    LdapServers = {}
    LdapObjects = {}
    LdapServersCSN = {}

    for srv, dn, pwd in servers:
        logging.info("Connect to %s", srv)
        LdapServers[srv] = LdapServer(
            srv, dn, pwd, options.starttls, page_size=options.page_size
        )

        if not LdapServers[srv].connect():
            if options.nagios:
                print(
                    "UNKWNON - Failed to connect to %s" % srv
                )  # pylint: disable=print-statement
                sys.exit(3)
            else:
                sys.exit(1)

        if not options.nocheckcontextcsn:
            LdapServersCSN[srv] = LdapServers[srv].getContextCSN(
                options.basedn, options.serverid
            )
            logging.info("ContextCSN of %s: %s", srv, LdapServersCSN[srv])

        if not options.onlycheckcontextcsn:
            logging.info("List objects from %s", srv)
            LdapObjects[srv] = {}

            if options.attrs:
                for obj in LdapServers[srv].search(
                    options.basedn, options.filterstr, []
                ):
                    logging.debug("Found on %s: %s", srv, obj[0][0])
                    LdapObjects[srv][obj[0][0]] = obj[0][1]
            else:
                for obj in LdapServers[srv].search(
                    options.basedn, options.filterstr, ["entryCSN"]
                ):
                    logging.debug(
                        "Found on %s: %s / %s", srv, obj[0][0], obj[0][1]["entryCSN"][0]
                    )
                    LdapObjects[srv][obj[0][0]] = obj[0][1]["entryCSN"][0]

            logging.info("%s objects founds", len(LdapObjects[srv]))

    if not options.onlycheckcontextcsn:
        not_found = {}
        not_sync = {}

        for srv in servers:
            not_found[srv] = []
            not_sync[srv] = []

        if options.attrs:
            logging.info(
                "Check if objects a are synchronized (by comparing attributes's values)"
            )
        else:
            logging.info("Check if objets are synchronized (by comparing entryCSN)")
        for obj in LdapObjects[options.provider]:
            logging.debug("Check obj %s", obj)
            for srv in LdapObjects:
                if srv == options.provider:
                    continue
                if obj in LdapObjects[srv]:
                    touch = False
                    if LdapObjects[options.provider][obj] != LdapObjects[srv][obj]:
                        if options.attrs:
                            attrs_list = []
                            for attr in LdapObjects[options.provider][obj]:
                                if attr in excl_attrs:
                                    continue
                                if attr not in LdapObjects[srv][obj]:
                                    attrs_list.append(attr)
                                    logging.debug(
                                        "Obj %s not synchronized: %s not present on %s",
                                        obj,
                                        ",".join(attrs_list),
                                        srv,
                                    )
                                    touch = True
                                else:
                                    LdapObjects[srv][obj][attr].sort()
                                    LdapObjects[options.provider][obj][attr].sort()
                                    if (
                                        LdapObjects[srv][obj][attr]
                                        != LdapObjects[options.provider][obj][attr]
                                    ):
                                        attrs_list.append(attr)
                                        logging.debug(
                                            "Obj %s not synchronized: "
                                            + "%s not same value(s)",
                                            obj,
                                            ",".join(attrs_list),
                                        )
                                        touch = True
                            if attrs_list:
                                not_sync[srv].append(
                                    "%s (%s)" % (obj, ",".join(attrs_list))
                                )
                        else:
                            logging.debug(
                                "Obj %s not synchronized: %s <-> %s",
                                obj,
                                LdapObjects[options.provider][obj],
                                LdapObjects[srv][obj],
                            )
                            not_sync[srv].append(obj)
                    if touch and options.touch:
                        orig_value = []
                        if options.touch in LdapObjects[options.provider][obj]:
                            orig_value = LdapObjects[options.provider][obj][
                                options.touch
                            ]
                        LdapServers[options.provider].touch_object(
                            obj, options.touch, orig_value, options
                        )
                else:
                    logging.debug("Obj %s: not found on %s", obj, srv)
                    not_found[srv].append(obj)
                    if options.touch:
                        orig_value = []
                        if options.touch in LdapObjects[options.provider][obj]:
                            orig_value = LdapObjects[options.provider][obj][
                                options.touch
                            ]
                        LdapServers[options.provider].touch_object(
                            obj, options.touch, orig_value, options
                        )

        for obj in LdapObjects[options.consumer]:
            logging.debug("Check obj %s of consumer", obj)
            if obj not in LdapObjects[options.provider]:
                logging.debug("Obj %s: not found on provider", obj)
                not_found[options.provider].append(obj)

    if options.nagios:
        errors = []
        warnings = []
        long_output = []

        if not options.nocheckcontextcsn:
            if not LdapServersCSN[options.provider]:
                errors.append("ContextCSN of LDAP server provider could not be found")
            else:
                long_output.append(
                    "ContextCSN on LDAP server provider = %s"
                    % LdapServersCSN[options.provider]
                )
                for srv in LdapServersCSN:
                    if srv == options.provider:
                        continue
                    if not LdapServersCSN[srv]:
                        errors.append("ContextCSN of %s not found" % srv)
                    elif LdapServersCSN[srv] != LdapServersCSN[options.provider]:
                        long_output.append(
                            "ContextCSN on LDAP server %s = %s"
                            % (srv, LdapServersCSN[srv])
                        )
                        if options.critical == 0:
                            errors.append(
                                "ContextCSN of %s not the same of provider" % srv
                            )
                        else:
                            diff = (
                                datetime.datetime.strptime(
                                    LdapServersCSN[options.provider][:14].decode(
                                        "utf-8"
                                    ),
                                    "%Y%m%d%H%M%S",
                                )
                                - datetime.datetime.strptime(
                                    LdapServersCSN[srv][:14].decode("utf-8"),
                                    "%Y%m%d%H%M%S",
                                )
                            ).total_seconds()
                            long_output.append(
                                "ContextCSN of %s is %d seconds behind provider"
                                % (srv, diff)
                            )
                            if diff > options.critical:
                                errors.append(
                                    "ContextCSN of %s is more than " % (srv)
                                    + "%d seconds behind provider" % (options.critical)
                                )
                            elif options.warning and diff > options.warning:
                                warnings.append(
                                    "ContextCSN of %s is more than " % (srv)
                                    + "%d seconds behind provider" % (options.warning)
                                )

        if not options.onlycheckcontextcsn:
            if not_found[options.consumer]:
                errors.append(
                    "%s not found object(s) on consumer"
                    % len(not_found[options.consumer])
                )
                long_output.append(
                    "Object(s) not found on server %s (consumer) :" % options.consumer
                )
                for obj in not_found[options.consumer]:
                    long_output.append(" - %s" % obj)
            if not_found[options.provider]:
                errors.append(
                    "%s not found object(s) on provider"
                    % len(not_found[options.provider])
                )
                long_output.append(
                    "Object(s) not found on server %s (provider) :" % options.provider
                )
                for obj in not_found[options.provider]:
                    long_output.append(" - %s" % obj)
            if not_sync[options.consumer]:
                errors.append(
                    "%s not synchronized object(s) on consumer"
                    % len(not_sync[options.consumer])
                )
                long_output.append(
                    "Object(s) not synchronized on server %s (consumer) :"
                    % options.consumer
                )
                for obj in not_sync[options.consumer]:
                    long_output.append(" - %s" % obj)
        if errors:
            print(
                "CRITICAL - " + ", ".join(errors) + "\n\n" + "\n".join(long_output)
            )  # pylint: disable=print-statement
            sys.exit(2)
        elif warnings:
            print(
                "WARNING - " + ", ".join(warnings) + "\n\n" + "\n".join(long_output)
            )  # pylint: disable=print-statement
            sys.exit(1)
        else:
            print(
                "OK - consumer and provider are synchronized"
                + "\n\n"
                + "\n".join(long_output)
            )  # pylint: disable=print-statement
            sys.exit(0)
    else:
        noerror = True
        for srv in servers:
            if not options.nocheckcontextcsn:
                if not LdapServersCSN[options.provider]:
                    logging.warning(
                        "ContextCSN of LDAP server provider could not be found"
                    )
                    noerror = False
                else:
                    for srv in LdapServersCSN:
                        if srv == options.provider:
                            continue
                        if not LdapServersCSN[srv]:
                            logging.warning("ContextCSN of %s not found", srv)
                            noerror = False
                        elif LdapServersCSN[srv] != LdapServersCSN[options.provider]:
                            logging.warning(
                                "ContextCSN of %s not the same of provider", srv
                            )
                            noerror = False

            if not options.onlycheckcontextcsn:
                if not_found[srv]:
                    logging.warning(
                        "Not found objects on %s :\n  - %s",
                        srv,
                        "\n  - ".join(not_found[srv]),
                    )
                    noerror = False
                if not_sync[srv]:
                    logging.warning(
                        "Not sync objects on %s: %s", srv, "\n  - ".join(not_sync[srv])
                    )
                    noerror = False

        if noerror:
            logging.info("No sync problem detected")


if __name__ == "__main__":
    main()
