import os
from typing import Union
from PIL import Image


def test_CompareImages(image_diff):
    image_fnames = ['HomePage.png', 'ProjectPage.png', 'ModelPage.png', 'AnalysisPage.png', 'SummaryPage.png']

    script_dir = os.path.dirname(__file__)
    current_work_dir = os.getcwd()

    actual_images_dir =  os.path.join(current_work_dir, '.tests', 'GuiTests', 'BasicGuiTest', 'ActualImages')
    expected_image_dir = os.path.join(script_dir, 'ExpectedImages')


    for image_fname in image_fnames:
        actual_image: Image or str or bytes = os.path.join(actual_images_dir, image_fname)
        expected_image: Image or str or bytes = os.path.join(expected_image_dir, image_fname)
        image_diff(actual_image, expected_image)


if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    current_work_dir = os.getcwd()
    actual_images_dir =  os.path.join(current_work_dir, '.tests', 'GuiTests', 'BasicGuiTest', 'ActualImages')
    expected_image_dir = os.path.join(script_dir, 'ExpectedImages')

    print('actual_images_dir', actual_images_dir)
    print('expected_image_dir', expected_image_dir)
