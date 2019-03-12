# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from installed_clients.KBaseReportClient import KBaseReport

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.VariationUtilClient import VariationUtil
from EMMAX_GWAS.Utils.AssociationUtils import AssociationUtils
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
        self.config['test_data_dir'] = os.path.abspath('/kb/testdata')
        self.shared_folder = config['scratch']
        self.dfu = DataFileUtil(self.config['SDK_CALLBACK_URL'])
        self.vu = VariationUtil(self.config['SDK_CALLBACK_URL'])

        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_emmax_association(self, ctx, params):
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

        """
            Here is where the meat of your logic will go. 
            I have created a few Utils classes in GEMMA_GWAS, and I would recommend doing it that way
            I have a class for association test, input validations, and report generation
            Your class calls and simple data validation can go here.
            
            For the time being use file local to the module for analysis and do not worry about Kbase objects
            i.e.
                file = '/path/to/local/file'
                
                emmax file
                
                *handle output*
                
            After this minimal viable product is achieved we can transition to KBase objects
        """

        # You can retreive the VCF file by:
        """
        
        once we're ready to do KBase testing, use this
        "get_variation_as_vcf" returns a file path and name
        
        variation_info = self.vu.get_variation_as_vcf({
            'variation_ref': params['variation'],
            # this is where the vcf will be saved to
            # use config['scratch'] location for all file operations
            'filename': os.path.join(self.config['scratch'], 'variation.vcf')
        })
        """

        # files = {'/data/ped_file.ped', '/data/map_file.map', '/data/pheno_file.pheno'}
        data_files = {'/data/'}

        association_util = AssociationUtils(self.config, data_files)

        assoc_file = associations.local_run_assoc(data_files)



        output = {}

        #END run_emmax_association

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_emmax_association return value ' +
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
