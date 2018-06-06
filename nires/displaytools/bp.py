#!/usr/bin/env python
# buffer picture for nires quicklook

import logging
import click
import configparser

import nires.displaytools.helpers as helpers

LOG = logging.getLogger(__name__)
METADATA_FILE = ".metadata"


def get_buffer(data_dir, inst):
    """
    get the buffer image if it exists
    :param inst:
    :return:
    """
    config = configparser.ConfigParser()
    config.read("{}/{}".format(data_dir, METADATA_FILE))
    try:
        return config["buffer"][inst]
    except (TypeError, KeyError):
        return None


def set_buffer_image(inst, value, data_dir="."):
    """
    set the buffer image for the instrument quicklook
    :param inst:
    :param value:
    :param data_dir:
    :return:
    """
    config = configparser.ConfigParser()
    config.read("{}/{}".format(data_dir, METADATA_FILE))
    try:
        config["buffer"][inst] = value
    except (TypeError, KeyError):
        config["buffer"] = {}
        config["buffer"][inst] = value

    with open("{}/{}".format(data_dir, METADATA_FILE), "w") as configfile:
        config.write(configfile)


@click.command()
@click.argument("inst", type=click.Choice(["v", "s"]), nargs=1)
@click.argument("fnum", nargs=1)
@click.option("--d", default=".")
def run(inst, fnum, d):
    """
    Script to display a picture
    """
    try:
        if fnum == "show":
            LOG.warning("Buffer image for instrument: %s is %s", inst, get_buffer(d, inst))
        elif fnum == "none":
            set_buffer_image(inst, "none", data_dir=d)
        else:
            fname = helpers.name_resolve(fnum, inst, data_dir=d)
            if fname:
                set_buffer_image(inst, fname, data_dir=d)
            else:
                LOG.warning("Buffer image for instrument: %s is %s", inst, get_buffer(d, inst))

    except (UnboundLocalError, ValueError, IndexError):
        LOG.warning("Bad Request:\n   Unable to display picture\n"
                    "Example valid requests:\n"
                    "   bp s 11\n"
                    "   bps 11\n"
                    "   bps lp\n"
                    "   bpv 7")

if __name__ == '__main__':
    run()
