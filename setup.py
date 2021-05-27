from setuptools import setup, find_packages

setup(
    name="nhanes_preprocessing",
    version="0.1",
    description="Preprocess the data from NHANES dataset.",
    packages=find_packages(),
    requires=["setuptools", "wheel"],
    install_requires=["numpy", "pandas"],
    extras_require={"dev": ["tqdm", "ipykernel", "black"]},
)
