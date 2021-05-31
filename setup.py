from setuptools import setup, find_packages

setup(
    name="nhanes_preprocessing",
    version="0.1",
    description="Preprocess the data from NHANES dataset.",
    packages=find_packages(),
    requires=["setuptools", "wheel"],
    install_requires=["numpy", "pandas", "pyarrow", "xport==2.0.2"],
    extras_require={"dev": ["tqdm", "jupyter", "black"]},
    entry_points={
        "console_scripts": [
            "fusion_examination=fusion.fusion:fusion_examination_cli",
        ]
    },
)
