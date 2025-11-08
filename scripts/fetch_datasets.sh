#!/usr/bin/env bash
set -e
DSDIR="datasets"
BUILDDIR="build"
OUTDIR="output"

if [ ! -d ${DSDIR} ]; then
    mkdir ${DSDIR}
fi

if [ ! -d ${BUILDDIR}]; then
    mkdir ${BUILDDIR}
fi

if [ ! -d ${OUTDIR}]; then
    mkdir ${OUTDIR}
fi

# retrieve the datasets
curl -o ${DSDIR}/zebf-auditory-restoration-1.zip https://figshare.com/ndownloader/files/55083911

# unpack the dataset
unzip -o ${DSDIR}/zebf-auditory-restoration-1.zip -d ${DSDIR}
mv ${DSDIR}/zebf-auditory-restoration-1/* ${DSDIR}/

# delete archive folder and zip file
rm -r ${DSDIR}/zebf-auditory-restoration-1 ${DSDIR}/*.zip
