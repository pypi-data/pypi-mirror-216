#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 21:31:31 2023

@author: everest
"""

import requests
from pathlib import Path
import typer
import click
import sys

@click.command()
@click.argument('species')
@click.option('-d', '--directory', help = 'Directory in which to save output', required = False)
def cli(species, directory):
    """
    Acquires all KGML files for a given species. Use KEGG species
    identification, usually a 3 to 4 letter organism code, as input.
    """
    if not directory:
        wd = Path.cwd()
        output_path = wd / 'kgml_{}'.format(species)
        typer.echo(f'No output directory provided. All files will be saved to:\n{output_path}')
        output_path.mkdir(exist_ok = True)
    else:
        output_path = Path(directory)
        if output_path.exists() == False:
            typer.echo('Directory does not exist or is invalid.\nPlease input a valid directory.')
            sys.exit()
    KEGGorg = 'http://rest.kegg.jp/list/organism'
    KEGGlist = 'http://rest.kegg.jp/list/pathway/%s'
    KEGGget = 'http://rest.kegg.jp/get/%s/kgml'
    response = requests.get(KEGGorg).text.split('\n')
    org_list = []
    taxonomy = []
    # The -1 avoids the last element of the list, which is usually a dangling newline
    for i in range(len(response) - 1):
        org_list.append(response[i].split('\t')[1])
        taxonomy.append(response[i].split('\t')[2])
    d = {org_list[i]: taxonomy[i] for i in range(len(taxonomy))}
    if species not in org_list:
        typer.echo(f'Please input a species name in KEGG organism ID format.\nThese are usually {len(min(org_list, key = len))} to {len(max(org_list, key = len))} letter codes.\n--Example: "Homo sapiens" is "hsa"')
    else:
        typer.echo(f'Now acquiring all KGML files for {d[species]}...')
        response = requests.get(KEGGlist % species).text.split('\n')
        # If statement required or will make empty .xml file that corrrupts folder
        pathways = [r.split('\t')[0] for r in response if r]
        for path in pathways:
            typer.echo(f'Now acquiring pathway {path}...')
            config = Path(output_path / '{}.xml'.format(path))
            paths = requests.get(KEGGget % path).text
            if config.is_file():
                pass
            else:
                with open(output_path / '{}.xml'.format(path), 'w') as outfile:
                    outfile.write(paths)