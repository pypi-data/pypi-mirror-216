from __future__ import absolute_import

import json
import os.path
import numpy as np
from pkg_resources import resource_string

import click
from jdeskew.estimator import get_angle

from ocrd.decorators import ocrd_cli_options, ocrd_cli_wrap_processor
from ocrd import Processor
from ocrd_utils import (
    getLogger,
    make_file_id,
    assert_file_grp_cardinality,
    MIMETYPE_PAGE
)
from ocrd_modelfactory import page_from_file
from ocrd_models.ocrd_page import (
    AlternativeImageType,
    PageType,
    to_xml
)

OCRD_TOOL = json.loads(resource_string(__name__, 'ocrd-tool.json').decode('utf8'))
TOOL = 'ocrd-jdeskew'

class JDeskew(Processor):

    def __init__(self, *args, **kwargs):
        kwargs['ocrd_tool'] = OCRD_TOOL['tools'][TOOL]
        kwargs['version'] = OCRD_TOOL['version']
        super().__init__(*args, **kwargs)

    def process(self):
        """Deskew the regions of the workspace.

        Open and deserialise PAGE input files and their respective images,
        then iterate over the element hierarchy down to the requested
        ``level-of-operation``.

        Next, for each segment, crop an image according to its layout annotation
        (via coordinates into the higher-level image, or from an existing
        alternative image), and determine optimal the deskewing angle for it
        (up to ``maxskew``). Annotate the angle in the page or region.

        Derotate the image, and add the new image file to the workspace along
        with the output fileGrp, and using a file ID with suffix ``.IMG-DESKEW``
        along with further identification of the segment.

        Produce a new output file by serialising the resulting hierarchy.
        """
        LOG = getLogger('processor.JDeskew')
        oplevel = self.parameter['level-of-operation']
        assert_file_grp_cardinality(self.input_file_grp, 1)
        assert_file_grp_cardinality(self.output_file_grp, 1)

        for n, input_file in enumerate(self.input_files):
            file_id = make_file_id(input_file, self.output_file_grp)
            page_id = input_file.pageId or input_file.ID
            LOG.info("INPUT FILE %i / %s", n, page_id)

            pcgts = page_from_file(self.workspace.download_file(input_file))
            pcgts.set_pcGtsId(file_id)
            self.add_metadata(pcgts)
            page = pcgts.get_Page()

            for page in [page]:
                page_image, page_coords, _ = self.workspace.image_from_page(
                    page, page_id, feature_filter='binarized')

                if oplevel == 'page':
                    self._process_segment(page, page_image, page_coords,
                                          "page '%s'" % page_id, input_file.pageId,
                                          file_id + '.IMG-DESKEW')
                    continue
                regions = page.get_AllRegions(classes=['Text'])
                if not regions:
                    LOG.warning("Page '%s' contains no text regions", page_id)
                for region in regions:
                    region_image, region_coords = self.workspace.image_from_segment(
                        region, page_image, page_coords, feature_filter='binarized')
                    self._process_segment(region, region_image, region_coords,
                                          "region '%s'" % region.id, input_file.pageId,
                                          file_id + '_' + region.id + '.IMG-DESKEW')

            self.workspace.add_file(
                ID=file_id,
                file_grp=self.output_file_grp,
                pageId=input_file.pageId,
                mimetype=MIMETYPE_PAGE,
                local_filename=os.path.join(self.output_file_grp,
                                            file_id + '.xml'),
                content=to_xml(pcgts))

    def _process_segment(self, segment, image, coords, where, page_id, file_id):
        LOG = getLogger('processor.JDeskew')
        angle0 = coords['angle'] # deskewing (w.r.t. top image) already applied to segment_image
        angle = get_angle(np.array(image), angle_max=self.parameter.get('maxskew', None))

        # segment angle: PAGE orientation is defined clockwise,
        # whereas PIL/ndimage rotation is in mathematical direction:
        orientation = -(angle + angle0)
        orientation = 180 - (180 - orientation) % 360 # map to [-179.999,180]
        segment.set_orientation(orientation) # also removes all deskewed AlternativeImages
        LOG.info("Found angle for %s: %.1f", segment.id, angle)
        # delegate reflection, rotation and re-cropping to core:
        if isinstance(segment, PageType):
            image, coords, _ = self.workspace.image_from_page(
                segment, page_id, fill='background', transparency=True)
        else:
            image, coords = self.workspace.image_from_segment(
                segment, image, coords, fill='background', transparency=True)
        if not angle:
            # zero rotation does not change coordinates,
            # but assures consuming processors that the
            # workflow had deskewing
            coords['features'] += ',deskewed'
        # annotate results
        file_path = self.workspace.save_image_file(
            image,
            file_id,
            file_grp=self.output_file_grp,
            page_id=page_id)
        segment.add_AlternativeImage(AlternativeImageType(
            filename=file_path, comments=coords['features']))
        LOG.debug("Deskewed image for %s saved as '%s'", where, file_path)

@click.command()
@ocrd_cli_options
def ocrd_jdeskew(*args, **kwargs):
    return ocrd_cli_wrap_processor(JDeskew, *args, **kwargs)

