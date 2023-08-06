import ome_types
import numpy as np
from warnings import warn

from ndbioimage import jvm
from loci.formats import ImageReader
from loci.formats import ChannelSeparator
from loci.formats import MetadataTools
from loci.formats import FormatTools
from loci.formats.meta import MetadataRetrieve


def get_ome(file):
    with ImageReader() as reader:
        omeMeta = MetadataTools.createOMEXMLMetadata()
        reader.setMetadataStore(omeMeta)
        reader.setId(file)
        return ome_types.from_xml(str(omeMeta.dumpXML()), parser='lxml')


class Reader:
    def __init__(self, path):
        reader = ImageReader()
        reader.setId(path)
        self.rdr = reader

    def read(self, c=None, z=0, t=0, series=None, index=None,
             rescale=True, wants_max_intensity=False, channel_names=None, XYWH=None):
        '''Read a single plane from the image reader file.
        :param c: read from this channel. `None` = read color image if multichannel
            or interleaved RGB.
        :param z: z-stack index
        :param t: time index
        :param series: series for ``.flex`` and similar multi-stack formats
        :param index: if `None`, fall back to ``zct``, otherwise load the indexed frame
        :param rescale: `True` to rescale the intensity scale to 0 and 1; `False` to
                  return the raw values native to the file.
        :param wants_max_intensity: if `False`, only return the image; if `True`,
                  return a tuple of image and max intensity
        :param channel_names: provide the channel names for the OME metadata
        :param XYWH: a (x, y, w, h) tuple
        '''
        # env = jutil.get_env()
        if series is not None:
            self.rdr.setSeries(series)

        if XYWH is not None:
            assert isinstance(XYWH, tuple) and len(XYWH) == 4, "Invalid XYWH tuple"
            openBytes_func = lambda x: self.rdr.openBytesXYWH(x, XYWH[0], XYWH[1], XYWH[2], XYWH[3])
            width, height = XYWH[2], XYWH[3]
        else:
            openBytes_func = self.rdr.openBytes
            width, height = self.rdr.getSizeX(), self.rdr.getSizeY()

        pixel_type = self.rdr.getPixelType()
        little_endian = self.rdr.isLittleEndian()
        if pixel_type == FormatTools.INT8:
            dtype = np.int8
            scale = 255
        elif pixel_type == FormatTools.UINT8:
            dtype = np.uint8
            scale = 255
        elif pixel_type == FormatTools.UINT16:
            dtype = '<u2' if little_endian else '>u2'
            scale = 65535
        elif pixel_type == FormatTools.INT16:
            dtype = '<i2' if little_endian else '>i2'
            scale = 65535
        elif pixel_type == FormatTools.UINT32:
            dtype = '<u4' if little_endian else '>u4'
            scale = 2 ** 32
        elif pixel_type == FormatTools.INT32:
            dtype = '<i4' if little_endian else '>i4'
            scale = 2 ** 32 - 1
        elif pixel_type == FormatTools.FLOAT:
            dtype = '<f4' if little_endian else '>f4'
            scale = 1
        elif pixel_type == FormatTools.DOUBLE:
            dtype = '<f8' if little_endian else '>f8'
            scale = 1
        max_sample_value = self.rdr.getMetadataValue('MaxSampleValue')
        if max_sample_value is not None:
            try:
                scale = max_sample_value
            except:
                warn("WARNING: failed to get MaxSampleValue for image. Intensities may be improperly scaled.")
        if index is not None:
            image = np.frombuffer(openBytes_func(index), dtype)
            if len(image) / height / width in (3, 4):
                n_channels = int(len(image) / height / width)
                if self.rdr.isInterleaved():
                    image.shape = (height, width, n_channels)
                else:
                    image.shape = (n_channels, height, width)
                    image = image.transpose(1, 2, 0)
            else:
                image.shape = (height, width)
        elif self.rdr.isRGB() and self.rdr.isInterleaved():
            index = self.rdr.getIndex(z, 0, t)
            image = np.frombuffer(openBytes_func(index), dtype)
            image.shape = (height, width, self.rdr.getSizeC())
            if image.shape[2] > 3:
                image = image[:, :, :3]
        elif c is not None and self.rdr.getRGBChannelCount() == 1:
            index = self.rdr.getIndex(z, c, t)
            image = np.frombuffer(openBytes_func(index), dtype)
            image.shape = (height, width)
        elif self.rdr.getRGBChannelCount() > 1:
            n_planes = self.rdr.getRGBChannelCount()
            rdr = ChannelSeparator(self.rdr)
            planes = [
                np.frombuffer(
                    (rdr.openBytes(rdr.getIndex(z, i, t)) if XYWH is None else
                     rdr.openBytesXYWH(rdr.getIndex(z, i, t), XYWH[0], XYWH[1], XYWH[2], XYWH[3])),
                    dtype
                ) for i in range(n_planes)]

            if len(planes) > 3:
                planes = planes[:3]
            elif len(planes) < 3:
                # > 1 and < 3 means must be 2
                # see issue #775
                planes.append(np.zeros(planes[0].shape, planes[0].dtype))
            image = np.dstack(planes)
            image.shape = (height, width, 3)
            del rdr
        elif self.rdr.getSizeC() > 1:
            images = [
                np.frombuffer(openBytes_func(self.rdr.getIndex(z, i, t)), dtype)
                for i in range(self.rdr.getSizeC())]
            image = np.dstack(images)
            image.shape = (height, width, self.rdr.getSizeC())
            if not channel_names is None:
                metadata = MetadataRetrieve(self.metadata)
                for i in range(self.rdr.getSizeC()):
                    index = self.rdr.getIndex(z, 0, t)
                    channel_name = metadata.getChannelName(index, i)
                    if channel_name is None:
                        channel_name = metadata.getChannelID(index, i)
                    channel_names.append(channel_name)
        elif self.rdr.isIndexed():
            #
            # The image data is indexes into a color lookup-table
            # But sometimes the table is the identity table and just generates
            # a monochrome RGB image
            #
            index = self.rdr.getIndex(z, 0, t)
            image = np.frombuffer(openBytes_func(index), dtype)
            if pixel_type in (FormatTools.INT16, FormatTools.UINT16):
                lut = self.rdr.get16BitLookupTable()
                if lut is not None:
                    lut = np.array(lut)
                    # lut = np.array(
                    #     [env.get_short_array_elements(d)
                    #      for d in env.get_object_array_elements(lut)]) \
                    #     .transpose()
            else:
                lut = self.rdr.get8BitLookupTable()
                if lut is not None:
                    lut = np.array(lut)
                    # lut = np.array(
                    #     [env.get_byte_array_elements(d)
                    #      for d in env.get_object_array_elements(lut)]) \
                    #     .transpose()
            image.shape = (height, width)
            if (lut is not None) \
                    and not np.all(lut == np.arange(lut.shape[0])[:, np.newaxis]):
                image = lut[image, :]
        else:
            index = self.rdr.getIndex(z, 0, t)
            image = np.frombuffer(openBytes_func(index), dtype)
            image.shape = (height, width)

        if rescale:
            image = image.astype(np.float32) / float(scale)
        if wants_max_intensity:
            return image, scale
        return image
