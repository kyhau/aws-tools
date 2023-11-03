"""
Retrieve account ID from the given AWS access key ID(s).

Modified from https://medium.com/@TalBeerySec/a-short-note-on-aws-key-id-f88cc4317489
"""
import base64
import binascii

import click


def get_account_id_from_access_key_id(key_id):
    # Remove ID prefix and do base32 decode
    x = base64.b32decode(key_id[4:])

    # The account ID is 5 bytes but data is shifted by one bit
    y = x[0:6]

    z = int.from_bytes(y, byteorder="big", signed=False)

    mask = int.from_bytes(binascii.unhexlify(b"7fffffffff80"), byteorder="big", signed=False)

    return (z & mask) >> 7


@click.command()
@click.option("--key", "-k", multiple=True, required=True, help="AWS access key ID")
def main(key):
    for k in key:
        print("{:012d}".format(get_account_id_from_access_key_id(k)))


if __name__ == "__main__":
    main()
