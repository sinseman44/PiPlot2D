# PiPlot2D

![PiPlot2D](https://github.com/sinseman44/PiPlot2D/blob/main/.github/images/PiPlot2D.png)

PiPlot2D est un système de plotter 2D construit à partir de deux anciens lecteurs de DVD-Rom, contrôlé par une raspberry pi 1.2b et d'un logiciel écrit en full python
PyCNC.
Ce logiciel permet d'interpreter du gcode en mouvement moteur sur les axes X, Y et Z.
Les moteurs X et Y sont des petits moteurs pas à pas biphasés 5V (20 pas), 4 fils.

L'axe des Z (du stylo) est contrôlé par un petit servo moteur SG90, dirigé par un ensemble de pignon/crémaillère. Le stylo est maintenu par le porte crayon à l'aide d'un piston (+ ressort conçu avec un fil de fer) permettant un appui constant sur la feuille.

Ce système se contrôle via une interface homme machine basique composée d'un écran HD44780 16x2 caractères ainsi que 3 boutons (UP, DOWN, OK) et du logiciel PiPlot2D.
.
Il permet de sélectionner les fichiers .gcode à dessiner par le système.

## Installation

### Dépendances
PiPlot2D à besoin d'un accès internet pour télécharger les dépendances suivantes :
* RPi.GPIO
* RPLCD
* PyCNC

### Instructions
```
$ sudo python3 setup.py install
```

```
$ sudo python3 setup.py install_service
```

Redemarrer le système pour voir apparaitre le menu ...
