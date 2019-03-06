/*
A KBase module: EMMAX_GWAS
*/

module EMMAX_GWAS {
    /* typedefs for input/output values */

    /* A boolean - 0 for false, 1 for true. @range (0, 1) */
    typedef int boolean;

    /* An X/Y/Z style reference*/
    typedef string obj_ref;

    /* KBase file path to staging files */
    typedef string filepath;

    /*
        KBase style object reference X/Y/Z to a KBaseMatrices.TraitMatrix structure
            @id ws KBaseMatrices.TraitMatrix
    */
    typedef string trait_ref;

    /*
        KBase style object reference X/Y/Z to a
            @id ws KBaseGwasData.Variations
    */
    typedef string var_ref;

    /*
        KBase style object reference X/Y/Z to a
            @id ws KBaseGwasData.Associations
    */
    typedef string assoc_ref;

	typedef structure {
	    string workspace_name;
	    string assoc_obj_name;
		trait_ref trait_matrix;
		var_ref variation;
	} GemmaGwasInput;

    typedef structure {
        string report_name;
        string report_ref;
        assoc_ref association_obj;
    } GwasResults;

    funcdef run_emmax_association(GemmaGwasInput params) returns (GwasResults output) authentication required;
};
