#!/usr/bin/python3
# coding: utf-8
from __future__ import absolute_import

import click
import json

def process(doc):
    print(json.dumps(doc, sort_keys=True, indent=4))

@click.command()
@click.option("--file", type=click.File("r"))
def cli(file):
    for line in file:
        doc = json.loads(line)
        process(doc)

if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
