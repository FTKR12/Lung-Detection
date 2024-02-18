import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Lung Detection")
    ########## base options ##########
    parser.add_argument('--seed', default=123, type=int)
    parser.add_argument('--output_dir', default='output')
    parser.add_argument('--dataset_dir', default='dir/to/dataset/dir')
    ########## model options ##########
    parser.add_argument('--model', default='R231', choices=['R231', 'LTRCLobes', 'R231CovidWeb'])
    parser.add_argument('--fillmodel', default='R231')

    args = parser.parse_args()
    return args