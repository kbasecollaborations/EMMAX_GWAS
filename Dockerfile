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

RUN wget https://github.com/EBIvariation/vcf-validator/releases/download/v0.9.1/vcf_validator_linux \
    && chmod 755 vcf_validator_linux \
    && mv vcf_validator_linux /kb/deployment/bin 
    
# RUN sudo apt-get -y install r-cran-ggplot2
# library for r, probably for graphics

# RUN sudo apt-get -y install plink
# maybe need this "sudo dpkg --configure -a" ? Could run into trouble with package configure.

RUN curl -O http://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20181202.zip \
    && unzip plink_linux_x86_64_20181202.zip \
    && mv plink /kb/deployment/bin \
    && mv prettify /kb/deployment/bin

RUN pip install pandas
# data analysis library, remove if not used

RUN curl -O http://csg.sph.umich.edu//kang/emmax/download/emmax-beta-07Mar2010.tar.gz \
    && tar -xzf emmax-beta-07Mar2010.tar.gz \
    && mv /emmax-beta-07Mar2010/emmax /kb/deployment/bin \
    && mv /emmax-beta-07Mar2010/emmax-kin /kb/deployment/bin

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
