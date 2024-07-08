# Porkchop Plotter

A (slow) CLI implementation of a porkchop plotter in Python.

## Requirements

- NumPy
- Matplotlib
- astrodynamics (can be found here: <https://github.com/ajlatzko/astrodynamics>)

## Usage

### KSP System

In ```mainKSP.py```, the variables ```depPlanet``` and ```arrPlanet``` represent the departure planet and arrival planet, respectively. Change them to your desired planets like so:

```python
depPlanet = pork.Kerbin
arrPlanet = pork.Duna
```

or

```python
depPlanet = pork.Moho
arrPlanet = pork.Jool
```

The ```resolution``` variable determines the resolution of the output plot. Large values and lead to very slow performance (a resolution of 300 takes about 4 seconds to compute on a Ryzen 7 5800X).

To change the date range of the plot, change the following variables, where y represents the year (minimum of 1) and d represents the day (between 1 and 426):

```python
yStart = 1
dStart = 1
yEnd = 3
dEnd = 1
```

To change the time of flight range, change the following variables (note that these are in days):

```python
fltTimeStart = 151
fltTimeEnd = 453
```

### RSS System

In ```mainRSS.py```, the variables ```depPlanet``` and ```arrPlanet``` represent the departure planet and arrival planet, respectively. Change them to your desired planets like so:

```python
depPlanet = pork.Earth
arrPlanet = pork.Mars
```

or

```python
depPlanet = pork.Venus
arrPlanet = pork.Jupiter
```

The ```resolution``` variable has the same usage as the KSP version.

To change the date range of the plot, change the following variables, where the format is (yyyy,m,d):

```python
TstartActual = date.date(2023,7,1)
TendActual = date.date(2027,7,1)
```

or

```python
TstartActual = date.date(2025,3,26)
TendActual = date.date(2030,12,11)
```

To change the time of flight range, change the numbers in following lines (note that these are in days):

```python
fltTimeStart = date.timedelta(100).total_seconds()
fltTimeEnd = date.timedelta(500).total_seconds()
```
