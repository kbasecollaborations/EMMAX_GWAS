import subprocess
import os
import operator
import shutil
import csv
from pprint import pprint as pp

from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.WorkspaceClient import Workspace


class AssociationUtils:
    def __init__(self, config, variation_path):
        self.dfu = DataFileUtil(config['SDK_CALLBACK_URL'])

        # variable used as the prefix for most files used here
        self.plink_base_prefix = 'plink_variation'

        # 0 while association is unsuccessful, 1 when completed successfully
        self.success = 0

    def run_association(self):
        # calls all class methods needed to perform EMMAX GWAS association.
        self.plink_method()
        self.create_newpheno()
        self.kinship_method()
        self.emmax_method()

        self.success = 1
        return 'emmax_assoc.ps'

    def kinship_method(self):
        # prepares the kinship matrix using emmax-kin
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
        # performs EMMAX association using an EMMAX command
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
        # produces .TPED and .TFAM files using Plink commands
        '''
        Currently testing commands to process a VCF

        Replace both of the commands below with this one if doing local testing. (no VCF,
        using the curl commands in the Dockerfile)

        plink_args = ['--file', 'genotype', '--output-missing-genotype', '0', '--recode', '12', 'transpose',
                      '--pheno', 'FLC.tsv', '--output-missing-phenotype', 'NA', '--allow-no-sex',
                      '--allow-extra-chr', '--out', self.plink_base_prefix]
        plink_cmd = ['plink']
        '''

        plink_args = ['--vcf', 'variation.vcf', '--out', self.plink_base_prefix]
        plink_cmd = ['plink']

        for args in plink_args:
            plink_cmd.append(args)
        try:
            proc = subprocess.Popen(plink_cmd)
            proc.wait()

        except Exception as e:
            exit(e)

        plink_args_2 = ['--bfile', self.plink_base_prefix, '--recode12',
                      '--output-missing-genotype', 0, '--transpose', '--out', self.plink_base_prefix]
        plink_cmd_2 = ['plink']

        for args in plink_args_2:
            plink_cmd_2.append(args)
        try:
            proc = subprocess.Popen(plink_cmd_2)
            proc.wait()

        except Exception as e:
            exit(e)

    def create_newpheno(self):
        # reformats pheno file to a format that EMMAX likes
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

    def success(self):
        return self.success
