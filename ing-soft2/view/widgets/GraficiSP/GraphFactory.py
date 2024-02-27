"""Modulo che fattorizza i grafici"""
from typing import Union
import tkinter as tk
from matplotlib import pyplot as ticker
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from icecream import ic
import model.chartOrganizer as co

class GraphFactory:
    """ factory class che produce il grafico richiesto """
    def __init__(self) -> None:
        """Inizializzatore della classe"""
        self.graphsList =  {name.lstrip('_'): getattr(self, name) for name in dir(self) if callable(getattr(self, name))}

    def makeGraph(self, master, graph : str, process_dict) -> Union[tk.Canvas, NavigationToolbar2Tk]:
        """ crea il grafico generale, poi chiamando uno dei metodi di specializzazione 
        crea il grafico specializzato richiesto """
        fig_loc = Figure(figsize=(8,5), dpi=100)
        ax_loc = fig_loc.add_subplot(111)
        fig_loc.subplots_adjust(left=0.176, bottom=0.205, right=0.9, top=0.88, wspace=0.2, hspace=0)
        fig_loc.set_facecolor("#2b2b2b")
        ax_loc.set_facecolor("#2b2b2b")
        ax_loc.spines['top'].set_visible(False)
        ax_loc.spines['right'].set_visible(False)
        ax_loc.spines['bottom'].set_color("white")
        ax_loc.spines['left'].set_color("white")
        ax_loc.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax_loc.tick_params(axis='x', colors='white')
        ax_loc.tick_params(axis='y', colors='white')
        graphProducer = self.graphsList[graph]
        fig = graphProducer(process_dict, fig_loc, ax_loc)
        canvas_loc = FigureCanvasTkAgg(fig, master=master)
        toolbar_revision = NavigationToolbar2Tk(canvas_loc)
        canvas_loc.draw()
        return canvas_loc.get_tk_widget(), toolbar_revision

    def _loc(self, process_dict, fig, axloc) -> Figure:
        """ contiene solo la specializzazione del grafico, vengono aggiunti gli elementi
          per renderlo un grafico LOC """
        x1, x2, x3, y = co.loc_number(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        axloc.plot(y2, x1, label='Linee di Codice', marker='o')
        axloc.plot(y2, x2, label='Linee vuote', marker='o')
        axloc.plot(y2, x3, label='Commenti', marker='o')
        axloc.set_title("Amount (in LOC) of previous change" ,color = "white")
        axloc.set_xticklabels(y2, rotation=30, ha='right')
        axloc.legend()
        if len(y2) <= 10:
            right = len(y2) -1
        else:
            right = 10
        axloc.set_xlim(left = y2[0], right = y2[right])
        return fig

    def _revisions(self, process_dict, fig, axloc) -> Figure:
        x, y = co.revision_number(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        axloc.plot(y2, x, label = "revisions", marker = "o")
        axloc.set_title("Number of revision", color= "white")
        axloc.set_xticklabels(y2, rotation=30, ha='right')
        axloc.legend()
        if len(y2) <= 10:
            right = len(y2) -1
        else:
            right = 10
        axloc.set_xlim(left = y2[0], right = y2[right])
        return fig

    def _bugfix(self, process_dict, fig, axloc) -> Figure:
        """Grafico dei bugfix"""
        x, y = co.bugfix(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        axloc.bar(y2, x)
        axloc.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        axloc.set_ylim(bottom= 0, top = 5)
        axloc.set_title("Number of bugfix commit", color= "white")
        axloc.set_xticklabels(y2, rotation=30, ha='right')
        if len(y2) <= 10:
            right = len(y2) -1
        else:
            right = 10
        axloc.set_xlim(left = y2[0], right = y2[right])
        return fig

    def _churn(self, process_dict, fig, axloc) -> Figure:
        """Grafico dei code churn"""
        x, y = co.codeC(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        axloc.bar(y2, x)
        axloc.set_title("Number of code churn commit" ,color = "white")
        axloc.set_xticklabels(y2, rotation=30, ha='right')
        if len(y2) <= 10:
            right = len(y2) -1
        else:
            right = 10
        axloc.set_xlim(left = y2[0], right = y2[right])
        return fig

    def _weeks(self, process_dict, fig, axloc: Axes) -> Figure:
        """Grafico delle settimane dei file"""
        x, y = co.weeks(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        axloc.bar(y2, x)
        axloc.set_title("Number of week", color = "white")
        axloc.set_xticklabels(y2, rotation=30, ha='right')
        if len(y2) <= 10:
            right = len(y2) -1
        else:
            right = 10
        axloc.set_xlim(left = y2[0], right = y2[right])
        return fig

    def _authors(self, process_dict, fig, axloc: Axes) -> Figure:
        """Grafico dei contribuenti"""
        x, y = co.authors(process_dict)
        x = ic([int(value) for value in x])
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        axloc.step(y2, x)
        axloc.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        axloc.set_ylim(bottom= 0, top = 5)
        axloc.set_title("Number of author" ,color = "white")
        axloc.set_xticklabels(y2, rotation=30, ha='right')
        if len(y2) <= 10:
            right = len(y2) -1
        else:
            right = 10
        axloc.set_xlim(left = y2[0], right = y2[right])
        return fig

    def _contributions(self,process_dict, fig, axloc) -> Figure:
        """Grafico a torta contribuenti"""
        authros = co.perAuthorContribution(process_dict)
        values = authros.values()
        labels = authros.keys()
        axloc.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        axloc.set_title("Per author contribution" ,color = "white")
        axloc.legend()
        return fig

    def _cbo(self, process_dict, fig, axloc) -> Figure:
        """Grafico CBO"""
        x, y = co.cbo(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        axloc.bar(y2, x)
        axloc.set_title("CBO (Coupling Between Object classes" ,color = "white")
        axloc.set_xticklabels(y2, rotation=30, ha='right')
        if len(y2) <= 10:
            right = len(y2) -1
        else:
            right = 10
        axloc.set_xlim(left = y2[0], right = y2[right])
        return fig

    def _wmc(self, process_dict, fig, axloc) -> Figure:
        """Grafico WMC"""
        x, y = co.wmc(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        axloc.bar(y2, x)
        axloc.set_title("WMC (Weighted Methods per Class" ,color = "white")
        axloc.set_xticklabels(y2, rotation=30, ha='right')
        if len(y2) <= 10:
            right = len(y2) -1
        else:
            right = 10
        axloc.set_xlim(left = y2[0], right = y2[right])
        return fig

    def _dit(self, process_dict, fig, axloc) -> Figure:
        """Grafico DIT"""
        x, y = co.dit(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        axloc.bar(y2, x)
        axloc.set_title("DIT (Depth of Inheritance" ,color = "white")
        axloc.set_xticklabels(y2, rotation=30, ha='right')
        if len(y2) <= 10:
            right = len(y2) -1
        else:
            right = 10
        axloc.set_xlim(left = y2[0], right = y2[right])
        return fig

    def _noc(self, process_dict, fig, axloc) -> Figure:
        """Grafico NOC"""
        x, y = co.noc(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        axloc.bar(y2, x)
        axloc.set_title("NOC (Number of Children) ", color = "white")
        axloc.set_xticklabels(y2, rotation=30, ha='right')
        if len(y2) <= 10:
            right = len(y2) -1
        else:
            right = 10
        axloc.set_xlim(left = y2[0], right = y2[right])
        return fig

    def _rfc(self, process_dict, fig, axloc) -> Figure:
        """Grafico RFC"""
        x, y = co.rfc(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        axloc.bar(y2, x)
        axloc.set_title("RFC (Response for a Class" ,color = "white")
        axloc.set_xticklabels(y2, rotation=30, ha='right')
        if len(y2) <= 10:
            right = len(y2) -1
        else:
            right = 10
        axloc.set_xlim(left = y2[0], right = y2[right])
        return fig

    def _lcom(self, process_dict, fig, axloc) -> Figure:
        """Grafico LCOM"""
        x, y = co.lcom(process_dict)
        y2 = [timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in y]
        axloc.bar(y2, x)
        axloc.set_title("LCOM (Lack of Cohesion of Methods" ,color = "white")
        axloc.set_xticklabels(y2, rotation=30, ha='right')
        if len(y2) <= 10:
            right = len(y2) -1
        else:
            right = 10
        axloc.set_xlim(left = y2[0], right = y2[right])
        return fig
