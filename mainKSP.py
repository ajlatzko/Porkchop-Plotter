import os
import numpy as np
import kspPorkchop as pork
import porkmap
import time
import astrodynamics as ast
import matplotlib.pyplot as plt
import multiprocessing as mp

def date2utKSP(y, d, h, m, s):
    # Convert a KSP date to universal time
    return s + m*60 + h*60*60 + d*60*60*6 + y*9203545

def getVectors(i, depPlanet, UTdeps, arrPlanet, UTarrs, resolution):
    # Get r and v vectors for departure and arrival planets
    r_dep = depPlanet.orbit.posAtTrueAnomaly(depPlanet.orbit.trueAnomalyAt(UTdeps[i]))
    v_dep = depPlanet.orbit.velocityAtTrueAnomaly(depPlanet.orbit.trueAnomalyAt(UTdeps[i]))
    r_arr = np.zeros((3, resolution))
    v_arr = np.zeros((3, resolution))
    for j in range(resolution):
        r_arr[:,j] = arrPlanet.orbit.posAtTrueAnomaly(arrPlanet.orbit.trueAnomalyAt(UTarrs[j,i]))
        v_arr[:,j] = arrPlanet.orbit.velocityAtTrueAnomaly(arrPlanet.orbit.trueAnomalyAt(UTarrs[j,i]))
    return i, r_dep, v_dep, r_arr, v_arr


def computeDV(index, rArrayDep, rArrayArr, fltTimes, mu, vArrayDep, vArrayArr):
    # Solve Lambert's problem to get the delta V
    i, j = index
    v1, v2 = ast.LambertSolver(rArrayDep[i, :], rArrayArr[i, :, j], fltTimes[j], mu)

    # Subtract planet velocity then compute delta V
    vInfDep = np.linalg.norm(v1 - vArrayDep[i, :])
    vInfArr = np.linalg.norm(v2 - vArrayArr[i, :, j])
    return j, i, vInfDep + vInfArr

if __name__ == '__main__':
    # Plot porkchop (KSP Version)
    print('*--------------------------*')
    print('|   KSP Porkchop Plotter   |')
    print('*--------------------------*\n')

    # Get number of CPU threads
    numWorkers = os.cpu_count()
    
    depPlanet = pork.Kerbin
    depPlanetName = depPlanet.name
    arrPlanet = pork.Duna
    arrPlanetName = arrPlanet.name
    
    resolution = 300
    
    # Date range
    yStart = 1
    dStart = 1
    yEnd = 3
    dEnd = 1
    
    # Time of flight range in days
    fltTimeStart = 151
    fltTimeEnd = 453
    
    mu = depPlanet.orbit.refBody.gravParameter

    # Calculate time ranges
    print('Calculating time ranges...')
    t0TRange = time.perf_counter()
    UTdepRange = (date2utKSP((yStart)-1,(dStart)-1,0,0,0), date2utKSP((yEnd)-1,(dEnd)-1,0,0,0))
    flightTimeRange = (date2utKSP(0,fltTimeStart,0,0,0), date2utKSP(0,fltTimeEnd,0,0,0))
    UTdeps = np.linspace(UTdepRange[0], UTdepRange[1], resolution)
    fltTimes = np.linspace(flightTimeRange[0], flightTimeRange[1], resolution)
    UTarrs = np.zeros((resolution,resolution))
    for i in range(resolution):
        UTarrs[i,:] = UTdeps + fltTimes[i]
    timeTime = time.perf_counter() - t0TRange
    if round(timeTime, 5) == 0:
        print('Completed.')
    else:
        print(f'Completed in {timeTime:.5f} seconds.')
    
    # Generate r and v vectors for each UT
    print('Generating r and v vectors...')
    t0RV = time.perf_counter()
    
    # Multithread for speed
    with mp.Pool(numWorkers) as pool:
        results = []
        for i in range(resolution):
            results.append(pool.apply_async(getVectors, args=(i, depPlanet, UTdeps, arrPlanet, UTarrs, resolution)))

        rArrayDep = np.zeros((resolution, 3))
        vArrayDep = np.zeros((resolution, 3))
        rArrayArr = np.zeros((resolution, 3, resolution))
        vArrayArr = np.zeros((resolution, 3, resolution))

        for result in results:
            i, r_dep, v_dep, r_arr, v_arr = result.get()
            rArrayDep[i,:] = r_dep
            vArrayDep[i,:] = v_dep
            rArrayArr[i,:,:] = r_arr
            vArrayArr[i,:,:] = v_arr
    
    rvTime = time.perf_counter() - t0RV
    if round(rvTime, 5) == 0:
        print('Completed.')
    else:
        print(f'Completed in {rvTime:.5f} seconds.')
    
    # Solve Lambert's problem for each time to get delta V
    print('Computing delta Vs...')
    t0Lam = time.perf_counter()
    dV = np.zeros((resolution, resolution))
    
    # Multithread for speed
    with mp.Pool(numWorkers) as pool:
        results = pool.starmap(computeDV, [(index, rArrayDep, rArrayArr, fltTimes, mu, vArrayDep, vArrayArr) for index in np.ndindex((resolution, resolution))])

    for j, i, result in results:
        dV[j, i] = result

    LambertTime = time.perf_counter() - t0Lam   
    if round(LambertTime, 5) == 0:
        print('Completed.')
    else:
        print(f'Completed in {LambertTime:.5f} seconds.')

    # Create figure
    fig, ax = plt.subplots()
    depStart = (yStart - 1)*426 + (dStart - 1)
    depEnd = (yEnd - 1)*426 + (dEnd - 1)
    porkPlot = ax.imshow(np.flipud(dV), vmin=np.round(np.min(dV)), vmax=np.round(np.percentile(dV,95)), extent=[depStart, depEnd, fltTimeStart, fltTimeEnd], aspect='auto', cmap=porkmap.pmap)
    ax.set_xlabel('Departure Date (days from epoch)')
    ax.set_xticks(np.round(np.linspace(depStart, depEnd, 5)))
    ax.set_ylabel('Time of Flight (days)')
    ax.set_yticks(np.round(np.linspace(fltTimeStart, fltTimeEnd, 5)))
    ax.set_title(f'{depPlanetName} to {arrPlanetName} Delta V Transfer Plot')
    cbarTicks = np.round(np.linspace(np.min(dV), np.percentile(dV,95), 5)).astype(int)
    cbar = plt.colorbar(porkPlot, ticks=cbarTicks)
    cbar.set_ticklabels(cbarTicks)
    cbar.set_label('Delta V (m/s)')
    plt.show()