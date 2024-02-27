"""Modulo per la rotazione dell'icona"""
import tkinter as tk
import threading
from PIL import Image, ImageTk, ImageOps

class RotatingIcon(tk.Canvas):
    """Classe dell'icona che ruota"""
    def __init__(self, master, iconPath, rotationSpeed = -3.5, backgroundColor = "black"):
        """Inizializza la classe RotatingIcon"""
        super().__init__(master, highlightthickness= 0 , bg= backgroundColor, width=30, height=28)
        self.keepRotating = True
        self.rotationSpeed = rotationSpeed
        # Carica l'immagine che vuoi ruotare
        self.image = Image.open(iconPath)
        self.image = self.image.resize((15,15), Image.LANCZOS)
        self.image = self.image = self.image.crop()
        self.image = ImageOps.expand(self.image, border=10, fill=backgroundColor)
        self.tk_image = ImageTk.PhotoImage(self.image, size= (15,15))
        self.image_id = self.create_image(10, 10, image=self.tk_image)
        # Avvia l'animazione

    def beginRotation(self):
        """Inizia rotazione"""
        self.keepRotating = True
        self.t = threading.Thread(target= self._animate, args= [0])
        self.t.start()

    def _animate(self, angle):
        """start animation on animation thread"""
        if self.keepRotating is True:
            # Ruota l'immagine di 10 gradi
            imageToDisplay = self.image.rotate(angle = angle, resample= Image.BICUBIC)
            self.tk_imageToDisplay = ImageTk.PhotoImage(imageToDisplay)
            self.delete(self.image_id)
            self.image_id = self.create_image(15, 15, image=self.tk_imageToDisplay)
            # Aggiorna l'immagine sul canvas
            self.itemconfig(id, image=self.tk_imageToDisplay)
            # Ripeti l'animazione dopo 100 millisecondi
            self.master.after(20, self._animate, (angle + self.rotationSpeed) % 360)

    def stop(self) -> None:
        """Finisci di ruotare"""
        self.keepRotating = False
