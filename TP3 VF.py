# Integrantes: Alexis Galasco, Brian Escalante, Rubén Guerra y Lorenzo Spallione
# Comisión: 114

import os
import pickle
import datetime
import math
import re

# -----------------------------------------------------------------------------------------
# --------------------------------- REGISTROS Y FORMATEOS ---------------------------------
# -----------------------------------------------------------------------------------------

class Operaciones:
    def __init__(self):
        self.patente = '' #string de 7 caracteres
        self.codigo_producto = '' #int
        self.fecha_cupo = '' #dd/mm/yyyy
        self.estado = 'P' #char
        self.bruto = 0 #int
        self.tara = 0 #int
    def __str__(self):
        global rutaProductos, archivoProductos
        string = '{:<12}'.format(self.fecha_cupo)
        string += '{:<12}'.format(self.patente)
        if os.path.getsize(rutaProductos) == 0:
            string += '{:<14}'.format("NO ENCONTRADO")
        else:
            archivoProductos.seek(0)
            producto = pickle.load(archivoProductos)
            string += '{:<14}'.format(producto.nombre[0:13])
        if str(self.bruto).strip() == '0':
            string += '{:^10}'.format('-')
            string += '{:^10}'.format('-')
        else:
            string += '{:>8}'.format(str(self.bruto).strip() + ' kg') + '  '
            string += '{:>8}'.format(str(self.tara).strip() + ' kg') + '  '
        string += '{:^6}'.format(str(self.estado).strip())
        return string

def mostrarTituloOperaciones():
    string = '-' * 68 + '\n'
    string += '{:<12}'.format("Fecha")
    string += '{:<12}'.format("Patente")
    string += '{:<14}'.format("Producto")
    string += '{:^10}'.format("Bruto")
    string += '{:^10}'.format("Tara")
    string += '{:^6}'.format("Estado")
    string +=  '\n' + '-' * 68
    print(string)

def formatearOperaciones(operacion):
    operacion.patente = str(operacion.patente).ljust(7,' ')
    operacion.codigo_producto = str(operacion.codigo_producto).ljust(5, ' ')
    operacion.fecha_cupo = str(operacion.fecha_cupo)[0:10]
    operacion.estado = str(operacion.estado)[0:1]
    operacion.bruto = str(operacion.bruto).ljust(5, ' ')
    operacion.tara = str(operacion.tara).ljust(5, ' ')

class Producto:
    def __init__(self):
        self.codigo = 0 #int
        self.nombre = '' #string
        self.estado = 'A' #char A: Activo - B:Baja
    def __str__(self):
        return '{:<10}'.format(self.codigo) + '{:<30}'.format(self.nombre) + '{:^6}'.format(self.estado)

def formatearProducto(producto):
    producto.codigo = str(producto.codigo).ljust(5,' ')
    producto.nombre = producto.nombre.ljust(30,' ')
    producto.estado = producto.estado[0:1] # nos aseguramos que sea de 1 caracter

class Rubro:
    def __init__(self):
        self.codigo = 0 #int
        self.nombre = '' #string
    def __str__(self):
        string = '{:<7}'.format(self.codigo)
        string += '{:<17}'.format(self.nombre)
        return string

def formatearRubro(vrRubro):
    vrRubro.codigo = str(vrRubro.codigo).ljust(5, ' ') 
    vrRubro.nombre = vrRubro.nombre.ljust(25, ' ')

class Rubro_X_Producto:
    def __init__(self):
        self.codigo_rubro = 0 #int
        self.codigo_producto = 0 #int
        self.min = 0 #float >= 0.0
        self.max = 100 # float <= 100.0

def formatearRubrosXProductos(rubroXProd):
    rubroXProd.codigo_producto = str(rubroXProd.codigo_producto).ljust(5,' ')
    rubroXProd.codigo_rubro = str(rubroXProd.codigo_rubro).ljust(5, ' ')
    rubroXProd.min = str(rubroXProd.min).ljust(5, ' ')
    rubroXProd.max = str(rubroXProd.max).ljust(5, ' ')


class Silo:
    def __init__(self):
        self.codigo = 0 #int
        self.nombre = '' #string
        self.codigo_producto = 0 #int
        self.stock = 0 #int
        self.camiones = 0 #int

def formatearSilo(vrSilo):
    vrSilo.codigo = str(vrSilo.codigo).ljust(10, ' ')
    vrSilo.codigo_producto = str(vrSilo.codigo_producto).ljust(5, ' ')
    vrSilo.stock = str(vrSilo.stock).ljust(7, ' ')
    vrSilo.nombre = vrSilo.nombre.ljust(40, ' ')
    vrSilo.camiones = str(vrSilo.camiones).ljust(7, ' ')

# -----------------------------------------------------------------------------------------
# ------------------------------------ PRINT DE MENUES ------------------------------------
# -----------------------------------------------------------------------------------------

# procedimiento
def printMenuPrincipal():
    print("*** MENÚ PRINCIPAL ***\n")
    print("1-Administraciones")
    print("2-Entrega de cupos")
    print("3-Recepción")
    print("4-Registrar calidad")
    print("5-Registrar peso bruto")
    print("6-Registrar descarga")
    print("7-Registrar tara")
    print("8-Reportes")
    print("9-Listado de silos y rechazos")
    print("0-Fin del programa")

# procedimiento
def printMenuAdministraciones():
    print("*** MENÚ ADMINISTRACIONES ***\n")
    print("A-Titulares")
    print("B-Productos")
    print("C-Rubros")
    print("D-Rubros por producto")
    print("E-Silos")
    print("F-Sucursales")
    print("G-Producto por titular")
    print("V-Volver al menú principal")

# procedimiento
def printMenuOpciones(seccion):
    print(f"*** MENÚ DE OPCIONES - {seccion} ***\n")
    print("A-Alta")
    print("B-Baja")
    print("C-Consulta")
    print("M-Modificación")
    print("V-Volver al menú anterior")

# -----------------------------------------------------------------------------------------
# -------------------------------------- OPERACIONES --------------------------------------
# -----------------------------------------------------------------------------------------

# funcion -> return boolean
# existente = boolean
# patentesCupos -> ver variables del programa principal
# patente = parámetro formal de tipo string
def getPosicionOperaciones(patente, fecha):
    global rutaOperaciones, archivoOperaciones
    tamArch = os.path.getsize(rutaOperaciones)
    if(tamArch == 0):
        return -1
    else:
        archivoOperaciones.seek(0)
        encontrado = -1
        while archivoOperaciones.tell() < tamArch and encontrado == -1:
            posicionAntesDeLeer = archivoOperaciones.tell()
            operacion = pickle.load(archivoOperaciones)
            if(str(operacion.fecha_cupo).strip() == fecha and str(operacion.patente).strip() == patente):
                encontrado = posicionAntesDeLeer
        return encontrado

# procedimiento
# opcion = string
# patente = string, al momento de invocar a la función esPatenteValida la variable pasa como parámetro real
# posicionCupo = integer
# i = integer
# estadosCupos -> ver variables del programa principal
# patentesCupos -> ver variables del programa principal
def entregaDeCupo():
    global rutaProductos, archivoOperaciones
    if (os.path.getsize(rutaProductos) == 0):
        limpiarPantalla()
        print("*** ENTREGA DE CUPOS ***\n")
        print('Debe registrar al menos un producto antes de solicitar un cupo.\n')
        print('Diríjase al Menú Principal -> 1.Adminstraciones -> B.Productos -> A.Alta\n')
        input("Presione enter para volver al menú anterior")
    else:
        if not hayProductosActivos():
            limpiarPantalla()
            print("*** ENTREGA DE CUPOS ***\n")
            print('No hay productos activos para asignar cupos\n')
            print('Diríjase al Menú Principal -> 1.Administraciones -> B.Productos -> A.Alta\n')
            input("Presione enter para volver al menú anterior")
        opcion = "S"
        while opcion == "S":
            limpiarPantalla()
            print("*** ENTREGA DE CUPOS ***\n")
            patente = input("Ingrese el número de patente para la reserva de cupo (formatos válidos AA000AA o AAA000): ").upper()
            while not esPatenteValida(patente):
                patente = input("Ingrese un numero de patente válido (formatos válidos AA000AA o AAA000): ").upper()
            fecha = insertFecha("Ingrese la fecha del día de hoy: ")
            while not esHoy(fecha):
                fecha = insertFecha("Sólo se permite ingresar la fecha del día actual: ")
            if (getPosicionOperaciones(patente, fecha) != -1):
                print(f'La patente {patente} ya cuenta con un cupo para el día {fecha}')
            else:
                printProductosRegistrados()
                codigo = input("\nIngrese el código del producto que contiene el camión: ")
                posicReg = getPosicionProducto(codigo)
                while posicReg == -1 or not esProductoActivo(codigo):
                    codigo = input("Debe ingresar un código de producto existente y que no esté dado de baja: ")
                    posicReg = getPosicionProducto(codigo)
                operacion = Operaciones()
                operacion.fecha_cupo = fecha
                operacion.patente = patente
                operacion.estado = 'P'
                operacion.codigo_producto = codigo
                formatearOperaciones(operacion)
                pickle.dump(operacion, archivoOperaciones)
                archivoOperaciones.flush()
                print("Cupo entregado con éxito")
            opcion = input("\nDeseas asignar otro cupo? (S para Sí o N para No): ").upper()
            while opcion != "S" and opcion != "N":
                error()
                opcion = input("\n¿Desea asignar otro cupo? (S para Sí o N para No): ").upper()

def printPatentes(fecha, estado):
    global archivoOperaciones, rutaOperaciones
    tamArch = os.path.getsize(rutaOperaciones)
    listadoPatentes = ""
    if tamArch != 0:
        archivoOperaciones.seek(0)
        contador = 1
        while archivoOperaciones.tell() < tamArch:
            operacion: Operaciones = pickle.load(archivoOperaciones)
            if (str(operacion.estado).strip() == estado and str(operacion.fecha_cupo).strip()  == fecha):
                listadoPatentes += str(contador).ljust(4, " ") + str(operacion.fecha_cupo).ljust(12, " ") + operacion.patente + "\n"
                contador += 1
    if listadoPatentes == "":
        print(f"No hay patentes con estado {estado} para el día {fecha}.")
        return False
    else:
        print("------------------------")
        print("#   Fecha       Patente")
        print("------------------------")
        print(listadoPatentes)
        return True

def puedeRecepcionar(patente):
    global archivoOperaciones, rutaOperaciones
    tamArch = os.path.getsize(rutaOperaciones)
    if tamArch == 0:
        return False
    else:
        puedeRec = False
        hoy = datetime.date.today().strftime("%d/%m/%Y")
        archivoOperaciones.seek(0)
        while archivoOperaciones.tell() < tamArch and not puedeRec:
            operacion: Operaciones = pickle.load(archivoOperaciones)
            if (str(operacion.fecha_cupo).strip()  == hoy and str(operacion.patente).strip() == patente and str(operacion.estado).strip() == "P"):
                puedeRec = True
    return puedeRec

def hayCuposParaRecepcionar(fecha):
    global rutaOperaciones, archivoOperaciones
    tamArch = os.path.getsize(rutaOperaciones)
    if tamArch == 0:
        return False
    else:
        archivoOperaciones.seek(0)
        hayCupo = False
        while archivoOperaciones.tell() < tamArch and not hayCupo:
            operacion: Operaciones = pickle.load(archivoOperaciones)
            if str(operacion.fecha_cupo).strip() == fecha and operacion.estado == "P":
                hayCupo = True
        return hayCupo

# procedimiento
# opcion = string
# patente = string
# posicionCupo = integer
# tipoProducto = integer
# estadosCupos -> ver variables del programa principal
def recepcion():
    global rutaOperaciones
    hoy = datetime.date.today().strftime("%d/%m/%Y")
    opcion = "S"
    if not hayProductosActivos():
        opcion = "N"
        limpiarPantalla()
        print("*** MENÚ RECEPCIÓN ***\n")
        print('No hay productos activos para asignar a los camiones pendientes de recepción\n')
        print('Diríjase al Menú Principal -> 1.Administraciones -> B.Productos -> A.Alta\n')
        input("Presione enter para volver al menú anterior")
    while opcion == "S":
        if not hayCuposParaRecepcionar(hoy):
            opcion = "N"
            limpiarPantalla()
            print("*** MENÚ RECEPCIÓN ***\n")
            print('No existen cupos pendientes de recepción para el día de hoy.\n')
            print('Diríjase al Menú Principal -> 2.Entrega de cupos\n')
            input("Presione enter para volver al menú anterior")
        else:
            limpiarPantalla()
            print("*** MENÚ RECEPCIÓN ***\n")
            
            printPatentes(hoy,"P")
            patente = input("Ingrese la patente del camión que desea recepcionar: ").upper()
            while not puedeRecepcionar(patente):
                limpiarPantalla()
                print("*** MENÚ RECEPCIÓN ***\n")
                printPatentes(hoy, "P")
                patente = input("Ingrese una patente pendiente de recepción: ").upper()

            posic = getPosicionOperaciones(patente, hoy)
            archivoOperaciones.seek(posic,0)
            operacion: Operaciones = pickle.load(archivoOperaciones)
            operacion.estado = "A"
            formatearOperaciones(operacion)
            archivoOperaciones.seek(posic,0)
            pickle.dump(operacion, archivoOperaciones)
            archivoOperaciones.flush()
            print("Camión recepcionado con éxito")
            
            opcion = input("\n¿Desea recepcionar otro camión? (S para sí o N para no): ").upper()
            while opcion != "S" and opcion != "N":
                opcion = input("Ingrese una opción correcta (S para sí o N para no): ").upper()



def busquedaDicoRubro(CR):
    global archivoRubxProd, archivoOperaciones, rutaOperaciones, rutaProductos, archivoProductos
    archivoRubros.seek(0, 0)
    aux = pickle.load(archivoRubros)
    tamRegis = archivoRubros.tell()
    cantRegis = int(os.path.getsize(rutaRubros) / tamRegis)
    desde = 0
    hasta = cantRegis-1
    medio = (desde + hasta) // 2 
    archivoRubros.seek(medio*tamRegis, 0)
    vrRubro = pickle.load(archivoRubros)
    while(int(vrRubro.codigo) != CR and desde < hasta):
        if CR < int(vrRubro.codigo):
            hasta = medio - 1
        else:
            desde = medio + 1
        medio = (desde + hasta) // 2
        archivoRubros.seek(medio*tamRegis, 0)
        vrRubro= pickle.load(archivoRubros)
    if int(vrRubro.codigo) == CR:
        return medio*tamRegis
    else:
        return -1


def puedeRegistrarCalidad():
    global archivoOperaciones, rutaOperaciones
    tamArch = os.path.getsize(rutaOperaciones)
    if tamArch == 0:
        return False
    else:
        archivoOperaciones.seek(0)
        puedeReg = False
        while archivoOperaciones.tell() < tamArch and not puedeReg:
            operacion: Operaciones = pickle.load(archivoOperaciones)
            if (str(operacion.estado).strip() == "A"):
                puedeReg = True
    return puedeReg

def patenteCorrecta(patente):
    global archivoOperaciones, rutaOperaciones
    tamArch = os.path.getsize(rutaOperaciones)
    if tamArch == 0:
        return False
    else:
        archivoOperaciones.seek(0)
        puedeReg = False
        while archivoOperaciones.tell() < tamArch and not puedeReg:
            operacion: Operaciones = pickle.load(archivoOperaciones)
            if (str(operacion.patente).strip() == patente) and (str(operacion.estado).strip() == "A"):
                puedeReg = True
    return puedeReg

def printPatentesParaReg():
    global archivoOperaciones, rutaOperaciones, rutaProductos, archivoProductos
    tamArch = os.path.getsize(rutaOperaciones)
    listadoPatentes = ""
    if tamArch != 0:
        archivoOperaciones.seek(0)
        contador = 1
        while archivoOperaciones.tell() < tamArch:
            operacion = pickle.load(archivoOperaciones)
            posicProd = getPosicionProducto(operacion.codigo_producto)
            archivoProductos.seek(posicProd)
            producto = pickle.load(archivoProductos)
            if (str(operacion.estado).strip() == "A"):
                listadoPatentes += '{:<4}'.format(str(contador).strip())
                listadoPatentes += '{:<23}'.format(str(operacion.codigo_producto).strip() + " - " + str(producto.nombre).strip()[0:19])
                listadoPatentes += '{:<7}'.format(str(operacion.patente).strip()) + "\n"
                contador += 1
            
        print("----------------------------------")
        print("#   Producto               Patente")
        print("----------------------------------")
        print(listadoPatentes)


def registrarCalidad():
    global archivoOperaciones, rutaOperaciones, archivoRubxProd
    if (os.path.getsize(rutaOperaciones) == 0):
        limpiarPantalla()
        print("*** REGISTRAR CALIDAD ***\n")
        print('Debe ingresar al menos un camión antes de realizar un registro de calidad.\n')
        input("Presione enter para volver al menú anterior")
    else:
        opcion = "S"
        if not puedeRegistrarCalidad():
            opcion = "N"
            limpiarPantalla()
            print("*** REGISTRAR CALIDAD ***\n")
            print('No hay camiones con estado "A - Arribado" a los cuales registrar se les pueda registrar su calidad\n')
            print('Diríjase al Menú Principal -> 3.Recepción\n')
            input("Presione enter para volver al menú anterior")
        while opcion == "S":
            if not puedeRegistrarCalidad():
                opcion = "N"
                limpiarPantalla()
                print("*** REGISTRAR CALIDAD ***\n")
                print('No hay camiones con estado "A - Arribado" a los cuales registrar se les pueda registrar su calidad\n')
                print('Diríjase al Menú Principal -> 3.Recepción\n')
                input("Presione enter para volver al menú anterior")
            
            else:
                limpiarPantalla()
                print("*** REGISTRAR CALIDAD ***\n")
                printPatentesParaReg()
                patente = input("Ingrese el número de patente del camión al que desea realizar el registro de calidad: ").upper()
                while not patenteCorrecta(patente):
                    patente = input("Ingrese un número de patente pendiente de registrar su calidad: ").upper()
                hoy = datetime.date.today().strftime("%d/%m/%Y")
                posic = getPosicionOperaciones(patente, hoy)
                archivoOperaciones.seek(posic)
                operacion: Operaciones = pickle.load(archivoOperaciones)
                if productoTieneRubros(operacion.codigo_producto):
                    archivoRubxProd.seek(0)
                    tamArchRubrxProd = os.path.getsize(rutaRubxProd)
                    faltas = 0
                    while archivoRubxProd.tell() < tamArchRubrxProd:
                        rubroxProd: Rubro_X_Producto = pickle.load(archivoRubxProd)
                        if rubroxProd.codigo_producto == operacion.codigo_producto:
                            archivoRubros.seek(busquedaDicoRubro(int(rubroxProd.codigo_rubro)),0)
                            auxRubro: Rubro = pickle.load(archivoRubros)
                            auxValor = insertFloat(f"Ingrese el valor para el rubro {str(auxRubro.nombre).strip()}\nSera de calidad entre los valores {rubroxProd.min} y {rubroxProd.max}: ")
                            if(auxValor < float(rubroxProd.min) or auxValor > float(rubroxProd.max)):
                                faltas += 1
                    if(faltas >= 2):
                        operacion.estado = 'R'
                        print("Camion en estado rechazado por tener 2 faltas al estándar de calidad\n")
                    else:
                        operacion.estado = 'C'
                        print("Calidad registrada exitosamente\n")
                    archivoOperaciones.seek(posic)
                    formatearOperaciones(operacion)
                    pickle.dump(operacion, archivoOperaciones)
                    archivoOperaciones.flush()
                else:
                    print("\nEl producto asociado al camión no cuenta con rubros por productos vinculados a él")
                    print("\nDiríjase al Menú Principal -> 1.Administraciones -> D.Rubros por producto -> A.Alta")

            opcion = input("\nDeseas registrar la calidad de otra patente? (S para Sí o N para No): ").upper()
            while opcion != "S" and opcion != "N":
                opcion = input("\n¿Deseas registrar la calidad de otra patente (S para Sí o N para No): ").upper()

# procedimiento
# opcion = string
# patente = string
# posicionCupo = integer
# pesoBruto = integer
# estadosCupos -> ver variables del programa principal
# camiones -> ver variables del programa principal
def registrarPesoBruto():
    global rutaOperaciones,archivoOperaciones
    limpiarPantalla()
    if (os.path.getsize(rutaOperaciones) == 0):
        print('Debe registrar al menos una patente antes de registrar el peso bruto.')
        input("Presione enter para volver al menú anterior\n")
    else:
        limpiarPantalla()
        print("*** REGISTRAR PESO BRUTO ***\n")
        opcion = "S"
        hoy = datetime.date.today().strftime("%d/%m/%Y")
        while opcion == "S":
            if not hayPatentesParaRegistrar(hoy, "C"):
                print('No hay camiones pendientes de registrar su peso bruto.')
                input("Presione enter para volver al menú anterior")
                opcion = "N"
            else:
                printPatentes(hoy,"C")
                patente = input("Ingrese la patente a la que desea registrarle la tara: ").upper()
                posic = getPosicionOperaciones(patente, hoy)
                if posic != -1:
                    archivoOperaciones.seek(posic)
                    RegOperaciones = pickle.load(archivoOperaciones)
                while posic == -1 or RegOperaciones.estado != "C":
                    patente = input("Ingrese una patente válida a la que desea registrarle el peso bruto: ").upper()
                    posic = getPosicionOperaciones(patente, hoy)
                    if posic != -1:
                        archivoOperaciones.seek(posic)
                        RegOperaciones = pickle.load(archivoOperaciones)
                if(not productoTieneSilo(str(RegOperaciones.codigo_producto).strip())):
                    print("No existe Silo correspondiente al producto que contiene el camión")
                else:
                    archivoOperaciones.seek(posic)
                    RegOperaciones: Operaciones = pickle.load(archivoOperaciones)
                    RegOperaciones.bruto = insertInt(f"Ingrese el peso bruto a registrar para la patente {patente}: ")
                    RegOperaciones.estado = 'B'
                    archivoOperaciones.seek(posic, 0)
                    formatearOperaciones(RegOperaciones)
                    pickle.dump(RegOperaciones, archivoOperaciones)
                    archivoOperaciones.flush()
                    print("Peso bruto registrado con exito y estado modificado a B")

                opcion = input("Deseas registrar el peso bruto de otra patente? (S para Sí o N para No): ").upper()
                while opcion != "S" and opcion != "N":
                    error()
                    opcion = input("\n¿Deseas registrar el peso bruto de otra patente (S para Sí o N para No): ").upper()
           
# procedimiento
# opcion = string
# patente = string
# posicionCupo = integer
# tara = integer
# estadosCupos -> ver variables del programa principal
# camiones -> ver variables del programa principal
def buscarPatente(patentes):
    global archivoOperaciones, rutaOperaciones
    RegOperaciones = Operaciones()
    tamArchOperaciones=os.path.getsize(rutaOperaciones)
    archivoOperaciones.seek(0,0)
    RegOperaciones=pickle.load(archivoOperaciones)
    if(patentes==RegOperaciones.patente):
        return False
    while(archivoOperaciones.tell()<tamArchOperaciones):
        RegOperaciones=pickle.load(archivoOperaciones)
        if(patentes==RegOperaciones.patente):
            return False
    return True

def patenteEstadoBruto(patentes):
    global archivoOperaciones, rutaOperaciones
    RegOperaciones = Operaciones()
    tamArchOperaciones=os.path.getsize(rutaOperaciones)
    archivoOperaciones.seek(0,0)
    RegOperaciones=pickle.load(archivoOperaciones)
    while((archivoOperaciones.tell()<tamArchOperaciones) and patentes!=RegOperaciones.patente):
        pickle.load(archivoOperaciones)
    if(int(RegOperaciones.bruto) == 0):
        return True
    else:
        return False

def TaraYaRegistrada(patente):
    global archivoOperaciones
    global rutaOperaciones
    RegOperaciones=Operaciones()
    archivoOperaciones.seek(0,0)
    while(RegOperaciones.patente!=patente):
        RegOperaciones=pickle.load(archivoOperaciones)
    if RegOperaciones.estado=='F':
        return True
    else:
        return False

def productoTieneSilo(codigoProducto):
    global archivoSilos, rutaSilos
    tamArch = os.path.getsize(rutaSilos)
    if tamArch == 0:
        return False
    else:
        tieneSilo = False
        archivoSilos.seek(0)
        while archivoSilos.tell() < tamArch and not tieneSilo:
            silo: Silo = pickle.load(archivoSilos)
            if str(silo.codigo_producto).strip() == str(codigoProducto).strip():
                tieneSilo = True
        return tieneSilo

def hayPatentesParaRegistrar(fecha, estado):
    global archivoOperaciones, rutaOperaciones
    tamArch = os.path.getsize(rutaOperaciones)
    if tamArch == 0:
        return False
    else:
        hayPatentes = False
        archivoOperaciones.seek(0)
        while archivoOperaciones.tell() < tamArch and not hayPatentes:
            operacion: Operaciones = pickle.load(archivoOperaciones)
            if str(operacion.fecha_cupo).strip() == fecha and str(operacion.estado).strip() == estado:
                hayPatentes = True
        return hayPatentes

# procedimiento
# opcion = string
# patente = string
# posicionCupo = integer
# tara = integer
# estadosCupos -> ver variables del programa principal
# camiones -> ver variables del programa principal
def registrarTara():
    global rutaProductos, archivoOperaciones
    global rutaSilos, archivoSilos
    opcion = "S"
    while opcion == "S":
        limpiarPantalla()
        print("*** REGISTRACIÓN DE TARA ***\n")
        hoy = datetime.date.today().strftime("%d/%m/%Y")
        if not hayPatentesParaRegistrar(hoy, "B"):
            print('No hay camiones pendientes de registrar su tara.')
            input("Presione enter para volver al menú anterior")
            opcion = "N"
        else:
            printPatentes(hoy,"B")
            patente = input("Ingrese la patente a la que desea registrarle la tara: ").upper()
            posic = getPosicionOperaciones(patente, hoy)
            if posic != -1:
                archivoOperaciones.seek(posic)
                RegOperaciones = pickle.load(archivoOperaciones)
            while posic == -1 or RegOperaciones.estado != "B":
                patente = input("Ingrese una patente válida a la que desea registrarle la tara: ").upper()
                posic = getPosicionOperaciones(patente, hoy)
                if posic != -1:
                    archivoOperaciones.seek(posic)
                    RegOperaciones = pickle.load(archivoOperaciones)

            if(not productoTieneSilo(str(RegOperaciones.codigo_producto).strip())):
                print("No existe Silo correspondiente al producto que contiene el camión")
            else:
                archivoOperaciones.seek(posic, 0)
                RegOperaciones: Operaciones = pickle.load(archivoOperaciones)
                PesoTara = insertInt(f"Ingrese el peso de la tara (Bruto es de {str(RegOperaciones.bruto).strip()}): ")
                while(int(RegOperaciones.bruto) < PesoTara):
                    PesoTara=insertInt(f"El peso de la tara debe ser menor al bruto (Bruto es de {str(RegOperaciones.bruto).strip()}): ")
                RegOperaciones.estado = 'F'
                RegOperaciones.tara = PesoTara
                formatearOperaciones(RegOperaciones)
                archivoOperaciones.seek(posic, 0)
                pickle.dump(RegOperaciones, archivoOperaciones)
                archivoOperaciones.flush()

                posicSilo = getPosicionSilos(RegOperaciones.codigo_producto)
                archivoSilos.seek(posicSilo,0)
                RegSilos: Silo = pickle.load(archivoSilos)
                RegSilos.stock = int(RegSilos.stock) + int(RegOperaciones.bruto) - int(PesoTara)
                RegSilos.camiones = int(RegSilos.camiones) + 1
                formatearSilo(RegSilos)
                archivoSilos.seek(posicSilo,0)
                pickle.dump(RegSilos, archivoSilos)
                archivoSilos.flush()
                print("\nTara registrada con éxito")
            opcion = input("\n¿Desea registrar la tara de otra patente? (S para sí o N para no) \n").upper()
            while opcion != "S" and opcion != "N":
                error()
                opcion = input("¿Desea registrar la tara de otra patente? (S para sí o N para no) \n").upper()


# procedimiento
# opcion = string
# menuReporte = string
# camiones = parámetro real, ver variables del programa principal
# patentesCupos = parámetro real, ver variables del programa principal
def reportes():
    opcion = 1
    if(os.path.getsize(rutaOperaciones) == 0):
        limpiarPantalla()
        opcion = 0
        print("\nSIN OPERACIONES REALIZADAS")
        input("\nPresione enter para continuar...")
    while opcion != 0:
        limpiarPantalla()
        mostrarSubMenuReportes()
        opcion = insertInt("\nIngrese una opcion: ")
        while validarRangoEnteros(opcion, 0, 5):
            opcion = insertInt("Ingrese una opción válida: ")
        if opcion == 1:
            limpiarPantalla()
            print(f"La cantidad de cupos otorgados es de {countCuposOtorgados()}")
            input("\nPresione enter para continuar...")
        elif opcion == 2:
            limpiarPantalla()
            totalCamiones()
            input("\nPresione enter para continuar...")
        elif opcion == 3:
            limpiarPantalla()
            Camiones_x_Producto()
            input("\nPresione enter para continuar...")
        elif opcion == 4:
            limpiarPantalla()
            PrintPesoNetoTotalYPromedioDeproductos()
            input("\nPresione enter para continuar...")
        elif opcion == 5:
            limpiarPantalla()
            PatenteMenorCantidad()
            input("\nPresione enter para continuar...")
    



def mostrarSubMenuReportes():
    print("*** MENÚ REPORTES ***\n")
    print("1-Cantidad de cupos otorgados")
    print("2-Cantidad total de camiones recibidos")
    print("3-Cantidad total de camiones de cada producto")
    print("4-Peso neto total de cada producto y promedio por camión.")
    print("5-Patente que menor cantidad descargó")
    print("0-Volver al menú anterior\n")

def PrintPesoNetoTotalYPromedioDeproductos():
    global rutaSilos
    global archivoSilos
    RegSilos=Silo()
    TamArchSilos=os.path.getsize(rutaSilos)
    archivoSilos.seek(0,0)
    RegSilos=pickle.load(archivoSilos)
    while(int(RegSilos.stock)==0 and TamArchSilos>archivoSilos.tell()):
        RegSilos=pickle.load(archivoSilos)
    if(int(RegSilos.stock)!=0):
        archivoSilos.seek(0,0)
        print("-------------------------------------------------------")
        while(archivoSilos.tell()<TamArchSilos):
            RegSilos=pickle.load(archivoSilos)
            if(int(RegSilos.stock)>0):
                print("Peso neto total del producto",int(RegSilos.codigo_producto),":",RegSilos.stock)
        print("-------------------------------------------------------")
        archivoSilos.seek(0,0)
        print("-------------------------------------------------------")
        while(archivoSilos.tell()<TamArchSilos):
            RegSilos=pickle.load(archivoSilos)
            if(int(RegSilos.camiones)>0):
                print("Promedio de peso neto por camión del producto:",int(RegSilos.codigo_producto),":",int(RegSilos.stock)/int(RegSilos.camiones))
        print("-------------------------------------------------------")
    else:
        print("No hay ninguna descarga en Silos")

def PatenteMenorCantidad():
    global rutaProductos, archivoProductos
    global rutaOperaciones, archivoOperaciones
    RegOperaciones=Operaciones()
    RegProductos=Producto()
    tamArchProductos=os.path.getsize(rutaProductos)
    tamArchOperaciones=os.path.getsize(rutaOperaciones)
    archivoProductos.seek(0,0)
    print("-------------------------------------------------------")
    print("***PATENTE CON MENOR CANTIDAD DE DESCARGA POR PRODUCTO***\n")
    while(tamArchProductos>archivoProductos.tell()):
        RegOperaciones=pickle.load(archivoProductos)
        codigo=RegOperaciones.codigo
        nombre=RegOperaciones.nombre
        PteMenor=""
        cantidad=999999999999
        archivoOperaciones.seek(0,0)
        while(tamArchOperaciones>archivoOperaciones.tell()):
            RegOperaciones=pickle.load(archivoOperaciones)
            if(int(RegOperaciones.tara)!=0):
                if(codigo==RegOperaciones.codigo_producto):
                    if(int(RegOperaciones.bruto)-int(RegOperaciones.tara))<cantidad:
                        cantidad=int(RegOperaciones.bruto)-int(RegOperaciones.tara)
                        PteMenor=RegOperaciones.patente
        print("Producto:",nombre)
        if(PteMenor==""):
            print("No se registró ningún camión descargando este producto")
        else:
            print("Patente:",PteMenor)
        if(cantidad==999999999999):
            print("Cantidad descargada:",0)
        else:
            print("Cantidad descargada:",cantidad)
        print("-------------------------------------------------------")


def listadSiloMayorStock():
    global rutaSilos, archivoSilos, archivoProductos
    limpiarPantalla()
    print("*** LISTADO DE SILOS ***\n")
    tamArch = os.path.getsize(rutaSilos)
    if tamArch == 0:
        print("No hay silos registrados\n")
    else:
        archivoSilos.seek(0,0)
        aux=pickle.load(archivoSilos)
        tamReg=archivoSilos.tell()
        cantReg=int(tamArch/tamReg)
        for i in range(0,cantReg-1):
            for j in range (i+1,cantReg):
                archivoSilos.seek(i*tamReg,0)
                AuxI=pickle.load(archivoSilos)
                archivoSilos.seek(j*tamReg,0)
                AuxJ=pickle.load(archivoSilos)
                if(int(AuxI.stock)<int(AuxJ.stock)):
                    archivoSilos.seek(i*tamReg,0)
                    pickle.dump(AuxJ,archivoSilos)
                    archivoSilos.seek(j*tamReg,0)
                    pickle.dump(AuxI,archivoSilos)
        archivoSilos.seek(0,0)
        while(tamArch>archivoSilos.tell()):
            RegSilos=pickle.load(archivoSilos)
            posicProd = getPosicionProducto(RegSilos.codigo_producto)
            archivoProductos.seek(posicProd)
            producto: Producto = pickle.load(archivoProductos)
            print(f"Producto: {str(producto.codigo).strip()} - {str(producto.nombre).strip()}")
            print("Nombre del Silo:",RegSilos.nombre)
            print("Stock:",RegSilos.stock)
            print("Camiones ingresados:",RegSilos.camiones)
            print("------------------------------------------")

# procedimiento
# i = integer
# patentesCupos -> ver variables del programa principal
# estadosCupos -> ver variables del programa principal
def printCuposOtorgados():
    global archivoOperaciones, rutaOperaciones
    tamArchivo = os.path.getsize(rutaOperaciones)
    if(tamArchivo == 0):
        print("La lista de cupos se encuentra vacía")
    else:
        archivoOperaciones.seek(0)
        while(archivoOperaciones.tell() < tamArchivo):
            registroCupo = pickle.load(archivoOperaciones)
            print(f"Patente: {registroCupo.patente}, Estado: {registroCupo.estado}")

def countCuposOtorgados():
    global archivoOperaciones, rutaOperaciones
    tamArchivo = os.path.getsize(rutaOperaciones)
    if tamArchivo == 0:
        return 0
    else:
        archivoOperaciones.seek(0)
        auxOper = pickle.load(archivoOperaciones)
        tamReg = archivoOperaciones.tell()
        return tamArchivo // tamReg

def totalCamiones():
    tamArchivo = os.path.getsize(rutaOperaciones)
    if(tamArchivo == 0):
        print("No se recibio ningún camion")
    else:
        registro = Operaciones()
        archivoOperaciones.seek(0)
        contador = 0
        while(archivoOperaciones.tell()<tamArchivo):
            registro = pickle.load(archivoOperaciones)
            if(registro.estado != 'P'):
                contador += 1
        print(f"La cantidad de camiones recibidos es de {contador}")

def Camiones_x_Producto():
    tamArch = os.path.getsize(rutaSilos)
    if(tamArch==0):
        print("No hay camiones por producto")
    else:
        RegSilos=Silo()
        archivoSilos.seek(0,0)
        while(tamArch>archivoSilos.tell()):
            RegSilos=pickle.load(archivoSilos)
            print("Se recibieron",int(RegSilos.camiones)," camiones para el código de producto",RegSilos.codigo_producto)


def camionesPorProducto():
    t = os.path.getsize(rutaProductos)
    tReg = archivoProductos.tell()
    if (t == 0):
        print("no hay camiones por producto")
    else:
        registroProd = Producto()
        cantProductos = 0
        archivoProductos.seek(0)
        cantProductos = int(t/tReg)
        listaProductos = [[0 for i in range(cantProductos)] for j in range(2)]
        for i in range(cantProductos-1):
            archivoProductos.seek(i*tReg,0)
            registroProd = pickle.load(archivoProductos)
            listaProductos[0][i] = registroProd.codigo
            i+=1
        registroOp = Operaciones()
        for j in range(cantProductos):
            while(archivoOperaciones.tell()<os.path.getsize(rutaOperaciones)):
                registroOp = pickle.load(archivoOperaciones)
                if(registroOp.codigo_producto == listaProductos[0][j]):
                    listaProductos[1][j] += 1
        for k in range(cantProductos):
            print(f"Se recibieron {listaProductos[1][k]} camiones para el codigo de producto {listaProductos[0][k]}")


# funcion -> return boolean
# patente = string
def esPatenteValida(patente):
    largoOk = len(patente) >= 6 and len(patente) <= 7
    formatoOk = re.search("([a-zA-Z]{2}[0-9]{3}[a-zA-Z]{2})|([a-zA-Z]{3}[0-9]{3})", patente)
    return largoOk and formatoOk

def listadoRechazos():
    limpiarPantalla()
    print("*** LISTADO DE PATENTES RECHAZADAS ***\n")
    RegOperaciones = Operaciones()
    tamArch=os.path.getsize(rutaOperaciones)
    fecha = insertFecha("Ingrese una fecha para consultar: ")
    cant = 0
    string = ""
    while(tamArch>archivoOperaciones.tell()):
        operacion: Operaciones = pickle.load(archivoOperaciones)
        if(str(operacion.estado).strip() == "R" and str(operacion.fecha_cupo).strip() == fecha):
            cant += 1
            string += '{:<11}'.format(operacion.fecha_cupo.strip())
            string += '{:<7}'.format(operacion.patente.strip()) + "\n"
    if cant > 0:
        print("------------------")
        print("Fecha      Patente")
        print("------------------")
        print(string)
    else:
        print(f"\nNo hay camiones rechazados para la fecha {fecha}")
            

def listadoSilosYRechazos():
    op="2"
    while op!="0":
        limpiarPantalla()
        print("***Silos y rechazos***\n")
        print("1-Listado de silos")
        print("2-Listado de Rechazos")
        print("0-Volver al menú anterior")
        op=input("\nIngrese una opción: ")
        while validarRangoEnteros(op, 0, 2):
            limpiarPantalla()
            print("***Silos y rechazos***\n")
            print("1-Listado de silos")
            print("2-Listado de Rechazos")
            print("0-Volver al menú anterior")
            op=input("\nIngrese una opción correcta: ")
        if(op=="1"):
            listadSiloMayorStock()
            input("Presione enter para volver al menú anterior")
        elif(op=="2"):
            listadoRechazos()
            input("Presione enter para volver al menú anterior")


# -----------------------------------------------------------------------------------------
# --------------------------------------- PRODUCTOS ---------------------------------------
# -----------------------------------------------------------------------------------------

# procedimiento
# archivoProductos, rutaProductos -> ver variables del programa principal
# tamArch = integer
# producto = registro de tipo producto
# ------------------------ NO TOCAR, YA ESTÁ OK ------------------------
def printProductosRegistrados():
    global archivoProductos, rutaProductos
    tamArch = os.path.getsize(rutaProductos)
    if (tamArch == 0):
        print("Lista vacía")
    else:
        titulo = '-' * 46 + '\n'
        titulo += '{:<10}'.format('Código')
        titulo += '{:<30}'.format('Nombre')
        titulo += 'Estado'
        titulo += '\n' + '-' * 46
        print(titulo)
        archivoProductos.seek(0,0)
        while archivoProductos.tell() < tamArch:
            producto: Producto = pickle.load(archivoProductos)
            print(producto)

def hayProductosActivos():
    global rutaProductos, archivoProductos
    tamArch = os.path.getsize(rutaProductos)
    if(tamArch == 0):
        return False
    else:
        hayProductos = False
        archivoProductos.seek(0)
        while(not hayProductos and archivoProductos.tell() < tamArch):
            producto: Producto = pickle.load(archivoProductos)
            if(producto.estado == 'A'):
                hayProductos = True
        return hayProductos

def esProductoActivo(codigoProducto):
    global rutaProductos, archivoProductos
    posic = getPosicionProducto(codigoProducto)
    if posic == -1:
        return False
    else:
        archivoProductos.seek(posic, 0)
        producto: Producto = pickle.load(archivoProductos)
        if producto.estado == 'A':
            return True
        else: 
            return False

# procedimiento
# opcion = string
# i = integer
# nombreProducto = string, cuando se invoca la función esProductoRepetido es usado como parámetro real
# productos -> ver variables del programa principal
def productosAlta():
    global archivoProductos, rutaProductos
    opcion = "S"
    while opcion == "S":
        limpiarPantalla()
        print("*** MENÚ DE OPCIONES - PRODUCTOS - ALTA ***\n")
        ultimoRegistro = getUltimoProducto()
        producto = Producto()
        if (ultimoRegistro != None):
            producto.codigo = int(ultimoRegistro.codigo) + 1
        else:
            producto.codigo = 1
        producto.nombre = input("Ingrese el nombre del nuevo producto (No se permiten duplicados): ").upper()
        while esNombreProductoUsado(producto.nombre):
            limpiarPantalla()
            print("*** MENÚ DE OPCIONES - PRODUCTOS - ALTA ***\n")
            producto.nombre = input("Ya existe un producto con ese nombre, ingrese otra opción: ").upper()
        formatearProducto(producto)
        archivoProductos.seek(0,2)
        pickle.dump(producto, archivoProductos)
        archivoProductos.flush()
        opcion = input("¿Desea registrar otro producto? (S para sí o N para no): ").upper()
        while(opcion != "S" and opcion != "N"):
            error()
            opcion = input("¿Desea registrar un producto? (S para sí o N para no): ").upper()

# procedimiento
# opcion = string
# numero = integer, (numero-1) es usado como parámetro real cuando se invoca a la función esProductoUsado
# productos -> ver variables del programa principal
def productosBaja():
    global archivoProductos, rutaProductos
    if os.path.getsize(rutaProductos) == 0:
        limpiarPantalla()
        print("*** MENÚ DE OPCIONES - PRODUCTOS - BAJA ***\n")
        print("No hay productos registrados para dar de baja.")
        input("\nPresione enter para volver al menú anterior")
    else:
        opcion = "S"
        while opcion == "S":
            limpiarPantalla()
            print("*** MENÚ DE OPCIONES - PRODUCTOS - BAJA ***\n")
            printProductosRegistrados()
            codigo = input("\nIngrese el código de producto que quiere dar de baja: ")
            posic = getPosicionProducto(codigo)
            while posic == -1:
                limpiarPantalla()
                print("*** MENÚ DE OPCIONES - PRODUCTOS - BAJA ***\n")
                printProductosRegistrados()
                codigo = input("\nDebe ingresar un código de producto válido: ")
                posic = getPosicionProducto(codigo)
            archivoProductos.seek(posic, 0)
            producto = pickle.load(archivoProductos)
            if(str(producto.estado) == "A"):
                producto.estado = "B"
                archivoProductos.seek(posic, 0)
                pickle.dump(producto, archivoProductos)
                archivoProductos.flush()
                limpiarPantalla()
                print("*** MENÚ DE OPCIONES - PRODUCTOS - BAJA ***\n")
                printProductosRegistrados()
                print(f"\nRegistro {str(producto.nombre).strip()} dado de baja exitosamente.\n")
            else:
                print("El producto ya se encuentra dado de baja.")
            opcion = input("¿Desea dar de baja otro producto? (S para sí o N para no): ").upper()
            while(opcion != "S" and opcion != "N"):
                error()
                opcion = input("¿Desea dar de baja otro producto? (S para sí o N para no): ").upper()

# procedimiento
# opcion = string
# numero = integer
# nombreProducto = string
# productos -> ver variables del programa principal
def productosModificacion():
    global archivoProductos, rutaProductos
    opcion = "S"
    while opcion == "S":
        limpiarPantalla()
        print("*** MENÚ DE OPCIONES - PRODUCTOS - MODIFICACIÓN ***\n")
        if (os.path.getsize(rutaProductos) == 0):
            print("No hay productos registrados para modificar")
            input("\nPresione enter para volver al menú anterior")
            opcion = "N"
        else:
            printProductosRegistrados()
            codigo = input("\nIngrese el código del producto que quiere modificar: ")
            posicReg = getPosicionProducto(codigo)
            while posicReg == -1:
                limpiarPantalla()
                print("*** MENÚ DE OPCIONES - PRODUCTOS - MODIFICACIÓN ***\n")
                printProductosRegistrados()
                codigo = input("\nDebe ingresar un código de producto existente: ")
                posicReg = getPosicionProducto(codigo)
            # --------------------- HAY QUE CHEQUEAR QUE NO SE ESTÉ USANDO, EN CASO DE QUE YA SE HAYA USADO
            # --------------------- PREGUNTAR SI ESTÁ SEGURO DE MODIFICAR Y ACLARAR QUE SE MODIFICARÁN LOS
            # --------------------- REGISTROS VINCULADOS A ÉL
            archivoProductos.seek(posicReg,0)
            producto = pickle.load(archivoProductos)
            limpiarPantalla()
            print("*** MENÚ DE OPCIONES - PRODUCTOS - MODIFICACIÓN ***\n")
            nombre = input(f"Ingrese un nuevo nombre para el producto {str(producto.codigo).strip()} - {producto.nombre.strip()}: ").upper()
            while esNombreProductoUsado(nombre):
                nombre = input(f"Debe ingresar un nombre nuevo distinto a los ya persistidos: ").upper()
            producto.nombre = nombre
            formatearProducto(producto)
            archivoProductos.seek(posicReg, 0)
            pickle.dump(producto, archivoProductos)
            archivoProductos.flush()
            opcion = input("¿Desea modificar otro producto? (S para sí o N para no): ").upper()
            while(opcion != "S" and opcion != "N"):
                error()
                opcion = input("¿Desea modificar otro producto? (S para sí o N para no): ").upper()

# procedimiento
def productosConsulta():
    limpiarPantalla()
    print("*** MENÚ DE OPCIONES - PRODUCTOS - CONSULTA ***\n")
    printProductosRegistrados()
    input("\nPresione enter para volver al menú anterior")

# funcion -> return boolean
# esRepetido = boolean
# nombre = parámetro formal. string
# producto = registro de tipo Producto
# tamArch = integer
# archivoProductos, rutaProductos -> ver variables del programa principal
# ------------------------ NO TOCAR, YA ESTÁ OK ------------------------
def esNombreProductoUsado(nombre):
    global archivoProductos, rutaProductos
    tamArch = os.path.getsize(rutaProductos)
    if tamArch == 0:
        return False
    else:
        archivoProductos.seek(0,0)
        esRepetido = False
        while (archivoProductos.tell() < tamArch and not esRepetido):
            producto: Producto = pickle.load(archivoProductos)
            if producto.nombre.strip() == nombre.strip():
                esRepetido = True
        return esRepetido

def getUltimoProducto():
    global archivoProductos, rutaProductos
    tamArch = os.path.getsize(rutaProductos)
    if tamArch == 0:
        return None
    else:
        archivoProductos.seek(0,0)
        primerRegistro = pickle.load(archivoProductos)
        tamReg = archivoProductos.tell()
        cantReg = tamArch // tamReg
        archivoProductos.seek((cantReg-1) * tamReg, 0)
        ultimoRegistro = pickle.load(archivoProductos)
        return ultimoRegistro

def getPosicionProducto(codigo):
    global archivoProductos, rutaProductos
    tamArch = os.path.getsize(rutaProductos)
    if (tamArch == 0):
        return -1
    else:
        archivoProductos.seek(0)
        producto = pickle.load(archivoProductos)
        tamReg = archivoProductos.tell()
        cantReg = tamArch // tamReg
        min = 0
        max = cantReg - 1
        while min <= max:
            pivote = math.floor((min + max) / 2)
            archivoProductos.seek(pivote * tamReg, 0)
            producto = pickle.load(archivoProductos)
            if str(producto.codigo).strip() == str(codigo).strip():
                return pivote * tamReg
            elif str(producto.codigo).strip() > str(codigo).strip():
                max = pivote - 1
            else:
                min = pivote + 1
        else:
            return -1


# -----------------------------------------------------------------------------------------
# ----------------------------------------- RUBROS ----------------------------------------
# -----------------------------------------------------------------------------------------

def printRubrosRegistrados():
    global archivoRubros, rutaRubros
    tamArch = os.path.getsize(rutaRubros)
    if (tamArch == 0):
        print("Aún no se han registrado rubros.")
    else:
        titulo = '-' * 34 + '\n'
        titulo += '{:<7}'.format('Código')
        titulo += '{:<27}'.format('Nombre')
        titulo += '\n' + '-' * 34
        print(titulo)
        archivoRubros.seek(0)
        while archivoRubros.tell() < tamArch:
            rubro = pickle.load(archivoRubros)
            print(rubro)

def consultaRubros():
    limpiarPantalla()
    print("*** MENÚ DE OPCIONES - RUBRO - CONSULTA ***\n")
    printRubrosRegistrados()
    input("\nPresione enter para volver al menú anterior")

def rubro():
    global archivoRubros, rutaRubros
    opcion = "S"
    while(opcion == "S"):
        limpiarPantalla()
        print("*** MENÚ DE OPCIONES - RUBRO - ALTA ***\n")
        rubro = Rubro()
        rubro.nombre = input("Ingrese nombre del rubro (no se permiten duplicados): ").upper()
        while esNombreRubroUsado(rubro.nombre) or rubro.nombre == '':
            rubro.nombre = input("Ingrese un nombre de producto válido (no se permiten duplicados): ").upper()
        tamArch = os.path.getsize(rutaRubros)
        if(tamArch == 0):
            rubro.codigo = 1
        else:
            archivoRubros.seek(0)
            rubroAux = pickle.load(archivoRubros)
            tamReg = archivoRubros.tell()
            cantReg = tamArch // tamReg
            archivoRubros.seek(-tamReg, 2)
            rubroAux = pickle.load(archivoRubros)
            rubro.codigo = int(rubroAux.codigo) + 1
        formatearRubro(rubro)
        archivoRubros.seek(0,2)
        pickle.dump(rubro, archivoRubros)
        archivoRubros.flush()
        print("Alta exitosa.\n")
        opcion = input("Desea dar de Alta otro Rubro? Ingrese S/N: ").upper()
        while(opcion != "S" and opcion != "N"):
            opcion = input("Opcion invalida. Ingrese S/N: ").upper()

def esNombreRubroUsado(nombre):
    global archivoRubros, rutaRubros
    tamArch = os.path.getsize(rutaRubros)
    if tamArch == 0:
        return False
    else:
        archivoRubros.seek(0,0)
        esRepetido = False
        while (archivoRubros.tell() < tamArch and not esRepetido):
            rubro = pickle.load(archivoRubros)
            if rubro.nombre.strip() == nombre.strip():
                esRepetido = True
        return esRepetido

def getPosicionRubro(codigo):
    global archivoRubros, rutaRubros
    tamArch = os.path.getsize(rutaRubros)
    if (tamArch == 0):
        return -1
    else:
        archivoRubros.seek(0)
        rubro = pickle.load(archivoRubros)
        tamReg = archivoRubros.tell()
        cantReg = tamArch // tamReg
        min = 0
        max = cantReg - 1
        while min <= max:
            pivote = math.floor((min + max) / 2)
            archivoRubros.seek(pivote * tamReg, 0)
            rubro = pickle.load(archivoRubros)
            if str(rubro.codigo).strip() == str(codigo).strip():
                return pivote * tamReg
            elif str(rubro.codigo).strip() > str(codigo).strip():
                max = pivote - 1
            else:
                min = pivote + 1
        else:
            return -1


# -----------------------------------------------------------------------------------------
# ---------------------------------- RUBROS POR PRODUCTO ----------------------------------
# -----------------------------------------------------------------------------------------

def existeRelacion(codigoProducto, codigoRubro):
    global archivoRubxProd, rutaRubxProd
    tamArch = os.path.getsize(rutaRubxProd)
    if(tamArch == 0):
        return False
    else:
        existe = False
        archivoRubxProd.seek(0)
        while archivoRubxProd.tell() < tamArch:
            rubXProd: Rubro_X_Producto = pickle.load(archivoRubxProd)
            if str(rubXProd.codigo_producto).strip() == str(codigoProducto).strip() and str(rubXProd.codigo_rubro).strip() == str(codigoRubro).strip():
                existe = True
        return existe
        
def productoTieneRubros(codigoProducto):
    global archivoRubxProd, rutaRubxProd
    tamArch = os.path.getsize(rutaRubxProd)
    if tamArch == 0:
        return False
    else:
        tieneRubro = False
        archivoRubxProd.seek(0)
        while not tieneRubro and archivoRubxProd.tell() < tamArch:
            registro: Rubro_X_Producto = pickle.load(archivoRubxProd)
            if(str(registro.codigo_producto).strip() == str(codigoProducto).strip()):
                tieneRubro = True
        return tieneRubro

def rubrosXproducto():
    global rutaProductos, archivoRubxProd, rutaRubros, archivoRubros
    opcion = "S"
    while opcion == "S":
        limpiarPantalla()
        print("*** MENÚ DE OPCIONES - RUBROS POR PRODUCTOS - ALTA ***\n")
        tamArchProductos = os.path.getsize(rutaProductos)
        tamArchRubros = os.path.getsize(rutaRubros)
        if (not hayProductosActivos() or tamArchRubros == 0):
            opcion = "N"
            print("Se debe contar al menos con un producto y un rubro activos para asociarlos.\n")
            input("Presione enter para volver al menú anterior.")
        else:
            printProductosRegistrados()
            opcionProducto = input("\nIngrese el código del producto al que quiere relacionarle un rubro: ")
            posicProducto = getPosicionProducto(opcionProducto)
            while posicProducto == -1 or not esProductoActivo(opcionProducto):
                opcionProducto = input("Ingrese un código de producto válido y que no se encuentre dado de baja: ")
                posicProducto = getPosicionProducto(opcionProducto)
            archivoProductos.seek(posicProducto, 0)
            producto = pickle.load(archivoProductos)
            
            printRubrosRegistrados()
            opcionRubro = input(f"\nIngrese el código del rubro que quiere vincular con el producto {str(producto.nombre).strip()}: ")
            posicRubro = getPosicionRubro(opcionRubro)
            while posicRubro == -1:
                opcionRubro = input("Ingrese un código de rubro válido: ")
                posicRubro = getPosicionRubro(opcionRubro)
            archivoRubros.seek(posicRubro, 0)
            rubro = pickle.load(archivoRubros)

            if existeRelacion(producto.codigo, rubro.codigo):
                print(f"Ya existe una relación entre {str(producto.nombre).strip()} y {str(rubro.nombre).strip()}")
            else:
                minimo = insertFloat("Ingrese el mínimo valor aceptable (entre 0.00 y 100.00): ")
                while(validarRangoReales(minimo, 0.00, 100.00)):
                    minimo = insertFloat("Ingrese un valor válido (entre 0.00 y 100.00): ")
                maximo = insertFloat(f"Ingrese el máximo valor aceptable (entre {minimo} y 100.00): ")
                while(validarRangoReales(maximo, minimo, 100.00)):
                    maximo = insertFloat(f"Ingrese un valor válido (entre {minimo} y 100.00): ")

                rubroXProducto = Rubro_X_Producto()
                rubroXProducto.codigo_producto = producto.codigo
                rubroXProducto.codigo_rubro = rubro.codigo
                rubroXProducto.min = minimo
                rubroXProducto.max = maximo

                formatearRubrosXProductos(rubroXProducto)
                archivoRubxProd.seek(0,2)
                pickle.dump(rubroXProducto, archivoRubxProd)
                archivoRubxProd.flush()

            opcion = input("¿Desea dar de alta otro rubro por producto? S/N: ").upper()
            while(opcion != "S" and opcion != "N"):
                opcion = input("Opcion inválida. Ingrese S/N : ").upper()
            
# -----------------------------------------------------------------------------------------
# ----------------------------------------- SILOS -----------------------------------------
# -----------------------------------------------------------------------------------------
def validarProductoSilo(codigoProducto):
    tamArch=os.path.getsize(rutaSilos)
    RegSilos=Silo()
    archivoSilos.seek(0,0)
    while(tamArch>archivoSilos.tell()):
        RegSilos=pickle.load(archivoSilos)
        if(int(RegSilos.codigo_producto)==int(codigoProducto)):
            return True
    return False


def getPosicionSilos(codigoProducto):
    global rutaSilos, archivoSilos
    tamArch = os.path.getsize(rutaSilos)
    if(tamArch == 0):
        return -1
    else:
        archivoSilos.seek(0)
        encontrado = -1
        while archivoSilos.tell() < tamArch and encontrado == -1:
            posicionAntesDeLeer = archivoSilos.tell()
            silo: Silo = pickle.load(archivoSilos)
            if(str(silo.codigo_producto).strip() == str(codigoProducto).strip()):
                encontrado = posicionAntesDeLeer
        return encontrado

def silos():
    global archivoSilos
    silosAux = Silo()
    opcion = "S"
    while(opcion == "S"):
        limpiarPantalla()
        print("*** MENÚ DE OPCIONES - SILOS - ALTA ***\n")
        ultimoRegistro = getUltimoProducto()
        if (ultimoRegistro != None):
            silosAux.codigo = int(ultimoRegistro.codigo) + 1
        else:
            silosAux.codigo = 1
        printProductosRegistrados()
        codDeProducto = input("\nIngrese el código del producto al que quiere asignarle un silo: ")
        posic = getPosicionProducto(codDeProducto)
        while posic == -1 or not esProductoActivo(codDeProducto):
            limpiarPantalla()
            print("*** MENÚ DE OPCIONES - SILOS - ALTA ***\n")
            printProductosRegistrados()
            codDeProducto = input("\nDebe ingresar un código de producto válido y que se encuentre activo: ")
            posic = getPosicionProducto(codDeProducto)
        if(validarProductoSilo(codDeProducto)):
            limpiarPantalla()
            print("*** MENÚ DE OPCIONES - SILOS - ALTA ***\n")
            print("Ya exite un silo para ese producto \n")
        else:
            nombre = input("\nIngrese un nombre para el silo: ").upper()
            silosAux.codigo_producto = codDeProducto
            silosAux.nombre = nombre
            formatearSilo(silosAux)
            archivoSilos.seek(0,2)
            pickle.dump(silosAux, archivoSilos)
            archivoSilos.flush()
            print("\nAlta exitosa\n")
        opcion = input("Desea dar de Alta otro Silo? Ingrese S/N : ").upper()
        while(opcion != "S" and opcion != "N"):
            opcion = input("Opcion inválida, ingrese S(sí) o N(no)").upper()

# -----------------------------------------------------------------------------------------
# ----------------------------------------- OTROS -----------------------------------------
# -----------------------------------------------------------------------------------------

def validarRangoReales(nro, desde, hasta):
    try:
        if float(nro)>=desde and float(nro)<=hasta:
            return False
        else:
            return True
    except:
        return True

def validarRangoEnteros(nro, desde, hasta):
    try:
        if isInteger(nro) and int(nro) >= desde and int(nro) <= hasta:
            return False
        else:
            return True
    except:
        return True

# funcion -> return archivo
# ruta = string
def abrirArchivo(ruta):
    if (os.path.exists(ruta)):
        return open(ruta, 'r+b')
    else:
        return open(ruta, 'w+b')

# procedimiento
def limpiarPantalla():
    if os.name in ('nt', 'dos'):  # Si el sistema operativo es Windows
        os.system("cls")
    else:
        os.system("clear")  # Si el sistema operativo es Mac o Linux

# procedimiento
def construccion():
    limpiarPantalla()
    print("\nEsta funcionalidad está en construcción")
    input("\nPresione enter para volver al menú anterior")

# procedimiento
def error():
    print("***********************************")
    print("*              ERROR              *")
    print("* Debe ingresar una opción válida *")
    print("***********************************")





# funcion -> return boolean
# numString = string
def isInteger(numString):
    try:
        float(numString)
    except ValueError:
        return False
    else:
        return float(numString).is_integer()

# funcion -> return boolean
# numString = string
def isFloat(numString):
    try:
        float(numString)
    except ValueError:
        return False
    else:
        return True

# funcion -> return float
# mensajeInicial = string
# numString = string
# numFloat = float
def insertFloat(mensajeInicial):
    numString = input(mensajeInicial)
    while (not isFloat(numString)):
        numString = input("Ingrese un número decimal válido: ")
    numFloat = float(numString)
    return numFloat



# funcion -> return integer
# mensajeInicial = string
# numString = string
# numInt = integer
def insertInt(mensajeInicial):
    numString = input(mensajeInicial)
    while (not isInteger(numString) or int(float(numString)) < 0):
        numString = input("Ingrese un número entero natural válido: ")
    numInt = int(float(numString))
    return numInt

def insertFecha(mensajeInicial):
    fechaValida = False
    fecha = input(mensajeInicial)
    try:
        datetime.datetime.strptime(fecha, '%d/%m/%Y')
        fechaValida = True
    except ValueError:
        while not fechaValida:
            try:
                fecha = input("Ingresa una fecha con formato dd/mm/aaaa: ")
                datetime.datetime.strptime(fecha, '%d/%m/%Y')
                fechaValida = True
            except ValueError:
                pass
    return fecha

def esHoy(fecha):
    return fecha == datetime.date.today().strftime("%d/%m/%Y")



# -----------------------------------------------------------------------------------------
# ---------------------------------------- MENUES -----------------------------------------
# -----------------------------------------------------------------------------------------




# procedimiento
# opcion = string
def administraciones():
    opcion = "A"
    while opcion != "V":
        limpiarPantalla()
        printMenuAdministraciones()
        opcion = input("\nIngrese una opcion: ").upper()
        while (opcion != "A" and opcion != "B" and opcion != "C" and opcion != "D" and opcion != "E" and opcion != "F"
               and opcion != "G" and opcion != "V"):
            error()
            opcion = input("Ingrese una opcion: ").upper()
        if opcion == "A":
            menuOpciones("TITULARES")
        elif opcion == "B":
            menuOpciones("PRODUCTOS")
        elif opcion == "C":
            menuOpciones("RUBROS")
        elif opcion == "D":
            menuOpciones("RUBROS POR PRODUCTO")
        elif opcion == "E":
            menuOpciones("SILOS")
        elif opcion == "F":
            menuOpciones("SUCURSALES")
        elif opcion == "G":
            menuOpciones("PRODUCTO POR TITULAR")





# procedimiento
# opcion = string
def menuOpciones(seccion):
    opcion = "A"
    while opcion != "V":
        limpiarPantalla()
        printMenuOpciones(seccion)
        opcion = input("\nIngrese una opcion: ").upper()
        while (opcion != "A" and opcion != "B" and opcion != "C" and opcion != "M" and opcion != "V"):
            limpiarPantalla()
            printMenuOpciones(seccion)
            error()
            opcion = input("Ingrese una opcion válida: ").upper()
        if opcion != "V":    
            if seccion == "SILOS" and opcion == "A":
                silos()
            elif seccion == "RUBROS" and opcion == "A":
                rubro()
            elif seccion == "RUBROS" and opcion == "C":
                consultaRubros()
            elif seccion == "RUBROS POR PRODUCTO" and opcion == "A":
                rubrosXproducto()
            elif seccion == "PRODUCTOS":
                if opcion == "A":
                    productosAlta()
                elif opcion == "B":
                    productosBaja()
                elif opcion == "C":
                    productosConsulta()
                elif opcion == "M":
                    productosModificacion()
            else:
                construccion()

# -----------------------------------------------------------------------------------------
# ---------------------------------- PROGRAMA PRINCIPAL -----------------------------------
# -----------------------------------------------------------------------------------------

rutaRaiz = os.path.dirname(__file__) #nos da la ruta en donde esté el .py
rutaFiles = os.path.abspath(rutaRaiz+'/files')
if not os.path.exists(rutaFiles): # si la carpeta files no existe la creamos
    os.makedirs(rutaFiles)
rutaProductos = os.path.abspath(rutaFiles+'/productos.dat')
rutaSilos = os.path.abspath(rutaFiles+'/silos.dat')
rutaOperaciones = os.path.abspath(rutaFiles+'/operaciones.dat')
rutaRubros = os.path.abspath(rutaFiles+'/rubros.dat')
rutaRubxProd = os.path.abspath(rutaFiles+'/rubxprod.dat')
archivoProductos = abrirArchivo(rutaProductos)
archivoSilos = abrirArchivo(rutaSilos)
archivoOperaciones = abrirArchivo(rutaOperaciones)
archivoRubros = abrirArchivo(rutaRubros)
archivoRubxProd = abrirArchivo(rutaRubxProd)

# opcion = string
opcion = "1"
while opcion != "0":
    limpiarPantalla()
    printMenuPrincipal()
    opcion = input("\nIngrese una opcion: ")
    while validarRangoEnteros(opcion, 0, 9):
        error()
        opcion = input("Ingrese una opción: ")
    if opcion == "1":
        administraciones()
    elif opcion == "2":
        entregaDeCupo()
    elif opcion == "3":
        recepcion()
    elif opcion == "4":
        registrarCalidad()
    elif opcion == "5":
        registrarPesoBruto()
    elif opcion == "6":
        construccion()
    elif opcion == "7":
        registrarTara()
    elif opcion == "8":
        reportes()
    elif opcion == "9":
        listadoSilosYRechazos()
    else:
        print()
        archivoProductos.close()
        archivoSilos.close()
        archivoOperaciones.close()
        archivoRubros.close()
        archivoRubxProd.close()
        print("Gracias por visitarnos")