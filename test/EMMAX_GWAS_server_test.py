# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from EMMAX_GWAS.EMMAX_GWASImpl import EMMAX_GWAS
from EMMAX_GWAS.EMMAX_GWASServer import MethodContext
from EMMAX_GWAS.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace

class EMMAX_GWASTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('EMMAX_GWAS'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'EMMAX_GWAS',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = EMMAX_GWAS(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_EMMAX_GWAS" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa

    # While in development you can leave tests alone. Tests will only run automatically if the function name
    # starts with 'test_'.
    
    def local_test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods

        result = self.serviceImpl.run_emmax_association(self.ctx, {
            'workspace_name': self.wsName,
            'variation': ' '})

    def test_kbase_your_method(self):
        result = self.serviceImpl.run_emmax_association(self.ctx, {
            'workspace_name': 'ntrobinson:narrative_1553207305943',
            'variation': '26606/3/1',
            'trait_matrix': '26606/2/1'})
