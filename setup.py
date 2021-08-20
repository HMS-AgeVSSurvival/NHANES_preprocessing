from setuptools import setup

setup(
    name="nhanes-preprocessing",
    version="0.1",
    description="Preprocess the data from NHANES dataset.",
    packages=[
        "fusion",
        "cleaning",
        "casting",
        "merge",
        "correlation_with_age",
        "utils",
    ],
    requires=["setuptools", "wheel"],
    install_requires=[
        "numpy==1.16.5",
        "pandas==1.2.4",
        "pyarrow==4.0.1",
        "xport==2.0.2",
        "gspread==3.7.0",
        "scipy==1.7.0",
        "matplotlib==3.4.2",
        "openpyxl==3.0.7",
    ],
    extras_require={"dev": ["tqdm==4.61.0", "jupyter==1.0.0", "ipympl==0.7.0", "black==21.5b2"]},
    entry_points={
        "console_scripts": [
            "fusion=fusion.fusion:fusion_cli",
            "cleaning=cleaning.cleaning:cleaning_cli",
            "casting=casting.casting:casting_cli",
            "merge=merge.merge:merge_cli",
            "correlation_with_age=correlation_with_age.upload_correlation:correlation_with_age_cli",
            "scatter_plot=correlation_with_age.scatter_plot:scatter_plot_cli",
        ]
    },
)
