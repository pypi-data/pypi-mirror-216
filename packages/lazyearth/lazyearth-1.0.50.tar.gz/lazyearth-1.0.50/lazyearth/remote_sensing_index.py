import xarray
import numpy

class index():
    # def __init__(self,DataArray):
        # self.DataArray = DataArray
    def __init__(self):
        pass
    @staticmethod
    def NDVI(DataArray):
        """
        calc NDVI (Normalized Difference vegetation Index)
        :param DataArray : (Red bands,NIR bands):
        :return          : NDVI array
        """
        DataArray = DataArray
        red = xarray.where(DataArray.red==-9999,numpy.nan,DataArray.red)
        nir = xarray.where(DataArray.nir==-9999,numpy.nan,DataArray.nir)
        ndvi1 = (nir-red)/(nir+red).to_numpy()
        ndvi3 = numpy.clip(ndvi1,-1,1)
        return ndvi3
    @staticmethod
    def EVI(DataArray):
        """
        calc EVI (Enhanced Vegetation Index)
        :param DataArray : (RED bands,BLUE bands,NIR bands):
        :return          : EVI array
        """
        red  = xarray.where(DataArray.red==-9999,numpy.nan,DataArray.red)
        blue = xarray.where(DataArray.blue==-9999,numpy.nan,DataArray.blue)
        nir  = xarray.where(DataArray.nir==-9999,numpy.nan,DataArray.nir)
        evi1 = (nir-red)/(nir+6*red-7.5*blue+1).to_numpy()
        evi3 = numpy.clip(evi1,-1,1)
        return evi3
    @staticmethod
    def NDMI(DataArray):
        """
        calc NDMI (Normalized Difference Moisture Index)
        :param DataArray : (SWIR-1 bands,NIR bands):
        :return          : NDMI array
        """
        if 'swir_1' in DataArray.data_vars:
            swir1 = DataArray.swir_1
        swir1 = DataArray.swir1
        swir  = xarray.where(swir1==-9999,numpy.nan,swir1)
        nir   = xarray.where(DataArray.nir==-9999,numpy.nan,DataArray.nir)
        ndmi1 = (nir-swir)/(nir+swir).to_numpy()
        ndmi3 = numpy.clip(ndmi1,-1,1)
        return ndmi3
    @staticmethod
    def BSI(DataArray):
        """
        calc BSI (Bare Soil Index)
        :param DataArray : (GREEN bands,NIR bands):
        :return          : BSI array
        """
        if 'swir_1' in DataArray.data_vars:
            swir1 = DataArray.swir_1
        swir1 = DataArray.swir1
        swir  = xarray.where(swir1==-9999,numpy.nan,swir1)
        red   = xarray.where(DataArray.red==-9999,numpy.nan,DataArray.red)
        blue   = xarray.where(DataArray.blue==-9999,numpy.nan,DataArray.blue)
        nir   = xarray.where(DataArray.nir==-9999,numpy.nan,DataArray.nir)
        bsi1 = ((red+swir) - (nir+blue)) / ((red+swir) + (nir+blue)).to_numpy()
        bsi3 = numpy.clip(bsi1,-1,1)
        return bsi3
    @staticmethod
    def NDWI(DataArray):
        """
        calc NDWI (Normalized Difference Water Index)
        :param DataArray : (SWIR bands,NIR bands):
        :return          : NDMI array
        """
        if 'swir_1' in DataArray.data_vars:
            swir1 = DataArray.swir_1
        swir1 = DataArray.swir1
        swir  = xarray.where(swir1==-9999,numpy.nan,swir1)
        nir   = xarray.where(DataArray.nir==-9999,numpy.nan,DataArray.nir)
        ndwi1 = (nir-swir)/(nir+swir).to_numpy()
        ndwi3 = numpy.clip(ndwi1,-1,1)
        return ndwi3
    @staticmethod
    def NMDI(DataArray):
        """
        calc NMDI (Normalized Multi-Band Drought Index)
        :param DataArray : (SWIR1 bands,SWIR2 bands,NIR bands):
        :return          : NMDI array
        """
        if 'swir_1' in DataArray.data_vars:
            swir1 = DataArray.swir_1
        swir1 = DataArray.swir1
        if 'swir_2' in DataArray.data_vars:
            swir2 = DataArray.swir_2
        swir2 = DataArray.swir1
        swir1 = xarray.where(swir1==-9999,numpy.nan,swir1)
        swir2 = xarray.where(swir2==-9999,numpy.nan,swir2)
        nir   = xarray.where(DataArray.nir==-9999,numpy.nan,DataArray.nir)
        nmdi1 = (nir-(swir1-swir2))/(nir-(swir1+swir2)).to_numpy()
        nmdi3 = numpy.clip(nmdi1,-1,1)
        return nmdi3
    @staticmethod
    def NDDI(DataArray):
        """
        calc NDDI (Normalized Difference Drought Index)
        :param DataArray : (RED bands,NIR bands,SWIR bands):
        :return          : NDDI array
        """
        if 'swir_1' in DataArray.data_vars:
            swir1 = DataArray.swir_1
        swir1 = DataArray.swir1
        red = xarray.where(DataArray.red==-9999,numpy.nan,DataArray.red)
        nir = xarray.where(DataArray.nir==-9999,numpy.nan,DataArray.nir)
        swir = xarray.where(swir1==-9999,numpy.nan,swir1)
        ndvi = (nir-red)/(nir+red)
        ndwi = (nir-swir)/(nir+swir)       
        nddi1 = (ndvi-ndwi)/(ndvi+ndwi).to_numpy() 
        nddi3 = numpy.clip(nddi1,-1,1)
        return nddi3
#############################################################################################################
    # # @staticmethod
    # def NDGI(DataArray):
    #     """
    #     Normalized Difference Glacier Index (NDGI) ???
    #     :param DataArray : (SWIR bands,NIR bands):
    #     :return          : NDMI array
    #     """
    #     blue   = xarray.where(DataArray.blue==-9999,numpy.nan,DataArray.blue)     #band2
    #     green  = xarray.where(DataArray.green==-9999,numpy.nan,DataArray.green)   #band3
    #     red    = xarray.where(DataArray.red==-9999,numpy.nan,DataArray.red)       #band4
    #     nir   = xarray.where(DataArray.nir==-9999,numpy.nan,DataArray.nir)        #band5
    #     if 'swir_1' in DataArray.data_vars:
    #         swir1 = DataArray.swir_1
    #     swir1 = DataArray.swir1                                                   #band6
    #     if 'swir_2' in DataArray.data_vars:
    #         swir2 = DataArray.swir_2
    #     swir2 = DataArray.swir2                                                   #band7
    #     fml = (green-swir1)/(green+swir1)
    #     val = fml.to_numpy()
    #     val = numpy.clip(val,-1,1)
    #     return val
    @staticmethod
    def NDWI(DataArray):
        """
        calc NDWI (Normalized Difference Water Index)
        :param DataArray : (SWIR bands,NIR bands):
        :return          : NDMI array
        """
        if 'swir_1' in DataArray.data_vars:
            swir1 = DataArray.swir_1
        swir1 = DataArray.swir1
        swir  = xarray.where(swir1==-9999,numpy.nan,swir1)
        nir   = xarray.where(DataArray.nir==-9999,numpy.nan,DataArray.nir)
        ndwi1 = (nir-swir)/(nir+swir).to_numpy()
        ndwi3 = numpy.clip(ndwi1,-1,1)
        return ndwi3
    @staticmethod
    def AVI(DataArray):
        """
        calc Advanced Vegetation Index (AVI)
        :param DataArray : (SWIR bands,NIR bands):
        :return          : NDMI array
        """
        red   = xarray.where(DataArray.red==-9999,numpy.nan,DataArray.red)
        nir   = xarray.where(DataArray.nir==-9999,numpy.nan,DataArray.nir)

        val = (nir*(1-red)*(nir-red))**1/3
        val = val.to_numpy()
        output = numpy.clip(val,-1,1)
        return output
    @staticmethod
    def SI(DataArray):
        """
        calc Shadow Index (SI) ???
        :param DataArray : (SWIR bands,NIR bands):
        :return          : NDMI array
        """
        blue   = xarray.where(DataArray.blue==-9999,numpy.nan,DataArray.blue)
        green  = xarray.where(DataArray.green==-9999,numpy.nan,DataArray.green)
        red    = xarray.where(DataArray.red==-9999,numpy.nan,DataArray.red)
        fml = ((1-blue)*(1-green)*(1-red))**(1/3)
        val = fml.to_numpy()
        val = numpy.clip(val,-1,1)
        return val
    @staticmethod
    def NDSI(DataArray):
        """
        Normalized Difference Snow Index (NDSI)
        :param DataArray : (SWIR bands,NIR bands):
        :return          : NDMI array
        """
        green  = xarray.where(DataArray.green==-9999,numpy.nan,DataArray.green)   #band3
        if 'swir_1' in DataArray.data_vars:
            swir1 = DataArray.swir_1
        swir1 = DataArray.swir1                                                   #band6
        fml = (green-swir1)/(green+swir1)
        val = fml.to_numpy()
        val = numpy.clip(val,-1,1)
        return val
    @staticmethod
    def NDGI(DataArray):
        """
        Normalized Difference Glacier Index (NDGI)
        :param DataArray : (SWIR bands,NIR bands):
        :return          : NDMI array
        """
        green  = xarray.where(DataArray.green==-9999,numpy.nan,DataArray.green)   #band3
        red    = xarray.where(DataArray.red==-9999,numpy.nan,DataArray.red)       #band4
        fml = (green-red)/(green+red)
        val = fml.to_numpy()
        val = numpy.clip(val,-1,1)
        return val
    @staticmethod
    def NBRI(DataArray):
        """
        Normalized Burned Ratio Index (NBRI)
        :param DataArray : (SWIR bands,NIR bands):
        :return          : NDMI array
        """
        nir   = xarray.where(DataArray.nir==-9999,numpy.nan,DataArray.nir)        #band5
        if 'swir_2' in DataArray.data_vars:
            swir2 = DataArray.swir_2
        swir2 = DataArray.swir2                                                   #band7
        fml = (nir-swir2)/(nir+swir2)
        val = fml.to_numpy()
        val = numpy.clip(val,-1,1)
        return val
    @staticmethod
    def NDGI(DataArray):
        """
        Normalized Pigment Chlorophyll Ratio Index (NPCRI)
        :param DataArray : (SWIR bands,NIR bands):
        :return          : NDMI array
        """
        blue   = xarray.where(DataArray.blue==-9999,numpy.nan,DataArray.blue)     #band2
        red    = xarray.where(DataArray.red==-9999,numpy.nan,DataArray.red)       #band4
        fml = (red-blue)/(red+blue)
        val = fml.to_numpy()
        val = numpy.clip(val,-1,1)
        return val