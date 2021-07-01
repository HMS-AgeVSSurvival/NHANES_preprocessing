from setuptools import setup

setup(
    name="nhanes-preprocessing",
    version="0.1",
    description="Preprocess the data from NHANES dataset.",
    packages=["fusion", "cleaning", "casting", "merge", "correlation_with_age", "utils"],
    requires=["setuptools", "wheel"],
    install_requires=["numpy", "pandas", "pyarrow", "xport==2.0.2", "gspread", "scipy", "matplotlib", "openpyxl"],
    extras_require={"dev": ["tqdm", "jupyter", "ipympl", "black"]},
    entry_points={
        "console_scripts": [
            "fusion=fusion.fusion:fusion_cli",
            "cleaning=cleaning.cleaning:cleaning_cli",
            "casting=casting.casting:casting_cli",
            "merge=merge.merge:merge_cli",
            "correlation_with_age=correlation_with_age.upload_correlation:correlation_with_age_cli",
            "scatter_plot=correlation_with_age.scatter_plot:scatter_plot_cli"
        ]
    },
)
