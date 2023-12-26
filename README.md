<div align="center">
  
# primkit - Primer Toolkit

![DigitalChristmasTreeFarm Cover](./img/primkit,jpg)

</div>


## Introduction
`primkit` is a comprehensive tool designed to facilitate the primer design process for various molecular biology applications. It assists researchers with the creation, analysis, and preprocessing of primer results, optimizing both convenience and efficiency.

## Features
- **Automated Primer Design**: Quickly generate primers suited to your specific requirements.
- **Compatibility Check**: Verify the compatibility of your primers with target sequences.
- **Result Preprocessing**: Easily format and preprocess your primer design outcomes.
- **User-Friendly**: An intuitive tool for both experienced and novice users in bioinformatics.

## Installation

### From PyPI
You can install the released version of `primkit` from PyPI with a simple pip command:
```bash
pip install primkit
```
**Make sure you have Python 3.6 or later installed.**

### Using a Mirror
For users in China, or in case the PyPI is slow or restricted in your location, you may opt to use a Chinese mirror. Here are examples using Aliyun and Tencent Cloud mirrors:

- Using Aliyun:
```bash
pip install primkit -i https://mirrors.aliyun.com/pypi/simple/

```
- Using Tencent Cloud:
```bash
pip install primkit -i https://mirrors.cloud.tencent.com/pypi/simple
```

### From GitHub (Using pip)
To install the latest version directly from GitHub using pip:
```bash
pip install git+https://github.com/Enthusiasm23/primkit.git
```
### From Source (Using git clone and setup.py)
If you prefer to install from source for a development environment, you can clone the repository and use `setup.py`:
```bash
git clone https://github.com/Enthusiasm23/primkit.git
cd primkit
python setup.py install
```

**Note: Installing directly from GitHub is recommended for developers or if you need features that have not yet been released to PyPI.**

## Usage
After installing `primkit`, you can use it to design primers with your specific requirements. Here is a basic example of how to use `primkit`:

```python
import primkit

# Define your primer design parameters
primer_data = {
    'DB': 'hg19.fa',                                                          # Reference database
    'SnpFilter': 'yes',                                                       # SNP filtering option
    'PrimerMinSize': '17',                                                    # Minimum size of the primer
    'PrimerOptSize': '22',                                                    # Optimal size of the primer
    'PrimerMaxSize': '25',                                                    # Maximum size of the primer
    'PrimerMinTm': '58',                                                      # Minimum melting temperature of the primer
    'PrimerOptTm': '60',                                                      # Optimal melting temperature of the primer
    'PrimerMaxTm': '62',                                                      # Maximum melting temperature of the primer
    'ProdMinSize': '80',                                                      # Minimum size of the product
    'ProdMaxSize': '120',                                                     # Maximum size of the product
    'DimerScore': '5',                                                        # Maximum acceptable dimer score
    'HairpinScore': '5',                                                      # Maximum acceptable hairpin score
    'Tm': '47',                                                               # Annealing temperature
    'SpecMinSize': '0',                                                       # Minimum size for specificity check
    'SpecMaxSize': '500',                                                     # Maximum size for specificity check
    'BedInput': 'chr7\t55249070\t55249073\nchr22\t42538507\t42538510\n...'    # Target regions in BED format
}

# Call the design_primers function with the primer data
primer_result = primkit.design_primers(primer_data)

# The 'primer_result' variable will contain the results of the primer designt primkit
```
For comprehensive guides and usage examples, check the [documentation](docs/README.md).

## Contributing
Contributions to primkit are welcome! Feel free to submit pull requests or open issues to propose enhancements or add new features.

## Acknowledgments and Disclaimer
`primkit` serves as a convenient interface for primer design, building upon the robust primer design capabilities of [MFEprimer3](https://mfeprimer3.igenetech.com/muld). We extend our sincere gratitude to the original authors of MFEprimer-3.0 for their significant contributions to the scientific community. You can find the original MFEprimer-3.0 tool and source code on their [GitHub repository](https://github.com/quwubin/MFEprimer-3.0).

While `primkit` aims to simplify the primer design process, users who intend to apply this for commercial purposes should do so with caution. We do not guarantee the correctness of the primer design results generated by `primkit`. For rigorous and commercial-grade applications, we recommend using the [original MFEprimer-3.0 web interface](https://mfeprimer3.igenetech.com/muld) directly.

## License
`primkit` is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
If you have any questions or feedback, reach out to us at lbfeng23@gmail.com.

**Enjoy using primkit, and may your primer design be effortless and precise!**
