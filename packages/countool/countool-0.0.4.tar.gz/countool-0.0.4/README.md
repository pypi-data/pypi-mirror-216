
"""
This is a demo for cvisp, 开发板、相机等拍摄设备取到的RAW with metadata，可以直接用该工具包进行demosaic，得到RGB图像，以便于展示。
    - pip install cvisp
    - from cvisp.utils import Demosaic_RAW
    
"""

"""
三种模式，分别为：预览raw图，推理GDIP，预览demosaic（自用）
    run_demosaic(): return the demosaiced image, (HWC, u16, bmp)
    run_isp_with_meta(): return the rgb image , (HWC, u8, bmp)
    run_model(weight_path = './your.pt', model = GDIP(), device = 'cuda:0'): return the output of       your          model, (HWC, u8, bmp) 
    
    完整传参说明：
    - Demosaic_RAW(mode : str = None, input_data_path : str = None, show_meta_data : bool = True, 
    show_image : bool = False, save_image : bool = True, result_output_dir : str = None):
        mode: defatult = 'simple_dm', choices = ['simple_dm', 'opencv_dm']
        input_data_path: raw图片路径，支持单张图片，如：'./test.dng'
        show_meta_data: show the meta data of the input data, default = True，你可以选择是否展示meta data
        show_image: show the output image, default = False，你可以选择是否展示输出图像
        save_image: save the output image, default = True，你可以选择是否保存输出图像，保存路径为result_output_dir
        result_output_dir: the output dir of the result image, default = './demosaic/'，你可以选择保存路径
"""

if __name__ == '__main__':
    for im in glob.glob(image_path_list + '*.dng'):
        demosaicd_raw = Demosaic_RAW(input_data_path = im).run_model(weight_path = './your.pt', model = GDIP(), device = 'cuda:0')
        # rgb = Demosaic_RAW(input_data_path = im).run_isp_with_meta()
        # gdip_out = Demosaic_RAW(input_data_path = im).run_model(weight_path = './your.pt', model = GDIP(), device = 'cuda:0')
