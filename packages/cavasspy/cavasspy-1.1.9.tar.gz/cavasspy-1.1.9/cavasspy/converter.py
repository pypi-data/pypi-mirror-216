import os
import shutil
from uuid import uuid4

from cavasspy.sys_helper import execute_cmd


def nifti2dicom(input_file, output_dir, accession_number=1):
    """
    Require nifti2dicom.
    sudo apt install nifti2dicom
    https://github.com/biolab-unige/nifti2dicom
    """
    cmd = f'nifti2dicom -i {input_file} -o {output_dir} -a {accession_number}'
    result = os.popen(cmd)
    return result.readlines()


def dicom2cavass(input_dir, output_file, add_value=0):
    """
    Note that if the output file path is too long, this command may be failed.
    """
    r = execute_cmd(f'from_dicom {input_dir}/* {output_file} +{add_value}')
    return r


def nifti2cavass(input_file, output_file, add_value=1024, dicom_accession_number=1):
    save_path = os.path.split(output_file)[0]
    tmp_dicom_dir = os.path.join(save_path, f'{uuid4()}')
    r1 = nifti2dicom(input_file, tmp_dicom_dir, dicom_accession_number)
    r2 = dicom2cavass(tmp_dicom_dir, output_file, add_value)
    shutil.rmtree(tmp_dicom_dir)
    return r1, r2
