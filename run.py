import os
import glob
from tqdm import tqdm
import nibabel as nib
import SimpleITK as sitk

from utils.seed import set_seed
from utils.logger import setup_logger
from utils.options import get_args
from lungmask import LMInferer

def main(args, logger):

    data_path = glob.glob(args.dataset_dir+'*')
    logger.info(f'Patient Number: {len(data_path)}')

    inferer = LMInferer(modelname = args.model)

    for data in tqdm(data_path):
        cts = glob.glob(data+'/*')
        for ct_path in cts:
            # segmentation
            ct_file = glob.glob(ct_path+'/*')[0]
            x = sitk.ReadImage(ct_file)
            seg = inferer.apply(x)
            # save nifti
            img = sitk.GetArrayFromImage(x)
            img = img.transpose(2,1,0)
            seg = seg.transpose(2,1,0)
            new_img = nib.Nifti1Image(img, None)
            new_seg = nib.Nifti1Image(seg, None)
            out_path = ct_file.replace(args.dataset_dir, f'{args.output_dir}/ct_seg/')
            os.makedirs(ct_path.replace(args.dataset_dir, f'{args.output_dir}/ct_seg/'), exist_ok=True)
            nib.save(new_img, out_path+'.gz')
            nib.save(new_seg, out_path.replace('.nii', '_seg.nii.gz'))


if __name__ == '__main__':

    args = get_args()
    set_seed(args.seed)
    os.makedirs(f'{args.output_dir}/ct_seg', exist_ok=True)

    logger = setup_logger('Lung Detection', f'{args.output_dir}')
    logger.info(str(args).replace(',','\n'))

    main(args, logger)

