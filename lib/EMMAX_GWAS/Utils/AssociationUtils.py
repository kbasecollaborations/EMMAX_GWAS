import subprocess
import os
import operator
import shutil
import csv
from pprint import pprint as pp

from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.WorkspaceClient import Workspace

class AssociationUtils:
    def __init__(self, config):
        self.dfu = DataFileUtil(config['SDK_CALLBACK_URL'])
        self.datadir = config['TEST_DATA_DIR']

    def local_run_association(self):
        # univariate analysis?

        # prepare phenotype - set of physical characteristics associated with a trait (genotype has to do with DNA)
        # for the moment, we are curling these in the docker terminal
        pheno = {}

        # plink files generated for
        plink = self.plink_method()
        print(plink)

        # kinship matrix
        kinmatrix = {}

        # EMMAX association
        # call create_newpheno to format phenotype file for EMMAX
        emmax = {}

    def plink_method(self):
        plink_base_prefix = 'plink_variation'

        plink_args = ['--file', 'genotype', '--output-missing-genotype', '0', '--recode', '12', 'transpose',
                         '--pheno', 'FLC.tsv', '--output-missing-phenotype', 'NA', '--out', plink_base_prefix]
        plink_cmd = ['plink']

        for args in plink_args:
            plink_cmd.append(args)

        try:
            proc = subprocess.Popen(plink_cmd, cwd='../data/')
            proc.wait()

        except Exception as e:
            exit(e)

        return {'output': '?PLACEHOLDER OUTPUT?'}

    def create_newpheno(self):
        # Chris Schneider's phenotype stuff, reformats pheno file to a format that EMMAX likes
        inputphenos = []
        with open('test_tped.tfam', 'r', newline='\n') as delimfile:
            phenoreader = csv.reader(delimfile, delimiter=' ')
            for row in phenoreader:
                inputphenos.append(row)
            delimfile.close()
        with open('newpheno', 'w') as newfile:
            for pheno in inputphenos:
                newfile.write(pheno[0] + ' ' + pheno[1] + ' ' + pheno[5] + '\n')
            newfile.close()