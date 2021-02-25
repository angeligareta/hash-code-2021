import numpy as np
import pandas as pd
import sys
import math    
import random

## Ideas
# Priorizar coches que tengan minima suma de costes de calle

# Propuesta de Angelito
# { "calle-a": [duracion_calle = 3, duracion_semaforo_fin_calle = 1] }

# Propuesta de Dautito
# { "intersection_id": [(in_street_name, green_seconds)] }

# Propuesta del impostor
# [ time_0: [intersection_0_semaphore_green_id, intersection_1_semaphore_green_id, ... ],
#   time_1: [intersection_0_semaphore_green_id, intersection_1_semaphore_green_id, ... ], 
#   ... ]

def write_solution(solution, output_file_path):
  """
  3
  1
  2
  rue-d-athenes 2
  rue-d-amsterdam 1
  0
  1
  rue-de-londres 2
  2
  1
  rue-de-moscou 1
  """
  with open(output_file_path, 'w') as writer:
    
    count = 0
    temp = ""
    for intersection_id, in_streets in solution.items():
      if len(in_streets) > 0:
        count += 1
        temp += str(intersection_id) + "\n"
        temp += str(len(in_streets)) + "\n"
        for street_name, green_seconds in in_streets:
          temp += str(street_name) + ' ' + str(green_seconds) + '\n'

    writer.write(str(count) + "\n")
    writer.write(temp)


#
# solution = {
#   time = D
# }
def get_problem_statement_from_file(file_path):
  """
    6 4 5 2 1000
    2 0 rue-de-londres 1
    0 1 rue-d-amsterdam 1
    3 1 rue-d-athenes 1
    2 3 rue-de-rome 2
    1 2 rue-de-moscou 3
    4 rue-de-londres rue-d-amsterdam rue-de-moscou rue-de-rome
    3 rue-d-athenes rue-de-moscou rue-de-londres
  """

  statement = {}
  with open(file_path, 'r') as reader:
    [D, I, S, V, F] = [int(x) for x in reader.readline().split()]
    statement["info"] = [D, I, S, V, F]
    
    statement["streets"] = {}
    statement["intersections"] = {}
    for street in range(S):
      [inter_in, inter_out, street_name, street_duration] = reader.readline().split()
      statement["streets"][street_name] = [int(street_duration), int(inter_in), int(inter_out), 0] 
      
      if inter_out not in statement["intersections"]:
        statement["intersections"][inter_out] = []

      # Añadimos la interseccion con 1, luego en generacion de solucion cambios ese numero
      statement["intersections"][inter_out].append((street_name, 1))


    # Aqui empieza demanda de la calle
    statement["cars"] = {}
    for raw_car in range(V):
      raw_car_array = reader.readline().split()

      car_id = int(raw_car_array[0])
      car_streets = raw_car_array[1:]
      for street in car_streets: #[:len(car_streets) // 2]:
        statement["streets"][street][3] += 1 # Añadimos numero de veces que aparece esa calle
        
      statement["cars"][car_id] = car_streets
          
  # print(statement)

  return statement


def get_naive_solution_from_statement(statement):
  solution = {}
  # dtype = [('street_duration', int), ('inter_in', int), ('inter_out', int), ('car_count', int)]

  for inter_out, streets_raw in statement["intersections"].items():
    # [0, [(street_name, 1), (street_name, 2)]]
    number_of_streets = len(streets_raw)
    streets = []
    sum_street_values = 1
    sum_street_duration = 1
    for street_name, x in streets_raw:
      street_info = statement["streets"][street_name] # ('street_duration', 'inter_in', 'inter_out', 'car_count')
      street_value = street_info[3]
      street_duration = street_info[0]

      sum_street_values += street_value
      sum_street_duration += street_duration

      streets.append((street_name, street_value, sum_street_duration))

    # Normalizar street_value
    normalized_streets = []
    for street_name, street_value, street_duration in streets:
      normalized_value = (street_value / sum_street_values) # - (street_duration / sum_street_duration)
      normalized_streets.append((street_name, max(normalized_value, 0), street_duration))
      
    # Ordenar probando
    normalized_streets = sorted(normalized_streets, key=lambda item: item[-1], reverse=True)
    # print(sorted_streets)
    
    solution[inter_out] = []
    for street_index in range(len(normalized_streets)):
      duration = math.ceil(normalized_streets[street_index][1] * 2)
      duration = min(duration, statement["info"][0])
      if duration > 0:
        solution[inter_out].append((normalized_streets[street_index][0], int(duration * 1.3)))

    # for street_index in range(len(normalized_streets)):
    #   duration = 
    #   if duration > 0:
    #     solution[inter_out].append((normalized_streets[street_index][0], duration))

  return solution


if __name__ == "__main__":
  for code in range(ord('a'), ord('f') + 1):
    statement = get_problem_statement_from_file('data/' + chr(code) + '.txt')
    solution = get_naive_solution_from_statement(statement)
    write_solution(solution, 'out/' + chr(code) + '.txt')
  
      

    


