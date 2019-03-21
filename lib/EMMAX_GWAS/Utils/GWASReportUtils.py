import os
import json
import csv
import shutil
import logging
import uuid

from pprint import pprint as pp

from installed_clients.DataFileUtilClient import DataFileUtil


class GWASReportUtils:
    def __init__(self, config):
        self.config = config
        self.scratch = config["scratch"]
        self.callback_url = config["SDK_CALLBACK_URL"]
        self.dfu = DataFileUtil(self.callback_url)
        if os.path.isdir(os.path.join(self.scratch, 'mhplot')):
            shutil.rmtree(os.path.join(self.scratch, 'mhplot'))
        shutil.copytree('/kb/module/lib/EMMAX_GWAS/Utils/Report/mhplot/', os.path.join(self.scratch, 'mhplot'))
        self.htmldir = os.path.join(self.scratch, 'mhplot')

    def make_output(self, params, assoc_results):
        # returns out html report object
        assoc_details = []
        html_info = []
        js_pheno_inputs = []
        file_links = []
        failed_phenos = []

        html_info_entry, assoc_results = self.make_html_report(assoc_results, params['variation'])

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
