import numpy as np
import time
from PIL import ImageGrab
import cv2
import pyautogui

# Tamanho da tela do jogo
SCREEN_REGION = (0, 40, 800, 540)

# Parâmetros genéticos
POPULATION_SIZE = 50
MUTATION_RATE = 0.1

def capture_screen():
    screen = np.array(ImageGrab.grab(bbox=SCREEN_REGION))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    return screen

def jump():
    pyautogui.press('up')

def run_generation(population):
    for i in range(len(population)):
        screen = capture_screen()
        if np.mean(screen) < 200:  # Se a tela estiver escura, o dinossauro pulou um obstáculo
            population[i]['fitness'] += 1
            jump()
            time.sleep(0.1)
        else:
            population[i]['fitness'] -= 1

def select_parents(population):
    fitness_scores = np.array([individual['fitness'] for individual in population])
    probabilities = fitness_scores / fitness_scores.sum()
    parents = np.random.choice(population, size=2, p=probabilities, replace=False)
    return parents

def crossover(parent1, parent2):
    child = {}
    for key in parent1:
        if np.random.rand() > 0.5:
            child[key] = parent1[key]
        else:
            child[key] = parent2[key]
    return child

def mutate(child):
    for key in child:
        if np.random.rand() < MUTATION_RATE:
            child[key] = np.random.uniform(-1, 1)
    return child

# Inicialização da população
population = [{'weights': np.random.uniform(-1, 1, 4), 'fitness': 0} for _ in range(POPULATION_SIZE)]

# Loop principal
generation = 0
while True:
    print(f"Generation {generation}")
    run_generation(population)
    
    population.sort(key=lambda x: x['fitness'], reverse=True)
    parents = select_parents(population)
    child = crossover(parents[0]['weights'], parents[1]['weights'])
    child = mutate(child)
    population[-1]['weights'] = child
    
    generation += 1
