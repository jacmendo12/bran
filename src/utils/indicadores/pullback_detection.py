import math
import numpy as np

class PullbackDetection:
    def __init__(self, data, minimum_tresure=2.1):
        self.data = data
        self.minimum_tresure = minimum_tresure


    def detect_pullbacks(self, data, minimum_tresure=None):
        # Usar el valor proporcionado o el del constructor
        if minimum_tresure is None:
            minimum_tresure = self.minimum_tresure
            
        #configuracion inicial 
        rangoAlto=data.iloc[0]["high"]
        rangoBajo=data.iloc[0]["low"]
        RealRangoAlto=rangoAlto
        RealRangoBajo=rangoBajo
        tendencia=0
        pocBajosArray=[rangoAlto]
        pocAltosArray=[rangoBajo]
        indexPocs=[0]
        
        #analisis
        # print(data)
        for i  in range(1,len(data)-1 ):  
            current_candle = data.iloc[i]
            previous_candle = data.iloc[i - 1]
            next_candle = data.iloc[i + 1]
        
            # Detectar TODOS los pivots locales (sin filtro de rangos)
            # Pivot Alto: high mayor que la vela anterior Y mayor que la siguiente
            if(current_candle["high"] > previous_candle["high"] and current_candle["high"] > next_candle["high"]):
                data.loc[i, 'pivotAlto'] = current_candle["high"]
            
            # Pivot Bajo: low menor que la vela anterior Y menor que la siguiente
            if(current_candle["low"] < previous_candle["low"] and current_candle["low"] < next_candle["low"]):
                data.loc[i, 'pivotBajo'] = current_candle["low"]
        
            if(rangoAlto<=current_candle["parteAlta"]):
                tendencia=1
            elif(rangoBajo>=current_candle["parteBaja"]):
                tendencia=-1
            #pivotAlto de estructura mayor (rompe rangos)
            if(current_candle["high"]>=previous_candle["high"] and tendencia==1):
               if (current_candle["high"]>next_candle["high"] and  rangoAlto<current_candle["parteAlta"]):     
                   data.loc[i, 'altos'] = current_candle["high"]
                   rangoAlto=current_candle["high"]
                   index=indexPocs[np.argmin(pocAltosArray)]
                   rangoBajo = min(pocAltosArray)
                   data.loc[index, 'pocAltos'] = rangoBajo
                   data.loc[index+1:, 'pocAltos'] = math.nan
                   RealRangoAlto = rangoAlto
                   RealRangoBajo = rangoBajo
 
                   if data.iloc[index]["pocAltos"]!=data.iloc[index]["altos"] and not math.isnan(data.iloc[index]["altos"]):
                        data.loc[index, 'pocAltos'] = math.nan
                        pocAltosArray.pop(0)
                        indexPocs.pop(0)
                        index=indexPocs[np.argmin(pocAltosArray)]
                        rangoBajo = min(pocAltosArray)
                        data.loc[index, 'pocAltos'] = rangoBajo
                        RealRangoBajo = rangoBajo
 

                   pocAltosArray=[]
                   pocBajosArray=[]
                   indexPocs=[]
                    

            #pivotBajo de estructura mayor (rompe rangos)
            if(current_candle["low"]<=previous_candle["low"]  and tendencia==-1):
                if (current_candle["low"]<next_candle["low"] and rangoBajo>current_candle["parteBaja"] ):
                    data.loc[i, 'bajos'] = current_candle["low"]
                    rangoBajo=current_candle["low"]
                    index=indexPocs[np.argmax(pocBajosArray)]
                    rangoAlto = max(pocBajosArray)
                    data.loc[index, 'pocBajos'] = rangoAlto
                    data.loc[index+1:, 'pocBajos'] = math.nan
                    RealRangoAlto = rangoAlto
                    RealRangoBajo = rangoBajo
                    
                    if data.iloc[index]["pocBajos"]!=data.iloc[index]["bajos"] and not math.isnan(data.iloc[index]["bajos"]):
                        data.loc[index, 'pocBajos'] = math.nan
                        pocBajosArray.pop(0)
                        indexPocs.pop(0)
                        index=indexPocs[np.argmax(pocBajosArray)]
                        rangoAlto = max(pocBajosArray)
                        data.loc[index, 'pocBajos'] = rangoAlto
                        RealRangoAlto = rangoAlto

                    pocAltosArray=[]
                    pocBajosArray=[]
                    indexPocs=[]      

            pocBajosArray.append(current_candle["high"])
            pocAltosArray.append(current_candle["low"])    
            indexPocs.append(i)
            data.loc[i, 'tendencia'] = tendencia

        rangos = {
            'rangoBajo': rangoBajo,
            'rangoAlto': rangoAlto,
            'tendencia': tendencia,
            'minimum_tresure': minimum_tresure
        }
        return data, rangos
