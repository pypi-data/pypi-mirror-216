from pprint import pprint


def remove_stub_domains(domains: list) -> list:

    blacklist = set([
        '',
        'com',
        'net',
        'space'
    ])

    return list(
        set(domains) - blacklist
    )


def read_domain_file(f: str) -> list:

    domains_normal = list()
    # Read the file and append the domains to the list
    with open(f, 'r') as f:
        for line in f:
            domains_normal.append(line.strip())
    return domains_normal


def write_domain_file(domains: list, f: str) -> None:

    with open(f, 'w') as f:
        for domain in domains:
            f.write(domain + '\n')


def get_longest_domain(domains: list) -> str:
    longest_domain = domains[0]

    for domain in domains:
        if domain.count('.') > longest_domain.count('.'):
            longest_domain = domain

    return longest_domain


def permute_domains_recursive(domains_normal: list, domains_permuted: list) -> list:

    # get the longest domain to see how many times we have to permute
    longest_domain = get_longest_domain(domains_normal)

    # do it once
    domains_permuted = permute_domains(domains_normal)

    # Keep chopping them down
    for i in range(0, longest_domain.count('.')-2):
        domains_permuted = permute_domains(domains_permuted)

    # sort by reverse of string contents, like how DNS likes it :3
    domains_permuted = sorted(domains_permuted, key=lambda x: x[::-1])

    return domains_permuted


def permute_domains(domains_normal: list) -> list:
    domains_permuted = list()
    domains_permuted += domains_normal

    # Permutate the domains
    for domain in domains_normal:
        domain_split = domain.split('.')
        domain_permuted = []
        for i in range(len(domain_split)-1, 0, -1):
            domain_part = domain_split[i]
            domain_permuted.append(domain_part)
        domains_permuted.append('.'.join(domain_permuted[::-1]))

    domains_permuted = remove_stub_domains(domains_permuted)

    return domains_permuted


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--domainfile", required=True, help="Path to a newline-separated list of domains.")
    args = parser.parse_args()

    domain_file_path = args.domainfile
    domain_file_path_permuted = domain_file_path + '.chopped'

    domains_normal = read_domain_file(domain_file_path)

    domains_permuted = permute_domains_recursive(domains_normal, list())
    write_domain_file(domains_permuted, domain_file_path_permuted)
    print("WRITE "+domain_file_path_permuted)

    pprint(set(domains_normal))
    pprint(set(domains_permuted))
