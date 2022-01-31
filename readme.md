# SSL Junior ~ Enseirb IA
Ce projet a été réalisé dans le cadre d'un projet semestriel au semestre 9 de l'ENSEIRB en fillière IA par [Romain Bonnefon](https://github.com/RomainBnfn) et [Mohamed Kouhou](https://github.com/KouhouMed). Le but était de réaliser une IA par machine learning permettant de controler les 2 robots d'une équipe de SSL Socker Junior pour la compétition Robocup. (Plus de détails sur le contexte du projet dans le rapport (`nom_rapport.pdf`). 

Afin de permettre l'entrainement de cette IA, un simulateur `gym.env` a été réalisé; l'IA quant à elle a été réalisé en suivant l'architecture DDPG (voir nos choix sur le rapport).

# 1. Installation

Pour utiliser ce projet, il est nécessaire d'installer les différentes bibliothèques utilisées. Pour ce faire, il suffit de créer un environement virtuel avec Python >3.8 et exécuter la commande `pip install -r requirements.txt` sur un terminal (depuis le dossier du projet).

# 2. Architecture du projet
Comme indiqué précédemment, le projet comporte un simulateur permettant de simuler un match de SSL Junior avec ses élements dans le temps, et les différents fichiers relatif à l'IA.

*A noter, le dossier `/assets` comporte les différents fichiers nécessaires à l'éxécution du projet: images, ...*

## 2.1. Simulateur

Le code du simulateur est disponible dans le dossier `/socker_simulator`. Le simulateur a été créé en important la class `Environment` de la bibliothèque `gym` car c'est une biliothèque destinée et régulièrement utilisé dans l'apprentissage par renforcement. 

*A noter: Ce simulateur a été pensé pour pouvoir être intégrer au game controleur réel réalisé par l'équipe Roban. De fait, pour controler les robots il est nécessaire de spécifier la vitesse (selon chaque axe) souhaitée à chaque instant.*

### 2.1.1. Fichiers du simulateur

Ce simulateur est consitué de plusieurs fichiers ayant des roles particuliers :
- `socker_environment.py` : Ce fichier est le fichier principal du simulateur. Il contient la class `SockerEnvironement` qui fournit les 3 méthodes d'un environement gym : step, reset, render. Cette class est un "squelette" qui regroute et utilise les autres fichiers et class pour fonctionner. 
- `socker_field.py` : Ce fichier permet la gestion interne d'un terrain de jeu. Il gère la physique, les déplacement des éléments (balle et robots) et les colisions. C'est ce fichier qui est utilisé pour connaitre d'évolution du terrain entre deux crans de temps.
- `socker_render.py` : Ce fichier permet d'afficher un terrain grace à la bibliothèque pygame. Il récupère les positions des différents élément et les affiche.
- `socker_constants.py` : Ce fichier comporte toutes les constantes du simulateur. Ces constantes sont les constantes physiques (tailles, poids des robots, positions des éléments clefs...) et autre (différents images). Ces constantes sont utilisées dans tous les autres fichiers. 

### 2.1.2. Utilisation du simulateur

Pour utiliser le simulateur, un schéma classique est de l'instancier (en lui précisant les paramètres : l'équipe à controler), puis de lancer une boucle en effectuant la fonction `SockerEnvironement.step()` à chaque itération. 

La constant `TIME_STEP` (dans le fichier des constantes) représente le temps (en seconde) simulé entre chaque itération. Pour un match "en temps réel", il est possible de faire attendre le programme `TIME_STEP` seconde (avec `time.sleep()` de python), ou non si on souhaite effectuer de nombreux matchs sans la contrainte du temps.

La fonction `SockerEnvironement.step()` prend un seul paramètre qui est un tableau indiquant les différente actions à réaliser par les robots de son équipe selon la forme: `[dX1, dY1, dO1, k1, dX2, dY2, dO2, k2]` avec `dX1, dX2, ...` des vitesses en X, Y ou rotation (O) pour le robot 1 ou 2 de l'équipe et `k1, k2` la puissance du kicker.

```python
import gym
import time
from socker_environment import SockerEnvironement
from socker_constants import TIME_STEP

env = SockerEnvironement('blue')
env.reset()
done = false
while not done:
    new_state, reward, done, _ = env.step([ 0,  100, 0, 0,   # actions robot 1
                                            0, -100, 0, 0 ]) # actions robot 2
    env.render() # Pour afficher le terrain (optionnel)
    time.sleep(TIME_STEP)
print("Partie terminée !")
```

Il est à noter que pour le simulateur, l'équipe qu'il controle se situe toujours (du moins au départ) en haut du terrain (x>0). (car le problème est symétrique : l'IA apprend à controler une équipe contre celle adverse, peu importe les couleurs)

### 2.1.3. Fonctionnement général interne

Afin d'indiquer aux robots le comportement souhaité, il faut passer dans les paramètres de la fonction `step` les différents actions des robots. Ces actions correpondent à la vitesse souhaitée de chaque robot. Cette vitesse est atteinte progressivement pour simuler le temps de réaction & de démarrage des moteurs.

Pour la gestion de la **physique**, chaque composant hérite de la class Mobable, qui permet de gérer les composant bougeant. Une somme des forces (sans prendre en compte les colisions) est appliquée afin de modifier l'accélération de chaque objet, et ainsi la vitesse puis la position. De fait, un robot a comme force celle de son moteur et la force de frotement, la balle elle n'est ralentie que par la force de frotement (dont le coef de frotement est défini dans le fichier des constantes). 

Les **collisions** sont gérées après le déplacement de chaque objet, si deux objets après déplacement sont trop près l'un de l'autre, le simulateur gère ce comportement selon les différents cas:
- **Robot/Robot** : Les robots sont instanéments stopés l'un contre l'autre
- **Balle/Robot (sur le kicker)** : La balle prend la vitesse & l'accélération du robot pour rester devant son kicker
- **Balle/Robot (ailleurs)** : La balle rebondie en changeant de direction. (conservation totale de la vitesse) 

A la fin de chaque step, les différents configuration de jeu (fin de jeu, balle hors du terrain...) sont regardées et le reward renvoyé au modèle est ajusté. Chaque type de faute/bonne action est associé à un reward défini dans le fichier des constantes. 

## 2.2. IA DDPG

C'est la partie susceptible d'apprendre aux agents (robots) de prendre des décisions "intelligentes" en se basant sur les observations du terrain. **Deep Deterministic Policy Gradient (DDPG)** est une technique d'apprentissage par renforcement qui combine à la fois le Q-learning et les *Policy gradients*. Le DDPG se compose de deux réseaux :
- **Acteur** : prend l'observation en entrée et produit l'action exacte (continue), au lieu d'une distribution de probabilité sur les actions (comme en DQN par exemple)
- **Critique** : c'est un réseau de *Q-value* qui prend en entrée l'observation et l'action et produit la Q-value ($$Q(s,a)$$ est une mesure de la récompense globale attendue en supposant que l'agent est dans l'état $s$ et effectue l'action $$a$$)

# 3. Démonstrations & résulats

## 3.1. Démonstrations du simulateur

(images)
(gif)

## 3.2. DDPG : Comportements des robots

# 4. Pistes d'améliorations

## 4.1. Simulateur

Le simulateur permet d'entrainer l'IA. Plus le simulateur est proche de la réalité plus l'IA sera performante et controlera correctement les robots. Afin de pouvoir lancer un entrainement avant la fin du projet, certains comportement physiques n'ont pas été réaliser correctement (collision balle/robot, force du moteur du robot). De fait, amélioration ce simulateur permettrait grandement d'améliorer les performances des robots sur le monde réél. 

D'autres règles et comportement peuvent être ajouter pour coller à un fonctionement plus réaliste, notamment le scénario lors d'une sortie de balle. Pour le moment si un robot sort la balle du terrain, il est 'punni' par une reward négatif et les robots et la balle sont repositionnés comme au début du match. Cela est à modifié dans la fonction `step` du socker_field pour adapter au scénario réel. 
