from setuptools import setup

setup(
    name="nhanes-preprocessing",
    version="0.1",
    description="Preprocess the data from NHANES dataset.",
    packages=["fusion", "cleaning", "casting", "merge"],
    requires=["setuptools", "wheel"],
    install_requires=["numpy", "pandas", "pyarrow", "xport==2.0.2"],
    extras_require={"dev": ["tqdm", "jupyter", "ipympl", "black", "matplotlib", "openpyxl"]},
    entry_points={
        "console_scripts": [
            "fusion=fusion.fusion:fusion_cli",
            "cleaning=cleaning.cleaning:cleaning_cli",
            "casting=casting.casting:casting_cli",
            "merge=merge.merge:merge_cli"
        ]
    },
)
