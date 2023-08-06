'''' Useful funcs '''
import numpy as np


def cart2pol(x, y):
    ''' Converts karthesian to cylindrial '''
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def fit_uncertainty(pcov):
    return np.sqrt(np.diag(pcov))

def uncertainty(data, NB=0, variable=False, disp=True):
    '''' Funkce na výpočet nejistot '''
    if len(data) <= 1:
        raise TypeError("Data must have MORE elements than 1!")

    stud_koef =[0 ,6.3, 4.3, 3.18, 2.78, 2.57, 2.45, 2.37, 2.31, 2.26, 2.2, 2.14, 2.09, 2.04, 2.00, 1.98, 1.96]
    X = data

    n = len(X)

    if n <= 10:
        k = stud_koef[n-1]
    elif n <= 12:
        k = stud_koef[10]
    elif n <= 15:
        k = stud_koef[11]
    elif n <= 20:
        k = stud_koef[12]
    elif n <= 30:
        k = stud_koef[13]
    elif n <= 60:
        k = stud_koef[14]
    elif n <= 120:
        k = stud_koef[15]
    else:
        k = stud_koef[16]


    xs = 1/n*sum(X) # střední hodnota
    sumx = 0

    for x in X:
        sumx = sumx + (x-xs)**2 # suma (xi - xs)**2


    sigma = np.sqrt( 1/(n*(n-1)) * sumx) # výpočet sigmy
    NA = k * sigma # Nejistota typu A
    N = np.sqrt(NA**2 + NB**2) # Výpočet nejistoty

    if disp == True:
        print(f"x = ({xs} $\pm$ {N})")
    if variable == True:
        return (xs,N)


    ### Tvorba Grafu #####
    # xsv = zeros(1,n)+xs
    # max = zeros(1,n)+xs+N
    # min = zeros(1,n)+xs-N

    # plot(x,"b-")
    # plot(xsv,"r-")
    # plot(max,"g-")
    # plot(min,"g-")
    #####################

def GetMinIndex(inputlist):
    '''get index of the minimum value in the list'''
    min_value = min(inputlist)

    # return the index of minimum value

    min_index = []

    for i in range(0, len(inputlist)):

        if min_value == inputlist[i]:
            min_index.append(i)

    return min_index

def log_b(a,b):
    ''' logaritm from a of base b'''
    return np.log(a)/np.log(b)
