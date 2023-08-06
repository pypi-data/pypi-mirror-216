import pandas as pd
from plotly.offline import iplot
import plotly.graph_objs as go
import seaborn as sns
import cufflinks as cf
import math
import numpy as np
import scipy as sy
import matplotlib
import matplotlib.pyplot as plt
#%matplotlib inline
from pylab import *
from numpy import *
from timeit import default_timer
plt.rcParams['text.usetex'] = True
#import matplotlib as mpl
#mpl.rcParams.update(mpl.rcParamsDefault)
#cf.go_offline()
def cheb(N):
    if N==0: 
        D = 0.; x = 1.
    else:
        n=arange(0,N+1) #genero un vector que va desde 0 hasta N+1 con paso 1
        #Tomo el array n y lo convierto en una matriz de N+1 filas (cada fila le aplica el coseno)y 1 columna
        x = cos(pi*n/N).reshape(N+1,1)
        #hstack concatena 3 arrays: [2.] con ones(N-1) con [2.]. Y luego los afecta por (-1)**n. Como resultado
        #obtengo un array de N+1, al cual luego le hago reshape para hecerlo columna
        c = (hstack(( [2.], ones(N-1), [2.]))*(-1)**n).reshape(N+1,1)
        #Genero una matríz con tile(). En este caso toma al vector x y lo convierte en una matriz de 1 fila y N+1 columnas
        #Pero cada elemento de la matriz nueva es el vector x. Entonces el vector columna x (de N+1 filas) 
        #se replica N+1 veces, dando como resultado una matriz cuadrada de N+1xN+1
        X = tile(x,(1,N+1)) 
        #Defino dX como la resta de X y su transpuesta
        dX = X - X.T
        # c*(1./c).T Crea los coeficientes de atras de cada elemento de D
        D=(c*(1./c).T)/(dX+eye(N+1))
        #Resto D menos una matriz donde cada elemento de la diagonal contiene la suma de los elementos de la
        #columna de D.T correspondiente
        D=D-diag(sum(D.T,axis=0)) 
        #retorno tanto D como el vector que tiene los puntos de Chebyshev, como un vector fila
    return D, x.reshape(N+1)
def Dmat(N):
    #Acá hago lo que hice en el Program 38 para dejar listas las matrices de diferenciación 
    #y poder resolver el problema
    [D,y]=cheb(N);
    y2=y*y
    D2=dot(D,D)
    S=diag(hstack(([0.],1/(1-y2[1:-1]),[0.])))
    D4=dot((dot(diag(1-y2),dot(D2,D2))-8*dot(diag(y),dot(D,D2))-12*D2),S)
    D=D[1:-1,1:-1] 
    D2=D2[1:-1,1:-1] 
    D4=D4[1:-1,1:-1] 
    return D,D2,D4
def grafica_desarrollado(Ra):
    y=arange(-1,1,0.01)
    y2=y*y
    y4=y2*y2
    A=1.5
    k=Ra**0.25/sqrt(2)
    E=-2*k*sqrt(Ra)*(cosh(2*k)+cos(2*k))/(sinh(2*k)-sin(2*k))
    m=(-Ra)**0.25
    F=(2*(m)**3)/(tanh(m)-tan(m))
    if Ra==0:
        Ubase=-A*(y2-1)
        titabase=-A*(y4/12-y2/2+(5/12)) 
    else:
        if Ra>0:
            Ubase=-E/sqrt(Ra)*(sinh(k*(1+y))*sin(k*(1-y))+sinh(k*(1-y))*sin(k*(1+y)))/(cosh(2*k)+cos(2*k))
            titabase=E/Ra*(1-(((cosh(k*(1+y))*cos(k*(1-y)))+(cosh(k*(1-y))*cos(k*(1+y))))/(cosh(2*k)+cos(2*k))))
        else:
            Ubase=F/(2*(m)**2)*((cosh(m*y)/cosh(m))-(cos(m*y)/cos(m)))
            titabase=F/(2*(m)**4)*((cosh(m*y)/cosh(m))+(cos(m*y)/cos(m))-2)
    plt.style.use('ggplot')

    plt.plot(y, Ubase, "-", label=r'$U_{base}$')
    plt.plot(y, titabase, "-", label=r'$ \theta_{base}$')



    plt.legend(bbox_to_anchor=(1.33, 0.75, 0, 0), loc="lower right", fontsize=18,edgecolor='gray')

    label_text = r'$Ra = {:.2f}$'
    label_text = label_text.format(Ra)
    plt.text(1.17, 0.8, label_text, ha='left', va='center', fontsize=14, bbox=dict(facecolor=(0.9,0.9,0.9), edgecolor='gray', boxstyle='round'))


    plt.xlabel(r'$y$', fontsize=18)
    plt.title('Perfil base de velocidades',fontsize=18)
    plt.savefig("flujobase.png")
    plt.show()
        
    return 
def flujobase(N,Ra):
    D,y = cheb(N)
    y2=y*y
    D2=dot(D,D)
    
    if Ra==0:
        A=1.5
        U=-A*(y2-1)
    else:
        if Ra>0: 
            k=Ra**0.25/sqrt(2)
            E=-2*k*sqrt(Ra)*(cosh(2*k)+cos(2*k))/(sinh(2*k)-sin(2*k))
            U=-E/sqrt(Ra)*(sinh(k*(1+y))*sin(k*(1-y))+sinh(k*(1-y))*sin(k*(1+y)))/(cosh(2*k)+cos(2*k))
        else:
            m=(-Ra)**0.25
            F=(2*(m)**3)/(tanh(m)-tan(m))
            U=F/(2*(m)**2)*((cosh(m*y)/cosh(m))-(cos(m*y)/cos(m)))
    #Convierto el vector fila que me devuelva cheb en uno columna para luego multiplicar por D
    U=U.reshape(N+1,1)
    y=y.reshape(N+1,1)
    #Hago ya esto para luego resolver por autovalores
    U1=dot(D,U)
    U2=dot(D2,U)
    U=U[1:-1]; U1=U1[1:-1] ;U2=U2[1:-1];
    return U,U1,U2
def titabase(N,Ra):
    D,y = cheb(N)
    y2=y*y
    y4=y2*y2
    D2=dot(D,D)
    
    if Ra==0:
        A=1.5
        tita=-A*(y4/12-y2/2+(5/12)) 
    else:
        if Ra>0:
            k=Ra**0.25/sqrt(2)
            E=-2*k*sqrt(Ra)*(cosh(2*k)+cos(2*k))/(sinh(2*k)-sin(2*k))
            tita=E/Ra*(1-(cosh(k*(1+y))*cos(k*(1-y))+cosh(k*(1-y))*cos(k*(1+y))))/(cosh(2*k)+cos(2*k))
        else:
            m=(-Ra)**0.25
            F=(2*(m)**3)/(tanh(m)-tan(m))
            tita=F/(2*(m)**4)*((cosh(m*y)/cosh(m))+(cos(m*y)/cos(m))-2)
    #Convierto el vector fila que me devuelva cheb en uno columna para luego multiplicar por D
    tita=tita.reshape(N+1,1)
    y=y.reshape(N+1,1)
    #Hago ya esto para luego resolver por autovalores
    tita1=dot(D,tita)
    tita=tita[1:-1]; tita1=tita1[1:-1]
    return tita, tita1
def Orr_Sommerfeld(N,Ra,Pr,Re,alpha,beta) :
   

    D,D2,D4=Dmat(N)
    #Chekeado que Dmat funciona bien
    U,U1,U2=flujobase(N,Ra)    
    #U,U1,U2=Poiseuille(N)
    tita,tita1=titabase(N,Ra)
    #Checkeado que flujobase() anda bien
    
    #Calculo parámetros de mis ecuaciones
    I=eye(N-1)
    k2=(alpha*alpha)+(beta*beta)
    k22=k2*k2
    
    #--------------------------------------------------------------------------
    if Ra==0:
        H = -(D4-2.*k2*D2+k2*k2*I)/(Re) - 1j*alpha*U2*I + 1j*alpha*dot(U*I,D2)-1j*alpha*k2*U*I 
        P = 1j*alpha*(D2-k2*I)
    else:
        #Para v
        d= - 1j*alpha*dot((U*I),D2) + 1j*alpha*k2*U*I + 1j*alpha*U2*I + (D4-(2.*k2*D2)+(k22*I))/(Re)
        e= - (1j*alpha*Ra*D)/(Re)
        f= - 1j*alpha*(D2-(k2*I))
        #Para tita
        a= - (D2-(k2*I))/(Re*Pr) + 1j*alpha*(U*I)
        b= tita1*I + (1j*alpha*D/(Re*Pr*k2))
        c= (beta*I)/(Re*Pr*k2)
        #Para eta
        n= - (D2-(k2*I))/(Re) + (1j*alpha*U*I)
        g= beta*U1*I
        m= -beta*Ra*I/(Re)
        ceros=zeros((N-1,N-1))

        #---------------------------------------------------------------------------

        H1=concatenate((d,e,ceros), axis=1)
        H2=concatenate((b,a,c), axis=1)
        H3=concatenate((g,m,n), axis=1)   
        H=concatenate((H1,H2,H3), axis=0)

        P1=concatenate((f,ceros,ceros), axis=1)
        P2=concatenate((ceros,(1j*alpha*I),ceros), axis=1)
        P3=concatenate((ceros,ceros,(1j*alpha*I)), axis=1)
        P=concatenate((P1,P2,P3), axis=0)

    #--------------------------------------------------------------------------
    
    S=dot(inv(P),H)
    
    #Creo vector de autovalores y vector de autovectores
    lam, V = eig(S)
    
    ii = argsort(-lam.imag) 
    lam = lam[ii]
    V = V[:,ii]
    
    imaginaria=lam.imag
    max_imag=imaginaria[0]
    real=lam.real
    max_real=real[0]

    return lam,V,max_real,max_imag
def grafica_autovalores(N,Ra,Pr,Re,alpha,beta):
    lam,V,max_real,max_imag=Orr_Sommerfeld(N,Ra,Pr,Re,alpha,beta)
    imaginaria=lam.imag
    real=lam.real
    #Grafico comun
    #plt.style.use('ggplot')

    plt.ylim(-2,0.2)
    plt.xlim(0.1,1.5)
    plt.grid(color='lightgray')
    plt.axhline(y=0, color='limegreen', linewidth=1.5, linestyle='-')
    plt.scatter(real, imaginaria, marker='o', c='red' , s=9)

    label_text = r'$Re= {:.2f}$' + "\n" + r'$Ra = {:.2f}$' + "\n" + r'$ Pr = {:.2f}$' + "\n" + r'$ \alpha = {:.3f}$' + "\n" + r'$ \beta= {:.2f}$'
    label_text = label_text.format(Re, Ra, Pr, alpha, beta)
    plt.text(0.2, -1.5, label_text, ha='left', va='center', fontsize=14, bbox=dict(facecolor='white', edgecolor='lightgray', boxstyle='round'))
    plt.text(max_real, max_imag+0.03, r'$(%0.5f,\,%0.5f)$' % (max_real, max_imag), ha='center', va='bottom', fontsize=10)
    plt.scatter(max_real, max_imag, c='orange', s=9)

    plt.xlabel(r'$c_r$', fontsize=18)
    plt.ylabel(r'$c_i$', fontsize=18)
    plt.title('Gráfico de autovalores', fontsize=18)
    

    plt.savefig("Autovalores.png")
    plt.show()

    #-------------------------------------
    #Para hacer grafico interactivo, para que funcione descomentar bibliotecas arriba del todo

    df = pd.DataFrame({
        'real': real,
        'imaginaria': imaginaria})

    colores = ['orange'] + ['red']*(len(df)-1)
    traza = go.Scatter(x=df['real'], y=df['imaginaria'], mode='markers', marker=dict(color=colores, size=5))
    titulo = r"Gráfico interactivo de autovalores para $Re={}, Ra={}, \alpha={}, \beta={}$".format(Re, Ra, alpha, beta)

    layout = go.Layout(title=dict(text=titulo), xaxis=dict(title='r$c_{r}$',titlefont=dict(size=18), tickfont=dict(family='latex')), 
                                                                   yaxis=dict(title=r'$c_{i}$',titlefont=dict(size=18), tickfont=dict(family='latex')),
                                                                   plot_bgcolor='rgba(0,0,0,0.1)',
                                                                   title_x=0.5)
    fig = go.Figure(data=[traza], layout=layout)
    iplot(fig)
    return
def vector_perturbaciones(N,lam,V,n,alpha,beta,Re,Ra):
    D,D2,D4=Dmat(N)
    #Chekeado que Dmat funciona bien
    U,U1,U2=flujobase(N,Ra)
    #Calculo parámetros de mis ecuaciones
    I=eye(N-1)
    k2=(alpha*alpha)+(beta*beta)
    k22=k2*k2
   
    v=V[0:(N-1),n]
    if Ra==0:
        tita=zeros(N-1)
        eta=dot((-(D4-2.*k2*D2+k2*k2*I)/(Re) + 1j*alpha*U*I - 1j*alpha*lam[n]*I),-1j*beta*dot(U1*I,v))
        #Expresión de u
        u= (1j*alpha*dot(D,v)/k2) + dot(beta/k2,(eta/1j))
        #Expresión de w
        w=((beta*u)-(eta/1j))/alpha
    else:
        tita=V[(N-1):(2*(N-1)),n]
        eta=V[2*(N-1):3*(N-1),n]
        #Expresión de u
        u= (1j*alpha*dot(D,v)/k2) + dot(beta/k2,eta)
        #Expresión de w
        w=((beta*u)-eta)/alpha
    # Falta agregar la presion 
    return  v,u,w,tita
def normalizacion(v,u,w,tita):
    if any(v):
	    vr=v.real
	    vi=v.imag
	    #Busca el valor de màxima norma de u
	    norm= vr*vr+vi*vi
	    i=np.where(abs(norm) == np.max(norm))
	    #Para ese valor máximo, multiplico por un complejo c=a+bj/su fase sea cero y su norma sea 1
	    a=vr[i]/norm[i]
	    b=-vi[i]/norm[i]
	    #a=vi[i]/sqrt(norm[i])
	    #b=-v[i]**2/(vr[i]*sqrt(norm[i]))
	    c= a + (1j*b)   
	    #Luego normalizo todas las autofunciones con el c hallado
	    v=c*v
	    u=c*u
	    w=c*w
	    tita=c*tita
    v= (hstack(( [0.],v , [0.])))
    u= (hstack(( [0.],u , [0.])))
    w= (hstack(( [0.],w , [0.])))
    tita= (hstack(( [0.],tita , [0.])))
    return v,u,w,tita  
def grafica_autofunciones(N,Ra,Pr,Re,alpha,beta):
    #plt.style.use('ggplot')
    #Vector y
    D,y = cheb(N)
    #Vectores de perturbaciones para un autovalor dado. En este caso tomo el mayor de todos dado que Orr_Sommerfeld() las ordena y voy a elegir n=0
    n=0
    lam,V,max_real,max_imag=Orr_Sommerfeld(N,Ra,Pr,Re,alpha,beta)

    v,u,w,tita=vector_perturbaciones(N,lam,V,n,alpha,beta,Re,Ra)
    v,u,w,tita=normalizacion(v,u,w,tita)

    realv = v.real
    imv = v.imag
    realtita = tita.real
    imtita = tita.imag
    realu = u.real
    imu = u.imag 
    realw = w.real 
    imw = w.imag

    plt.plot(y,realv,c='red',label= "$v_r(y)$")
    plt.plot(y,imv,"--",c='red',label= "$v_i(y)$")
    plt.plot(y,realtita,"-",c='blue',label= r'$\theta_{r}(y)$')
    plt.plot(y,imtita,"--",c='blue',label= r'$\theta_{i}(y)$')
    plt.plot(y,realu,c='lightgreen',label= r'$u_{r}(y)$')
    plt.plot(y,imu,"--",c='lightgreen',label= r'$u_{i}(y)$')
    #plt.plot(y,realw,c='pink',label= r'$w_{r}(y)$')
    #plt.plot(y,imw,"--",c='pink',label= r'$w_{i}(y)$')


    plt.xlim(-1,1)
    #plt.ylim(-41,45)

    plt.xlabel(r'$y^{*}$', fontsize=18)
    title('Perfil de las perturbaciones',  fontsize=18)
    plt.legend()
    plt.grid(color='lightgray')
    plt.savefig('ejemploautofunc1.png')
    plt.show()
    return
