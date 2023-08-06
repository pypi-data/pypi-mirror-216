# import matplotlib.pyplot as plt
import numpy
import xarray
from matplotlib import colors
import os
from keras import Sequential
from keras.layers import Convolution2D

# def _inter_from_256(x):
#     return np.interp(x=x,xp=[0,255],fp=[0,1])
# def __rgb_to_colormapcode(r,g,b):
#     return (_inter_from_256(r),_inter_from_256(g),_inter_from_256(b))
def bluesea():
    """
    Bluesea colormap used for waterqualtiy.
    :return : colormap.
    """
    RGB6 = (0.1       , 0.1       , 0.1       )     #RGB(252,252,252)
    RGB5 = (0.        , 0.31372549, 0.45098039)     #RGB(114,199,236)
    RGB4 = (0.0627451 , 0.49019608, 0.6745098 )     #RGB(30,186,214)
    RGB3 = (0.09411765, 0.60392157, 0.82745098)     #RGB(23,153,210)
    RGB2 = (0.11764706, 0.73333333, 0.84313725)     #RGB(16,125,171)
    RGB1 = (0.44313725, 0.78039216, 0.9254902 )     #RGB(0,79,113)
    # RGB0 = (0.99      , 0.99      , 0.99      )     #RGB(25,25,25)
    RGB0 = (1.00      , 1.00      , 1.00      )     #RGB(0,0,0)
    cdict = {
        'red':  ((1  / 6 * 0, RGB0[0]  ,RGB0[0]),
                (1  / 6 * 1, RGB1[0]  ,RGB1[0]),
                (1  / 6 * 2, RGB2[0]  ,RGB2[0]),
                (1  / 6 * 3, RGB3[0]  ,RGB3[0]),
                (1  / 6 * 4, RGB4[0]  ,RGB4[0]),
                (1  / 6 * 5, RGB5[0]  ,RGB5[0]),
                (1  / 6 * 6, RGB6[0]  ,RGB6[0])
                ),
        'green':((1  / 6 * 0, RGB0[1]    , RGB0[1]),
                (1  / 6 * 1, RGB1[1]    , RGB1[1]),
                (1  / 6 * 2, RGB2[1]    , RGB2[1]),
                (1  / 6 * 3, RGB3[1]    , RGB3[1]),
                (1  / 6 * 4, RGB4[1]    , RGB4[1]),
                (1  / 6 * 5, RGB5[1]    , RGB5[1]),
                (1  / 6 * 6, RGB6[1]    , RGB6[1])
                ),
        'blue': ((1  / 6 * 0, RGB0[2]    , RGB0[2]),
                (1  / 6 * 1, RGB1[2]    , RGB1[2]),
                (1  / 6 * 2, RGB2[2]    , RGB2[2]),
                (1  / 6 * 3, RGB3[2]    , RGB3[2]),
                (1  / 6 * 4, RGB4[2]    , RGB4[2]),
                (1  / 6 * 5, RGB5[2]    , RGB5[2]),
                (1  / 6 * 6, RGB6[2]    , RGB6[2])
                ),
    }
    nc = colors.LinearSegmentedColormap('bluesea',segmentdata=cdict)
    return nc    

@staticmethod
def leafwood():
    """
    Leafwood colormap used for NDVI.
    :return : colormap.
    """
    #https://mycolor.space/gradient?ori=to+right+top&hex=%2385A938&hex2=%233C770E&sub=1
    #https://imagecolorpicker.com/en
    RGB1   = (0.30588235, 0.05490196, 0.05490196)   #RGB(78,14,14)          
    RGB2   = (0.39215686, 0.09803922, 0.07843137)   #RGB(100,25,20)
    RGB3   = (0.43921569, 0.18431373, 0.00392157)   #RGB(112,47,1)
    RGB4   = (0.50980392, 0.23529412, 0.05098039)   #RGB(130,60,13)
    RGB5   = (0.54901961, 0.2745098 , 0.05882353)   #RGB(140,70,15)
    RGB6   = (0.61960784, 0.30588235, 0.02745098)   #RGB(158,78,7)
    RGB7   = (0.70980392, 0.40784314, 0.0627451 )   #RGB(181,104,16) 
    RGB8   = (0.79607843, 0.49019608, 0.16470588)   #RGB(203, 125, 42)
    RGB9   = (0.85490196, 0.58823529, 0.04705882)   #RGB(218,150,12)
    RGB10  = (0.85882353, 0.63529412, 0.05490196)   #RGB(219,162,14)
    RGB11  = (0.88235294, 0.7254902 , 0.01568627)   #RGB(225,185,4)
    RGB12  = (0.87058824, 0.8       , 0.05098039)   #RGB(222,204,13)
    RGB13  = (0.89019608, 0.8745098 , 0.07058824)   #RGB(227,223,18)
    RGB14  = (0.92156863, 0.91764706, 0.09019608)   #RGB(235,234,23)
    RGB15  = (0.81176471, 0.85882353, 0.2745098 )   #RGB(207,219,70)
    RGB16  = (0.68627451, 0.77647059, 0.26666667)   #RGB(175,198,68)
    RGB17  = (0.56078431, 0.69803922, 0.25882353)   #RGB(143,178,66)
    RGB18  = (0.52156863, 0.6627451 , 0.21960784)   #RGB(133,169,56)
    RGB19  = (0.38039216, 0.56470588, 0.14117647)   #RGB(97, 144, 36)
    RGB20  = (0.23529412, 0.46666667, 0.05490196)   #RGB(60,119,14)
    RGB21  = (0.16078431, 0.36862745, 0.04313725)   #RGB(41,94,11)
    cdict = {
        'red':  ((1  / 20 * 0,  (RGB1[0])  ,(RGB1[0])),
                (1  / 20 * 1,  (RGB2[0])  ,(RGB2[0])),
                (1  / 20 * 2,  (RGB3[0])  ,(RGB3[0])),
                (1  / 20 * 3,  (RGB4[0])  ,(RGB4[0])),
                (1  / 20 * 4,  (RGB5[0])  ,(RGB5[0])),
                (1  / 20 * 5,  (RGB6[0])  ,(RGB6[0])),
                (1  / 20 * 6,  (RGB7[0])  ,(RGB7[0])),
                (1  / 20 * 7,  (RGB8[0])  ,(RGB8[0])),
                (1  / 20 * 8,  (RGB9[0])  ,(RGB9[0])),
                (1  / 20 * 9,  (RGB10[0])  ,(RGB10[0])),
                (1  / 20 * 10, (RGB11[0])  ,(RGB11[0])),
                (1  / 20 * 11, (RGB12[0])  ,(RGB12[0])),
                (1  / 20 * 12, (RGB13[0])  ,(RGB13[0])),
                (1  / 20 * 13, (RGB14[0])  ,(RGB14[0])),
                (1  / 20 * 14, (RGB15[0])  ,(RGB15[0])),
                (1  / 20 * 15, (RGB16[0])  ,(RGB16[0])),
                (1  / 20 * 16, (RGB17[0])  ,(RGB17[0])),
                (1  / 20 * 17, (RGB18[0])  ,(RGB18[0])),
                (1  / 20 * 18, (RGB19[0])  ,(RGB19[0])),
                (1  / 20 * 19, (RGB20[0])  ,(RGB20[0])),
                (1  / 20 * 20, (RGB21[0])  ,(RGB21[0]))),
        'green':((1  / 20 * 0,  (RGB1[1])  ,(RGB1[1])),
                (1  / 20 * 1,  (RGB2[1])  ,(RGB2[1])),
                (1  / 20 * 2,  (RGB3[1])  ,(RGB3[1])),
                (1  / 20 * 3,  (RGB4[1])  ,(RGB4[1])),
                (1  / 20 * 4,  (RGB5[1])  ,(RGB5[1])),
                (1  / 20 * 5,  (RGB6[1])  ,(RGB6[1])),
                (1  / 20 * 6,  (RGB7[1])  ,(RGB7[1])),
                (1  / 20 * 7,  (RGB8[1])  ,(RGB8[1])),
                (1  / 20 * 8,  (RGB9[1])  ,(RGB9[1])),
                (1  / 20 * 9,  (RGB10[1])  ,(RGB10[1])),
                (1  / 20 * 10, (RGB11[1])  ,(RGB11[1])),
                (1  / 20 * 11, (RGB12[1])  ,(RGB12[1])),
                (1  / 20 * 12, (RGB13[1])  ,(RGB13[1])),
                (1  / 20 * 13, (RGB14[1])  ,(RGB14[1])),
                (1  / 20 * 14, (RGB15[1])  ,(RGB15[1])),
                (1  / 20 * 15, (RGB16[1])  ,(RGB16[1])),
                (1  / 20 * 16, (RGB17[1])  ,(RGB17[1])),
                (1  / 20 * 17, (RGB18[1])  ,(RGB18[1])),
                (1  / 20 * 18, (RGB19[1])  ,(RGB19[1])),
                (1  / 20 * 19, (RGB20[1])  ,(RGB20[1])),
                (1  / 20 * 20, (RGB21[1])  ,(RGB21[1]))),
        'blue': ((1  / 20 * 0,  (RGB1[2])  ,(RGB1[2])),
                (1  / 20 * 1,  (RGB2[2])  ,(RGB2[2])),
                (1  / 20 * 2,  (RGB3[2])  ,(RGB3[2])),
                (1  / 20 * 3,  (RGB4[2])  ,(RGB4[2])),
                (1  / 20 * 4,  (RGB5[2])  ,(RGB5[2])),
                (1  / 20 * 5,  (RGB6[2])  ,(RGB6[2])),
                (1  / 20 * 6,  (RGB7[2])  ,(RGB7[2])),
                (1  / 20 * 7,  (RGB8[2])  ,(RGB8[2])),
                (1  / 20 * 8,  (RGB9[2])  ,(RGB9[2])),
                (1  / 20 * 9,  (RGB10[2])  ,(RGB10[2])),
                (1  / 20 * 10, (RGB11[2])  ,(RGB11[2])),
                (1  / 20 * 11, (RGB12[2])  ,(RGB12[2])),
                (1  / 20 * 12, (RGB13[2])  ,(RGB13[2])),
                (1  / 20 * 13, (RGB14[2])  ,(RGB14[2])),
                (1  / 20 * 14, (RGB15[2])  ,(RGB15[2])),
                (1  / 20 * 15, (RGB16[2])  ,(RGB16[2])),
                (1  / 20 * 16, (RGB17[2])  ,(RGB17[2])),
                (1  / 20 * 17, (RGB18[2])  ,(RGB18[2])),
                (1  / 20 * 18, (RGB19[2])  ,(RGB19[2])),
                (1  / 20 * 19, (RGB20[2])  ,(RGB20[2])),
                (1  / 20 * 20, (RGB21[2])  ,(RGB21[2])),
        )
    }
    nc4 = colors.LinearSegmentedColormap('leafwood',segmentdata=cdict)
    return nc4

@staticmethod
def sweetrose():
    """
    Sweetrose colormap used for NDVI.
    :return : colormap.
    """
    RGB1  = (1.        , 1.        , 1.        )    # rgba(254,254,254,255)
    RGB2  = (0.98823529, 0.88627451, 0.98823529)    # rgba(254,225,253,255)
    RGB3  = (0.98823529, 0.79215686, 0.99607843)    # rgba(252,202,254,255)
    RGB4  = (0.98823529, 0.79215686, 0.99607843)    # rgba(248,129,255,255)
    RGB5  = (0.96470588, 0.02352941, 1.        )    # rgba(235,14,243,255)
    RGB6  = (0.96470588, 0.01960784, 0.40784314)    # rgba(244,6,102,255)
    RGB8  = (0.96078431, 0.01960784, 0.        )    # rgba(251,2,0,255)
    RGB7  = (0.98431373, 0.35294118, 0.03529412)    # rgba(244,90,0,255)
    RGB9  = (0.98039216, 0.6745098 , 0.00392157)    # rgba(250,169,6,255)
    RGB10 = (0.96862745, 0.8       , 0.01176471)    # rgba(242,204,16,255)
    RGB11 = (0.99607843, 0.99215686, 0.01568627)    # rgba(255,253,8,255)
    RGB12 = (0.02745098, 0.58431373, 0.18039216)    # rgba(3,150,51,255)
    RGB13 = (0.02352941, 0.6627451 , 0.03137255)    # rgba(7,170,2,255)
    RGB14 = (0.04705882, 0.98039216, 0.02352941)    # rgba(12,250,4,255)
    RGB15 = (0.03921569, 0.97647059, 0.50980392)    # rgba(8,250,130,255)

    cdict = {
        'red':  ((1  / 14 * 0,  (RGB1[0])  ,(RGB1[0])),
                (1  / 14 * 1,  (RGB2[0])  ,(RGB2[0])),
                (1  / 14 * 2,  (RGB3[0])  ,(RGB3[0])),
                (1  / 14 * 3,  (RGB4[0])  ,(RGB4[0])),
                (1  / 14 * 4,  (RGB5[0])  ,(RGB5[0])),
                (1  / 14 * 5,  (RGB6[0])  ,(RGB6[0])),
                (1  / 14 * 6,  (RGB7[0])  ,(RGB7[0])),
                (1  / 14 * 7,  (RGB8[0])  ,(RGB8[0])),
                (1  / 14 * 8,  (RGB9[0])  ,(RGB9[0])),
                (1  / 14 * 9,  (RGB10[0])  ,(RGB10[0])),
                (1  / 14 * 10, (RGB11[0])  ,(RGB11[0])),
                (1  / 14 * 11, (RGB12[0])  ,(RGB12[0])),
                (1  / 14 * 12, (RGB13[0])  ,(RGB13[0])),
                (1  / 14 * 13, (RGB14[0])  ,(RGB14[0])),
                (1  / 14 * 14, (RGB15[0])  ,(RGB15[0]))),
        'green':((1  / 14 * 0,  (RGB1[1])  ,(RGB1[1])),
                (1  / 14 * 1,  (RGB2[1])  ,(RGB2[1])),
                (1  / 14 * 2,  (RGB3[1])  ,(RGB3[1])),
                (1  / 14 * 3,  (RGB4[1])  ,(RGB4[1])),
                (1  / 14 * 4,  (RGB5[1])  ,(RGB5[1])),
                (1  / 14 * 5,  (RGB6[1])  ,(RGB6[1])),
                (1  / 14 * 6,  (RGB7[1])  ,(RGB7[1])),
                (1  / 14 * 7,  (RGB8[1])  ,(RGB8[1])),
                (1  / 14 * 8,  (RGB9[1])  ,(RGB9[1])),
                (1  / 14 * 9,  (RGB10[1])  ,(RGB10[1])),
                (1  / 14 * 10, (RGB11[1])  ,(RGB11[1])),
                (1  / 14 * 11, (RGB12[1])  ,(RGB12[1])),
                (1  / 14 * 12, (RGB13[1])  ,(RGB13[1])),
                (1  / 14 * 13, (RGB14[1])  ,(RGB14[1])),
                (1  / 14 * 14, (RGB15[1])  ,(RGB15[1]))),
        'blue': ((1  / 14 * 0,  (RGB1[2])  ,(RGB1[2])),
                (1  / 14 * 1,  (RGB2[2])  ,(RGB2[2])),
                (1  / 14 * 2,  (RGB3[2])  ,(RGB3[2])),
                (1  / 14 * 3,  (RGB4[2])  ,(RGB4[2])),
                (1  / 14 * 4,  (RGB5[2])  ,(RGB5[2])),
                (1  / 14 * 5,  (RGB6[2])  ,(RGB6[2])),
                (1  / 14 * 6,  (RGB7[2])  ,(RGB7[2])),
                (1  / 14 * 7,  (RGB8[2])  ,(RGB8[2])),
                (1  / 14 * 8,  (RGB9[2])  ,(RGB9[2])),
                (1  / 14 * 9,  (RGB10[2])  ,(RGB10[2])),
                (1  / 14 * 10, (RGB11[2])  ,(RGB11[2])),
                (1  / 14 * 11, (RGB12[2])  ,(RGB12[2])),
                (1  / 14 * 12, (RGB13[2])  ,(RGB13[2])),
                (1  / 14 * 13, (RGB14[2])  ,(RGB14[2])),
                (1  / 14 * 14, (RGB15[2])  ,(RGB15[2])),
        )
    }
    nc5 = colors.LinearSegmentedColormap('new_cmap',segmentdata=cdict)
    return nc5

def load_data(rgb):
        x = []
        x.append(rgb)
        return numpy.array(x)
def get_model(Xaxis,Yaxis):
        h5_dir = os.path.join(os.path.dirname(__file__), 'models')
        weights_path = os.path.join(h5_dir,'weights.h5')
        model = Sequential()
        model.add(
            Convolution2D(
                32, 9, activation="relu", input_shape=(Xaxis, Yaxis, 3), padding="same"
            )
        )
        model.add(Convolution2D(16, 5, activation="relu", padding="same"))
        model.add(Convolution2D(3, 5, activation="relu", padding="same"))
        if weights_path:
            model.load_weights(weights_path)
        model.compile(optimizer="adam", loss="mse", metrics=["accuracy"])
        return model
def superresolution(rgb):
    """
    superressolution of rgb image
    :param rgb : numpy rgb image 
    :return    : shapen image
    """
    # model_weights_path = r"C:\Users\tul\Desktop\models\weights.h5"
    Xa,Ya,_ = rgb.shape
    model = get_model(Xa,Ya)                #Prepare model
    x = load_data(rgb)
    out_array = model.predict(x)
    for index in range(out_array.shape[0]):
        num, rows, cols, channels = out_array.shape
        for i in range(rows):
            for j in range(cols):
                for k in range(channels):
                    if out_array[index][i][j][k] > 1.0:
                        out_array[index][i][j][k] = 1.0
        # out_img = Image.fromarray(np.uint8(out_array[0] * 255))
        out_img = numpy.uint8(out_array[0] * 255)
    return out_img