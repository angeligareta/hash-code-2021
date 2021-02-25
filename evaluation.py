# Propuesta de Dautito
# { "intersection_id": [(in_street_name, green_seconds)] }


def evaluate_solution(solution, statement):
  D, I, S, V, F = statement["info"]
  # cars= {car_1: [street_name, L, arrived, t, path]}
  # intersections = {intersection_1: { current_green_street, seconds_to_change, street_index }}
  

  # initial_street_queue['street_name'] -> Cola de coches en el instante 0 de esta calle
  # Utilizada para inicializar correctamente streets
  initial_street_queue = {}
  next_streets = {}

  # cars
  cars = {}
  for car_id, streets in statement["cars"].items():
    initial_street = streets[0]
    if not initial_street in initial_street_queue:
      initial_street_queue[initial_street] = []
    initial_street_queue[initial_street].append(car_id)
    
    # cars= {car_1: [street_name, L, arrived, t]}
    cars[car_id] = {"street_name" = streets[0], "time_to_finish" = 0, "arrived" = False, "time_spent" = 0}
    for i in range(len(streets)):
      if (i != len(streets) - 1):
        current = streets[i]
        next_street = streets[i + 1]
        next_streets[str(car_id) + current] = next_street
    
  # streets = {street_1: {[car_1, car_2], intersection_id}}
  # streets['street_name'][0] -> Cola de coches actual en esta calle
  # streets['street_name'][1] -> Id de la intersección a la que pertenece esta calle
  streets = {}
  for intersection_id, in_streets in solution.items():
    for in_street in in_streets:
      
      street_name = in_street[0]
      streets[street_name] = {'street_queue': initial_street_queue[street_name], 'intersection_id': intersection_id }
  
  intersections = {}
  for intersection_id, in_streets in solution.items():
    intersections[intersection_id] = { 'green_street': in_streets[0][0], 'seconds_to_change': in_streets[0][1], 'street_index': 0}
  
  for second in range(D):

    for car_id, car_info in cars.items():
      if (car_info['time_to_finish'] > 0):
        car_info["time_to_finish"] = car_info['time_to_finish'] - 1

    for intersection_id, intersection_info in intersections.item():
      green_street = intersection_info['green_street']
      street_queue = streets[green_street]['street_queue'] 
      if (len(street_queue) > 0):
        car_id = street_queue.pop(0)
        next_street_index = str(car_id) + cars[car_id]['current_street']
        if (next_street_index in next_streets):
          next_street = next_streets[next_street_index]
          cars[car_id]["street_name"] = next_street
          cars[car_id]["time_to_finish"] = statement["streets"][next_street][0]
        else:
          cars[car_id]["arrived"] = True
          cars[car_id]["time_spent"] = second
      
      intersection_info['seconds_to_change']

    for car_id, car_info in cars.items():
      if (car_info['time_to_finish'] > 0):
        car_info["time_to_finish"] = car_info['time_to_finish'] - 1

        
  #for t in range(D):
        
  #pass