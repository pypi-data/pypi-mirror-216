import onnx_tool
import torch
import torch.nn as nn
# import onnx
import os
from thop import profile, clever_format
import netron
#
# def load_onnx_model(onnx_path):
#     onnx_model = onnx.load(onnx_path)
#     onnx.checker.check_model(onnx_model)
#     return onnx_model
#
# def load_pytorch_model(model_path):
#     model = torch.load(model_path)
#     return model
#
# def compare_model(onnx_model, pytorch_model, input_size, input_tensor):
#     onnx_input = input_tensor.cpu().numpy()
#     pytorch_input = input_tensor
#     onnx_output = onnx_tool.run_onnx_model(onnx_model, onnx_input)
#     pytorch_output = pytorch_model(pytorch_input)
#     print('onnx_output:', onnx_output)
#     print('pytorch_output:', pytorch_output)
#     print('onnx_output - pytorch_output:', onnx_output - pytorch_output)

def mkfolder(path):
    if isinstance(path, list):
        for p in path:
            if not os.path.exists(p):
                os.makedirs(p)
                print({p}, 'is created for saving the results.')
    else:
        if not os.path.exists(path):
            os.makedirs(path)
            print({path}, 'is created for saving the results.')

def calpipe(
                onnx_path: str,
                output_path: str = None,
                use_model: nn.Module = None,
                use_onnx_sim: bool = True,
                use_onnx_tool: bool = True,
                use_opcounter: bool = False,
                use_netron: bool = False,
                sufix:str = '.txt'):

    assert isinstance(use_model, nn.Module), 'model must be a nn.Module'
    assert isinstance(input_shape, tuple), 'input_data must be a torch.tensor'
    assert isinstance(onnx_path, str), 'onnx_path must be a str'
    assert isinstance(output_path, str), 'output_path must be a str'
    assert isinstance(use_onnx_tool, bool), 'use_onnx_tool must be a bool'
    assert isinstance(use_opcounter, bool), 'use_opcounter must be a bool'
    assert isinstance(use_netron, bool), 'use_netron must be a bool'
    assert isinstance(sufix, str), 'sufix must be a str'

    if sufix not in ['.txt', '.csv']:
        raise ValueError('sufix must be txt or csv')

    # input_data = torch.randn(input_shape)
    # model.eval()

    if use_opcounter and use_model is not None:
        input_data = torch.randn(1, 3, 512, 512)
        print('use opcounter to profile model...')
        flops, params = profile(use_model, inputs=(input_data, ))
        flops, params = clever_format([flops, params], "%.3f")
        print(f'Macs: {flops}, Params: {params}')

    if use_onnx_tool:
        if use_onnx_sim:
            onnx_sim_path = onnx_path[:-5] + '_sim.onnx'
            sim_onnx, check = simplify(onnx.load(onnx_path))
            assert check, 'Simplified ONNX model could not be validated'
            onnx.save(sim_onnx, onnx_sim_path)
            onnx_tool.model_profile(onnx_sim_path)
            print('use onnx_sim to simply..')
        # with torch.no_grad():
        #     torch.onnx.export(
        #         model,
        #         input_data,
        #         output_path,
        #         opset_version=11,
        #         input_names=['input'],
        #         output_names=['output'])
        # onnx_model = onnx.load(output_path)
        # try:
        #     onnx.checker.check_model(onnx_model)
        # except Exception:
        #     print("×××, Model incorrect, please debug")
        # else:
        #     print("2.onnx_Model correct...")
        print('use onnx_tool to profile model...')
        onnx_tool.model_profile(onnx_path)  # pass file name
        onnx_tool.model_profile(onnx_path, savenode=f'{output_path[:-5]}' + sufix)  # save profile table to txt file
    if use_netron:
        print('4.use netron to visualize model...')
        netron.start(onnx_sim_path) if use_onnx_sim else netron.start(onnx_path)



# if __name__ == "__main__":
#     from pth2onnx import ControlNetHED_Apache2
#     model = ControlNetHED_Apache2()
#     model.eval()
#     input_data = (1, 3, 512, 512)
#     output_path = 'controlnethed.onnx'
#     calpipe(model, input_data, output_path, use_onnx_tool=True, use_opcounter=True, sufix='.csv')