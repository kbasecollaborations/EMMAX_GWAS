FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

RUN apt-get -y update \
    && apt-get -y install gcc \
    && apt-get -y install g++ \
    && apt-get -y install autoconf \
    && apt-get -y install zlib1g-dev \
    && apt-get -y install wget \
    && apt-get -y install pkg-config \
    && apt-get -y install vim

RUN pip install --upgrade pip \
    && pip install -q pyvcf

RUN git clone https://github.com/vcftools/vcftools.git \
    && cd vcftools \
    && ./autogen.sh \
    && ./configure \
    && make \
    && make install

# taking this out for now RUN chmod 755 deps/vcf_validator_linux
    
RUN sudo apt-get -y install r-cran-ggplot2
# library for r, probably for graphics

RUN pip install pandas
# data analysis library, remove if not used

# ./plink --vcf test_with_chr.vcf --out output
# ./plink --bfile output --recode12 --output-missing-genotype 0 --transpose --out output2


# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

ENV PATH=$PATH:/kb/module/deps

# RUN cd data \
#    && curl -J -L https://easygwas.ethz.ch/rest/phenotype/download/public/AT_P_43/ -o FLC.tsv \
#    && curl -J -L https://easygwas.ethz.ch/down/dataset/download/1/ -o AtPolyDB.zip \
#    && unzip AtPolyDB.zip \
#    && rm phenotypes.pheno

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
