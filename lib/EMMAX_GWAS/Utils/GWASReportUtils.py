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
        assembly_contigs = assembly_obj['data']['contigs']
        contig_ids = list(assembly_contigs.keys())
        contig_ids.sort()

        contig_baselengths = {}
        prev_len = 0

        for id in contig_ids:
            contig_baselengths[id] = assembly_contigs[id]['length']
        pp(contig_baselengths)

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

    def make_html_report(self, assoc_results, variation_ref):
        assoc_results = self.filter_assoc_results(trai)

        return {}, {}

    def create_tsv(self):
        ps_file = 'emmax_assoc.ps'
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
        # sortedps = sorted(inputps, key=lambda x: x[2])

        with open(output_file, 'w') as newfile:
            for row in inputps:
                newfile.write(row[0] + tsv_delim + row[1] + tsv_delim + row[2] + '\n')
            newfile.close()
