
import os
import numpy as np
import rawpy
import cv2
import torch
from tqdm import tqdm
import torch.nn as nn
# from colour_demosaicing import demosaicing_CFA_Bayer_bilinear, demosaicing_CFA_Bayer_Malvar2004, demosaicing_CFA_Bayer_Menon2007

class Demosaic_RAW():
    def __init__(self, mode : str = None, input_data_path : str = None, show_meta_data : bool = True, show_image : bool = False, save_image : bool = True, result_output_dir : str = None):
        super(Demosaic_RAW, self).__init__()
        assert os.path.exists(input_data_path), 'input_data_path is not exist, please check the path.'
        self.mode = 'simple_dm' if mode is None else mode
        result_output_dir = os.getcwd() if result_output_dir is None else result_output_dir
        self.result_output_dir = os.path.join(result_output_dir, self.mode)
        self.mkfolder(self.result_output_dir)
        self.input_data_path = input_data_path
        self.mkfolder(self.result_output_dir)
        self.meta_data, self.raw_data = self.get_metadata(self.input_data_path)
        self.white_level, self.black_level, self.h, self.w = self.meta_data['white_level'], self.meta_data['black_level'], self.meta_data['height'], self.meta_data['width']
        self.white_balance_gain, self.ccm = self.meta_data['white_balance_gain'], self.meta_data['ccm']
        self.gamma = self.meta_data['gamma'] if 'gamma' in self.meta_data.keys() else 2.2
        self.bayer_pattern = self.get_bayer_pattern(self.meta_data['bayer_pattern_matrix'])
        self.target_bayer_pattern = 'RGGB'
        self.show_image = show_image
        self.save_image = save_image
        assert self.mode in ['simple_dm', 'bilinear_dm', 'mal04_dm', 'men07_dm', 'opencv_dm'], 'mode is not exist, please check the mode.'
        print('--{} white_level : {}, black_level : {}, height : {}, width : {}, bit : {}, bayer_pattern: {}'.format(os.path.basename(self.input_data_path),
                                                                                                           self.white_level, self.black_level, self.h, self.w, int(np.log2(self.white_level + 1)), self.bayer_pattern)) if show_meta_data else None
    def mkfolder(self, path : str):
        if not os.path.exists(path):
            os.makedirs(path)
            print({path}, 'is created for saving the results.')

    def check_raw_image(self, image_path:str):
        for id in tqdm(os.listdir(image_path)):
            if not id.endswith('.dng'):
                continue
            image = rawpy.imread(os.path.join(image_path, id)).raw_image_visible
            assert image is not  None, 'image is not exist, please check the image path.'

    def inv_normalization(self, input_data : np.ndarray, black_level : int, white_level : int)->np.ndarray:
        output_data = np.clip(input_data, 0, 1) * (white_level - black_level) + black_level
        output_data = output_data.astype(np.uint16)
        return output_data

    def normalization(self, input_data : np.ndarray, black_level : int, white_level : int)->np.ndarray:
        output_data = np.maximum(input_data.astype(float) - black_level, 0) / (white_level - black_level)
        return output_data
    
    def pack_img(self, input_data : np.ndarray)->np.ndarray:
        h, w = input_data.shape[:2]
        output_data = np.zeros((h//2, w//2, 4), dtype=np.float32)
        output_data[:, :, 0] = input_data[0:h:2, 0:w:2]
        output_data[:, :, 1] = input_data[0:h:2, 1:w:2]
        output_data[:, :, 2] = input_data[1:h:2, 0:w:2]
        output_data[:, :, 3] = input_data[1:h:2, 1:w:2]
        return output_data

    def gamma_correction(self, input_data : np.ndarray, gamma : float)->np.ndarray:
        output_data = np.power(np.clip(input_data, 1e-8, 1), 1 / gamma).clip(0, 1)
        return output_data

    def apply_ccm(self, input_data : np.ndarray, ccm : np.ndarray)->np.ndarray:
        output_data = np.clip(np.matmul(input_data, ccm.T), 0, 1)
        return output_data


    def apply_wb(self, input_data : np.ndarray, wb : np.ndarray)->np.ndarray:
        output_data = (input_data * wb).clip(0, 1)
        return output_data

    def apply_lut(self, input_data : np.ndarray, lut : np.ndarray)->np.ndarray:
        output_data = lut[input_data]
        return output_data

    def apply_usm(self, input_data : np.ndarray, strength : float, radius : int)->np.ndarray:
        output_data = cv2.GaussianBlur(input_data, (radius, radius), 0)
        output_data = input_data + strength * (input_data - output_data)
        return output_data

    def f32_to_u8(self, input_data : np.ndarray)->np.ndarray:
        assert input_data.min() >= 0 and input_data.max() <= 1, 'input_data is not in range [0, 1], please check the input_data.'
        output_data = np.clip(input_data * 255, 0, 255).astype(np.uint8)
        return output_data

    def show_demo_image(self, img : np.ndarray):
        cv2.imshow('demo_img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_demo_image(self, save_path : str, img : np.ndarray):
        assert isinstance(save_path, str), 'save_path is not string, please check the save_path.'
        assert isinstance(img, np.ndarray), 'img is not numpy.ndarray, please check the img.'
        assert img.shape[0] > 0 and img.shape[1] > 0, 'img is empty, please check the img.'
        cv2.imwrite(save_path, img)
        print('save the result to {}'.format(save_path))

    def get_bayer_pattern(self, bayer_pattern_matrix : str)->str:
        bayer_desc = 'RGBG'
        input_bayer_pattern = ''
        if bayer_pattern_matrix is not None:
            for i in range(2):
                for k in range(2):
                    input_bayer_pattern += (bayer_desc[bayer_pattern_matrix[i][k]])
        else:
            input_bayer_pattern = 'RGGB'
        return input_bayer_pattern

    def bayer_unify(self, raw: np.ndarray, input_pattern: str, target_pattern: str, mode: str) -> np.ndarray:
        BAYER_PATTERNS = ["RGGB", "BGGR", "GRBG", "GBRG", "BGRG", "RGBG", "GRGB", "GBGR"]
        if input_pattern not in BAYER_PATTERNS:
            raise ValueError('Unknown input bayer pattern!')
        if target_pattern not in BAYER_PATTERNS:
            raise ValueError('Unknown target bayer pattern!')
        if not isinstance(raw, np.ndarray) or len(raw.shape) != 2:
            raise ValueError('raw should be a 2-dimensional numpy.ndarray!')
        if input_pattern == target_pattern:
            h_offset, w_offset = 0, 0
        elif input_pattern[0] == target_pattern[2] and input_pattern[1] == target_pattern[3]:
            h_offset, w_offset = 1, 0
        elif input_pattern[0] == target_pattern[1] and input_pattern[2] == target_pattern[3]:
            h_offset, w_offset = 0, 1
        elif input_pattern[0] == target_pattern[3] and input_pattern[1] == target_pattern[2]:
            h_offset, w_offset = 1, 1
        else:  # This is not happening in ["RGGB", "BGGR", "GRBG", "GBRG"]
            # raise RuntimeError('Unexpected pair of input and target bayer pattern!')
            h_offset, w_offset = 0, 0
        if mode == "pad":
            out = np.pad(raw, [[h_offset, h_offset], [w_offset, w_offset]], 'reflect')
        elif mode == "crop":
            h, w, c = raw.shape
            out = raw[h_offset:h - h_offset, w_offset:w - w_offset]
        else:
            raise ValueError('Unknown normalization mode!')
        return out

    def get_metadata(self, input_path : str)->np.ndarray:
        assert os.path.exists(input_path), 'Input path does not exist!, please check your input path'
        assert not input_path.endswith(('jpg', 'png', 'raw')), 'Input path should be raw file such as [.dng, .ARW] or other camera sensor dtype, ' \
                                                               'not jpg/png/raw file, please check your input path'
        raw = rawpy.imread(input_path)
        assert raw is not None, 'Raw data is None, please check your input path'
        metadata = {}
        metadata['black_level'] = raw.black_level_per_channel[0]
        metadata['white_level'] = raw.white_level
        metadata['white_balance_gain'] = np.asarray(raw.camera_whitebalance[:3]) / np.asarray(raw.camera_whitebalance[1])
        metadata['ccm'] = np.asarray(raw.color_matrix[:, :3])
        metadata['color_desc'] = raw.color_desc
        metadata['height'] = raw.sizes.height
        metadata['width'] = raw.sizes.width
        metadata['bayer_pattern_matrix'] = raw.raw_pattern
        rawdata = raw.raw_image_visible
        assert rawdata.shape[0] == metadata['height'] and rawdata.shape[1] == metadata['width'], 'Raw data shape does not match metadata, rawdata should be {}x{}, but got {}x{}'.format(metadata['height'], metadata['width'], rawdata.shape[0], rawdata.shape[1])
        assert len(rawdata.shape) == 2 or rawdata.shape[2] == 1, 'Raw data shape does not match metadata, rawdata should be 2D or 3D with 1 channel, but got {}'.format(rawdata.shape)
        assert rawdata.dtype == np.uint16, 'Raw data type should be uint16, but got {}'.format(rawdata.dtype)
        return metadata, rawdata

    def run_demosaic(self):
        raw_data = self.normalization(self.raw_data, self.black_level, self.white_level)
        raw_data = self.bayer_unify(raw_data, self.bayer_pattern, self.target_bayer_pattern, 'pad')
        if self.mode == 'opencv_dm':
            raw_data = self.inv_normalization(raw_data)
            raw_data = cv2.cvtColor(raw_data, cv2.COLOR_BAYER_RG2RGB).astype(np.float32)
            raw_data = self.normalization(raw_data, 0, 255)
        elif self.mode == 'simple_dm':
            raw_data = self.pack_img(raw_data)
            raw_data = np.stack((raw_data[:, :, 0],
                                np.mean(raw_data[:, :, 1:3], -1),
                                raw_data[:, :, 3]), -1)
            raw_data = cv2.resize(raw_data, (self.w, self.h), interpolation=cv2.INTER_LINEAR)
        elif self.mode == 'bilinear_dm':
            raw_data = demosaicing_CFA_Bayer_bilinear(raw_data, 'RGGB')
        elif self.mode == 'mal04_dm':
            raw_data = demosaicing_CFA_Bayer_Malvar2004(raw_data, 'RGGB')
        elif self.mode == 'men07_dm':
            raw_data = demosaicing_CFA_Bayer_Menon2007(raw_data, 'RGGB')

        raw_data = self.gamma_correction(raw_data, self.gamma)
        raw_data = self.f32_to_u8(raw_data)
        # raw_data = self.bayer_unify(raw_data, self.target_bayer_pattern, self.bayer_pattern, 'crop')
        self.show_demo_image(raw_data) if self.show_image else None
        self.save_demo_image(os.path.join(self.result_output_dir, str(self.mode) + '_'  + os.path.basename(self.input_data_path).replace('.dng', '.bmp')),
                           raw_data[..., ::-1]) if self.save_image else None
        return raw_data

    def run_isp_with_meta(self):
        raw_data = self.normalization(self.raw_data, self.black_level, self.white_level)
        raw_data = self.bayer_unify(raw_data, self.bayer_pattern, self.target_bayer_pattern, 'pad')
        if self.mode == 'opencv_dm':
            raw_data = self.inv_normalization(raw_data)
            raw_data = cv2.cvtColor(raw_data, cv2.COLOR_BAYER_RG2RGB).astype(np.float32)
            raw_data = self.normalization(raw_data, 0, 255)
        elif self.mode == 'simple_dm':
            raw_data = self.pack_img(raw_data)
            raw_data = np.stack((raw_data[:, :, 0],
                                 np.mean(raw_data[:, :, 1:3], -1),
                                 raw_data[:, :, 3]), -1)
            raw_data = cv2.resize(raw_data, (self.w, self.h), interpolation=cv2.INTER_LINEAR)
        elif self.mode == 'bilinear_dm':
            raw_data = demosaicing_CFA_Bayer_bilinear(raw_data, 'RGGB')
        elif self.mode == 'mal04_dm':
            raw_data = demosaicing_CFA_Bayer_Malvar2004(raw_data, 'RGGB')
        elif self.mode == 'men07_dm':
            raw_data = demosaicing_CFA_Bayer_Menon2007(raw_data, 'RGGB')

        raw_data = self.apply_wb(raw_data, self.white_balance_gain)
        raw_data = self.apply_ccm(raw_data, self.ccm)
        raw_data = self.gamma_correction(raw_data, self.gamma)

        # raw_data = self.apply_lut(raw_data, self.lut)
        # raw_data = self.apply_usm(raw_data, strength=0.5, radius=7)
        raw_data = self.f32_to_u8(raw_data)

        self.show_demo_image(raw_data) if self.show_image else None
        self.save_demo_image(os.path.join(self.result_output_dir, str(self.mode) + '_' + 'isp_' + os.path.basename(self.input_data_path).replace('.dng', '.bmp')),
                           raw_data[..., ::-1]) if self.save_image else None
        return raw_data

    # def run_isp(self):
    #     raw_data = self.normalization(self.raw_data, self.black_level, self.white_level)
    #     if self.mode == 'opencv_dm':
    #         raw_data = self.inv_normalization(raw_data)
    #         raw_data = cv2.cvtColor(raw_data, cv2.COLOR_BAYER_RG2RGB).astype(np.float32)
    #         raw_data = self.normalization(raw_data, 0, 255)
    #     elif self.mode == 'simple_dm':
    #         raw_data = self.pack_img(raw_data)
    #         raw_data = np.stack((raw_data[:, :, 0],
    #                              np.mean(raw_data[:, :, 1:3], -1),
    #                              raw_data[:, :, 3]), -1)
    #         raw_data = cv2.resize(raw_data, (self.w, self.h), interpolation=cv2.INTER_LINEAR)
    #     elif self.mode == 'bilinear_dm':
    #         raw_data = demosaicing_CFA_Bayer_bilinear(raw_data, 'RGGB')
    #     elif self.mode == 'mal04_dm':
    #         raw_data = demosaicing_CFA_Bayer_Malvar2004(raw_data, 'RGGB')
    #     elif self.mode == 'men07_dm':
    #         raw_data = demosaicing_CFA_Bayer_Menon2007(raw_data, 'RGGB')
    #     self.white_balance_gain = np.array([1.9075353622436523, 1.0,  1.7717266607284546])
    #     self.white_balance_gain /= self.white_balance_gain[1]
    #     self.ccm = np.array([[ 1.631906, -0.381807, -0.250099],
    #                         [-0.298296, 1.614734, -0.316438],
    #                         [0.023770, -0.538501, 1.514732 ]])
    #     raw_data = (raw_data * self.white_balance_gain).clip(0., 1.)
    #     raw_data = raw_data.dot(np.array(self.ccm).T).clip(0, 1)
    #     raw_data = raw_data ** (1 / 2.2)
    #     raw_data = (raw_data * 255).clip(0, 255).astype(np.uint8)
    #     self.save_demo_image(os.path.join(self.result_output_dir,
    #                                       str(mode) + '_'  + os.path.basename(im).replace('.dng', '.bmp'),
    #                                       raw_data[..., ::-1])) if self.save_image else None

    def run_model(self, weights_path : str, model: nn.Module, device: torch.device = None):
        assert os.path.exists(weights_path), 'No weights found, please check the path!'
        assert isinstance(device, torch.device), 'Device must be a torch.device, e.g. torch.device("cpu") or torch.device("cuda:0")!'
        model = model.to(device)
        device = device if device is not None else torch.device('cpu')
        ckpt = torch.load(weights_path, 'cpu')
        assert ckpt is not None, 'No checkpoint found, please check the path!'
        # isp_csd_ = {k[12:]:v for k, v in ckpt['state_dict'].items() if 'pre_encoder' in k}
        isp_csd_ = {k[10:]: v for k, v in ckpt.items() if 'gated_dip' in k}
        model.load_state_dict(isp_csd_)
        model.eval()

        raw_data = self.normalization(self.raw_data, self.black_level, self.white_level)
        raw_data = self.bayer_unify(raw_data, self.bayer_pattern, self.target_bayer_pattern, 'pad')

        if self.mode == 'simple_dm':
            raw_data = self.pack_img(raw_data)
            raw_data = np.stack((raw_data[:, :, 0],
                                np.mean(raw_data[:, :, 1:3], -1),
                                raw_data[:, :, 3]), -1)
            raw_data = cv2.resize(raw_data, (self.w, self.h), interpolation=cv2.INTER_LINEAR)

        raw_data = torch.from_numpy(raw_data).permute(2, 0, 1).float().unsqueeze(0).to(device)
        raw_data, gated = model(raw_data)
        raw_data = raw_data[0].permute(1, 2, 0).detach().cpu().numpy()
        raw_data = self.f32_to_u8(raw_data)
        self.show_demo_image(raw_data) if self.show_image else None
        self.save_demo_image(os.path.join(self.result_output_dir,
                                          str(self.mode) + '_' + 'GDIP_' + os.path.basename(self.input_data_path).replace('.dng', '.bmp')),
                             raw_data[..., ::-1]) if self.save_image else None
        print('wb:%f'%gated[0][0], 'gamma:%f'%gated[0][1], 'identity:%f'%gated[0][2], 'sharpning:%f'%gated[0][3],'fog:%f'%gated[0][4],'contrast:%f'%gated[0][5],'tone:%f'%gated[0][6], '\n')
        return raw_data




