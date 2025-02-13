
# Dataset from StoreNet community project in Dingle, Ireland

"StoreNet" is an industry-led, collaborative project where the  International Energy Research Centre led the consortium formed by: Electric Ireland (utility supplier), Solo Energy (aggregator), and ESB Networks (network operator). 20 houses have been selected to form the demonstration; each house has been equipped with a 3.3kW/10kWh residential Sonnen battery and a smart meter considering day/night-time tariffs. However, only ten houses have installed 2.4kW rooftop solar PV systems.  


## Authors

- [@Rohit-Trivedi](https://github.com/Rohit-Trivedi)

- [@IERC-iG](https://github.com/IERC-iG)

## Acknowledgements

 - [Storenet project Consortium](https://www.ierc.ie/launch-of-ierc-storenet-project-dingle-communities-to-test-new-energy-storage-batteries-in-their-connected-homes/)
 - [MIFIC project](https://www.ierc.ie/research/mific/)


## Installation

Install instructions:

- Clone this repository to a folder of your choice: 
```bash
  git clone https://github.com/Rohit-Trivedi/nat-data.git
```
- Create a new conda environment: 
```bash
  conda create --name nat-data python=3.8
```
- Activate the environment: 
```bash
  conda activate nat-data
```

- Install the package with all requirements: pip install .
```bash
  pip install .
```


- For dependencies installation, following to be used:

```bash
from setuptools import setup, find_packages

setup(
    name='StoreNet',
    version='1.0',
    description='Software to download, process and plot data',
    maintainer='Rohit Trivedi',
    maintainer_email='rohit.trivedi@ierc.ie',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'pandas==1.2.4',
        'numpy==1.20.1',
        'h5py==2.10.0',
        'matplotlib==3.3.4',
        'pytz==2021.1',
        'plotly==5.12.0'
    ]
)
```

    
## Deployment

To deploy this project:

```bash
  npm run deploy
```


## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)


## Documentation

[Documentation](https://linktodocumentation) (A link to published paper will be added).


## Feedback

If you have any feedback, please reach out to us at info@ierc.ie


## Contributing

Contributions are always welcome!

See following link to get started
https://github.com/github/docs/blob/main/CONTRIBUTING.md

Please adhere to this project's `code of conduct`.


## Features

- Light/dark mode toggle
- Live previews
- Fullscreen mode
- Cross platform


## Screenshots

![Storenet Setup](https://d2ygkcw3bu7ib2.cloudfront.net/app/uploads/2022/03/Untitled-design-13.jpg)

