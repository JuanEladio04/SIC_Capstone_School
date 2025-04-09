#!/usr/bin/env python
# coding: utf-8

# # SIC_Capstone_School

# ## City Simulation

# In[ ]:


class CitySimulation:
    def __init__(self):
        pass

    def command_loop(self):
        print("Starting City simulation... Type 'q' to exit")
        while True:
            command = input('> ')
            if command == 'q':
                break
            self.process_command(command)
            self.agent_manager.check_ready_services()  


# ## Agent

# In[ ]:


class Agent:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"{self.name}"

    def describe(self):
        return self.__str__()


# ## Agent Manager

# In[ ]:


class AgentManager:
    """Clase base para gestionar la creación y eliminación de agentes."""
    def __init__(self):
        self.agents = {}                    # Diccionario para almacenar agentes
        self.TIME_THRESHOLD = 10            # Umbral de 10 segundos

    def filter_agents(self,*agents_types):
        """Filtra agentes según los tipos proporcionados."""
        filtered_agents = {
            name: agent for name, agent in agents.items()
            if isinstance(agent, tuple(agents_types))      # Filtrar según tipos
        }
        return filtered_agents
    
    def get_agent_by_name(self, agent_name, agent_type):
        """Devuelve el agente con el nombre dado y tipo específico, o None si no se encuentra."""
        return next((agent for agent in agents.values() 
                     if isinstance(agent, agent_type) and agent.name == agent_name), None)

    def add_agent(self, agent_type, agent_name):
        """Añade un nuevo agente al sistema."""
        if isinstance(agent_type, type) and agent_type == Client: 
            agents[agent_name] = Client(agent_name)
        elif isinstance(agent_type, type) and agent_type == TownHall:
            agents[agent_name] = TownHall(agent_name)
        else:
            print(f"Invalid agent type: {agent_type}. Please use valid agent.")
            return
            
        print(f'{agent_type.__name__} {agent_name} added to the system.')

    def remove_agent(self, agent_name):
        """Elimina un agente del sistema."""
        if agent_name in agents:
            del agents[agent_name]
            print(f'Agent {agent_name} removed from the system.')
        else:
            print(f'Agent {agent_name} not found.')

    def list_agents(self, agent_type=None):
        """Muestra todos los agentes o filtra por clientes o ayuntamientos en el sistema."""
        if agent_type:
            print(f"Current {agent_type.__name__}(s):")
            filtered_agents = self.filter_agents(agent_type)
            for agent in filtered_agents.values():               # Imprimir descripciones de los agentes filtrados
                print(agent.describe())
        else:
            print("Current agents:")
            for agent in agents.values():
                print(agent.describe())     

    def check_ready_services(self):
        """Verifica si hay servicios listos para ser atendidos por cada ayuntamiento."""
        filtered_agents = self.filter_agents(TownHall)  # Filtrar solo los ayuntamientos
        for town_hall in filtered_agents.values():
            while not town_hall.request_services.is_empty():  # Procesar todos los servicios en la cola
                if self.is_time_to_serve(town_hall):  # Verificar si es tiempo de atender el servicio
                    town_hall.process_request_service()  # Procesar el servicio
                else:
                    break  # Salir si no es tiempo de procesar el siguiente servicio

    def is_time_to_serve(self, town_hall):
        """Verifica si es el momento de atender el siguiente servicio en la cola."""
        if not town_hall.request_services.is_empty():
            last_request = town_hall.request_services.peek()  # Obtenemos la última solicitud
            current_time = time.time()                        # Método que deberías implementar para obtener el tiempo actual
            return (current_time - last_request['timestamp']) >= self.TIME_THRESHOLD  # Define el umbral

        return False        
    
    def validate_client_location(self, client, town_hall_name):
        if client.current_town_hall() is None:
            print(f'Client {client.name} cannot perform this action because not in it.')
            return False
        elif client.current_town_hall() != town_hall_name:
            print(f'Client {client.name} is in a different town hall: {client.current_town_hall()}.')
            return False
        return True

    def load_agents_from_file(self, file_path):
        """Carga agentes desde un fichero JSON."""

        import json
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Cargar town_halls
            for town_hall_name, town_hall_data in data.get("town_halls", {}).items():
                self.add_agent(TownHall, town_hall_name)
                town_hall = self.get_agent_by_name(town_hall_name, TownHall)
                if town_hall:
                    # Añadir servicios
                    for service in town_hall_data.get("services", []):
                        town_hall.add_service(service)
                    # Añadir solicitudes en cola
                    for request in town_hall_data.get("queue", []):
                        town_hall.add_request_service(request["client_name"], request["service_name"])

            # Cargar clients
            for client_name, client_data in data.get("clients", {}).items():
                self.add_agent(Client, client_name)
                client = self.get_agent_by_name(client_name, Client)
                if client and client_data.get("current_town_hall"):
                    client.enter_town_hall(client_data["current_town_hall"])

            print(f"--- Agents loaded successfully from {file_path}. --- ")
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except json.JSONDecodeError:
            print(f"Error: File '{file_path}' is not a valid JSON file.")
        except Exception as e:
            print(f"An error occurred while loading agents: {e}")     


# ## Clients

# In[ ]:


class Client(Agent):
    """Clase que representa a un cliente que interactúa con el ayuntamiento."""
    def __init__(self, name):
        super().__init__(name)
        self.town_hall_stack = Stack()  # En que ayuntamiento se encuentra

    def enter_town_hall(self, town_hall_name):
        """Método para marcar la entrada en un ayuntamiento."""
        self.town_hall_stack.push(town_hall_name)
        print(f'{self.name} entered {town_hall_name}.')

    def exit_town_hall(self):
        """Método para marcar la salida del último ayuntamiento visitado."""
        town_hall_name = self.town_hall_stack.pop()
        if town_hall_name:
            print(f'{self.name} exited {town_hall_name}.')
        else:
            print(f'{self.name} is not in any town hall.')

    def current_town_hall(self):
        """Método para obtener el ayuntamiento actual."""
        return self.town_hall_stack.peek()    
    
    HELP_MESSAGES = {
        "add_client": "client add_client <client_name>: Add a new client to the system.",
        "show_all": "client show_all: Show the list of all clients in the system.",
        "remove_client": "client remove_client <client_name>: Remove a client from the system.",
        "request_service": "client request_service <client_name> <town_hall_name> <service_name>: Request a specific service from the town hall.",
        "enter_town_hall": "client enter_town_hall <client_name> <town_hall_name>: Allow a client to enter the town hall.",
        "exit_town_hall": "client exit_town_hall <client_name> <town_hall_name>: Allow a client to exit the town hall.",
        "quit": "q: Exit the simulation."
    }

    @classmethod
    def help(cls):
        """Muestra los comandos disponibles para los clientes."""
        print("Available commands for client:")
        for command, description in cls.HELP_MESSAGES.items():
            print(f"- {description}")


# ## School

# In[ ]:


class School(Agent):
    pass


# ## Main program

# In[ ]:


import time
if __name__ == "__main__":
    simulation = CitySimulation()
    simulation.command_loop()

