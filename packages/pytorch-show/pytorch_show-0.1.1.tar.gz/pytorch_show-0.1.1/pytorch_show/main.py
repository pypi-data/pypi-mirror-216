import argparse
from utils import draw
import importlib
import torch
from torch import nn
import os


def parse_py(py_path: str) -> list[nn.Module]:
    spec = importlib.util.spec_from_file_location('module_name', py_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module_classes = [m for _, m in module.__dict__.items() if
                      isinstance(m, (nn.Module, type)) or issubclass(type(m),nn.Module)]
    if len(module_classes) == 0:
        raise ValueError('No nn.Module class found in the file.')
    return module_classes


def main():
    parser = argparse.ArgumentParser(description="Draw a model structure diagram")
    parser.add_argument('--file', '-f', type=str, required=True, help='the file of model(only support .py)')
    parser.add_argument('--input-size', '-i', type=int, nargs='+', default=[224, 224],
                        help='the size of model input,just img size')
    parser.add_argument('--dir', '-d', default='./Save', type=str, help='The path of save dir')
    parser.add_argument('--name', '-n', default='model.svg', type=str, help='The name of save svg')
    args = parser.parse_args()

    if not os.path.exists(args.dir):
        os.makedirs(args.dir)

    model_file = args.file
    model_list = []
    inputs_shape = [1, 3]
    inputs_shape.extend(args.input_size)
    inputs = torch.randn(inputs_shape)

    if model_file.endswith('.py'):
        model_list = parse_py(model_file)
    else:
        print("Just support .py !!!")

    for index, model_name in enumerate(model_list):

        try:
            if not isinstance(model_name, nn.Module):
                model = model_name()

            else:
                model = model_name
            args.name=type(model).__name__+'.svg'
            draw(model, inputs, save_dir=args.dir, save_name=args.name)
        except:
            print(f"{model_name} draw failed")
            pass


if __name__ == "__main__":
    main()
