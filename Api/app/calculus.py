import base64
from flask import Response
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd

class Operation():
    
    def DAS (data):
        df =pd.DataFrame(data)
        
        df["DAS_sig"] = df["sig"] - df["PS_sig"]
        return df
        
    def plot(data):
        data = pd.DataFrame(data)
        print(data)
        fig = Figure()
        
        ax = fig.add_subplot(3,1,1)
        ax.plot(data[1])
        ax.title.set_text("PS")
        ax = fig.add_subplot(3,1,2)
        ax.plot(data[2])
        ax.title.set_text("Antena 1")
        ax = fig.add_subplot(3,1,3)
        ax.plot(data[3])
        ax.title.set_text("DAS")

        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        
        return Response(output.getvalue(),mimetype='image/png')
                
        