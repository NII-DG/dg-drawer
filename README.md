# dg-drawer (in development)

Drawing module for NII data governance

## Function

* Drawing images from Data Governance data as defined in the [NII Data Governance function](https://rcos.nii.ac.jp/service/dmp/).
  * Supported Data Governance Images
    * Research Flow History
    * (In development....)


## Installation

0. Requirements
    * Python : >= 3.9

1. Install dg-drawer

    ```bash
    # Install from PyPI [TODO: not available yet]
    $ pip install dg-packager

    # install from source on [GitHub Repository](https://github.com/NII-DG/dg-drawer)
    pip install git+https://github.com/NII-DG/dg-drawer.git@feature/drawer
    ```

## Usage

 * [Research Flow History](./doc/ResearchFlowHistory.md)

### Research Flow History



## Branch and Release Management

- `main`: Latest Release Branches
  - Direct push to main is prohibited.
- `develop/<name>`: branch for development
- `feature/<name>`: branch for each function/modification
  - Basically, create a `feature/<name>` branch from `develop/<name>` and merge it into the `develop/<name>` branch.

## License

[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).

See the [LICENSE](./LICENSE).