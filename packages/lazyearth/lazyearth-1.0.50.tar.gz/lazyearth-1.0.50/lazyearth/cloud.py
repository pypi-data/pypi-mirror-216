# def clearcloud(self,Dataset0,Dataset1):
#     '''
#     Clear the clouds
#     :param Dataset0 : The image that want to clear cloud.
#     :param Dataset1 : The better image that used to maske the first image better.
#     :return         : better cloud image
#     '''
#     self.Dataset0 = Dataset0
#     self.Dataset1 = Dataset1
#     pixel0 = self.Dataset0.pixel_qa
#     mask1 = xarray.where(pixel0==352,1,0)    
#     mask2 = xarray.where(pixel0==480,1,0)
#     mask3 = xarray.where(pixel0==944,1,0)
#     sum = mask1+mask2+mask3
#     mask0 = xarray.where(sum.data>0,1,0)
#     blue        = xarray.where(mask0,self.Dataset1.blue,self.Dataset0.blue)
#     green       = xarray.where(mask0,self.Dataset1.green,self.Dataset0.green)
#     red         = xarray.where(mask0,self.Dataset1.red,self.Dataset0.red)
#     nir         = xarray.where(mask0,self.Dataset1.nir,self.Dataset0.nir)
#     pixel_qa    = xarray.where(mask0,self.Dataset1.pixel_qa,self.Dataset0.pixel_qa)
#     # Create DataArray
#     return xarray.merge([blue,green,red,nir,pixel_qa])


# def percentcloud(self,Dataset):
#     '''
#     :param Dataset : Xarray dataset pixel_qa bands
#     :return        : percent of the cloud in the image
#     '''
#     self.Dataset = Dataset
#     FashCloud = [352,480,944]
#     dstest    = self.Dataset.pixel_qa
#     dsnew     = xarray.where(dstest == FashCloud[0],numpy.nan,dstest)
#     dsnew     = xarray.where(dsnew  == FashCloud[1],numpy.nan,dsnew)
#     dsnew     = xarray.where(dsnew  == FashCloud[2],numpy.nan,dsnew)
#     Cpixel    = (numpy.isnan(dsnew.to_numpy())).sum()
#     Allpixel  = int(self.Dataset.pixel_qa.count())
#     Cloudpercent = (Cpixel/Allpixel)*100
#     print("Percent Cloud : %.4f"%Cloudpercent,"%")
