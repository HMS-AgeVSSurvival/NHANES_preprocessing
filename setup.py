from setuptools import setup

setup(
    name="nhanes-preprocessing",
    version="0.1",
    description="Preprocess the data from NHANES dataset.",
    packages=["fusion", "cleaning"],
    requires=["setuptools", "wheel"],
    install_requires=["numpy", "pandas", "pyarrow", "xport==2.0.2"],
    extras_require={"dev": ["tqdm", "jupyter", "ipympl", "black", "matplotlib"]},
    entry_points={
        "console_scripts": [
            "fusion_examination=fusion.fusion:fusion_examination_cli",
            "cleaning_examination=cleaning.cleaning:cleaning_examination_cli",
        ]
    },
)
