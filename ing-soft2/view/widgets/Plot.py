"""Widget per il plot"""
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotCartesian(ctk.CTkFrame):
    """Classe per fare i plot"""
    def __init__(self, master, Xcoordinates, Ycoordinates,  name = None):
        """Inizializzazione classe"""
        super().__init__(master, width= 400, height= 400)
        if name is not None:
            self.name = name
            label = ctk.CTkLabel(self, text = self.name)
            label.pack()
        # Creare un oggetto Figure di Matplotlib
        fig = Figure(figsize=(5, 4), dpi=100, facecolor= "#2b2b2b")
        # Aggiungere un subplot al figure
        ax = fig.add_subplot(111)
        ax.plot(Xcoordinates, Ycoordinates)  # Esempio di dati per il grafico
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_color('white')  # Asse delle ascisse (X)
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='both', colors='white')
        ax.set_facecolor("#2b2b2b")
        # Creare un oggetto FigureCanvasTkAgg per il grafico
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill= "x")
