import shutil

import numpy as np

from cavasspy.op import get_ct_resolution, read_cavass_file, save_cavass_file


def match_im0(im0_file, bim_file, output_file):
    shape_1 = get_ct_resolution(im0_file)
    shape_2 = get_ct_resolution(bim_file)
    if shape_1[2] == shape_2[2]:
        shutil.copy(bim_file, output_file)
    else:
        original_data = read_cavass_file(bim_file)
        data = np.zeros(shape_1, dtype=bool)
        data[..., :original_data.shape[2]] = original_data
        save_cavass_file(output_file, data, True, reference_file=im0_file)


if __name__ == '__main__':
    ct_file = '/data/xzw/VAA/IM0/N130-A-CT.IM0'
    gt_file = '/data/xzw/VAA/labels-bim/VAA-Abdomen/N130-A-CT/N130-A-LAdG-CT.BIM'
    output_file = '/data/xzw/VAA_cavass/N130-A-CT/N130-A-LAdG-CT.BIM'
    match_im0(ct_file, gt_file, output_file)
