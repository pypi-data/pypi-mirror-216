# Orr-Sommerfeld-convmix-CGB Package
It is a python package developed in order to solve the Orr Sommerfeld equations. It is free for the community and allows to calculate disturbances for one flow of interest: Mixed convection in vertical rectangular channels like the following one: 

<p align="center">
  <img src="https://gitlab.com/mecom-cnea-os/orr-sommerfeld-convmix-cgb/-/raw/main/Examples/Canal.png" alt="Descripción de la imagen" width="300px">
</p>

[Link to channel description image on Gitlab repository](https://gitlab.com/mecom-cnea-os/orr-sommerfeld-convmix-cgb/-/raw/main/Examples/Canal.png)

The perturbations can be used to analyze the phenomenon of the laminar-turbulent transition. 

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Installation](#installation)
* [Examples](#examples)

## General info

Fluid systems are often described and characterized by their stability or receptivity behavior. Perturbations of infinitesimal amplitude that grow when superimposed on an equilibrium state of the flow render the base flow unstable.
The laminar-turbulent transition can have a significant impact on heat transfer, especially in mixed convection applications where temperature effects are manifested through buoyancy forces.

To understand the flow conditions that cause this transition mathematically and how it affects heat transfer, the linear stability theory can be used. This theory predicts when a laminar flow becomes turbulent by analyzing small disturbances and determining if they will grow or dissipate. If the disturbances grow, the laminar flow becomes unstable and transitions to turbulence. This package focuses on examining the temporal transition, using spatial variables as inputs.

## Technologies
Project is created with:
* [NumPy](https://numpy.org/)
* [SciPy](https://scipy.org/)
* [Plotly](https://plotly.com/)
* [Pandas](https://pandas.pydata.org/)
* [PyPi](https://pypi.org/) to publish Python package.

In the next figure, it is shown the flux diagram of the main function: Orr-Sommerfeld

<p align="center">
  <img src="https://gitlab.com/mecom-cnea-os/orr-sommerfeld-convmix-cgb/-/raw/main/Examples/Funciones.png" alt="Flux Diagram" width="300px">
</p>

[Link to flux diagram image on Gitlab repository](https://gitlab.com/mecom-cnea-os/orr-sommerfeld-convmix-cgb/-/raw/main/Examples/Funciones.png)


## Installation
It is possible to install using pip:
```Python
pip install Orr-Sommerfeld-convmix-CGB
```
## Examples
* Importing the package:
```Python3.9
from Orr_Sommerfeld_convmix_CGB import OS_CM
```
* The necessary inputs to compute the spectrum of temporal eigenvalues and their respective perturbations are:
```Python
N=100 #Number of nodes t
Ra=100 #Rayleigh number
Pr=0.71 #Prandtl number
Re=300 #Reynolds number
alpha=2.5 #perturbation wavelength in the x-direction
beta=0 #perturbation wavelength in the z-direction
```
* Can compute the spectrum of temporal eigenvalues (disturbances frecuency) and their respective eigenvectors, which are the amplitude of the disturbances. Also can obtain the real and imaginary parts of the eigenvalue which its imaginary part is the maximum:
```Python
[lam,V,max_real,max_imag]=OS_CM.Orr_Sommerfeld(N,Ra,Pr,Re,alpha,beta)
```
* The lam array is sorted from highest imaginary part to lowest imaginary part, and it contains all the eigenvalues. To obtain the eigenvectors corresponding to a given eigenvalue, you can do:
```Python
[v,u,w,tita]=OS_CM.vector_perturbaciones(N,lam,V,0,alpha,beta,Re,Ra)
```
* Where v, u and w are de amplitudes of the velocity disturbances and tita is the amplitude of the temperature disturbance. In this example, the eigenvalue choosen was the first one in lam. 
* There is also available a function to normalize the disturbances such that when the phase of v is zero, its norm is maximum and equal to 1:
```Python
[v,u,w,tita]=OS_CM.normalizacion(v,u,w,tita)
```
* Additionally, there is a function that plots the eigenvalues using the matplotlib library. The package also includes an interactive plot of the eigenvalues using pandas
```Python
OS_CM.grafica_autovalores(N,Ra,Pr,Re,alpha,beta)
```
The result is for example:

<p align="center">
  <img src="https://gitlab.com/mecom-cnea-os/orr-sommerfeld-convmix-cgb/-/raw/main/Examples/ejautovalores1.png" alt="Eigenvalues example" width="300px">
</p>

[Link to eigenvalues image on Gitlab repository](https://gitlab.com/mecom-cnea-os/orr-sommerfeld-convmix-cgb/-/raw/main/Examples/ejautovalores1.png)

<p align="center">
  <img src="https://gitlab.com/mecom-cnea-os/orr-sommerfeld-convmix-cgb/-/raw/main/Examples/ejemploautovalores.png" alt="Interactive eigenvalues plot example" width="600px">
</p>

[Video showing interactive plot](https://gitlab.com/mecom-cnea-os/orr-sommerfeld-convmix-cgb/-/raw/main/Examples/output_video.webm)
* Eigenvectors can also be plotted using the previously mentioned normalization:
```Python
OS_CM.grafica_autofunciones(N,Ra,Pr,Re,alpha,beta)
```

The result is something like this:

<p align="center">
  <img src="https://gitlab.com/mecom-cnea-os/orr-sommerfeld-convmix-cgb/-/raw/main/Examples/autofunciongod.png" alt="Eigenvectors plot example" width="300px">
</p>

[Link to eigenvectors image on Gitlab repository](https://gitlab.com/mecom-cnea-os/orr-sommerfeld-convmix-cgb/-/raw/main/Examples/autofunciongod.png)