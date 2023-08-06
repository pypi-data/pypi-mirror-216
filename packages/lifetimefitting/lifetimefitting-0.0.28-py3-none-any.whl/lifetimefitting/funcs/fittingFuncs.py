import struct
import numpy as np
from phdimporter import TRF
from scipy.optimize import curve_fit
from PyQt6.QtWidgets import QMessageBox, QLineEdit
from .gui import Ui_Form
from .expFuncs import expFunc, expFuncWC
from .expFuncs import FLFuncList, FLLinFuncList

def chiSQ(y_obs: list[float], y_pred: list[float], popt: list[float]) -> float:
    dof = len(y_obs) - (len(popt))
    # ensure no divide by 0
    y_pred_max_1 = [i + 1 if i == 0 else i for i in y_pred]
    return np.sum(np.divide(np.square(np.subtract(y_obs, y_pred)), y_pred_max_1)) / len(y_pred)


def loadAndCull(fc: QLineEdit, ui: Ui_Form) -> tuple[list[float], list[int], bool]:
    loaded = False
    x = y = []

    if fc.text() == '':
        QMessageBox(icon=QMessageBox.Icon.Critical, text='TRF or IRF not loaded!').exec()
    elif fc.text()[-4:] == '.asc' and ui.binSize_widg.value() == 0.0:
        QMessageBox(icon=QMessageBox.Icon.Critical, text='BinWidth must be manually set when using .asc files').exec()
    else:
        filename = fc.text().split("/")[-1].split("\\")[-1]
        try:
            trf = TRF(fc.text(), binSize=ui.binSize_widg.value())
            y = trf.y
            x = trf.x
            ui.binSize_widg.setValue(trf.Resolution_int)
            loaded = True
        except struct.error:
            QMessageBox(icon=QMessageBox.Icon.Critical, text=f'There was a problem reading {filename}').exec()
        except UnboundLocalError:
            QMessageBox(icon=QMessageBox.Icon.Critical, text=f'There was a problem reading {filename}').exec()

    return x, y, loaded

def fitLifetime(ui: Ui_Form, x: list[float], y: list[float], maxIter: int) -> tuple[list[float], int]:
    expCount = ui.expCount_widg.value()

    minbounds = [max(y) - 500]
    maxbounds = [max(y) + 500]

    fitFunc = FLFuncList[expCount]
    if ui.logFit_widg.isChecked():
        y = np.log(y)
        fitFunc = FLLinFuncList[expCount]

    for i in range(expCount):
        minbounds += [0, 0]
        maxbounds += [99999999, 1]

    popt, pcov = curve_fit(fitFunc, x, y,
                           bounds=(minbounds, maxbounds),
                        #    maxfev=maxIter,
                           max_nfev=999999999999,
                           # verbose=2,
                           )

    residual = np.sum(np.subtract(y, FLFuncList[expCount](x, *popt)))

    return popt, residual

def fitFL(ui: Ui_Form, plot: bool = True, x_in: list[float] = None, y_in: list[int] = None, irf_in: list[int] = None) -> str:
    csv = 'x,y_lin,y_log\n'
    csvTail = '\n'
    outPrint = ''
    maxIter = ui.maxIter_widg.value()
    binSize = ui.binSize_widg.value()
    expCount = ui.expCount_widg.value()

    global t
    global spectrumObject

    irf = irf_in
    irf = np.array(irf)

    irfMaxBin = irf.tolist().index(max(irf))
    for c, i in enumerate(irf[irfMaxBin:]):
        if i == 0:
            zeroBin = c + irfMaxBin
            break
    irf = irf[:zeroBin]

    for c, i in enumerate(reversed(irf[:irfMaxBin])):
        if i == 0:
            zeroBin = irfMaxBin - c
            break
    irf = irf[zeroBin:]

    x_raw = x_in
    y_raw = y_in

    max_y = max(y_raw)
    irf = list(reversed(irf))  # the kernel is flipped in convolutions
    y_raw = np.append(y_raw, np.zeros((len(y_raw), 1)))
    y_raw = np.convolve(y_raw, irf, 'full')
    x_raw = [i*binSize*1e-3 for i in range(len(y_raw))]

    y_raw = np.divide(y_raw, max(y_raw)/max_y)

    maxTime = ui.maxTime_widg.value()
    maxBins = int(maxTime*ui.binSize_widg.value()*1e3)
    maxBin = y_raw.tolist().index(max(y_raw))
    for c, i in enumerate(y_raw[maxBin:]):
        if i == 0:
            zeroBin = c + maxBin
            break
    x_raw = x_raw[:zeroBin]
    y_raw = y_raw[:zeroBin]

    x_start = y_raw.tolist().index(max(y_raw)) + ui.startOffset_widg.value()

    x_raw = np.subtract(x_raw, (x_start * binSize) / 1000)
    x = x_raw[x_start:]
    y = y_raw[x_start:]

    try:
        index = np.argmin(np.abs(np.array(x)-ui.maxTime_widg.value()))
    except ValueError:
        QMessageBox(icon=QMessageBox.Icon.Critical, text=f'The chosen start offset of {ui.startOffset_widg.value()} was too large for the data').exec()
        return

    cutoff = x[index]
    x = x[:index]
    y = y[:index]

    if plot:
        if ui.plotIRF_widg.isChecked() and plot:
            ui.axList += ui.ax3.plot([i*binSize*1e-3 for i in range(len(irf))], irf, c='g')

        x_func = np.arange(-2, ui.max_x.value(), 0.01)
        # Log Plot
        ui.ax1.set_xlim(-2, ui.max_x.value())
        ui.axList += [ui.ax1.axvline(cutoff, c='r', lw=0.5)]
        ui.axList += [ui.ax1.scatter(x_raw, y_raw, s=0.1, c='b')]
        # Linear plot
        ui.ax3.set_ylim(-300, max(y_raw)+300, auto=False)
        ui.axList += [ui.ax3.axvline(cutoff, c='r', lw=0.5)]
        ui.axList += [ui.ax3.scatter(x_raw, y_raw, s=0.1, c='b')]


    popt, residual = fitLifetime(ui, x, y, maxIter)
    I0 = popt[0]
    popt_culled = popt[1:]

    cList = []
    for i in range(expCount):
        cList += [popt_culled[(i * 2) + 1]]
    cList_norm = np.multiply(cList, 1 / np.sum(cList))

    I0 = I0 / (1 / np.sum(cList))

    popt = [I0]
    τList = []
    for i in range(expCount):
        τ = popt_culled[i * 2]
        τList += [τ]
        c = cList_norm[i]
        popt += [τ, c]

    chi2 = chiSQ(FLFuncList[expCount](x, *popt), y, popt)
    chi2_log = chiSQ(FLLinFuncList[expCount](x, *popt), np.log(y), popt)

    if plot:
        outPrint += f'𝜒² (lin space): {chi2:.4f}\n'
        csvTail += f'chi2,{chi2}\n'
        outPrint += f'Residual: {residual:.8f}\n'
        csvTail += f'residual,{residual}\n'
        outPrint += f'I0: {I0:.2f}\n'
        csvTail += f'I0,{I0}\n'
        for i in range(expCount):
            τ = popt_culled[i * 2]
            c = cList_norm[i]
            outPrint += f'τ: {τ:.2f}\n'
            csvTail += f'tau,{τ}\n'
            outPrint += f'Contribution: {c*100:.2f}%\n'
            csvTail += f'contribution,{c}\n'
            if ui.scaled_widg.isChecked():
                ui.axList += ui.ax1.plot(x_func, expFuncWC(x_func, I0, τ, c), 'g--', lw=0.5)
                ui.axList += ui.ax3.plot(x_func, expFuncWC(x_func, I0, τ, c), 'g--', lw=0.5)
            else:
                ui.axList += ui.ax1.plot(x_func, expFunc(x_func, I0, τ), 'g--', lw=0.5)
                ui.axList += ui.ax3.plot(x_func, expFunc(x_func, I0, τ), 'g--', lw=0.5)
        ui.axList += ui.ax1.plot(x_func, FLFuncList[expCount](x_func, *popt), 'k--', lw=1)
        ui.axList += ui.ax3.plot(x_func, FLFuncList[expCount](x_func, *popt), 'k--', lw=1)

        residualList = np.subtract(FLLinFuncList[expCount](x, *popt), np.log(y))
        ui.axList += [ui.ax2.scatter(x, residualList, s=0.1, c='b')]
        residualList = np.subtract(FLFuncList[expCount](x, *popt), y,)
        ui.axList += [ui.ax4.scatter(x, residualList, s=0.1, c='b')]

        ui.canvas.draw()
        ui.text_output.setText(outPrint)

        for x, y_lin, y_log in zip(x_in, FLFuncList[expCount](x_raw, *popt), FLLinFuncList[expCount](x_raw, *popt)):
            csv += f'{x},{y_lin},{y_log}\n'
        csv += f'\n{csvTail}'

    return csv
