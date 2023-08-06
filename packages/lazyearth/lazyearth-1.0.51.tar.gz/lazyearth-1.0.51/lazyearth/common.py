import subprocess
import numpy
try:
    import matplotlib.pyplot as plt
except:
    print("install matplolib ...")
    subprocess.run('pip install matplolib',shell='true')
    import matplotlib.pyplot as plt
from matplotlib import colors
try:
    import xarray
except:
    print("install xarray ...")
    subprocess.run('pip install xarray',shell='true')
    import xarray
try:
    import sklearn
except:
    print("install sklean ...")
    subprocess.run('pip install -U scikit-learn',shell='true')
    import sklearn
    
try:
    from osgeo import gdal
except:
    #TODO set env conda env ไม่รู้จัก path
    raise ModuleNotFoundError('1.You have to install gdal first with this command "conda install -c conda-forge gdal" 2.pip install lazyearth again')

import lazyearth.virtual as vt
import lazyearth.plot as p

class objearth():
    def __init__(self):
        pass  
    @staticmethod
    def genimg(size=(2,2),datarange=(-1,1),nan=0,inf=0):
        """
        Generate 1D images with random values.
        :param size  : size of image
        :param range : Range of value
        :param nan   : Number of NaN
        :param inf   : Number of Inf
        :return      : 1D array image
        """
        data = numpy.random.uniform(datarange[0],datarange[1],[size[0],size[1]])
        index_nan = numpy.random.choice(data.size,nan,replace=1)
        data.ravel()[index_nan] = numpy.nan
        index_inf = numpy.random.choice(data.size,inf,replace=1)
        data.ravel()[index_inf] = numpy.inf
        return data
    
    @staticmethod
    def bandopen(target):
        """
        Open TIFF image
        :param target : path of image
        :return       : ndarray
        """
        return gdal.Open(target).ReadAsArray()

    @staticmethod
    def montage(img1,img2):
        """
        compare 2 image.
        :param img1 : first array
        :param img2 : second array
        """
        plt.figure(figsize=(15,15))
        plt.subplot(121),plt.imshow(img1, cmap = 'gray')
        plt.title('Image 1'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img2, cmap = 'viridis')
        plt.title('Image 2'), plt.xticks([]), plt.yticks([])
        plt.show()
        
    @staticmethod
    def falsecolor(Dataset1,Dataset2,Dataset3,bright=10):
        """
        combination 3 bands which any bands (Used with Xarray)
        :param Dataset1 : band 1
        :param Dataset1 : band 2
        :param Dataset3 : band 3
        :param bright   : brightness of image
        :return         : The stacked array 
        """
        BAND1    = xarray.where(Dataset1==-9999,numpy.nan,Dataset1)
        band1    = BAND1.to_numpy()/10000*bright
        BAND2    = xarray.where(Dataset2==-9999,numpy.nan,Dataset2)
        band2    = BAND2.to_numpy()/10000*bright
        BAND3    = xarray.where(Dataset3==-9999,numpy.nan,Dataset3)
        band3    = BAND3.to_numpy()/10000*bright
        product  = numpy.stack([band1,band2,band3],axis=2)
        return product

    @staticmethod
    def truecolor(Dataset,bright=10):
        """
        combination 3 bands which Red Green Blue bands (Used with Xarray)
        :param Dataset : Dataset of satellite bands
        :param bright  : brightness of image
        :return        : RGB array stacked 
        """
        RED    = xarray.where(Dataset.red==-9999,numpy.nan,Dataset.red)
        red    = RED.to_numpy()/10000*bright
        BLUE   = xarray.where(Dataset.blue==-9999,numpy.nan,Dataset.blue)
        blue   = BLUE.to_numpy()/10000*bright
        GREEN  = xarray.where(Dataset.green==-9999,numpy.nan,Dataset.green)
        green  = GREEN.to_numpy()/10000*bright
        rgb    = numpy.stack([red,green,blue],axis=2)
        return rgb
    
    # Fix bug
    # @staticmethod
    # def geo_save(array,filename,geo_transform = (0.0,1.0,0.0,0.0,0.0,1.0),projection='',dtype=gdal.GDT_Byte):
    #     """
    #     Save array to image
    #     :param array    : ndarray
    #     :param filename : filename
    #     :return         : TIFF image 
    #     """
    #     filename = Path(os.getcwd()).joinpath(filename+'.tif').as_posix()
    #     cols = array.shape[1]
    #     rows = array.shape[0]
    #     driver = gdal.GetDriverByName('GTiff')
    #     out_raster = driver.Create(filename,cols,rows,1,dtype,options=['COMPRESS=PACKBITS'])
    #     out_raster.SetGeoTransform(geo_transform)
    #     out_raster.SetProjection(projection)
    #     outband=out_raster.GetRasterBand(1)
    #     outband.SetNoDataValue(0)
    #     outband.WriteArray(array)
    #     outband.FlushCache()
    #     print('Saving image: '+filename)

    @staticmethod
    def gengaussian(size=(10,10)):
        """
        Create gaussian function array
        :param x_size : number
        :param y_size : number
        :return: gaussian ndarray
        """
        x, y = numpy.meshgrid(numpy.linspace(-1,1,size[0]), numpy.linspace(-1,1,size[1]))
        d = numpy.sqrt(x*x+y*y)
        sigma, mu = 0.5, 1.0
        g = numpy.exp(-( (d-mu)**2 / ( 2.0 * sigma**2 ) ) )
        return g
    @staticmethod
    def bandcombination(band1,band2,band3,bright=10):
        """
        combination 2 bands which Red,Green,Blue bands (Used with .tif file)
        :param band1 : band1
        :param band2 : band2
        :param band3 : band3
        :return      : numpy stacked array
        """
        b1  = band1/10000 *bright
        b2  = band2/10000 *bright
        b3  = band3/10000 *bright
        return numpy.stack([b1,b2,b3],axis=2)

    @staticmethod
    def plotshow(*args,**kwargs):
        # print(len(args))
        # 1 image mode
        if len(args)==1:
            DataArray = args[0]
            if 'figsize' in kwargs:
                    figsize = kwargs['figsize']
            else:
                figsize=(7,7)
            if 'title' in kwargs:
                title = kwargs['title']
            else:
                title = ""
            if 'xlabel' in kwargs:
                xlabel = kwargs['xlabel']
            else:
                xlabel = "x axis size"
            if 'ylabel' in kwargs:
                ylabel = kwargs['ylabel']
            else:
                ylabel = "y axis size"
            if 'ts' in kwargs:
                ts = kwargs['ts']
            else:
                ts = 0.07
            if 'cmap' in kwargs:
                cmap = kwargs['cmap']
            else:
                cmap = True

            # 01 xarray Data
            if type(DataArray) == xarray.core.dataarray.DataArray:
                # print("This is xarray")
                if 'area' in kwargs:
                    ymax = kwargs['area'][0]
                    ymin = kwargs['area'][1]
                    xmin = kwargs['area'][2]
                    xmax = kwargs['area'][3]
                else:
                    ymax = 0
                    ymin = args[0].shape[0]
                    xmin = 0
                    xmax = args[0].shape[1]
                lon  =  DataArray.longitude.to_numpy()[xmin:xmax]
                lon0 =  lon[0] ; lon1 =  lon[-1]
                lat  =  DataArray.latitude.to_numpy()[ymax:ymin]
                lat0 = -lat[-1] ; lat1 = -lat[0]
                def longitude(lon):
                    return [lon0,lon1]
                def latitude(lat):
                    return [lat0,lat1]
                def axis(x=0):
                    return x
                fig,ax = plt.subplots(constrained_layout=True)
                fig.set_size_inches(figsize)
                ax.set_title(title)
                ax.set_xlabel(xlabel)
                ax.set_ylabel(ylabel)
                ax.imshow(DataArray[ymax:ymin,xmin:xmax],extent=[xmin,xmax,ymin,ymax])
                secax_x = ax.secondary_xaxis('top',functions=(longitude,axis))
                secax_x.set_xlabel('longitude')
                secax_x = ax.secondary_xaxis('top',functions=(longitude,axis))
                secax_x.set_xlabel('longitude')
                secax_y = ax.secondary_yaxis('right',functions=(latitude,axis))
                secax_y.set_ylabel('latitute')
                plt.grid(color='w', linestyle='-', linewidth=ts)
                plt.show()
            # 02 Numpy Data
            elif type(DataArray) == numpy.ndarray:
                if 'area' in kwargs:
                    ymax = kwargs['area'][0]
                    ymin = kwargs['area'][1]
                    xmin = kwargs['area'][2]
                    xmax = kwargs['area'][3]
                else:
                    ymax = 0
                    ymin = args[0].shape[0]
                    xmin = 0
                    xmax = args[0].shape[1]
                # print("This is numpy")
                real_margin_img = DataArray[ymax:ymin,xmin:xmax]

                #plotshow
                plt.figure(figsize=(figsize))
                plt.subplots(constrained_layout=True)
                color_map = plt.imshow(real_margin_img,extent=[xmin,xmax,ymin,ymax])

                plt.title(title)
                plt.xlabel(xlabel)
                plt.ylabel(ylabel)
                plt.grid(color='w', linestyle='-', linewidth=ts)
                # faction
                im_ratio = real_margin_img.shape[1]/real_margin_img.shape[0]
                if im_ratio<1:
                    fac = 0.0485
                elif im_ratio==1:
                    fac = 0.045
                else:
                    fac = 0.0456*(im_ratio**(-1.0113))
                # print(real_margin_img.shape[1],real_margin_img.shape[0],im_ratio,fac)

                #colorbar
                min = real_margin_img.min()
                max = real_margin_img.max()
                plt.clim(min,max)
                if cmap==True:
                    color_map.set_cmap('viridis')
                else:
                    color_map.set_cmap(cmap)
                plt.colorbar(orientation="vertical",fraction=fac)
                plt.show()
            # 03 waterquality
            # print(len(args[0]))
            elif type(args[0]) == dict and len(args[0]) == 3:
                if 'area' in kwargs:
                    ymax = kwargs['area'][0]
                    ymin = kwargs['area'][1]
                    xmin = kwargs['area'][2]
                    xmax = kwargs['area'][3]
                else:
                    ymax = 0
                    ymin = args[0]['DataArray'].shape[0]
                    xmin = 0
                    xmax = args[0]['DataArray'].shape[1]
                DataArray = args[0]['DataArray']
                min_value = args[0]['Datavalue'][0]
                max_value = args[0]['Datavalue'][1]
                colormap  = args[0]['Datacolor']
                # colormap='jet'
                real_margin_img = DataArray[ymax:ymin,xmin:xmax]
                #plotshow
                plt.figure(figsize=(figsize))
                plt.subplots(constrained_layout=True)
                color_map = plt.imshow(real_margin_img,extent=[xmin,xmax,ymin,ymax])
                # faction
                im_ratio = real_margin_img.shape[1]/real_margin_img.shape[0]
                if im_ratio<1:
                    fac = 0.0485
                elif im_ratio==1:
                    fac = 0.045
                else:
                    fac = 0.0456*(im_ratio**(-1.0113))
                    # print(real_margin_img.shape[1],real_margin_img.shape[0],im_ratio,fac)
                #colorbar
                plt.clim(min_value,max_value)
                # color_map.set_cmap('viridis')
                if colormap != None:
                        cmap = plt.get_cmap(colormap)
                else:
                        cmap = vt.bluesea()
                color_map.set_cmap(cmap)
                plt.colorbar(orientation="vertical",fraction=fac,label='Pollution\nmg/l')
                # plt.set_label('x')
                plt.show()

            # Error
            else:
                raise ValueError("Nonetype :",type(DataArray))
        # more that 1 image mode 
        else:
            #clean waterquality type
            Ags = []
            for i in range(len(args)):
                if type(args[i])==dict:
                    Ags.append(args[i]['DataArray'])
                else:
                    Ags.append(args[i])
            args = Ags
            if 'area' in kwargs:
                ymax = kwargs['area'][0]
                ymin = kwargs['area'][1]
                xmin = kwargs['area'][2]
                xmax = kwargs['area'][3]
            else:
                ymax = 0
                ymin = args[0].shape[0]
                xmin = 0
                xmax = args[0].shape[1]
            Dl = len(args)
            img = args
            if Dl==2:
                p.plot02(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                )
            elif Dl==3:
                p.plot03(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                ,img[2][ymax:ymin,xmin:xmax]
                )
            elif Dl==4:
                p.plot04(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                ,img[2][ymax:ymin,xmin:xmax]
                ,img[3][ymax:ymin,xmin:xmax]
                )
            elif Dl==5:
                p.plot05(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                ,img[2][ymax:ymin,xmin:xmax]
                ,img[3][ymax:ymin,xmin:xmax]
                ,img[4][ymax:ymin,xmin:xmax]
                )
            elif Dl==6:
                p.plot06(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                ,img[2][ymax:ymin,xmin:xmax]
                ,img[3][ymax:ymin,xmin:xmax]
                ,img[4][ymax:ymin,xmin:xmax]
                ,img[5][ymax:ymin,xmin:xmax]
                )
            elif Dl==7:
                p.plot07(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                ,img[2][ymax:ymin,xmin:xmax]
                ,img[3][ymax:ymin,xmin:xmax]
                ,img[4][ymax:ymin,xmin:xmax]
                ,img[5][ymax:ymin,xmin:xmax]
                ,img[6][ymax:ymin,xmin:xmax]
                )
            elif Dl==8:
                p.plot08(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                ,img[2][ymax:ymin,xmin:xmax]
                ,img[3][ymax:ymin,xmin:xmax]
                ,img[4][ymax:ymin,xmin:xmax]
                ,img[5][ymax:ymin,xmin:xmax]
                ,img[6][ymax:ymin,xmin:xmax]
                ,img[7][ymax:ymin,xmin:xmax]
                )
            elif Dl==9:
                p.plot09(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                ,img[2][ymax:ymin,xmin:xmax]
                ,img[3][ymax:ymin,xmin:xmax]
                ,img[4][ymax:ymin,xmin:xmax]
                ,img[5][ymax:ymin,xmin:xmax]
                ,img[6][ymax:ymin,xmin:xmax]
                ,img[7][ymax:ymin,xmin:xmax]
                ,img[8][ymax:ymin,xmin:xmax]
                )
            else:
                print('error')

    @staticmethod
    def stamp(project=''):
        import datetime,platform
        print(datetime.datetime.now().strftime('"""\n%c'))
        print('name :',project)
        print('OS system : ',platform.system())
        print('@author : Tun.k\n"""')
    # stamp()
