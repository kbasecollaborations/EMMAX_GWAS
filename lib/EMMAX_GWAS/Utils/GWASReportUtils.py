import os
import json
import csv
import shutil
import logging
import uuid

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

    def make_output(self, params, assoc_results):
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
            contig_baselengths[id] = contigs[id]['length']
        pp(contig_baselengths)

        self.create_tsv()

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

    def create_test_tsv(self):
        tsv_filtered_headers = "SNP\tCHR\tBP\tP\tPOS\n"

        filtered_tsv_file = 'test_tsv.tsv'

        with open(filtered_tsv_file, 'w') as tsv_filtered:
            tsv_filtered.write(tsv_filtered_headers)

            tsv_filtered.write('Chr5_10172992' + "\t" + '5' + "\t" + '10172992' + "\t" + '3.355332e-11' + "\t"
                               + '102343838' + "\n")
            tsv_filtered.write('Chr1_6148689' + "\t" + '1' + "\t" + '6148689' + "\t" + '1.171374e-11' + "\t"
                               + '6148689' + "\n")
            tsv_filtered.write('Chr3_18592228' + "\t" + '3' + "\t" + '18592228' + "\t" + '1.927625e-08' + "\t"
                               + '68718188' + "\n")
            tsv_filtered.write('Chr1_1493521' + "\t" + '1' + "\t" + '1493521' + "\t" + '9.377403e-08' + "\t"
                               + '1493521' + "\n")
            tsv_filtered.write('Chr1_4128051' + "\t" + '1' + "\t" + '4128051' + "\t" + '1.846375e-07' + "\t"
                               + '4128051' + "\n")

            tsv_filtered.close()

        with open(filtered_tsv_file, 'r') as tsv_filtered_opened:
            print(tsv_filtered_opened.read())

    def ps_to_tsv(self):
        output_file = 'pyoutput.tsv'
        assoc_entry_limit = 5000
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
                SNP = 's' + CHR + BP
                newfile.write(SNP + tsv_delim + CHR + tsv_delim + BP + tsv_delim + P + '\n')
            newfile.close()
