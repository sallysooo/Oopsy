# -*- encoding: utf-8 -*-
from urllib.parse import urlparse
from utils import for_app


@for_app('whois')
def match(command):
    """
    What the `whois` command returns depends on the 'Whois server' it contacted
    and is not consistent through different servers. But there can be only two
    types of errors I can think of with `whois`:
        - `whois https://en.wikipedia.org/` → `whois en.wikipedia.org`;
        - `whois en.wikipedia.org` → `whois wikipedia.org`.
    So we match any `whois` command and then:
        - if there is a slash: keep only the FQDN;
        - if there is no slash but there is a point: removes the left-most
          subdomain.

    We cannot either remove all subdomains because we cannot know which part is
    the subdomains and which is the domain, consider:
        - www.google.fr → subdomain: www, domain: 'google.fr';
        - google.co.uk → subdomain: None, domain; 'google.co.uk'.
    """
    return len(command.script_parts) >= 2


def get_new_command(command):
    url = command.script_parts[1]

    if '/' in url: # https://en.wikipedia.org/
        return 'whois ' + urlparse(url).netloc
    elif '.' in url: # en.wikipedia.org -> wikipedia.org
        domain_parts = url.split('.')
        if len(domain_parts) > 2:
            return "whois " + '.'.join(domain_parts[1:])
    return command.script

'''
$ whois https://en.wikipedia.org/

oops -> $ whois en.wikipedia.org
'''