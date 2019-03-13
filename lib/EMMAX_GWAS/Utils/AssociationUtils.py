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
        # phenotype file is given
        pheno = {}

        # plink files generated for
        plink = {}

        # kinship matrix
        kinmatrix = {}

        # EMMAX association
        emmax = {}

    def plink_files(self):

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