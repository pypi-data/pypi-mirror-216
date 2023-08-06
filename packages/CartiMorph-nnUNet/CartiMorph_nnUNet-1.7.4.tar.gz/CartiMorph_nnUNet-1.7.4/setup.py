from setuptools import setup, find_namespace_packages

setup(name='CartiMorph_nnUNet',
      packages=find_namespace_packages(include=["CartiMorph_nnUNet", "CartiMorph_nnUNet.*"]),
      version='1.7.4',
      description='nnU-Net with minor revisions tailored for the CartiMorph framework.',
      url='https://github.com/YongchengYAO/CartiMorph-nnUNet',
      author='Yongcheng Yao, Chinese University of Hong Kong',
      license='Apache License Version 2.0, January 2004',
      install_requires=[
            "torch>1.10.0",
            "tqdm",
            "dicom2nifti",
            "scikit-image>=0.14",
            "medpy",
            "scipy",
            "batchgenerators>=0.23",
            "numpy",
            "sklearn",
            "SimpleITK",
            "pandas",
            "requests",
            "nibabel", 
            "tifffile", 
            "matplotlib",
      ],
      entry_points={
          'console_scripts': [
              'CartiMorph_nnUNet_plan_and_preprocess = CartiMorph_nnUNet.experiment_planning.nnUNet_plan_and_preprocess:main',
              'CartiMorph_nnUNet_train = CartiMorph_nnUNet.run.run_training:main',
              'CartiMorph_nnUNet_predict = CartiMorph_nnUNet.inference.predict_simple:main'
          ],
      },
      keywords=['deep learning', 'image segmentation', 'medical image analysis',
                'medical image segmentation', 'nnU-Net', 'nnunet']
      )
