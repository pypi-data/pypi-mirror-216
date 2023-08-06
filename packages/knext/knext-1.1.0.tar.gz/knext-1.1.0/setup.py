# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['knext']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'networkx>=3.1,<4.0',
 'pandas>=2.0.2,<3.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'pytest>=7.3.2,<8.0.0',
 'requests>=2.31.0,<3.0.0',
 'typer>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['knext = src.__main__:cli']}

setup_kwargs = {
    'name': 'knext',
    'version': '1.1.0',
    'description': 'Kyoto Encylopedia of Genes and Genomes Markup Language File parser and converter',
    'long_description': "\nKEGG NetworkX Topological (KNeXT) parser\n========================================\n\nKNeXT downloads and parses Kyoto Encylopedia of Genes and Genomes \n(KEGG) markup language files (KGML). This tool employs NetworkX's framework\nto create gene-only networks, but mixed (gene, compound, pathway) networks\ncan also be generated. All output files are in TSV format. KNeXT also\nretrieves a TXT file of node x-y axis coordinates for use in NetworkX's\ngraph visualization library, and it is able to convert KEGG IDs \ninto Uniprot and NCBI IDs. KNeXT also maximizes metadata information\nthrough preserving each edge's information.\n\nUsage\n-----\n\n.. code:: text\n\n    Primary line: knext get-kgml [SPECIES_NAME]\n      \n      KEGG NetworkX Topological (KNeXT) parser uses the KEGG\n      API to gather all KGML files for a single species. \n      Input species name in 3 to 4 letter KEGG organism code. \n    \n    Options:\n      --help,\tshows options and website for KEGG organism codes\n      -d/--d,\tdirectory in which to save output\n\n    Primary line: knext genes [Input]\n\n      KNeXT parser deploy's NetworkX's\n      framework to create gene-only representations of KGML files.\n      Genes between compounds are propagated before compounds are dropped.\n\n    Options:\n      Input\tKGML file or folder of KGML files to parse\n      -r/--results\tfile or folder where output should be stored\t\n      -g/--graphics\toutputs TXT file of x-y axis coordinates\n      -u/--unique\tTSV file's genes have a terminal modifier\n      --help\tshows options and file types\n\n    Primary line: knext mixed [Input]\n\n      KNeXT parser creates mixed (genes, compounds, pathways)\n      representations of KGML files.\n\n    Options:\n      Input\tKGML file or folder of KGML files to parse\n      -r/--results\tfile or folder where output should be stored\n      -g/--graphics\toutputs TXT file of x-y axis coordinates\n      -u/--unique\tTSV file's genes have a terminal modifier\n      --help\tshows options and file types\n\n    Primary line: knext convert [OPTIONS]\n      \n      KNeXT parser converts KEGG entry IDs in TSV output files into\n      UniProt or NCBI IDs.\n    \n    Options:\n      file\tPATH:\tpath to TSV file\n      species\tTEXT:\tKEGG 3 to 4 letter organism code\n      --uniprot\toptional flag for output:\tuse if UniProt IDs are the desired output\n      --unique\toptional flag for output:\tuse if the TSV file has terminal modifiers\n      --graphics\tPATH:\tgraphics file\n      --help\toptional flag:\tshows options\n\n    Options:\n      folder\tPATH:\tpath to folder containing TSV files         \n      species\tTEXT:\tKEGG 3 to 4 letter organism code\n      --uniprot\toptional flag for output:         use if UniProt IDs are the desired output\n      --unique\toptional flag for output:         use if the TSV file has terminal modifiers   \n      --graphics\tPATH:       path to folder containing graphics files          \n      --help\toptional flag:            shows options\n\nFor example, KNeXT can obtain all KGML files for Homo sapiens:\n\n.. code:: text\n\n    $ knext get-kgml hsa\n\nThe resulting output folder can be used to parse the files:\n\n.. code:: text\n      \n    $ knext genes folder kgml_hsa --graphics\n\nThe resulting output folder can be used to convert the TSV files and graphics file:\n\n.. code:: text\n      \n    $ knext convert folder kegg_gene_network_hsa hsa --graphics kegg_gene_network_hsa\n\nInputs\n------\n\nKNeXT only accepts KGML files downloaded from `KEGG <https://www.genome.jp/kegg/>`__\n\nThe output of which can be used in successive commands.\nAll input formats *must be* in TSV format.\nColumn names are mandatory and should not be changed.\n\nData Frames\n'''''''''''\n\n.. csv-table:: Example TSV file with KEGG ID's\n\t:header: entry1, entry2, type, value, name\n\n\thsa:100271927-98, hsa:22800-12, PPrel, -->, activation\n\thsa:100271927-98, hsa:22808-12, PPrel, -->, activation\n\thsa:100271927-98, hsa:3265-12, PPrel, -->, activation\n\n.. csv-table:: Example TSV file for uniprot conversion with `--unique` output \n\t:escape: `\n        :header: entry1, entry2, type, value, name\n\n\tQ9Y243-23, O15111-59, PPrel, -->, activation\n\tQ9Y243-23, Q6GYQ0-240, PPrel`,`PPrel, --``|```,`+p, inhibition`,`phosphorylation\n\tQ9Y243-23, O14920-59, PPrel, -->, activation\n\nInstallation\n------------\n\nThe current release is :code:`v1.1.0`\nInstallation is via pip:\n\n.. code:: bash\n\n    $ pip install https://github.com/everest/knext/knext-1.0.0.tar.gz\n\nRepo can be downloaded and installed through poetry__:\n\n.. code:: bash\n\n    $ git clone https://github.com/everest/knext.git\n    $ cd knext\n    $ poetry shell\n    $ poetry install\n    $ poetry run knext [get-kgml, genes, mixed, or convert]\n\n.. __: https://python-poetry.org/\n\nRequirements\n------------\n\nRequirements are (also see ``pyproject.toml``):\n\n- Python >= 3.9\n- typer__\n- click__\n- requests__\n- pandas__\n- networkx__\n- pytest__\n- pathlib__\n- pytest__\n\n.. __: https://typer.tiangolo.com/\n.. __: https://click.palletsprojects.com/en/8.1.x/\n.. __: https://requests.readthedocs.io/en/latest/\n.. __: https://pandas.pydata.org/\n.. __: https://networkx.org/\n.. __: https://docs.pytest.org/en/7.2.x/\n.. __: https://pathlib.readthedocs.io/en/pep428/\n.. __: https://docs.pytest.org/en/7.1.x/contents.html\n",
    'author': 'Everest Uriel Castaneda',
    'author_email': 'everest_castaneda1@baylor.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
