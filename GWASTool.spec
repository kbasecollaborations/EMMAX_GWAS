/*
A KBase module: GWASTool
*/

module GWASTool {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef plink_file_conversions(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
