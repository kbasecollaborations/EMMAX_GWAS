# -*- coding: utf-8 -*-
############################################################
#
# Autogenerated by the KBase type compiler -
# any changes made here will be overwritten
#
############################################################

from __future__ import print_function
# the following is a hack to get the baseclient to import whether we're in a
# package or not. This makes pep8 unhappy hence the annotations.
try:
    # baseclient and this client are in a package
    from .baseclient import BaseClient as _BaseClient  # @UnusedImport
except ImportError:
    # no they aren't
    from baseclient import BaseClient as _BaseClient  # @Reimport


class snp2gene(object):

    def __init__(
            self, url=None, timeout=30 * 60, user_id=None,
            password=None, token=None, ignore_authrc=False,
            trust_all_ssl_certificates=False,
            auth_svc='https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login',
            service_ver='dev',
            async_job_check_time_ms=100, async_job_check_time_scale_percent=150, 
            async_job_check_max_time_ms=300000):
        if url is None:
            raise ValueError('A url is required')
        self._service_ver = service_ver
        self._client = _BaseClient(
            url, timeout=timeout, user_id=user_id, password=password,
            token=token, ignore_authrc=ignore_authrc,
            trust_all_ssl_certificates=trust_all_ssl_certificates,
            auth_svc=auth_svc,
            async_job_check_time_ms=async_job_check_time_ms,
            async_job_check_time_scale_percent=async_job_check_time_scale_percent,
            async_job_check_max_time_ms=async_job_check_max_time_ms)

    def annotate_gwas_results(self, params, context=None):
        """
        annotate_gwas_results:
        inputs:
            file path to gwas results
            genome object - with reference to GFF file
        outputs:
            TSV file represented by shock/handle ids and
        :param params: instance of type "annotate_gwas_input" -> structure:
           parameter "gwas_result_file" of type "file_path" (A valid file
           path), parameter "genome_obj" of type "genome_ref" (KBase style
           object reference X/Y/Z @id ws KBaseGenomes.Genome)
        :returns: instance of type "annotate_gwas_output" -> structure:
           parameter "snp_to_gene_list" of type "file_path" (A valid file
           path)
        """
        return self._client.run_job('snp2gene.annotate_gwas_results',
                                    [params], self._service_ver, context)

    def status(self, context=None):
        return self._client.run_job('snp2gene.status',
                                    [], self._service_ver, context)