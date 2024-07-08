import os
import numpy as np
import datetime as date
import rssPorkchop as pork
import porkmap
import time
import astrodynamics as ast
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import multiprocessing as mp

def seconds2days(s):
    # Convert seconds to days
    return s / (60*60*24)

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
    # Plot porkchop (RSS Version)
    print('*--------------------------*')
    print('|   RSS Porkchop Plotter   |')
    print('*--------------------------*\n')

    # Get number of CPU threads
    numWorkers = os.cpu_count()
    
    depPlanet = pork.Earth
    depPlanetName = depPlanet.name
    arrPlanet = pork.Mars
    arrPlanetName = arrPlanet.name
    
    resolution = 300
    
    epoch = date.date(2020,1,1)
    
    # Date range
    TstartActual = date.date(2023,7,1)
    TendActual = date.date(2027,7,1)
    
    Tstart = (TstartActual - epoch).total_seconds()
    Tend = (TendActual - epoch).total_seconds()
    
    # Time of flight range in days
    fltTimeStart = date.timedelta(100).total_seconds()
    fltTimeEnd = date.timedelta(500).total_seconds()
    
    mu = depPlanet.orbit.refBody.gravParameter

    # Calculate time ranges
    print('Calculating time ranges...')
    t0TRange = time.perf_counter()
    ETdepRange = (Tstart, Tend)
    flightTimeRange = (fltTimeStart, fltTimeEnd)
    ETdeps = np.linspace(ETdepRange[0], ETdepRange[1], resolution)
    fltTimes = np.linspace(flightTimeRange[0], flightTimeRange[1], resolution)
    ETarrs = np.zeros((resolution,resolution))
    for i in range(resolution):
        ETarrs[i,:] = ETdeps + fltTimes[i]
    timeTime = time.perf_counter() - t0TRange
    if round(timeTime, 5) == 0:
        print('Completed.')
    else:
        print(f'Completed in {timeTime:.5f} seconds.')
    
    # Generate r and v vectors for each ET
    print('Generating r and v vectors...')
    t0RV = time.perf_counter()
    
    # Multithread for speed
    with mp.Pool(numWorkers) as pool:
        results = []
        for i in range(resolution):
            results.append(pool.apply_async(getVectors, args=(i, depPlanet, ETdeps, arrPlanet, ETarrs, resolution)))

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
    porkPlot = ax.imshow(np.flipud(dV), vmin=np.round(np.min(dV)), vmax=np.round(np.percentile(dV,50)), extent=[TstartActual, TendActual, seconds2days(fltTimeStart), seconds2days(fltTimeEnd)], aspect='auto', cmap=porkmap.pmap)
    ax.set_xlabel('Departure Date')
    dateFormat = mdates.DateFormatter('%b %Y')
    ax.xaxis.set_major_formatter(dateFormat)
    ax.tick_params(axis='x', rotation=60)
    ax.set_ylabel('Time of Flight (days)')
    ax.set_yticks(np.round(np.linspace(seconds2days(fltTimeStart), seconds2days(fltTimeEnd), 5)))
    ax.set_title(f'{depPlanetName} to {arrPlanetName} Delta V Transfer Plot')
    cbarTicks = np.round(np.linspace(np.min(dV), np.percentile(dV,50), 5)).astype(int)
    cbar = plt.colorbar(porkPlot, ticks=cbarTicks)
    cbar.set_ticklabels(cbarTicks)
    cbar.set_label('Delta V (m/s)')
    plt.show()