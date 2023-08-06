# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 10:29:45 2022

@author: 50381
"""
# V1: July 18 th 2022 - Created - Jaime Dwaigth Pinzon Casallas- 
# Version: 0.0.1 2023-06-29 Entrada en producción


# Import Libraries


import pyodbc
import json
import pandas as pd
import math as m
import requests #APIs
from pandas import json_normalize
import pytz #Cambio de zonas horarias

#----------------------------------------------------------------------
#---------------Funciones----------------------------------------------
#----------------------------------------------------------------------
class ConsultaPmu:
    
       
    
    def __init__(self, Initime, Endtime, Var, Ph_DSN, Ph_UID, Ph_PWD, Adm_DSN, Adm_UID, Adm_PWD, Ip_api, Tension = 0, Equipo = 0, Pmu_id = 0):
        '''Definicion de Variables iniciales para la clase'''
        self.PhUID = Ph_UID                                                                    # Nombre de usuraio phasorpoint
        self.PhPWD = Ph_PWD                                                                    # Contraseña phasorpoint
        self.PhDSN = Ph_DSN                                                                    # Nombre Driver para la conexión
        self.AdmUID = Adm_UID                                                                  # Nombre de usuario AdminWams Azure
        self.AdmPWD = Adm_PWD                                                                  # Contraseña AdminWams Azure
        self.AdmDSN = Adm_DSN                                                                  # Nombre Driver para la conexión
        self.initime = Initime                                                                 # Tiempo inicial para la consulta de datos
        self.endtime = Endtime                                                                 # Tiempo final para la consulta de datos
        self.var = Var                                                                         # Variable a consultar frecuencia: f, df/dt: dfdt, va_m, vb_m, v_m, va_a, v_a, vb_a, p, q, ia_m, ib_m, ic_m, i_m, ia_a, ib_a, ic_a, i_a
        self.tension = Tension                                                                 # Nivel de tensión (500,345,230,220,138,110,34,22,18) o para consultar todas las PMU (0)
        self.equipo = Equipo                                                                   # Equipo a consultar (opcional- cero es todos)
        self.pmu_id = Pmu_id
        self.ip_api = Ip_api                                                                   # Lista de IDs de las PMU
        '''output - dataframe with the vaiables required with timestamp taking to account the filters enter by the user'''
    
    def ApiPhasor(self):
        '''
        Función para consulta con API de la estructura de datos operativos con el fin de conocer el nombre real de las variables con la cual se haría las consultas en SQL
        
        Parameters
        ----------
        username : Str
            Nombre usuario phasorpoint.
        password : Str
            Contraseña credenciales phasorpoint.
        self.ip_api: Str
            IP y puerto para la conexión a la API de phsor point operacional "IP:puerto"
        Returns
        -------
        dfmeasure: DataFrame
            Tabla con las variables operativas con su nombre, pmu_id, entre otros (se usa está tabla para luego obtener los nombres de las tablas de históricos)

        '''
        username= self.PhUID
        password= self.PhPWD
        ip_api= self.ip_api
        s = requests.Session()
        url = "https://"+ip_api+"/eterra-rs/live/v1/authenticate"
        response = s.post(url, data={"Username": username, "Password": password}, verify=False)
        #print(response.status_code)   #print(response.headers)
        head = response.headers['Set-Cookie']
        #print(head)
        
        sessionid = head.split(';') #Extraer el session ID
        url_config = "https://"+ip_api+"/eterra-rs/live/v1/configuration"
        response_config = s.get(url_config, headers={"header": sessionid[0]}, verify=False)
        #print(response_config.status_code) #print(response_config.content) #print(type(response_config))
        
        varstruc = json.loads(response_config.content.decode("utf-8")) # convertir de type "bytes array" a JSON
        dfmeasure =pd.DataFrame() 
        for measure in varstruc ["measurements"]:                       # ORganiza todas las medidas de todas las PMU operativas en un dataframe con la info de pmu_id, stationname, channelname (var name), type
            df = json_normalize(measure["source"]["details"])
            dfmeasure = pd.concat([dfmeasure, df]) 
        return(dfmeasure)
    
    # Limpieza de los datos operativos  para obtener dataframe con nombres de los fasores de tensión y corriente de cada PMU    
    def clean_operdata (self, dfmeasure):
        var_list = ["VOLTAGE_PHASOR", "CURRENT_PHASOR"] #"FREQUENCY", "DFDT",
        dfmeasure.query('type in @var_list',inplace =True)              #1) en el type filtrar "FREQUENCY", "DFDT", "VOLTAGE_PHASOR", "CURRENT_PHASOR"
        dfmeasure.drop_duplicates(inplace=True)                         #2) Eliminar duplicados de channel name discriminado por pmu id (para no elimianr los f y dfdt que tienen el mismo nombre para todas las PMU)
        dfmeasure = dfmeasure.rename(columns={"stationName": "station_name", "channelName": "phasor_name"}) #3) Cambiar nombres de columnas
        dfmeasure = dfmeasure[['id','station_name', 'phasor_name', 'type']]
        dfmeasure = dfmeasure.reset_index(drop=True)
        dfmeasure["phasor_name"] = dfmeasure["phasor_name"].astype(str)
        sym =[' + ', '  ', '-', '+ ', ' ']
        for i in sym:                                                   #3) convertir caracteres " + ", "  ", "-", "+ ", " " en "_"
            dfmeasure["phasor_name"]= dfmeasure["phasor_name"].map(lambda x: x.replace(i , '_'))
            
        dfmeasure["phasor_name"]= dfmeasure["phasor_name"].str.lower()  #Cambiar a minúscula ya que los nombres de las variables en hist pmu están en minus
        pd.options.mode.chained_assignment = None                       ## disable chained assignments
        dfmeasure['var_name'] =""
        for i in range(0,len(dfmeasure["phasor_name"])):                ## si inicia por "va", si termina en "_a", si es igual a "tension1" and type=voltage_phasor; si inicia por "ia", si termina en "_a" and type=current_phasor
            if dfmeasure.type[i] == 'VOLTAGE_PHASOR' :
                 if dfmeasure.phasor_name[i].startswith('va') or dfmeasure.phasor_name[i].endswith('_a') or dfmeasure.phasor_name[i] == 'tension1':
                    dfmeasure.var_name[i]="va"
                 elif  dfmeasure.phasor_name[i].startswith('vb') or dfmeasure.phasor_name[i].endswith('_b') or dfmeasure.phasor_name[i] == 'tension2':    
                    dfmeasure.var_name[i]="vb"
                 elif  dfmeasure.phasor_name[i].startswith('vc') or dfmeasure.phasor_name[i].endswith('_c') or dfmeasure.phasor_name[i] == 'tension3':
                    dfmeasure.var_name[i]="vc"
                 else:
                     dfmeasure.var_name[i]="v"
            else:
                 if dfmeasure.phasor_name[i].startswith('ia') or dfmeasure.phasor_name[i].endswith('_a') or dfmeasure.phasor_name[i] =='i1':
                    dfmeasure.var_name[i]="ia"
                 elif  dfmeasure.phasor_name[i].startswith('ib') or dfmeasure.phasor_name[i].endswith('_b') or dfmeasure.phasor_name[i] =='i2':
                    dfmeasure.var_name[i]="ib"
                 elif  dfmeasure.phasor_name[i].startswith('ic') or dfmeasure.phasor_name[i].endswith('_c') or dfmeasure.phasor_name[i] =='i3':
                    dfmeasure.var_name[i]="ic"
                 else:
                     dfmeasure.var_name[i]="i"
                     
        return (dfmeasure)
        
    
    #Función para consultar id PMUs de acuerdo con tipo de activo monitoreado
    #medida_id -> 1=Autotransformador, 2=Barra, 3=capacitorshunt, 4=capacitorserie,5=carga, 6=generador, 7, reactor
                #8=reactordelinea, 9=transformador, 10=SVC, 11=solar, 12=linea, 15=eolico
    def QueryAdmin(self, query=''):
        '''
        Función consulta de datos de admin de WAMS (funcionando) se puede realizar consultas SQl su argumento es el query en formato de consulta SQL "SELECT... FROM... WHERE..."
        Parámetros: query, AdmUID, AdmPWD, AdmDSN
        '''
        
        server = 'dbmdcbackupserver.database.windows.net'
        database = self.AdmDSN
        username = self.AdmUID
        password = self.AdmPWD
        driver= '{ODBC Driver 17 for SQL Server}'
        connec_admwams = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
        dfpmudb = pd.read_sql_query(query, connec_admwams)
        return(dfpmudb)
        
    def QueryInfopmu (self):
        '''
        Función consulta de parametrización de bases de datos de pmu de acuerdo a datos de entrada como nivel de tensión (500,345,230,220,138,110,34,22,18), equipo medido
        Parámetros: self.tension, self.equipo
        '''
        dfnivelkv = self.QueryAdmin("SELECT * FROM dbo.NIVELKV")                            #Consulta base de datos de mapeo de niveles de tensión con su puntero o id
        dnivelkv =  dict([(i,a) for i,a in zip(dfnivelkv['nivelkv'], dfnivelkv['Id'])])     #Conversion de dataframe de niveles de tensión a diccionario -> ej: dnivelkv [500]  da como resultado 1 lo cual siginifica que el id 1 es el puntero  a ese nivelkv en la bd PMU  
        dnivelkv['0'] = "%"                                                                 #Cuando no se especifica nivelkv se utilizria el % para el query (es decir todos)
        dfequipo = self.QueryAdmin("SELECT * FROM dbo.MEDIDA")                              #Consulta base de datos de mapeo de tipos de quipos monitoreados con su puntero o id
        dequipo =  dict([(i,a) for i,a in zip(dfequipo['mide'], dfequipo['Id'])])           #Conversion de dataframe de niveles de tensión a diccionario -> ej: dnivelkv [500]  da como resultado 1 lo cual siginifica que el id 1 es el puntero  a ese nivelkv en la bd PMU  
        dequipo['0'] = "%"
        QInfopmu = "SELECT pmuid FROM dbo.PMU WHERE (nivelkv_id LIKE '" + str(dnivelkv[self.tension]) + "' AND medida_id LIKE '" + str(dequipo[self.equipo]) + "')"
        dfinfopmu = self.QueryAdmin (QInfopmu)
        return (dfinfopmu)
    
    def get_var_names (self, phasor_names, dfinfopmu):                                   #con las pmuid y variables que se requieren consultar construir el nombre de las tablas en una columna agregada llamada table_name del objeto de salida vari_names
        '''
        Función para construir data frame con los nombres de variables a consultar y el nombre de la tabla en phasorpoint
        Parámetros: phasor_names, dfinfopmu, self.var
        '''
        var = self.var
        
        if ('p' or 'q') in var:
            power_var = ['v_m','v_a','i_m','i_a']
            var = list(set(power_var + list(var)))
        vari_names=pd.DataFrame()
        for id_pmu in dfinfopmu:
            for vari in var:
                if vari == 'va_m':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & (phasor_names['var_name'] == 'va')]
                    a['table_name'] = 'v_'+ a['phasor_name'] +'_m'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'va_a':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & (phasor_names['var_name'] == 'va')]
                    a['table_name'] = 'v_'+ a['phasor_name'] +'_a'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'vb_m':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & (phasor_names['var_name'] == 'vb')]
                    a['table_name'] = 'v_'+ a['phasor_name'] +'_m'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'vb_a':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & (phasor_names['var_name'] == 'vb')]
                    a['table_name'] = 'v_'+ a['phasor_name'] +'_a'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'vc_m':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & (phasor_names['var_name'] == 'vc')]
                    a['table_name'] = 'v_'+ a['phasor_name'] +'_m'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'vc_a':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & (phasor_names['var_name'] == 'vc')]
                    a['table_name'] = 'v_'+ a['phasor_name'] +'_a'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'v_m':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & ((phasor_names['var_name'] == 'v') |(phasor_names['var_name'] == 'va')) ]
                    a['var_name'] = 'v'
                    a['table_name'] = 'v_'+ a['phasor_name'] +'_m'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'v_a':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & ((phasor_names['var_name'] == 'v') |(phasor_names['var_name'] == 'va'))]
                    a['var_name'] = 'v'
                    a['table_name'] = 'v_'+ a['phasor_name'] +'_a'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'ia_m':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & (phasor_names['var_name'] == 'ia')]
                    a['table_name'] = 'i_'+ a['phasor_name'] +'_m'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'ia_a':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & (phasor_names['var_name'] == 'ia')]
                    a['table_name'] = 'i_'+ a['phasor_name'] +'_a'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'ib_m':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & (phasor_names['var_name'] == 'ib')]
                    a['table_name'] = 'i_'+ a['phasor_name'] +'_m'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'ib_a':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & (phasor_names['var_name'] == 'ib')]
                    a['table_name'] = 'i_'+ a['phasor_name'] +'_a'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'ic_m':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & (phasor_names['var_name'] == 'ic')]
                    a['table_name'] = 'i_'+ a['phasor_name'] +'_m'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'ic_a':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & (phasor_names['var_name'] == 'ic')]
                    a['table_name'] = 'i_'+ a['phasor_name'] +'_a'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'i_m':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & ((phasor_names['var_name'] == 'i') |(phasor_names['var_name'] == 'ia')) ]
                    a['var_name'] = 'i'
                    a['table_name'] = 'i_'+ a['phasor_name'] +'_m'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'i_a':
                    a = phasor_names[(phasor_names['id'] == id_pmu) & ((phasor_names['var_name'] == 'i') |(phasor_names['var_name'] == 'ia'))]
                    a['var_name'] = 'i'
                    a['table_name'] = 'i_'+ a['phasor_name'] +'_a'
                    vari_names= pd.concat([vari_names, a])
                elif vari == 'f':
                    df = pd.DataFrame.from_dict({'id': int(id_pmu), 'type':'FREQUENCY', 'var_name':'f', 'table_name': 'f'}, orient='index').T
                    vari_names= pd.concat([vari_names, df],ignore_index=True) #Version 1.0.8
                elif vari == 'dfdt':
                    df = pd.DataFrame.from_dict({'id': int(id_pmu), 'type':'DFDT', 'var_name':'dfdt', 'table_name': 'dfdt'}, orient='index').T
                    vari_names= pd.concat([vari_names, df],ignore_index=True) #Version 1.0.8
        vari_names = vari_names.reset_index(drop=True)
        vari_names['id'] = vari_names['id'].astype(int)
        return vari_names
    
        
    def StrucQuery(self):        #Estructura un Query según Tags
        '''
        Función creación de queries con su estructura (funcionando) - join query  incluyendo los fasores de tensión y corriente para el cálculo de potencias activa y reactiva
        Parámetros: self.initime, self.endtime, self.var, self.tension, self.equipo, self.pmu_id
        '''
        
        dfnivelkv = self.QueryAdmin("SELECT * FROM dbo.NIVELKV")                        # Consulta base de datos de mapeo de niveles de tensión con su puntero o id
        dnivelkv =  dict([(i,a) for i,a in zip(dfnivelkv['nivelkv'], dfnivelkv['Id'])]) # Conversion de dataframe de niveles de tensión a diccionario -> ej: dnivelkv [500]  da como resultado 1 lo cual siginifica que el id 1 es el puntero  a ese nivelkv en la bd PMU  
        dnivelkv[0] = "%"                                                               # Cuando no se especifica nivelkv se utilizria el % para el query (es decir todos)
        dfequipo = self.QueryAdmin("SELECT * FROM dbo.MEDIDA")                          # Consulta base de datos de mapeo de tipos de quipos monitoreados con su puntero o id
        dequipo =  dict([(i,a) for i,a in zip(dfequipo['mide'], dfequipo['Id'])])       # Conversion de dataframe de niveles de tensión a diccionario -> ej: dnivelkv [500]  da como resultado 1 lo cual siginifica que el id 1 es el puntero  a ese nivelkv en la bd PMU  
        dequipo[0] = "%" 
        dnivelkv_inv = dict([(a,i) for i,a in zip(dfnivelkv['nivelkv'], dfnivelkv['Id'])])
        if self.pmu_id == 0:
            QInfopmu = "SELECT pmuid FROM dbo.PMU WHERE (nivelkv_id LIKE '" + str(dnivelkv[self.tension]) + "' AND medida_id LIKE '" + str(dequipo[self.equipo]) + "' AND operativo_id = 3)"  #Query con el nivelkv, tipoequipo, y que la PMU esté operativa y en phasor point "operativo_id=3"
            dfinfopmu = self.QueryAdmin(QInfopmu)
            dfinfopmu = list(dfinfopmu['pmuid'])
        else:
            if type(self.pmu_id) ==list: 
                print('pmu_id es una lista')
                dfinfopmu = self.pmu_id
            else:
                dfinfopmu = list([self.pmu_id])
                print('pmu_id NO es una lista')
        sQuerypmu= "SELECT * FROM dbo.PMU"
        dfconfpmu= self.QueryAdmin(sQuerypmu)
        #dfconfpmu= ConsultaPmu(initime, endtime, var, PhDSN, PhUID, PhPWD,  AdDSN, AdUID, AdPWD, tension, equipo, pmu_id).QueryAdmin(sQuerypmu)
        dfconfpmu_ = dfconfpmu[dfconfpmu['pmuid'].isin(dfinfopmu)]
        linfokv = list(dfconfpmu_['nivelkv_id'].map(lambda x: dnivelkv_inv[x]))
        dfinfokv = pd.DataFrame({'pmuid': dfinfopmu, 'nivelkv':linfokv})
        self.dfinfopmu = dfinfopmu.copy()
               
        dfmeasure= self.ApiPhasor()                                                         # Consulta de datos de phasor point operacional
        phasor_names = self.clean_operdata (dfmeasure)                                      # limpieza de datos de PhaPo operacional
        phasor_exact_names = self.get_var_names (phasor_names, dfinfopmu)                   # Obtener dataframe uen el que tiene el id de pmu (id) y el nombre exacto de la tabla para consultar en el hist de PhaPo (table_name)
        phasor_exact_names['nivelkv'] = list(phasor_exact_names['id'].map(lambda x: int(dfinfokv[dfinfokv.pmuid == x].nivelkv)))
        self.phasor_exact_names = phasor_exact_names.copy()
        phasor_exact_names=phasor_exact_names.drop_duplicates(subset=['table_name']).reset_index(drop=True) #Version 1.0.8
        
        Nv = phasor_exact_names.shape[0]
        #Nv = 2
        lqueryf = [None]*Nv
        #print(phasor_exact_names)
        if len(phasor_exact_names)==0 : 
            print('Las variables requeridas de las PMU no existen o no se están alamacenando. Con esta excepción no continúa la ejecución')
            raise SystemExit
        else:
            for i in range(0,Nv):
                
                print(i, str(phasor_exact_names['id'].loc[i]),str(phasor_exact_names['table_name'].loc[i]) )
                columnsvars = "pmu_"+ str(phasor_exact_names['id'].loc[i]) +"_10." + str(phasor_exact_names['table_name'].loc[i])
                pmusname = "public.pmu_"+ str(phasor_exact_names['id'].loc[i]) +"_10"
                if i == 0:
                    defcolvars = "ts" + ", " + columnsvars
                    defpmus = pmusname
                else:
                    defcolvars = defcolvars + ", " + columnsvars
                    defpmus = defpmus + ", " + pmusname
            try:
                lqueryf = "SELECT " + defcolvars + " FROM " + defpmus +" WHERE (ts BETWEEN '" + self.initime + "' AND '" + self.endtime + "')"
                
            except: 
                print ("Error en la estructura para la consulta a la tabla" + str(phasor_exact_names['id'].loc[0])+"_10 la telemedida " + str(phasor_exact_names['table_name'].loc[0]) )
        return(lqueryf)
    
    def QueryData(self, SQLquery):
        '''
        Función para realizar la consulta de datos de PMU a la base de datos de históricos

        Parameters
        ----------
        SQLquery : Str
            Query en formato SQL.
        database : Str
            Nombre base de datos Phsorpoint.
        username : Str
            Nombre usuario phasorpoint.
        password : Str
            Contraseña credenciales phasorpoint.

        Returns
        -------
        dfpmudata : DataFrame
            Tabla con los datos consultados según query.
        '''
        
        database= self.PhDSN
        username= self.PhUID
        password= self.PhPWD
        Nv = len(SQLquery)
        #Nv= 8
        connection_phasor = pyodbc.connect('DSN='+database+';UID='+username+';PWD='+ password)
        dfpmudata =pd.DataFrame()
        if type(SQLquery) == str:                                                       #Sentencia para evaluar si el query es individual o una lista de queries (else)
            try:
               dfpmudata = pd.read_sql_query(SQLquery, connection_phasor)               #query con filtro de tiemp
            except Exception as e:
                print ("Error en la consulta singular: ", SQLquery)
                print(repr(e))
        else:
            for i in range (0,Nv):
                queryrow =SQLquery [i]
                try:
                    dfpmudata [i+1] = pd.read_sql_query(queryrow, connection_phasor)    #query con filtro de tiempo
                except Exception as e:
                    print ("Error en la consulta: ", SQLquery[i])
                    print(repr(e))
                    raise SystemExit
        return (dfpmudata)
    
    def PowerCalc (self, dfpmudata):
        '''
        Función para el cálculo de potencias activa y reactiva con los fasores de tensión y corriente

        Parameters
        ----------
        dfpmudata : DataFrame
            Tabla con los datos consultados según el query.
        self.var: list
            Lista de variables

        Returns
        -------
        power_data :DataFrame
            Tabla con las potencias calculadas

        '''
        var = self.var
        
        if ('p' or 'q') in self.var:
            dfinfopmu = self.dfinfopmu
            phasor_exact_names= self.phasor_exact_names
            power_vars=pd.DataFrame()
            power_data =pd.DataFrame()
            for i in dfinfopmu:
                try:
                    v_m = "pmu_" + str(i) + '_10.v_'+ str(phasor_exact_names[(phasor_exact_names['id'] == i) & (phasor_exact_names['type'] == 'VOLTAGE_PHASOR')].phasor_name.values[0]) + '_m'
                    v_a = "pmu_" + str(i) + '_10.v_'+ str(phasor_exact_names[(phasor_exact_names['id'] == i) & (phasor_exact_names['type'] == 'VOLTAGE_PHASOR')].phasor_name.values[0]) + '_a'
                    i_m = "pmu_" + str(i) + '_10.i_'+ str(phasor_exact_names[(phasor_exact_names['id'] == i) & (phasor_exact_names['type'] == 'CURRENT_PHASOR')].phasor_name.values[0]) + '_m'
                    i_a = "pmu_" + str(i) + '_10.i_'+ str(phasor_exact_names[(phasor_exact_names['id'] == i) & (phasor_exact_names['type'] == 'CURRENT_PHASOR')].phasor_name.values[0]) + '_a'
                    df = pd.DataFrame.from_dict({'id': int(i), 'v_m': v_m, 'v_a':v_a, 'i_m': i_m, 'i_a': i_a}, orient='index').T
                    power_vars= pd.concat([power_vars, df],ignore_index=True) #Version 1.0.8       
                    #print(power_vars)
                    power_vars['id'] = power_vars['id'].astype(int)
                    #power_data[i] = 3* dfpmudata[v_m] * dfpmudata[i_m] *m.cos(mapm.radians(dfpmudata[v_a]) - m.radians(dfpmudata[i_a])) 
                    if 'p' in var:
                        try:
                            power_data['pmu_'+str(i)+'_10.p'] = list(map(lambda v_mag, v_an, i_mag, i_an: 3 * v_mag * i_mag * m.cos(v_an - i_an), dfpmudata[v_m], dfpmudata[v_a], dfpmudata[i_m], dfpmudata[i_a])) #angulos medidos en radianes
                        except:
                            print("Una o varias de las entradas para el cálculo de P es errado de la PMU con ID:" + str(i))
                    if 'q' in var:
                        try:
                            power_data['pmu_'+str(i)+'_10.q'] = list(map(lambda v_mag, v_an, i_mag, i_an: 3 * v_mag * i_mag * m.sin(v_an - i_an), dfpmudata[v_m], dfpmudata[v_a], dfpmudata[i_m], dfpmudata[i_a]))
                        except:
                            print("Una o varias de las entrdas para el cálculo de Q es errado de la PMU con ID:" + str(i))
                except:
                    print("Una o varias de las entradas para el cálculo de potencias no existe de la PMU con ID:" + str(i))
        return(power_data)
    
    def DeleteVars (self, dfpmudata):
        dffinal = pd.DataFrame()
        dffinal ['ts'] = dfpmudata['ts']#.reset_index()
        dfinfopmu = self.dfinfopmu
        var = self.var
        phasor_exact_names= self.phasor_exact_names
        lvar= ['v_m', 'va_m', 'vb_m', 'vc_m', 'i_m', 'ia_m', 'ib_m', 'ic_m', 'v_a', 'va_a', 'vb_a', 'vc_a', 'i_a', 'ia_a', 'ib_a', 'ic_a']
        for i in dfinfopmu:
            for vari in var:
                try:
                    if vari in lvar:
                        colname = "pmu_" + str(i) + '_10.'+vari[0]+'_'+ str(phasor_exact_names[(phasor_exact_names['id'] == i) & (phasor_exact_names['var_name'] == vari[0:vari.index('_')])].phasor_name.values[0]) + '_'+vari[-1]
                        fname= str(phasor_exact_names[(phasor_exact_names['id'] == i)].nivelkv.values[0]) + "_pmu_" + str(i) + '.'+ vari
                        dfcol =pd.DataFrame(dfpmudata[colname].copy()).iloc[:,0]
                        dffinal [fname] = dfcol
                    else:
                        colname = "pmu_" + str(i) + '_10.' + vari
                        fname = str(phasor_exact_names[(phasor_exact_names['id'] == i)].nivelkv.values[0]) + "_pmu_" + str(i) + '.'+ vari
                        print(colname, fname)
                        dffinal[fname] = dfpmudata[colname]
                except: 
                    print("La variable "+ vari +" no existe, de la PMU con ID:" + str(i))    
        return(dffinal)
    
    def VoltageLine(self, dfpmudata):
        var = self.var
        volvars= ['v_m', 'va_m', 'vb_m', 'vc_m']  
        #lvoltagecol = []
        for vari in var:
            if vari in volvars:
                dfinfopmu = self.dfinfopmu
                phasor_exact_names= self.phasor_exact_names
                for i in dfinfopmu:
                    try:
                        v_m = str(phasor_exact_names[(phasor_exact_names['id'] == i)].nivelkv.values[0]) + "_pmu_" + str(i) + '.'+ vari
                        dfpmudata [v_m] = dfpmudata [v_m] * m.sqrt(3)
                    except: 
                        print("La magnitud de tensión no existe, de la PMU con ID:" + str(i))
        return(dfpmudata)    
    def convert_timezone (self, data, sColumnTime, sTimezone):
        data.index = data[sColumnTime]
        time = pytz.timezone(sTimezone)
        data.index = data.index.tz_localize(pytz.utc).tz_convert(time)
        data.drop(columns=sColumnTime, inplace=True)
        return(data)
            
    def ejecucion_consulta(self):
        lsqlquery = self.StrucQuery()
        #print(lsqlquery)
        dfpmudata = self.QueryData(lsqlquery)
        try:
            dfpower = self.PowerCalc(dfpmudata)
            dfdata =pd.concat(objs=[dfpmudata, dfpower], axis = 1)
        except:
            dfdata = dfpmudata

        dfdata_exactvars = self.DeleteVars(dfdata)
        dfdata_vl = self.VoltageLine(dfdata_exactvars)
        dffinal = self.convert_timezone(dfdata_vl, 'ts', 'Etc/GMT+5')
        return(dffinal)
