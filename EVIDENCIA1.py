
from datetime import datetime, timedelta
salas = {}
id_sala = 1000

clientes = {}
id_cliente = 0

reservas = {}
folio_contador = 0


while True:
  print('\n************ MENÚ ************')
  print('1. REGISTRAR RESERVACION DE UNA SALA')
  print('2. EDITAR EL NOMBRE DE UN EVENTO DE UNA RESERVACION YA HECHA')
  print('3. CONSULTAR RESERVACIONES EXISTENTES')
  print('4. REGISTRAR UN CLIENTE')
  print('5. REGISTRAR UNA SALA')
  print('6. SALIR') 

  opcion = input('Ingrese una opción: ')


  if opcion not in '123456':
     print('\nError. Respuesta no valida')
     continue
  

  if opcion == '1':
    if clientes:
      while True:

        clientes_ordenados = sorted(
        clientes.items(),
        key=lambda item: item[1][1].lower()
        )

        print("\n********** Clientes Registrados **********")
        print(f'{'ID':<5}{'Apellido':<20}{'Nombre':<20}')
        for id, datos in clientes_ordenados:
            nombre, apellido = datos
            print(f'{id:<5}{apellido:<20}{nombre:<20}')


        id_cliente_buscar = input('\nDigite su ID: ').strip()
        if not id_cliente_buscar.isdigit():
          print('Error. Id invalido')
          continue
        else:
          id_cliente_buscar = int(id_cliente_buscar)
          if id_cliente_buscar not in clientes.keys():
            print('Error. ID no registrado')
            continue
          else:
            print('ID encontrado')


        hoy = datetime.now().date()  
        fecha_minima = hoy + timedelta(days=2)
        fecha_usuario_str=input("\nINGRESE LA FECHA DE RESERVA (YYYY-MM-DD): ").strip()
        try:
            fecha_usuario = datetime.strptime(fecha_usuario_str, "%Y-%m-%d").date()

            if fecha_usuario >= fecha_minima:
              print("La fecha es valida para reserva")
            else:
               print(f'Error. La fecha debe de ser por lo menos 2 dias posteriores a hoy {hoy}')
               continue
        except ValueError:
            print("Formato de fecha invalido")
            continue
        

        turnos = {'M':'Matutino', 'V': 'Vespertino', 'N': 'Nocturno'}
        while True:
          print('TURNOS: "Matutino"(M) | "Vespertino"(V) | "Nocturno"(N)')
          seleccionar_turno = input("Ingrese turno el turno que desea (M/V/N): ").upper().strip()
          if seleccionar_turno not in turnos.keys():
            print('Error. Seleccione un turno valido')
            continue
          else:
            turno_sala = turnos[seleccionar_turno]
            print('Turno registrado')
            break
        
        print("\n********** SALAS DISPONIBLES **********")
        print(f'{'ID':<5}{'Nombre':<15}{'Cupo':<15}')
        salas_disponibles = []
        for id_sala_item, (nombre_sala, cupo_sala) in salas.items():
          ocupada = False
          for folio, datos_reserva in reservas.items():
            if (datos_reserva['sala_id'] == id_sala_item and
                datos_reserva['fecha'] == fecha_usuario and
                datos_reserva['turno'] == turno_sala):
              ocupada = True
              break
          if not ocupada:
            print(f"{id_sala_item:<5}{nombre_sala:<15}{cupo_sala:<15}")
            salas_disponibles.append(id_sala_item)

        if not salas_disponibles:
          print("No hay salas disponibles en esa fecha y turno.")
          break

        
        try:
          sala_seleccionada = int(input("\nIngrese el ID de la sala: "))
        except ValueError:
          print("Error. Debe ingresar un número de sala válido.")
          continue

        if sala_seleccionada not in salas_disponibles:
          print("La sala seleccionada no está disponible.")
          continue

        
        nombre_reserva = input('\nIngrese el nombre de la reservación de la sala: ').strip()
        if not nombre_reserva:
          print('Error. El nombre no puede estar vacío')
          continue

        
        folio_contador += 1
        folio = f"F{folio_contador}"

        reservas[folio] = {
          'cliente_id': id_cliente_buscar,
          'sala_id': sala_seleccionada,
          'fecha': fecha_usuario,
          'turno': turno_sala,
          'evento': nombre_reserva
        }

        print(f"\nReservación registrada con éxito. Folio: {folio}")
        print(f"Cliente: {clientes[id_cliente_buscar][1]} {clientes[id_cliente_buscar][0]}")
        print(f"Sala: {salas[sala_seleccionada][0]} (Cupo: {salas[sala_seleccionada][1]})")
        print(f"Fecha: {fecha_usuario} | Turno: {turno_sala} | Evento: {nombre_reserva}")
        break
   

    else:
      print('Error. Aún no hay clientes registrados')
      continue


  if opcion == '2':
    
    if reservas:

    
      try:
        fecha_inicio_str = input("\nIngrese fecha de inicio (YYYY-MM-DD): ").strip()
        fecha_fin_str = input("Ingrese fecha final (YYYY-MM-DD): ").strip()

        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()

        if fecha_fin < fecha_inicio:
          print("Error. La fecha final no puede ser anterior a la fecha de inicio.")
          continue
      except ValueError:
        print("Formato de fecha inválido")
        continue

    
      reservas_en_rango = {}
      for folio, datos in reservas.items():
        if fecha_inicio <= datos['fecha'] <= fecha_fin:
          reservas_en_rango[folio] = datos

      if not reservas_en_rango:
        print("No hay reservaciones en ese rango de fechas.")
        continue

    
      print("\nFOLIO\tFECHA\t\tSALA\t\tCLIENTE\t\tEVENTO\t\tTURNO")
      for folio, datos in reservas_en_rango.items():
        cliente_id = datos['cliente_id']
        sala_id = datos['sala_id']
        nombre_cliente = f"{clientes[cliente_id][1]} {clientes[cliente_id][0]}"
        nombre_sala = salas[sala_id][0]
        print(f"{folio}\t{datos['fecha']}\t{nombre_sala}\t{nombre_cliente}\t{datos['evento']}\t{datos['turno']}")

      
      folio_sel = input("\nIngrese el folio de la reserva que desea modificar: ").strip()
      if folio_sel not in reservas_en_rango.keys():
        print("Error. Folio no válido o fuera del rango.")
        continue

      
      nuevo_evento = input("Ingrese el nuevo nombre del evento: ").strip()
      if not nuevo_evento:
        print("Error. El nombre del evento no puede estar vacío.")
        continue

      reservas[folio_sel]['evento'] = nuevo_evento
      print(f"Reserva {folio_sel} actualizada con éxito. Nuevo evento: {nuevo_evento}")

    else:
      print('No hay reservaciones registradas')
      continue


  if opcion == '3':
    fecha_consulta_str = input("Ingrese la fecha a consultar (YYYY-MM-DD): ").strip()
    try:
      fecha_consulta = datetime.strptime(fecha_consulta_str, "%Y-%m-%d").date()
    except ValueError:
      print("Error. Formato de fecha inválido")
      continue

  
    reservas_para_fecha = {}
    for folio, datos in reservas.items():
      if datos['fecha'] == fecha_consulta:
        reservas_para_fecha[folio] = datos

    if not reservas_para_fecha:
      print(f"No hay reservaciones hechas para la fecha {fecha_consulta}.")
      continue

  
    print("**************************")
    print(f"*  REPORTE DE RESERVAS PARA EL DÍA {fecha_consulta}  *")
    print("**************************")
    print("FOLIO\tSALA\t\tCLIENTE\t\tEVENTO\t\tTURNO")
    for folio, datos in reservas_para_fecha.items():
      cliente_id = datos['cliente_id']
      sala_id = datos['sala_id']
      nombre_cliente = f"{clientes[cliente_id][1]} {clientes[cliente_id][0]}"
      nombre_sala = salas[sala_id][0]
      print(f"{folio}\t{nombre_sala}\t{nombre_cliente}\t{datos['evento']}\t{datos['turno']}")
    print("********* FIN DEL REPORTE ************")


  if opcion == '4':
    nombre_cliente = input('\nIngrese su nombre: ').strip().title()
    apellido_cliente = input('Ingrese su apellido: ').strip().title()
    
    if nombre_cliente and apellido_cliente:
      id_cliente+=1
      clientes[id_cliente] = nombre_cliente, apellido_cliente
      print('Cliente registrado')
    else:
      print('Error. El nombre y apellido no pueden estar vacios') 


  if opcion == '5':
    nombre_sala = input('\nIngrese el nombre de su sala: ').strip()
    cupo_sala_str = input('Ingrese el cupo de su sala: ').strip() 
    try:
      cupo_sala  = int(cupo_sala_str)
      if cupo_sala <= 0:
        raise ValueError
    except ValueError:
      print('Error. Cupo de sala invalido')
    else:   
      id_sala+=1  
      salas[id_sala] = nombre_sala, cupo_sala
      print('Sala creada')


  if opcion == '6':
    print('Gracias por su visita')
    break
