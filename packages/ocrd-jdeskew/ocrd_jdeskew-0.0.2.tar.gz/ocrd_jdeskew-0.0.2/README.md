[![PyPI version](https://badge.fury.io/py/ocrd-jdeskew.svg)](https://badge.fury.io/py/ocrd-jdeskew)

# ocrd_jdeskew

    OCR-D wrapper for Document Image Skew Estimation using Adaptive Radial Projection

  * [Introduction](#introduction)
  * [Installation](#installation)
  * [Usage](#usage)
     * [OCR-D processor interface ocrd-jdeskew](#ocr-d-processor-interface-ocrd-jdeskew)

## Introduction

This offers an [OCR-D](https://ocr-d.de) compliant [workspace processor](https://ocr-d.de/en/spec/cli) for [jdeskew](https://github.com/jdeskew/jdeskew).

## Installation

Create and activate a [virtual environment](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments) as usual.

To install this module along with its dependencies, do:

    pip install .

## Usage

### [OCR-D processor](https://ocr-d.de/en/spec/cli) interface `ocrd-jdeskew`

To be used with [PAGE-XML](https://github.com/PRImA-Research-Lab/PAGE-XML) documents in an [OCR-D](https://ocr-d.de/en/about) annotation workflow.

```
Usage: ocrd-jdeskew [OPTIONS]

  Deskew pages / regions with jdeskew

  > Deskew the regions of the workspace.

  > Open and deserialise PAGE input files and their respective images,
  > then iterate over the element hierarchy down to the requested
  > ``level-of-operation``.

  > Next, for each segment, crop an image according to its layout
  > annotation (via coordinates into the higher-level image, or from an
  > existing alternative image), and determine optimal the deskewing
  > angle for it (up to ``maxskew``). Annotate the angle in the page or
  > region.

  > Derotate the image, and add the new image file to the workspace
  > along with the output fileGrp, and using a file ID with suffix
  > ``.IMG-DESKEW`` along with further identification of the segment.

  > Produce a new output file by serialising the resulting hierarchy.

Options for processing:
  -m, --mets URL-PATH             URL or file path of METS to process [./mets.xml]
  -w, --working-dir PATH          Working directory of local workspace [dirname(URL-PATH)]
  -I, --input-file-grp USE        File group(s) used as input
  -O, --output-file-grp USE       File group(s) used as output
  -g, --page-id ID                Physical page ID(s) to process instead of full document []
  --overwrite                     Remove existing output pages/images
                                  (with "--page-id", remove only those)
  --profile                       Enable profiling
  --profile-file PROF-PATH        Write cProfile stats to PROF-PATH. Implies "--profile"
  -p, --parameter JSON-PATH       Parameters, either verbatim JSON string
                                  or JSON file path
  -P, --param-override KEY VAL    Override a single JSON object key-value pair,
                                  taking precedence over "--parameter"
  -l, --log-level [OFF|ERROR|WARN|INFO|DEBUG|TRACE]
                                  Override log level globally [INFO]

Options for Processing Worker server:
  --queue                         The RabbitMQ server address in format
                                  "amqp://{user}:{pass}@{host}:{port}/{vhost}"
                                  [amqp://admin:admin@localhost:5672]
  --database                      The MongoDB server address in format
                                  "mongodb://{host}:{port}"
                                  [mongodb://localhost:27018]
  --type                          type of processing: either "worker" or "server"

Options for information:
  -C, --show-resource RESNAME     Dump the content of processor resource RESNAME
  -L, --list-resources            List names of processor resources
  -J, --dump-json                 Dump tool description as JSON
  -D, --dump-module-dir           Show the 'module' resource location path for this processor
  -h, --help                      Show this message
  -V, --version                   Show version

Parameters:
   "maxskew" [number]
    modulus of maximum skewing angle (in degrees) to detect
   "level-of-operation" [string - "page"]
    PAGE XML hierarchy level granularity to annotate orientation and
    images for
    Possible values: ["page", "region"]

```


