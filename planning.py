# -*- coding: cp1252 -*-
import os,string
from math import *
import math
from StringIO import *
from glob import *
from string import *
from time import *


# Esta funcion agrega los literales negados que no aparecen en el estado inicial, para asi formar el mundo cerrado. 
def crearNivel0(predicados, estado_inicial):

    nivel0 = []
    for p in predicados:
        if (estado_inicial.count(p) > 0) :
            nivel0.append(p)
        else:
            nivel0.append('-'+p)
            
    return nivel0           


# Esta funcion comprueba que  todas las precondiciones de la accion esten en el nivel anterior. 
def comprobarPrecondiciones(precondiciones, literalesNivelAnterior):

    booleanos = []
    
    for p in precondiciones:
        if(literalesNivelAnterior.count(p)>0): 
            booleanos.append('True')
        else:
            booleanos.append('False')
                
    if (booleanos.count('False')>0):
        salida = False
    else:
        salida = True
    return salida

# Esta funcion comprueba que  todas las precondiciones de la accion esten en el nivel anterior. 
def noExcluyentes(precondiciones,enlacesMutexLiteralesAnterior):

    booleanos = []

    i = 0
    while (i < len(precondiciones)):
        j = i+1
        precondicion1 = precondiciones[i]
        while (j < len(precondiciones)):
            precondicion2 = precondiciones[j]
            if(precondicion1 != precondicion2):
                if((enlacesMutexLiteralesAnterior.count([precondicion1,precondicion2])==0) and (enlacesMutexLiteralesAnterior.count([precondicion2,precondicion1])==0)):
                    booleanos.append('True')
                else:
                    booleanos.append('False')
                
            j = j+1
        i = i+1
                
    if (booleanos.count('False')>0):
        salida = False
    else:
        salida = True
        
    return salida

# Esta funcion agrega las acciones cuyas precondiciones estan en el nivel anterior, mas las acciones de persistencias. 
def crearNivelAcciones(acciones, literalesNivelAnterior,enlacesMutexLiteralesAnterior ):

    accionesNuevas = []

    for a in acciones:
        precondiciones = a[1]
        if precondiciones == []:
            accionesNuevas.append(a)
        elif((comprobarPrecondiciones(precondiciones, literalesNivelAnterior)) and (noExcluyentes(precondiciones,enlacesMutexLiteralesAnterior))):
            accionesNuevas.append(a)
            
    # Agregamos las acciones de persistencia, cuyo nombre va a ser igual al nombre del literal. 
    for l in literalesNivelAnterior:
        accionesNuevas.append([l, [l], [l]])

        
    return accionesNuevas






#Esta funcion muestra los arcos que van desde los literales del nivel 0 a las acciones del nivel 1
def crearEnlacesLiteralesAcciones(nivelAcciones):

    arcos = []

    for a in nivelAcciones:
        precondiciones = a[1]
        for p in precondiciones:
            arco = [p,a[0]]
            arcos.append(arco)
            
    return arcos





#Esta funcion crea los arcos que van desde las acciones del nivel 1 a los literales del nivel 1
def crearEnlacesAccionesLiterales(nivelAcciones):

    arcos = []

    for a in nivelAcciones:
        efectos = a[2]
        for e in efectos:
            arco = [a[0],e]
            arcos.append(arco)
            
    return arcos





# Utilizada en el punto 4. En el mismo nivel, se añaden los literales que podrían ser ciertos ya que son efectos de las acciones de ese nivel. Además, todo literal que aparezca en el nivel anterior, aparecerá también en el nivel siguiente.  
def crearNivelLiterales(nivelAcciones):

    
    literales = []
    
    for a in nivelAcciones:
        efectos = a[2]
        for e in efectos:
            if(literales.count(e) == 0):
                literales.append(e)
            
    return literales







# Utilizada en la funcion crearEnlacesMutexAcciones. Un efecto de una acción niega una precondición de la otra.
def consecuencias(nivelAcciones):
    
    enlaces_mutex = []

    # Comprobar que las precondiciones de cada accion no estan en los efectos de las otras acciones con valor opuesto.
    i = 0
    while (i < len(nivelAcciones)):
        accion = nivelAcciones[i]
        precondiciones = accion[1]
        j = 0
        while(j  < len(nivelAcciones)):
            accion2 = nivelAcciones[j]
            if accion2 != accion:
                efectos2 = accion2[2]
                for p in precondiciones:
                    if p.count("-")>0:
                        pnew = p.replace("-", '')
                        for e in efectos2:
                            if(e.count("-")==0):
                                if e == pnew:
                                    if((enlaces_mutex.count([accion[0],accion2[0]]) == 0) and (enlaces_mutex.count([accion2[0],accion[0]]) == 0)):
                                        enlaces_mutex.append([accion[0],accion2[0]])
                                
                    else:
                        if efectos2.count("-"+p) > 0:
                            if((enlaces_mutex.count([accion[0],accion2[0]]) == 0) and (enlaces_mutex.count([accion2[0],accion[0]]) == 0)):
                                enlaces_mutex.append([accion[0],accion2[0]])
                    
                    
            j = j+1
        i = i+1


    return enlaces_mutex

	
#  Utilizada en la funcion crearEnlacesMutexAcciones. Un efecto de una es la negación de un efecto de otra.
def inconsistencia(nivelAcciones):

    enlaces_mutex = []


    i = 0
    while (i < len(nivelAcciones)):
        accion = nivelAcciones[i]
        efectos = accion[2]
        j = i+1
        while(j  < len(nivelAcciones)):
            accion2 = nivelAcciones[j]
           
            if accion2 != accion:
                efectos2 = accion2[2]
                for p in efectos:
                    if p.count("-")>0:
                        pnew = p.replace("-", '')
                        
                        for e in efectos2:
                            if(e.count("-")==0):
                                if e == pnew:
                                    if((enlaces_mutex.count([accion[0],accion2[0]]) == 0) and (enlaces_mutex.count([accion2[0],accion[0]]) == 0)):
                                        enlaces_mutex.append([accion[0],accion2[0]])
                                
                    else:
                        if efectos2.count("-"+p) > 0:
                            if((enlaces_mutex.count([accion[0],accion2[0]]) == 0) and (enlaces_mutex.count([accion2[0],accion[0]]) == 0)):
                                enlaces_mutex.append([accion[0],accion2[0]])
                    
                    
            j = j+1
        i = i+1


    return enlaces_mutex

# Utilizada en la funcion crearEnlacesMutexAcciones. Las acciones tienen precondiciones que se excluyen mutuamente.	
def necesidadesCompiten(nivelAcciones, enlacesMutexLiteralesAnterior):
	
    enlaces_mutex = []
	
    i = 0
    while (i < len(nivelAcciones)):
        accion = nivelAcciones[i]
        precondiciones = accion[1]
        j = i+1
        while(j  < len(nivelAcciones)):
            accion2 = nivelAcciones[j]
            if accion2 != accion:
                precondiciones2 = accion2[1]
		for p1 in precondiciones:
                    for p2 in precondiciones2:
                        if ((enlacesMutexLiteralesAnterior.count([p1,p2]) > 0) or (enlacesMutexLiteralesAnterior.count([p2,p1]) > 0)):
                            if((enlaces_mutex.count([accion[0],accion2[0]]) == 0) and (enlaces_mutex.count([accion2[0],accion[0]]) == 0)):
                                enlaces_mutex.append([accion[0],accion2[0]])
            j = j+1
        i = i+1
	
    return enlaces_mutex

	
	
	
# Utilizada en la funcion crearEnlacesMutexLiterales. Un literal  es la negación del otro.	
def soporteInconsistencia(nivelLiterales):

    enlaces_mutex = []
    
    i = 0
    while (i < len(nivelLiterales)):
        literal = nivelLiterales[i]

        j = i + 1
        while(j  < len(nivelLiterales)):
            literal2 = nivelLiterales[j]
            if literal != literal2:
                if literal.count("-")>0:
                        literalnew = literal.replace("-", '')
                        if(literal2.count("-")==0):
                            if literalnew == literal2:
                                enlaces_mutex.append([literal,literal2])
                else:
                    if literal2.count("-"+literal) > 0:
                        enlaces_mutex.append([literal,literal2])
                    
            j = j+1
        i = i+1
        
    return enlaces_mutex

	
# Utilizada en la funcion crearEnlacesMutexLiterales. Todo par de acciones que los producen son mutuamente excluyentes.
def efectosExcluyentes(nivelLiterales, enlacesMutexAcciones, arcosAccionesLiterales):

    literalesExcluyentes = []
    
    i = 0
    while (i < len(nivelLiterales)):
        literal = nivelLiterales[i]
        j = i + 1
        while(j  < len(nivelLiterales)):
            literal2 = nivelLiterales[j]
            acciones1 = []
            acciones2 = []
            
            if literal != literal2:
                for a in arcosAccionesLiterales:
                    if a[1] == literal:
                        acciones1.append(a[0])
                    if(a[1] == literal2):
                        acciones2.append(a[0])

            booleanos = []
            for a1 in acciones1:
                for a2 in acciones2:
                    if((enlacesMutexAcciones.count([a1,a2]) > 0 ) or (enlacesMutexAcciones.count([a2,a1]) > 0 )):
                        booleanos.append('True')
                    else:
                        booleanos.append('False')
            if booleanos.count('False')==0:
                literalesExcluyentes.append([literal, literal2])
                
            j = j+1
        i = i+1

                
    return literalesExcluyentes                   



    
# Esta Funcion define los enlaces mutex entre las acciones del nivel 1
def crearEnlacesMutexAcciones(nivelAcciones, enlacesMutexLiteralesAnterior):
    
    enlacesMutexInterferencia = consecuencias(nivelAcciones) # return enlaces_mutex

    enlacesMutex = enlacesMutexInterferencia

    enlacesMutexInconsistencia = inconsistencia(nivelAcciones) # return enlaces_mutex

    for e in enlacesMutexInconsistencia:
        if ((enlacesMutex.count([e[0],e[1]])==0) and (enlacesMutex.count([e[1],e[0]])==0)):
            enlacesMutex.append(e)

            
    enlacesMutexNecesidadesCompiten = necesidadesCompiten(nivelAcciones, enlacesMutexLiteralesAnterior) # return enlaces_mutex
    
    for e in enlacesMutexNecesidadesCompiten:
        if ((enlacesMutex.count([e[0],e[1]])==0) and (enlacesMutex.count([e[1],e[0]])==0)):
            enlacesMutex.append(e)
            
	

    return enlacesMutex
    


        
		
#Definimos los enlaces mutex entre los literales del nivel 1
def crearEnlacesMutexLiterales(nivelLiterales, enlacesMutexAcciones, arcosAccionesLiterales):
    
    enlacesMutexInconsistencia = soporteInconsistencia(nivelLiterales)

    enlacesMutex = enlacesMutexInconsistencia

    enlacesMutexExcluyentes = efectosExcluyentes(nivelLiterales, enlacesMutexAcciones, arcosAccionesLiterales )
 
    for e in enlacesMutexExcluyentes:
        if ((enlacesMutex.count([e[0],e[1]])==0) and (enlacesMutex.count([e[1],e[0]])==0)):
            enlacesMutex.append(e)


    return enlacesMutex
    




    
def planificacion():

    fichero_salida = open("Ejemplos" + '.txt','a')
    

 
    # 1. Inicialización del problema

    
    predicados = ['MANOSLIMPIAS', 'CENA', 'REGALO', 'SILENCIO', 'BASURA']
    estado_inicial = ['BASURA', 'MANOSLIMPIAS', 'SILENCIO']
    objetivo = ['CENA', 'REGALO', '-BASURA']
    accion1 = ['cocinar',['MANOSLIMPIAS'],['CENA']]
    accion2 = ['envolver',['SILENCIO'],['REGALO']]
    accion3 = ['sacarBasura',[],['-BASURA', '-MANOSLIMPIAS']]
    accion4 = ['triturar', [], ['-BASURA', '-SILENCIO']]
    acciones = [accion1, accion2, accion3, accion4]

################   RESTO DE EJEMPLOS   ###################

##      predicados = ['a', 'b', 'c', 'd']
##      estado_inicial = ['a', 'c']
##      objetivo = ['-b','d']
##      accion1 = ['accion1',['a','c'],['d','-b']]
##      accion2 = ['accion2',[],['a','c','d']]
##      accion3 = ['accion3',['d'],['-b','a']]
##      acciones = [accion1,accion2, accion3]

##    predicados = ['p1', 'p2', 'e1','e2','e3','e4']
##    estado_inicial = ['p1', 'p1']
##    objetivo = ['e1','e4']
##    accion1 = ['a1',['p1'],['e1']]
##    accion2 = ['a2',['p2'],['-e1','e2','e3']]
##    accion3 = ['a3',['e1','e2','e3'],['-e2','e4']]
##    acciones = [accion1,accion2, accion3]

##    predicados = ['p1', 'p2', 'p3','p4','p5','p6']
##    estado_inicial = ['p1', 'p2']
##    objetivo = ['p5','p6']
##    accion1 = ['A',['p1'],['p3','p4']]
##    accion2 = ['B',['p2','p4'],['-p3','-p5','p6']]
##    accion3 = ['C',['p3'],['-p3','p5']]
##    acciones = [accion1,accion2, accion3]

##    predicados = ['p0', 'p1', 'p2','p3','p4']
##    estado_inicial = ['p0']
##    objetivo = ['p2','p4']
##    accion1 = ['A',[],['-p1','p3']]
##    accion2 = ['B',['p0','p3'],['p4']]
##    accion3 = ['C',['p1'],['-p0','p2']]
##    accion4 = ['D',[],['p1','-p2']]
##    acciones = [accion1,accion2, accion3, accion4]



     
    fichero_salida.write("Predicados: "+str(predicados).strip('[]')+ '\r\n\r\n' )
    fichero_salida.write("Estado Inicial: "+str(estado_inicial).strip('[]')+ '\r\n\r\n')
    fichero_salida.write("Objetivo: "+str(objetivo).strip('[]')+ '\r\n\r\n' )
    for a in acciones:
        fichero_salida.write("Accion "+str(a[0])+": Precondiciones: "+ str(a[1])+". Efectos: "+str(a[2])+ '\r\n' )
    fichero_salida.write('\r\n')    

    

	
	
    literalesNivelAnterior = []
    accionesNivelAnterior = []
    arcosAccionesLiteralesAnterior= []
    enlacesMutexLiteralesAnterior = []
    enlacesMutexAccionesAnterior = []
    nivelesNoIdenticos = True
    objetivoNoAlcanzado = True
    aux = 1	
	
	
    # 2.Formar la capa de literales L(0) del nivel 0 del grafo 
    literalesNivel0 = crearNivel0(predicados, estado_inicial)
    
    fichero_salida.write("Nivel L(0) del grafo: "+'\r\n'+str(literalesNivel0).strip('[]')+ '\r\n\r\n' )
    
    print "Literales L(0)"
    print (literalesNivel0)
    print ('----------------------------------------')
    
    literalesNivelAnterior = literalesNivel0

    while(nivelesNoIdenticos and objetivoNoAlcanzado):

        
        # 3.Formar la capa de acciones A(i) del nivel i del grafo 
        nivelAcciones = crearNivelAcciones(acciones, literalesNivelAnterior,enlacesMutexLiteralesAnterior) #A(1)
        
        fichero_salida.write("Nivel A("+str(aux)+") del grafo: "+'\r\n')
        for a in nivelAcciones:
            fichero_salida.write(str(a)+'\r\n')
        fichero_salida.write('\r\n')
        
        print "Acciones A(i)"
        print (nivelAcciones)
        print ('----------------------------------------')
            
            
        
        # 4.Formar la capa de literales L(i) del nivel i del grafo  
        nivelLiterales = crearNivelLiterales(nivelAcciones)
        
        fichero_salida.write("Nivel L("+str(aux)+") del grafo: "+'\r\n'+str(nivelLiterales).strip('[]')+ '\r\n\r\n' )
        
        print "Literales L(i)"
        print (nivelLiterales)
        print ('----------------------------------------')


        
        # 5. Formar los enlaces entre la capa de literales L(i-1) y la capa de acciones A(i)
        arcosLiteralesAcciones = crearEnlacesLiteralesAcciones(nivelAcciones)
        
        fichero_salida.write("Arcos L("+str(aux-1)+") - A("+str(aux)+")"+'\r\n')
        for a in arcosLiteralesAcciones:
            fichero_salida.write(str(a[0]) + ' -> ' + str(a[1])+ '\r\n')
        fichero_salida.write('\r\n')
        
        print "Arcos L(i-1)-A(i)"
        print (arcosLiteralesAcciones)
        print ('----------------------------------------')
        

        

            
        # 6. Formar los enlaces entre la capa de acciones A(i) y la capa de literales L(i)
        arcosAccionesLiterales = crearEnlacesAccionesLiterales(nivelAcciones)
        
        fichero_salida.write("Arcos A("+str(aux)+") - L("+str(aux)+")"+'\r\n')
        for a in arcosAccionesLiterales:
            fichero_salida.write(str(a[0]) + ' -> ' + str(a[1])+ '\r\n')
        fichero_salida.write('\r\n')
        
        print "Arcos A(i)-L(i)"
        print (arcosAccionesLiterales)
        print ('----------------------------------------')
        

        # 7. Calcular exclusiones mutuas entre dos acciones de la capa A(i)
        enlacesMutexAcciones= crearEnlacesMutexAcciones(nivelAcciones,enlacesMutexLiteralesAnterior)
        
        fichero_salida.write("Enlaces Mutex entre Acciones del nivel"+str(aux)+'\r\n')
        for a in enlacesMutexAcciones:
            fichero_salida.write(str(a)+ '\r\n')
        fichero_salida.write('\r\n')
        
        print "Enlaces mutex A(i)"
        print enlacesMutexAcciones
        print ('----------------------------------------')
        


        #8. Calcular exclusiones mutuas entre dos literales de la capa L(i)
        enlacesMutexLiterales= crearEnlacesMutexLiterales(nivelLiterales, enlacesMutexAcciones, arcosAccionesLiterales)
        
        fichero_salida.write("Enlaces Mutex entre Literales del nivel"+str(aux)+'\r\n')
        for a in enlacesMutexLiterales:
            fichero_salida.write(str(a)+ '\r\n')
        fichero_salida.write('\r\n')
        
        print "Enlaces mutex L(i)"
        print (enlacesMutexLiterales)
        print ('----------------------------------------')




	# 9. Comprobar criterios de parada
		
	# Comprobamos que dos niveles de literales, dos de acciones, dos enlaces y dos de enlaces mutex son iguales
        booleanos = []

				# Capa A(i) iguales o no
        for ac in accionesNivelAnterior:
            if(nivelAcciones.count(ac)>0):
                booleanos.append('True')
            else:
                booleanos.append('False')
                
        for ac in nivelAcciones:
            if(accionesNivelAnterior.count(ac)>0):
                booleanos.append('True')
            else:
                booleanos.append('False')


				# Capa L(i) iguales o no        
        for l in literalesNivelAnterior:
            if(nivelLiterales.count(l)>0):
                booleanos.append('True')
            else:
                booleanos.append('False')

        for l in nivelLiterales:
            if(literalesNivelAnterior.count(l)>0):
                booleanos.append('True')
            else:
                booleanos.append('False')


				# Enlaces A(i) - L(i) iguales o no
        for a in arcosAccionesLiteralesAnterior:
            if(arcosAccionesLiterales.count(a)>0):
                booleanos.append('True')
            else:
                booleanos.append('False')

        for a in arcosAccionesLiterales:
            if(arcosAccionesLiteralesAnterior.count(a)>0):
                booleanos.append('True')
            else:
                booleanos.append('False')

				# Enlaces mutex entre acciones iguales o no
        for e in enlacesMutexAcciones:
            if(enlacesMutexAccionesAnterior.count(e)>0):
                booleanos.append('True')
            else:
                booleanos.append('False')

        for e in enlacesMutexAccionesAnterior:
            if(enlacesMutexAcciones.count(e)>0):
                booleanos.append('True')
            else:
                booleanos.append('False')

				# Enlaces mutex entre literales iguales o no
        for e in enlacesMutexLiterales:
            if(enlacesMutexLiteralesAnterior.count(e)>0):
                booleanos.append('True')
            else:
                booleanos.append('False')

        for e in enlacesMutexLiteralesAnterior:
            if(enlacesMutexLiterales.count(e)>0):
                booleanos.append('True')
            else:
                booleanos.append('False')


        

        if(booleanos.count('False') == 0):
            nivelesNoIdenticos = False
            print 'Literales, acciones y arcos son iguales'
            fichero_salida.write('Literales, acciones y arcos son iguales'+ '\r\n\r\n')
            print ('----------------------------------------')
        else:
            nivelesNoIdenticos = True
            print 'Literales, acciones y arcos son diferentes'
            fichero_salida.write('Literales, acciones y arcos son diferentes'+ '\r\n\r\n')
            print ('----------------------------------------')
            accionesNivelAnterior = nivelAcciones
            literalesNivelAnterior = nivelLiterales
            arcosAccionesLiteralesAnterior = arcosAccionesLiterales
            enlacesMutexAccionesAnterior = enlacesMutexAcciones
            enlacesMutexLiteralesAnterior = enlacesMutexLiterales





        

	# Comprobamos que todos los literales del objetivo aparecen en la capa de literales sin enlaces mutex entre ellos.
        contarBooleanos = []
        i = 0
        while (i < len(objetivo)):
            o = objetivo[i]
            if(nivelLiterales.count(o) > 0):
                j = i+1
                while (j < len(objetivo)):
                    o2 = objetivo[j]
                    if(nivelLiterales.count(o2) > 0):
                        if((enlacesMutexLiterales.count([o,o2]) == 0) and (enlacesMutexLiterales.count([o2,o]) == 0)):
                            contarBooleanos.append('True')
                        else:
                            contarBooleanos.append('False')
                    else:
                        contarBooleanos.append('False')
                    j = j+1
            else:
                contarBooleanos.append('False')
            i = i+1


        if(contarBooleanos.count('False') == 0):
            objetivoNoAlcanzado = False
            print 'Estan todos los objetivos en los literales sin enlaces mutex'
            fichero_salida.write('Estan todos los objetivos en los literales sin enlaces mutex'+ '\r\n\r\n')
                
        else:
            objetivoNoAlcanzado = True
            print 'No estan todos los objetivos en los literales sin enlaces mutex'
            fichero_salida.write('No estan todos los objetivos en los literales sin enlaces mutex'+ '\r\n\r\n')
            print ('----------------------------------------')
            
    
            
        aux= aux + 1
    return literalesNivel0







planificacion()


