import os
import json
import csv
import shutil
import logging
import uuid
import subprocess

from pprint import pprint as pp

from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.snp2geneClient import snp2gene
from installed_clients.WorkspaceClient import Workspace


class GWASReportUtils:
    def __init__(self, config):
        self.config = config
        self.scratch = config["scratch"]
        self.callback_url = config["SDK_CALLBACK_URL"]
        self.dfu = DataFileUtil(self.callback_url)
        self.snp2gene = snp2gene(self.callback_url)
        #self.wsc = Workspace(config["ws_url"])

        if os.path.isdir(os.path.join(self.scratch, 'mhplot')):
            shutil.rmtree(os.path.join(self.scratch, 'mhplot'))
        shutil.copytree('/kb/module/lib/EMMAX_GWAS/Utils/Report/mhplot/', os.path.join(self.scratch, 'mhplot'))
        self.htmldir = os.path.join(self.scratch, 'mhplot')

    def make_output(self, params, ps_file):
        genome_ref = '26606/5/1'

        '''
        Our goal is to parse the .ps file resulting from EMMAX output and combining it
        with contig lengths from the assembly file into a formated TSV
        '''

        assembly_obj = self.dfu.get_objects({'object_refs': ['26606/5/1']})['data'][0]
        contigs = assembly_obj['data']['contigs']
        contig_ids = list(contigs.keys())
        contig_ids.sort()

        contig_baselengths = {}
        prev_len = 0

        for id in contig_ids:
            contig_baselengths[id] = prev_len
            prev_len += contigs[id]['length']

        print(contig_baselengths)

        pp(contig_baselengths)

        self.ps_to_tsv(ps_file, contig_baselengths)
        # should now have a file called 'test_tsv.tsv'

        mhplot_args = ['python3', '-m', 'http.server']
        subprocess.call(mhplot_args)

        report_obj = {
            'message': 'reportmsg',
            'objects_created': 'some kind of list',
            'direct_html': None,
            'direct_html_link_index': 0,
            'html_links': 'html_info',
            'file_links': 'file_links',
            'report_object_name': 'EMMAX_GWAS_report_',
            'workspace_name': params['workspace_name']
        }

        return report_obj

    def ps_to_tsv(self, ps_file, contig_baselengths):
        output_file = 'test_tsv.tsv'
        # assoc_entry_limit = 5000
        tsv_delim = '\t'

        inputps = []
        with open(ps_file, 'r', newline='\n') as delimfile:
            psreader = csv.reader(delimfile, delimiter='\t')
            for row in psreader:
                inputps.append(row)
            delimfile.close()

        inputps.sort(key=lambda x: float(x[2]), reverse=False)

        with open(output_file, 'w') as newfile:
            newfile.write("SNP\tCHR\tBP\tP\tPOS\n")
            for row in inputps:
                # row[0] = Chr<CHR>_<BP>
                # row[2] = <P>
                BP = row[0][5:]
                CHR = row[0][3]
                P = row[2]
                SNP = 'Chr' + CHR + '_' + BP
                global_base = int(contig_baselengths['Chr' + CHR])

                # previous contig's baselength + BP
                POS = str(int(BP) + global_base)
                newfile.write(SNP + tsv_delim + CHR + tsv_delim + BP + tsv_delim + P + tsv_delim + POS + '\n')
            newfile.close()

        with open('pheno.js', 'w') as f:
            f.write("var inputs = ['" + output_file + "']")
        f.close

        '''
        inputtsv = []
        with open(output_file, 'r', newline='\n') as tsv_done:
            tsvreader = csv.reader(tsv_done, delimiter='\t')
            for row in tsvreader:
                inputtsv.append(row)

            tsv_done.close()

        for row in inputtsv:
            print(row)
        '''
