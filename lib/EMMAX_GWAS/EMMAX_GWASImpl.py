# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import subprocess

from installed_clients.KBaseReportClient import KBaseReport

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.VariationUtilClient import VariationUtil
from EMMAX_GWAS.Utils.AssociationUtils import AssociationUtils
from EMMAX_GWAS.Utils.GWASReportUtils import GWASReportUtils
#END_HEADER


class EMMAX_GWAS:
    '''
    Module Name:
    EMMAX_GWAS

    Module Description:
    A KBase module: EMMAX_GWAS
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/kbasecollaborations/EMMAX_GWAS.git"
    GIT_COMMIT_HASH = "b1b0c587fb02054b3a2131330e5c633b360ff270"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
        self.shared_folder = config['scratch']
        self.dfu = DataFileUtil(self.config['SDK_CALLBACK_URL'])
        self.vu = VariationUtil(self.config['SDK_CALLBACK_URL'])

        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass

    def run_emmax_association(self, ctx, params):
        # we are in kb/module/test when this method is run in a server test

        """
        :param params: instance of type "GemmaGwasInput" -> structure:
           parameter "workspace_name" of String, parameter "assoc_obj_name"
           of String, parameter "trait_matrix" of type "trait_ref" (KBase
           style object reference X/Y/Z to a KBaseMatrices.TraitMatrix
           structure @id ws KBaseMatrices.TraitMatrix), parameter "variation"
           of type "var_ref" (KBase style object reference X/Y/Z to a @id ws
           KBaseGwasData.Variations)
        :returns: instance of type "GwasResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String,
           parameter "association_obj" of type "assoc_ref" (KBase style
           object reference X/Y/Z to a @id ws KBaseGwasData.Associations)
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_emmax_association

        if 'variation' not in params:
            raise ValueError('Variation KBase reference not set.')
        if 'trait_matrix' not in params:
            raise ValueError('Trait matrix KBase reference not set.')
        if 'assoc_obj_name' not in params:
            raise ValueError('Association object name not given.')

        logging.info("Downloading variation data from shock.")
        variations = VariationUtil(self.config['SDK_CALLBACK_URL'])
        variation_info = variations.get_variation_as_vcf({
            'variation_ref': params['variation'],
            'filename': os.path.join(self.config['scratch'], 'variation.vcf')
        })
        # downloads into /kb/module/work/tmp/variation.vcf
        # subprocess.call('pwd')

        logging.info("Performing association...")
        association_util = AssociationUtils(self.config, variation_info['path'])
        assoc_file = association_util.local_run_association()

        output = {}

        # check to see if association was successful before calling ReportUtils
        if association_util.success() == 1:
            logging.info("Formatting output...")
            gwas_report_util = GWASReportUtils(self.config)
            gwas_report = gwas_report_util.make_output(params, assoc_file)
            output = gwas_report

        '''
        Report functionality is not yet ready, but will look something like this,
        
        report_client = KBaseReport(self.config['SDK_CALLBACK_URL'])
        report = report_client.create_extended_report(report_obj)

        output = {
           'report_name': report['name'],
           'report_ref': report['ref'],
           'ws': params['workspace_name']
        }
        '''
        #END run_emmax_association

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_gemma_association return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
