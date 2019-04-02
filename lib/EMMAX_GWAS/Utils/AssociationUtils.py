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

        self.plink_base_prefix = 'plink_variation'

    def local_run_association(self):
        # univariate analysis?
        os.chdir('../data')
        subprocess.call('pwd')

        # plink files generated for
        self.plink_method()

        # prepare phenotype - set of physical characteristics associated with a trait (genotype has to do with DNA)
        # for the moment, we are curling these in the docker terminal
        self.create_newpheno()

        subprocess.call('ls')
        # kinship matrix
        self.kinship_method()

        # EMMAX association
        # call create_newpheno to format phenotype file for EMMAX
        self.emmax_method()

        return 'emmax_assoc.ps'

    def kinship_method(self):
        emmax_kin_args = ['-v', '-d', '10', self.plink_base_prefix]

        emmax_kin_cmd = ['emmax-kin']

        for args in emmax_kin_args:
            emmax_kin_cmd.append(args)

        try:
            proc = subprocess.Popen(emmax_kin_cmd)
            proc.wait()

        except Exception as e:
            exit(e)

    def emmax_method(self):
        emmax_args = ['-v', '-d', '10', '-t', self.plink_base_prefix, '-p', 'newpheno', '-k',
                      self.plink_base_prefix + '.BN.kinf', '-o', 'emmax_assoc']

        emmax_cmd = ['emmax']

        for args in emmax_args:
            emmax_cmd.append(args)

        try:
            proc = subprocess.Popen(emmax_cmd)
            proc.wait()

        except Exception as e:
            exit(e)

    def plink_method(self):
        plink_args = ['--file', 'genotype', '--output-missing-genotype', '0', '--recode', '12', 'transpose',
                      '--pheno', 'FLC.tsv', '--output-missing-phenotype', 'NA', '--allow-no-sex',
                      '--allow-extra-chr', '--out', self.plink_base_prefix]
        plink_cmd = ['plink']

        for args in plink_args:
            plink_cmd.append(args)
        try:
            proc = subprocess.Popen(plink_cmd)
            proc.wait()

        except Exception as e:
            exit(e)

    def create_newpheno(self):
        # Chris Schneider's phenotype stuff, reformats pheno file to a format that EMMAX likes
        # ex. input: 'test_tped.tfam'
        inputphenos = []
        with open('plink_variation.tfam', 'r', newline='\n') as delimfile:
            phenoreader = csv.reader(delimfile, delimiter=' ')
            for row in phenoreader:
                inputphenos.append(row)
            delimfile.close()
        with open('newpheno', 'w') as newfile:
            for pheno in inputphenos:
                newfile.write(pheno[0] + ' ' + pheno[1] + ' ' + pheno[5] + '\n')
            newfile.close()
