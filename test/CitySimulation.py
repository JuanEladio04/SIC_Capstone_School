#!/usr/bin/env python
# coding: utf-8

# # SIC_Capstone_School

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
    
    _instance = None  

    def __new__(cls, *args, **kwargs):
        """Controla la creación de una única instancia."""
        if cls._instance is None:
            cls._instance = super(AgentManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'agents'):  # Evita re-inicializar si ya existe
            self.agents = {}

    def filter_agents(self, *agents_types):
        """Filtra agentes según los tipos proporcionados."""
        filtered_agents = {
            name: agent for name, agent in self.agents.items()
            if isinstance(agent, tuple(agents_types))
        }
        return filtered_agents

    def get_agent_by_name(self, agent_name, agent_type):
        """Devuelve el agente con el nombre dado y tipo específico, o None si no se encuentra."""
        return next((agent for agent in self.agents.values()
                     if isinstance(agent, agent_type) and agent.name == agent_name), None)

    def add_agent(self, agent_type, agent_name):
        """Añade un nuevo agente al sistema."""
        if isinstance(agent_type, type) and agent_type == Client:
            self.agents[agent_name] = Client(agent_name)
        elif isinstance(agent_type, type) and agent_type == School:
            self.agents[agent_name] = School(agent_name)
        else:
            print(f"Invalid agent type: {agent_type}. Please use valid agent.")
            return
            
        print(f'{agent_type.__name__} {agent_name} added to the system.')

    def remove_agent(self, agent_name):
        """Elimina un agente del sistema."""
        if agent_name in self.agents:
            del self.agents[agent_name]
            print(f'Agent {agent_name} removed from the system.')
        else:
            print(f'Agent {agent_name} not found.')

    def list_agents(self, agent_type=None):
        """Muestra todos los agentes o filtra por clientes o ayuntamientos en el sistema."""
        if agent_type:
            print(f"Current {agent_type.__name__}(s):")
            filtered_agents = self.filter_agents(agent_type)
            for agent in filtered_agents.values():
                print(agent.describe())
        else:
            print("Current agents:")
            for agent in self.agents.values():
                print(agent.describe())  
    
    def load_agents_from_file(self, file_path):
        """Carga agentes desde un fichero JSON, incluyendo colas de inscripción, asistencias y otros datos relevantes."""
        import json
        global agents  # Asegurarse de usar el diccionario global

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Cargar escuelas
            for school_name, school_data in data.get("schools", {}).items():
                self.add_agent(School, school_name)
                school = self.get_agent_by_name(school_name, School)
                school.students = school_data.get("students", {})
                school.is_open = school_data.get("is_open", False)  # Restaurar el estado de apertura
                school.courses = {}  # Inicializar cursos como un diccionario
                for course_name, course_info in school_data.get("courses", {}).items():
                    course = Course(name=course_name)
                    course.students = course_info.get("students", [])
                    course.exams = {}  # Inicializar exámenes como un diccionario
                    course.assists = course_info.get("assists", {})  # Cargar asistencias
                    # Cargar exámenes como objetos
                    exams_data = course_info.get("exams", {})
                    for exam_name, exam_details in exams_data.items():
                        exam = Exam(exam_name)
                        exam.exams_student = exam_details.get("exams_student", {})
                        course.exams[exam_name] = exam
                    # Restaurar la cola de inscripción
                    course.enrollment_queue.queue = course_info.get("enrollment_queue", [])
                    school.courses[course_name] = course

            # Cargar clientes
            for client_name, client_data in data.get("clients", {}).items():
                self.add_agent(Client, client_name)
                client = self.get_agent_by_name(client_name, Client)
                enrolled_school = client_data.get("enrolled_school")
                if enrolled_school:
                    client.school_stack.push(enrolled_school)
                # Restaurar toda la pila de escuelas
                client.school_stack.stack = client_data.get("school_stack", [])

            print(f"--- Agents loaded successfully from {file_path}. ---")
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except json.JSONDecodeError:
            print(f"Error: File '{file_path}' is not a valid JSON file.")
        except Exception as e:
            print(f"An error occurred while loading agents: {e}")

    def save_agents_to_file(self, file_path):
        """Guarda los agentes en un fichero JSON, incluyendo colas de inscripción, asistencias y otros datos relevantes."""
        import json
        global agents  # Asegurarse de usar el diccionario global

        data = {
            "schools": {},
            "clients": {}
        }

        # Guardar escuelas
        for school in self.filter_agents(School).values():
            courses_data = {}
            for course in school.courses.values():
                exams_data = {}
                for exam in course.exams.values():
                    exams_data[exam.name] = {
                        "name": exam.name,
                        "exams_student": exam.exams_student
                    }
                courses_data[course.name] = {
                    "name": course.name,
                    "students": course.students,
                    "exams": exams_data,
                    "enrollment_queue": course.enrollment_queue.queue,
                    "assists": course.assists  # Guardar asistencias
                }
            data["schools"][school.name] = {
                "students": school.students,
                "courses": courses_data,
                "is_open": school.is_open  # Guardar el estado de apertura de la escuela
            }

        # Guardar clientes
        for client in self.filter_agents(Client).values():
            data["clients"][client.name] = {
                "enrolled_school": client.school_stack.peek(),
                "school_stack": client.school_stack.stack  # Guardar toda la pila de escuelas
            }

        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"--- Agents saved successfully to {file_path}. ---")
        except Exception as e:
            print(f"An error occurred while saving agents: {e}")


# ## Client

# In[ ]:


class Client(Agent):
    """Clase que representa a un cliente que interactúa con el colegio."""
    def __init__(self, name):
        super().__init__(name)
        self.school_stack = Stack()
        self.agent_manager = AgentManager()  
    
    HELP_MESSAGES = {
        "client add_client <client_name>": "Add a client (student) to the system.",
        "client enroll_in_school <client_name> <school_name>": "Enroll a client in an specific school.",
        "client leave_school <client_name>": "Allow a client to leave school.",
        "client join_enrollment_queue <client_name> <school_name> <course_name>": "Join a client in a queue to enroll a course.",
        "client assist_course <client_name> <course_name>": "Assist a course in a school.",
        "client show_list": "Show the list of clients in the system.",
        "client take_exam <client_name> <course_name> <exam_name>": "Allow a student to take an exam of a enrolled course.",
        "client remove_client <client_name>": "Removes the client from the agents.",
        "quit": "q: Exit the simulation."
    }
    
    # Client methods-------------------------------------------------------------------------------------------------------------------------
    
    def enroll_in_school(self, school):
        if self.school_stack.is_empty():
            self.school_stack.push(school.name)
            school.enroll_in_school(self.name)
        else:
            print(f'Client {self.name} is already enrolled in {self.school_stack.peek()}.')
    
    def leave_school(self):
        """Permite que un cliente deje la escuela en la que está inscrito."""
        if not self.school_stack.is_empty():
            school_name = self.school_stack.pop()
            if school_name:
                school = self.agent_manager.get_agent_by_name(school_name, School)
                if school:
                    if self.name in school.students:
                        del school.students[self.name]
                        self.school_stack.pop()
                        print(f'{self.name} exited {school_name}.')
                    else:
                        print(f"Error: {self.name} is not enrolled in {school_name}.")
            else:
                print(f"{self.name}'s school name was empty or invalid.")
        else:
            print(f'{self.name} is not currently enrolled in any school.')

    
    def join_enrollment_queue(self, school_name, course_name):
        school = self.agent_manager.get_agent_by_name(school_name, School)
        
        if school: 
            if self.name in school.students:
                course = school.getCourse(course_name)
                if course:
                    if self.name in course.students:
                        print(f"{self.name} is already enrolled in {course_name} at {school_name}.")
                    else:
                        if self.name in course.enrollment_queue.queue:
                            print(f"{self.name} is already in the enrollment queue for {course_name} in {school_name}.")
                        else:
                            course.enrollment_queue.enqueue(self.name)
                            print(f"{self.name} joined the enrollment queue for {course_name} in {school_name}.")
                else:
                    print(f"{course_name} is not available in {school_name}.")
            else:
                print(f"Client '{self.name}' not enrolled in school '{school.name}")
        else:
            print(f"School '{school_name}' do not exist.")
    
    def assist_course(self, course_name):
        import datetime as dt
        
        if not self.school_stack.is_empty():
            school_name = self.school_stack.peek()
            school = self.agent_manager.get_agent_by_name(school_name, School)

            if school:
                course = school.getCourse(course_name)
                if course:
                    if self.name in course.students:
                        if self.name not in course.assists:
                            course.assists[self.name] = [str(dt.datetime.now())]
                        else:
                            course.assists[self.name].append(str(dt.datetime.now()))
                        print(f"The student '{self.name}' assist to {course_name}.")
                    else:
                        print(f"The student {self.name} is not enrolled in course {course_name}.")
                else:
                    print(f"{course_name} is not available in {school_name}.")
            else:
                print(f"School '{school_name}' do not exist.")
        else:
            print(f"The student '{self.name}' is not enrolled in any school.")
    
    def take_exam(self, course_name, exam_name):
        if not self.school_stack.is_empty():
            school_name = self.school_stack.peek()
            school = self.agent_manager.get_agent_by_name(school_name, School)
            
            if school:
                if school.is_open == False:
                    print(f"The school '{school_name}' is closed. Cannot take exams.")
                    return
                
                course = school.getCourse(course_name)
                if course:
                    exam = course.getExam(exam_name)
                    if exam:
                        exam.exams_student[self.name] = ''
                        print(f"The exam '{exam.name}' has been taken by the student '{self.name}'.")
                    else:
                        print(f"The exam '{exam_name}' do not exist in course '{course.name}'.")
                else:
                    print(f"{course_name} is not available in {school_name}.")
            else:
                print(f"School '{school_name}' do not exist.")
        else:
            print(f"The student '{self.name}' is not enrolled in any school.")
    
    def remove_client(self):
        self.agent_manager.remove_agent(self.name)

    @classmethod
    def help(cls):
        """Muestra los comandos disponibles para los clientes."""
        print("Available commands for client:")
        for command, description in cls.HELP_MESSAGES.items():
            print(f"-{command}: {description}")


# ## School

# In[ ]:


class School(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.students = {}  
        self.courses = {}
        self.is_open = False 
        self.agent_manager = AgentManager() 

    HELP_MESSAGES = {
        "school add_school <school_name>": "Add a new school to the system.",
        "school create_course <course_name> <school_name>": "Create a new course at school.",
        "school show_students <school_name>": "Show the list of all students registered at school.",
        "school show_enrollment_queue <school_name> <course_name>": "Show the enrollment queue for the course.",
        "school admit_student_from_queue <school_name> <course_name>": "Admit the next student from the queue to enroll in to a course.",
        "school show_courses <school_name>": "Show the available courses at school.",
        "school remove_student <school_name> <client_name>": "Remove a student from school.",
        "school show_list": "Show the list of schools in the system",
        "school close / open <schol_name>": "Open / close school, if there isn't students at class",
        "school add_exam_to_course <school_name> <course_name> <exam_name>": "Add an exam to a specific course at school.",
        "school grade_exam <school_name> <course_name> <client_name> <exam_name> <grade>": "Grade an exam that the client has taken in a course.",
        "school remove_exam_from_course <school_name> <course_name> <exam_name>": "Remove an exam from a course if no client has submitted it.",
        "school show_exams <school_name> <course_name>": "Show the list of exams available for a course at the school.",
        "school remove_school <school_name>": "Removes the school from the agents.",
        
        "quit": "q: Exit the simulation."
    }
    
    # School methods-------------------------------------------------------------------------------------------------------------------------
    
    def create_course(self, course_name):
        if not course_name in self.courses:
            self.courses[course_name] = Course(course_name)
            print(f"Course '{course_name}' has been created in school '{self.name}'.")
        else:
            print(f"Course '{course_name}' already exists in school '{self.name}'.")
    
    def show_students(self):
        if len(self.students) == 0:
            print(f"No students enrolled in school '{self.name}'.")
        else:
            print(f"Students enrolled in school '{self.name}':")
            for student in self.students:
                print(f"- {student}")
    
    def show_enrollment_queue(self, course_name):
        course = self.getCourse(course_name)
        if course:
            if course.enrollment_queue.is_empty():
                print(f"The enrollment queue for course '{course_name}' in school '{self.name}' is empty.")
            else:
                print(f"Enrollment queue for course '{course_name}' in school '{self.name}':")
                for student in course.enrollment_queue.queue:
                    print(f"- {student}")
        else:
            print(f"The course '{course_name}' is not found at the school {self.name}.")
    
    def admit_student_from_queue(self, course_name):
        course = self.getCourse(course_name)
        if course:
            if not course.enrollment_queue.is_empty():
                student_name = course.enrollment_queue.dequeue()
                student = self.agent_manager.get_agent_by_name(student_name, Client)
                if student:
                    course.students.append(student_name)
                    print(f"The student '{student_name}' has been admitted to the course '{course.name}'.")
                else:
                    print(f"Client '{student_name}' not found.")
            else:
                print(f"The enrollment queue for course '{course.name}' is empty.")
        else:
            print(f"The course '{course_name}' is not found at the school {self.name}.")
    
    def show_courses(self):
        if len(self.courses) <= 0:
            print(f"There is no courses in school '{self.name}'.")
        else:
            print(f"Courses in school '{self.name}':")
            for course in self.courses:
                print(f"- {course}")
    
    def remove_student(self, client_name):
            student = self.agent_manager.get_agent_by_name(client_name, Client)
            
            if client_name in self.students:
                del self.students[client_name]
                student.school_stack.pop()
                print(f"Student '{client_name}' has been removed from school '{self.name}'.")
            else:
                print(f"Student '{client_name}' not found in school '{self.name}'.")     
    
    def open_close(self, school_name, action):
        if action == "open":
            if self.is_open:
                print(f"School '{school_name}' is already open.")
            elif len(self.students) > 0:
                self.is_open = True
                print(f"School '{school_name}' is now open.")
            else:
                print(f"School '{school_name}' cannot be opened while there are no students enrolled.")
        elif action == "close":
            if not self.is_open:
                print(f"School '{school_name}' is already closed.")
            elif len(self.students) == 0:
                self.is_open = False
                print(f"School '{school_name}' is now closed.")
            else:
                print(f"School '{school_name}' cannot be closed while there are students enrolled.")
        else:
            print(f"Unknown action '{action}'. Use 'open' or 'close'.")
    
    def add_exam_to_course(self, course_name, exam_name):
        course = self.getCourse(course_name)
        if course:
            exam = course.getExam(exam_name)
            if exam:
                print(f"The exam '{exam_name}' already exists and is associated with course '{course.name}'.")
            else:
                new_exam = Exam(exam_name)
                course.exams[new_exam.name] = new_exam
                print(f"The exam '{new_exam.name}' has been added to course '{course_name}'.")
        else:
            print(f"The course '{course_name}' is not found at the school {self.name}.")
    
    def grade_exam(self, course_name, client_name, exam_name, grade):
        if client_name not in self.students:
            print(f"The student '{client_name}' is not enrolled in school '{self.name}'.")
            return
        
        try:
            float(grade)
        except ValueError:
            print(f"The grade '{grade}' is not valid. It must be a number.")
            return
        
        course = self.getCourse(course_name)
        if course:
            exam = course.getExam(exam_name)
            if exam:
                if client_name in exam.exams_student:
                    if float(grade) >= 0 and float(grade) <= 10:
                        exam.exams_student[client_name] = grade
                        print(f"The exam '{exam.name}' has been graded with '{grade}' for the student '{client_name}'.")   
                    else:
                        print(f"The grade '{grade}' is not valid. It must be between 0 and 10.")
                else:
                    print(f"The student '{client_name}' has not taken the exam '{exam.name}'.")
            else:
                print(f"The exam '{exam_name}' do not exist in course '{course.name}'.")
        else:
            print(f"The course '{course_name}' is not found at the school {self.name}.")
    
    def remove_exam_from_course(self, course_name, exam_name):
        course = self.getCourse(course_name)
        if course:
            exam = course.getExam(exam_name)
            if exam:
                if len(exam.exams_student) <= 0:
                    del course.exams[exam.name]
                    print(f"The exam '{exam_name}' has been removed successfully from '{course.name}'.")
                else:
                    print(f"The exam '{exam.name}' cannot be removed because a student has already taken it.")
            else:
                print(f"The exam '{exam_name}' do not exist in course '{course.name}'.")
        else:
            print(f"The course '{course_name}' is not found at the school {self.name}.")
    
    def show_exams(self, course_name):
        course = self.getCourse(course_name)
        if course:
            if len(course.exams) > 0:
                print(f"Exams in {course.name}: ")
                for exam in course.exams:
                    print(f"- {exam}")
            else:
                print(f"There is no exams in {course.name}.")
        else:
            print(f"The course '{course_name}' is not found at the school {self.name}.")
    
    def remove_school(self):
        self.agent_manager.remove_agent(self.name)
    
    # Other methods-----------------------------------------------------------
    
    def getCourse(self, course_name):
        if course_name in self.courses:
            return self.courses[course_name]
    
    def enroll_in_school(self, client_name):
        if client_name not in self.students:
            self.students[client_name] = client_name
            print(f"Client '{client_name}' has been enrolled in school '{self.name}'.")
        else:
            print(f"Client '{client_name}' is already enrolled in school '{self.name}'.")

    @classmethod
    def help(cls):
        """Muestra los comandos disponibles para los ayuntamientos."""
        print("Available commands for school:")
        for command, description in cls.HELP_MESSAGES.items():
            print(f"-{command}: {description}")


# ## Course

# In[ ]:


class Course():
    def __init__(self, name):
        self.name = name
        self.students = []  
        self.exams = {}
        self.enrollment_queue = Queue()
        self.assists = {}
    
    def getExam(self, exam_name):
        if exam_name in self.exams:
            return self.exams[exam_name]


# ## Exam

# In[ ]:


class Exam():
    def __init__(self, name):
        self.name = name
        self.exams_student = {}


# ## City Simulation

# In[ ]:


class CitySimulation:
    def __init__(self):
        

        self.agent_manager = AgentManager()              
        self.agent_manager.agents = agents               
         
        self.ERROR_MESSAGES = {                           
            "": "",
            "invalid_command": "Error: Invalid command.",
            "school_not_found": "Error: School '{name}' not found.",
            "client_not_found": "Error: Client '{name}' not found.",
            "invalid_format": "Error: Invalid command format. Use '{expected_format}'."
        }
        
    def help_school(self):
        """Displays the list of available commands."""
        School.help()

    def help_client(self):
        """Muestra los comandos disponibles para los clientes."""
        Client.help()
        
    def help(self):
        """Displays general help information."""
        print("""
            Available help commands:
            - ? school: Show available commands for schools.
            - ? client: Show available commands for clients.
            - load_agents <file_path>: Load agents from a JSON file.
            - save_agents <file_path>: Save agents to a JSON file.
            - q: Exit the simulation.              
            """)

    def validate_command(self, parts, expected_length, error_key, expected_format):
        if len(parts) != expected_length:
            print(self.ERROR_MESSAGES[error_key].format(expected_format=expected_format))
            return False
        return True
    
    def get_agent_or_error(self, agent_name, agent_type, error_key):
        agent = self.agent_manager.get_agent_by_name(agent_name, agent_type)
        if not agent:
            print(self.ERROR_MESSAGES[error_key].format(name=agent_name))
        return agent

    def command_loop(self):
        """Bucle principal para gestionar comandos del usuario."""
        print("Starting city simulation... Type 'q' to exit")
        while True:
            command = input('> ')
            if command == 'q':
                break
            self.process_command(command)

    def process_command(self, command):
        """Procesa los comandos ingresados por el usuario."""
        parts = command.split()
        if not parts:
            return
        cmd = parts[0]
        if cmd == '?':
            if len(parts)==2:
                if parts[1]== 'school':
                    self.help_school()
                elif parts[1]== 'client':
                    self.help_client()
                else:
                    self.help()
            else:
                self.help()
            return
        
        elif cmd == 'load_agents':
            if self.validate_command(parts, 2, "invalid_format", "load_agents <file_path>"):
                _, file_path = parts
                self.agent_manager.load_agents_from_file(file_path)
                
        elif cmd == 'save_agents':
            if self.validate_command(parts, 2, "invalid_format", "save_agents <file_path>"):
                _, file_path = parts
                self.agent_manager.save_agents_to_file(file_path)
                
        elif cmd == 'school':
            if len(parts) < 2: 
                print(self.ERROR_MESSAGES["invalid_format"])
                self.help_school()
                
            elif parts[1] == 'add_school':
                if self.validate_command(parts, 3, "invalid_format", "school add_school <school_name>"):
                    _, _, school_name = parts
                    school = self.get_agent_or_error(school_name, School, "")
                    if not school:
                        self.agent_manager.add_agent(School, school_name)
                        print(f"School '{school_name}' added to the system.")
                    else:
                        print(f"School '{school_name}' already exists.")
                    
            elif   parts[1] == 'create_course':
                if self.validate_command(parts, 4, "invalid_format", "school create_course <course_name> <school_name>"):
                    _, _, course_name, school_name = parts
                    school = self.get_agent_or_error(school_name, School, "school_not_found")
                    if school:
                        school.create_course(course_name)     
                    
            elif   parts[1] == 'show_students':
                if self.validate_command(parts, 3, "invalid_format", "school show_students <school_name>"):
                    _, _, school_name = parts
                    school = self.get_agent_or_error(school_name, School, "school_not_found")
                    if school:
                        school.show_students()     

            elif   parts[1] == 'show_courses':
                if self.validate_command(parts, 3, "invalid_format", "school show_courses <school_name>"):
                    _, _, school_name = parts
                    school = self.get_agent_or_error(school_name, School, "school_not_found")
                    if school:
                        school.show_courses()     
                    
            elif   parts[1] == 'show_list':
                if self.validate_command(parts, 2, "invalid_format", "school show_list"):
                    self.agent_manager.list_agents(School)                     
            
            elif parts[1] == 'show_enrollment_queue':
                if self.validate_command(parts, 4, "invalid_format", "school show_enrollment_queue <school_name> <course_name>"):
                    _, _, school_name, course_name = parts
                    school = self.get_agent_or_error(school_name, School, "school_not_found")
                    if school:
                        school.show_enrollment_queue(course_name)
            
            elif parts[1] == 'admit_student_from_queue':
                if self.validate_command(parts, 4, "invalid_format", "school admit_student_from_queue <school_name> <course_name>"):
                    _, _, school_name, course_name = parts
                    school = self.get_agent_or_error(school_name, School, "school_not_found")
                    if school:
                        school.admit_student_from_queue(course_name)
            
            elif parts[1] == 'remove_student':
                if self.validate_command(parts, 4, "invalid_format", "school remove_student <school_name> <client_name>"):
                    _, _, school_name, client_name = parts
                    school = self.get_agent_or_error(school_name, School, "school_not_found")
                    if school:
                        school.remove_student(client_name)
                        
            elif parts[1] in ('open', 'close'):
                if self.validate_command(parts, 3, "invalid_format", "school open/close <school_name>"):
                    _, action, school_name = parts
                    school = self.get_agent_or_error(school_name, School, "school_not_found")
                if school:
                    school.open_close(school_name, action)
            
            elif parts[1] == 'add_exam_to_course':
                if self.validate_command(parts, 5, "invalid_format", "school add_exam_to_course <school_name> <course_name> <exam_name>"):
                    _, _, school_name, course_name, exam_name = parts
                    school = self.get_agent_or_error(school_name, School, "school_not_found")
                    if school:
                        school.add_exam_to_course(course_name, exam_name)
            
            elif parts[1] == 'grade_exam':
                if self.validate_command(parts, 7, "invalid_format", "school grade_exam <school_name> <course_name> <client_name> <exam_name> <grade>"):
                    _, _, school_name, course_name, client_name, exam_name, grade = parts
                    school = self.get_agent_or_error(school_name, School, "school_not_found")
                    if school:
                        school.grade_exam(course_name, client_name, exam_name, grade)
            
            elif parts[1] == 'remove_exam_from_course':
                if self.validate_command(parts, 5, "invalid_format", "school remove_exam_from_course <school_name> <course_name> <exam_name>"):
                    _, _, school_name, course_name, exam_name = parts
                    school = self.get_agent_or_error(school_name, School, "school_not_found")
                    if school:
                        school.remove_exam_from_course(course_name, exam_name)
            
            elif parts[1] == 'show_exams':
                if self.validate_command(parts, 4, "invalid_format", "school show_exams <school_name> <course_name>"):
                    _, _, school_name, course_name = parts
                    school = self.get_agent_or_error(school_name, School, "school_not_found")
                    if school:
                        school.show_exams(course_name)
        
            elif   parts[1] == 'remove_school':
                if self.validate_command(parts, 3, "invalid_format", "school remove_school <school_name>"):
                    _, _, school_name = parts
                    school = self.get_agent_or_error(school_name, School, "client_not_found")
                    if school:
                        school.remove_school()  
                        
            else:
                print(self.ERROR_MESSAGES["invalid_command"])
                self.help_school()
                
        elif cmd == 'client':
            if len(parts) < 2: 
                print(self.ERROR_MESSAGES["invalid_format"])
                self.help_client()
                
            elif  parts[1] == 'add_client':
                if self.validate_command(parts, 3, "invalid_format", "client add_client <client_name>"):
                    _, _, client_name = parts
                    client = self.get_agent_or_error(client_name, Client, "")
                    if not client:
                        self.agent_manager.add_agent(Client, client_name)
                        print(f"Client '{client_name}' added to the system.")
                    else:
                        print(f"Client '{client_name}' already exists.")
                    
            elif parts[1] == 'enroll_in_school':
                if self.validate_command(parts, 4, "invalid_format", "client enroll_in_school <client_name> <school_name>"):
                    _, _, client_name, school_name = parts
                    client = self.get_agent_or_error(client_name, Client, "client_not_found")
                    school = self.get_agent_or_error(school_name, School, "school_not_found")
                    if client and school:
                        client.enroll_in_school(school)
            
            elif parts[1] == 'leave_school':
                if self.validate_command(parts, 3, "invalid_format", "client leave_school <client_name>"):
                    _, _, client_name = parts
                    client = self.get_agent_or_error(client_name, Client, "client_not_found")
                    if client:
                        client.leave_school()
                        
            elif parts[1] == 'join_enrollment_queue':
                if self.validate_command(parts, 5, "invalid_format", "client join_enrollment_queue <client_name> <school_name> <course_name>"):
                    _, _, client_name, school_name, course_name = parts
                    client = self.get_agent_or_error(client_name, Client, "client_not_found")
                    if client:
                        client.join_enrollment_queue(school_name, course_name)
                        
            elif parts[1] == 'assist_course':
                if self.validate_command(parts, 4, "invalid_format", "client assist_course <client_name> <course_name>"):
                    _, _, client_name, course_name = parts
                    client = self.get_agent_or_error(client_name, Client, "client_not_found")
                    if client:
                        client.assist_course(course_name)

            elif   parts[1] == 'show_list':
                if self.validate_command(parts, 2, "invalid_format", "client show_list"):
                    self.agent_manager.list_agents(Client)
            
            elif   parts[1] == 'take_exam':
                if self.validate_command(parts, 5, "invalid_format", "client take_exam <client_name> <course_name> <exam_name>"):
                    _, _, client_name, course_name, exam_name = parts
                    client = self.get_agent_or_error(client_name, Client, "client_not_found")
                    if client:
                        client.take_exam(course_name, exam_name)
                    
            elif   parts[1] == 'remove_client':
                if self.validate_command(parts, 3, "invalid_format", "client remove_client <client_name>"):
                    _, _, client_name = parts
                    client = self.get_agent_or_error(client_name, Client, "client_not_found")
                    if client:
                        client.remove_client()

            else:
                print(self.ERROR_MESSAGES["invalid_format"])
                self.help_client()
                
        else:
            print("Unknown command. Type 'help' for a list of commands.")


# ## Stack

# In[ ]:


class Stack:
    def __init__(self):
        self.stack = []

    def is_empty(self):
        return True if len(self.stack) == 0 else False
    
    def push(self, item):
        self.stack.append(item)
        
    def pop(self):
        return None if self.is_empty() else self.stack.pop()
    
    def peek(self):
        return None if self.is_empty () else self.stack[-1]
    


# ## Queue

# In[ ]:


class Queue:
    
    def __init__(self):
        self.queue = []        
    
    def is_empty (self):
        return True if len(self.queue) == 0 else False
    
    def peek(self):
        return None if self.is_empty () else self.queue[0]
    
    def enqueue (self, item):
        self.queue.append(item)
    
    def dequeue(self):
        return None if self.is_empty() else self.queue.pop(0)
    
    def size(self):
        return len(self.queue)
    
    def pop(self):
        return None if self.is_empty() else self.stack.pop()
    
    def peek(self):
        return None if self.is_empty () else self.stack[-1]
    


# ## General agent dictionary

# In[ ]:


# Diccionario global para almacenar agentes
agents = {}


# # Main program

# In[ ]:


import time
if __name__ == "__main__":
    simulation = CitySimulation()
    simulation.command_loop() 

