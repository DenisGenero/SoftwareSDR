import serial
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import Funciones
from time import time

# Configuración del puerto serie
serial.PARITY_NONE
serial.EIGHTBITS
serial.STOPBITS_ONE
ser = serial.Serial('/dev/rfcomm3', 9600, timeout=.1)
ser.flush()

# Arreglos para trabajar
# Alojamiento para los datos que van ingresando
# por el puerto serie
senial=[]
# Alojamiento para los datos que se van obteniendo
# como resultado del filtrado
filtrada=[]
# Alojamiento para los datos que se van promediando
promediada=[]
# Alojamiento de los tiempos donde se detecta una
# transcicion entre inspiración y expiración, y
# viceversa
tiempo=[]
# Alojamiento de los tiempos de occurencia de las
# trancisiones entre inspiracion y espiraciones
evento=[]
# Amplitudes para graficar las detecciones
Amp_evento=[]
# Latencia promedio de procesamiento:
# abarca desde la adquisición de los datos hasta el
# fin de su filtrado y procesamiento
latencia=[]

# Valor para sincronizar la adquisición de datos
s = 115

# Frecuencia de muestreo
fs = 100
# Tiempo de muestreo
ts = 1 / fs
# Indice para almacenar los datos
i = 0
# Valor resultado del proceso de adquisición
valor = 0
# Variables auxiliares para el proceso de adquisición
num = 0
aux = 0

#Coeficientes de filtrado de pyFDA
b = [0.006136, 0.006136]
a = [1, 0.9877]

# Sincronización del puerto serie:
dato = int.from_bytes(ser.read(1),"little")
while dato != s:
    dato = int.from_bytes(ser.read(1),"little")

# Segundo que dura el estudio
segundos = 15
frec_muestreo = 100; # En Hz

# Algoritmo de adquisición y procesamiento
while i < segundos*frec_muestreo:
    dato = int.from_bytes(ser.read(1),"little")
    if dato == s:
        t_start = time()
        valor = num
        #reset de variable
        num = 0
        num = int.from_bytes(ser.read(1),"little") - 48
        
    else:
        aux = dato - 48
        num = num*10 + aux        
    if valor != 0:
        # Se ignoran valores fuera de rango (10 bits)
        if (valor > 0) & (valor < 1024):
            # Procesamiento en tiempo real
            senial.append(valor)
            valor = 0
            # Filtrado pasa bajos
            filtrada.append(Funciones.RealTimefilter(b, a, senial, filtrada, i))
            # Promediación con una ventana de 20 muestras
            promediada.append(Funciones.RealTimeAverage(filtrada, 20))
            if(i>1):
                # Detección de proceso: inspiración o espiración
                pend_anterior = promediada[i-1]-promediada[i-2]
                pend_actual = promediada[i]-promediada[i-1]
                if pend_actual<0:
                    estado = "espiracion"
                else:
                    estado = "inspiracion"
                if pend_anterior*pend_actual<0:
                    evento.append(i/100)
                    if estado == "inspiracion":
                        Amp_evento.append(promediada[i])
                        # Almacenamiento para determinar la frecuencia respiratoria
                        tiempo.append(i*ts)
                        #if (len(tiempo)>2):
                            # Determinación de la frecuencia respiratoria
                            #temp= tiempo [len(tiempo)-1] - tiempo[len(tiempo)-3]
                            #print("frecuencia respiratoria:")
                            #print(1/temp*60, "respiraciones por minuto")
                    else:
                        Amp_evento.append(promediada[i])
                    print(estado)
            # Se corre indice para la siguiente muestra
            t_end = time()
            temp_lat = (t_end - t_start)*1000
            latencia.append(temp_lat)
            i = i + 1                

# Frecuencia respiratoria promedio:
# Se considera la diferencia entre los tiempos
# de ocurrencia de dos inspiraciónes o espiraciones
temp = 0
for j in range(2,len(tiempo),1):
    temp = temp + tiempo [j] - tiempo[j-2]

temp_prom = temp/int((len(tiempo)/2))

frec = int(60/temp_prom)
print("La frecuencia respiratoria promdio es de:")
print(frec, "respiraciones por minuto")

# Latencia del procesamiento
lat_prom = np.mean(latencia)
print("La latencia promedio del sistema es:")
print(lat_prom, "mseg")

# Vectores para graficar
N = len(senial)                   # número de muestras en el archivo de audio
t = np.linspace(0, N*ts, N)   # vector de tiempo
f, fft_senial = funciones_fft.fft_mag(promediada, fs)

# Se reacomoda el vector de pyFDA para su correcta
# representación
a = [1, -0.9877]
# Respuesta en frecuencia del filtro implementado
f_Micro1, h_Micro1 = signal.freqz(b, a, worN=f, fs=fs)

# Grafica de los datos obtenidos, procesados, y de la respuesta del filtro
fig, ax0 = plt.subplots(3, 1, figsize=(15, 15), sharex=True)
ax0[0].plot(t, senial/np.max(senial), label='Señal Sucia', color='green')
ax0[0].legend(loc="upper right", fontsize=8)
ax0[0].set_xlabel("Tiempo [Seg]")
ax0[0].set_xlim(0,segundos)
ax0[1].plot(t,promediada/np.max(promediada), label='Señal Filrada', color='blue')
ax0[1].plot(evento, Amp_evento/np.max(Amp_evento), 'ro', label='Detección de eventos', color='red')
ax0[1].legend(loc="upper right", fontsize=8)
ax0[0].set_xlabel("Tiempo [Seg]")
ax0[1].set_xlim(0,segundos)
ax0[2].plot(f_Micro1, abs(h_Micro1)/np.max(abs(h_Micro1)), label='Filtro normalizado', color='purple')
ax0[2].set_xlim(0,fs/6)
ax0[2].legend(loc="upper right", fontsize=8)
ax0[2].set_xlabel("Frecuencia [Hz]")
plt.show()

ser.close()