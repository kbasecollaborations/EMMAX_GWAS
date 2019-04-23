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

        self.htmldir = os.path.join(self.scratch, 'mhplot')
        if os.path.isdir(self.htmldir):
            shutil.rmtree(self.htmldir)
        shutil.copytree('/kb/module/lib/EMMAX_GWAS/Utils/Report/mhplot/', self.htmldir)


    def make_output(self, params, ps_file):
        assembly_contigs = '26606/5/1'

        assembly_obj = self.dfu.get_objects({'object_refs': [assembly_contigs]})['data'][0]
        contigs = assembly_obj['data']['contigs']
        contig_ids = list(contigs.keys())
        contig_ids.sort()
        genome_ref = assembly_obj['data']['genome_ref']

        contig_baselengths = {}
        prev_len = 0

        for id in contig_ids:
            contig_baselengths[id] = prev_len
            prev_len += contigs[id]['length']

        pp(contig_baselengths)

        self.ps_to_tsv(ps_file, contig_baselengths)

        '''
        self.start_mhplot()
        self.snp2gene.annotate_gwas_results({
            'genome_obj': genome_ref,
            'gwas_result_file': 'filtered_tsv.tsv'
        })
        '''

        report_obj = {
            'message': 'reportmsg',
            'objects_created': 'some kind of list',
            'direct_html': None,
            'direct_html_link_index': 0,
            'html_links': self.htmldir,
            'file_links': 'file_links',
            'report_object_name': 'EMMAX_GWAS_report_',
            'workspace_name': params['workspace_name']
        }

        return report_obj

    def ps_to_tsv(self, ps_file, contig_baselengths):
        '''
        This method attempts to create a .TSV file as input for mhplot using both the PS file
        generated from EMMAX output and the contig lengths acquired from KBase
        :param ps_file, contig_baselengths:
        '''
        tsv_file = 'filtered_tsv.tsv'
        js_file = 'pheno.js'

        tsv_delim = '\t'

        inputps = []
        with open(ps_file, 'r', newline='\n') as delimfile:
            psreader = csv.reader(delimfile, delimiter='\t')
            for row in psreader:
                inputps.append(row)
            delimfile.close()

        inputps.sort(key=lambda x: float(x[2]), reverse=False)

        with open(tsv_file, 'w') as newfile:
            newfile.write("SNP\tCHR\tBP\tP\tPOS\n")
            snps_added = 0

            for row in inputps:
                snps_added = snps_added + 1

                if snps_added == 5000:
                    break
                # assoc_entry_limit = 5000, done to remove least significant data

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

        with open(js_file, 'w') as f:
            f.write("var inputs = ['" + tsv_file + "']")
        f.close

        # this moves the files in the data folder to the scratch directory for use in testing
        datadir = os.path.join(self.scratch, 'data')
        if os.path.isdir(datadir):
            shutil.rmtree(datadir)
        shutil.copytree('/kb/module/data/', datadir)

    '''
    def start_mhplot(self):
        # start a server
        mhplot_args = ['python3', '-m', 'http.server']
        # declare a port number? This is blocking our execution.
        mhplot_thread = subprocess.call(mhplot_args)
    '''

    def print_tsv(self):
        inputtsv = []
        with open(output_file, 'r', newline='\n') as tsv_done:
            tsvreader = csv.reader(tsv_done, delimiter='\t')
            counter = 0
            for row in tsvreader:
                inputtsv.append(row)
                counter = counter + 1
                if counter == 20:
                    break

            tsv_done.close()

        for row in inputtsv:
            print(row)