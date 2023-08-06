# LifetimeFittingTool
This is a quick tool I wrote to take some of my TCSPC fluorescence lifetime fitting tools from [spectraImport.ipynb](https://github.com/adreasnow/excided-state-notebooks/blob/main/spectraImport.ipynb) and make them usable for other people. It can read PicoHarp .phd files thanks to [adreasnow/picoharp-phd](https://github.com/adreasnow/picoharp-phd) and also reads the plain `.txt` output it can save.

![screenshot](screenshot.png)

The app itself is a basic least squares regression tool but allows you to fit in linear or logarithmic space, supports up to 4 decays, and can export images as well as .csv files of the fitted histograms

## Installing

### PyPi

The easiest way to get it is to install it directly from pypy, so as too pull all the dependencies:

```python
pip install lifetimefitting
```

### Manually

* Python (I'm not sure how old you could go, but I know it runs on >3.9)
* Matplotlib
* Numpy
* PyQt6
* Scipy

These can be installed pretty easily via pip

```bash
pip install matplotlib numpy scipy pyqt6
```

or conda

```bash
conda install matplotlib numpy scipy pyqt6
```

Then you can clone the module down and install it manually

```bash
git clone https://github.com/adreasnow/LifetimeFittingTool.git
cd LifetimeFittingTool
python setup.py install
```

## Usage

To run the app, all you need to do is execute the module in python and a QT window should appear :)

```bash
python -m lifetimefitting
```



## The Maths

Uses the form of the function:

$$
fl(t)=I_0 exp\bigg(-\frac{t}{\tau}\bigg)
$$

Where:
* $t =$ Time
* $\tau =$ Fluorescence lifetime
* $I_0 =$ Initial photon concentration

For the corrected fitting procedure, the convolved function is calculated as:

$$
fl=fl(t)_{IRF}\otimes fl(t)
$$

$$
fl_{fitted}=\sum_{i=1}^{\text{exponents}} C_i\cdot fl(t)_i
$$

Where:
* $fl(t)_{IRF} =$ Fitted instrument response function
* $fl(t)_i =$ Fitted function for each decay
* $C_i =$ Linear coefficient for each decay

$\chi^2$ is calculated as per [fluortools](http://www.fluortools.com/software/decayfit/documentation/fit)

$$
\chi^2 = \sum_{j=1}^{n} (c_j-\hat{c_j})^2/\hat{c_j}\\
\chi^2_{red}=\frac{\chi^2}{n}
$$
