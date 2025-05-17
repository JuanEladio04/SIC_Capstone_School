# Resultado de la ejecución de los casos de pruebas

**Fuente de revision:** *Copitolo en Visual Studio Code*

**Revisión de resultados e interpretaciones:** *BillyClassTime*

Análisis de la cobertura de las pruebas, En base a los **casos de prueba** proporcionados, en el fichero `test_city_simulation.py`, se puede observar que las pruebas cubren varias funcionalidades y escenarios clave que involucran las interacciones entre las clases mencionadas. 

------

### **1. Clases `Agent` y `AgentManager`**

#### **Clases involucradas:**

- **Agent:** Base de los agentes en el sistema, que representan clientes, escuelas, cursos, entre otros.
- **AgentManager:** Responsable de gestionar los agentes, lo que implica agregar, eliminar y buscar agentes.

#### **Cobertura en las pruebas:**

- **Agent:** Las pruebas no interactúan directamente con la clase `Agent` en sí, pero sus métodos se invocan de manera indirecta cuando se crean instancias de clientes y escuelas. Asegura que los agentes se agreguen y eliminen del sistema de manera correcta en las pruebas.
- **AgentManager:** Las interacciones con `AgentManager` son clave cuando se agregan o eliminan clientes y escuelas. Esto se cubre en pruebas como `test_client_add_client`, `test_school_add_school`, `test_client_remove_client`, y `test_school_remove_school`. La validación de que los agentes sean correctamente gestionados y eliminados se encuentra cubierta.

------

### **2. Clase `Client`**

#### **Comportamiento esperado:**

- Los **clientes** deben poder ser añadidos al sistema, inscribirse en una escuela, unirse a la cola de inscripción de un curso, asistir a clases, tomar exámenes y ser eliminados del sistema.

#### **Cobertura en las pruebas:**

- **Pruebas cubiertas:**
  - **`test_client_add_client`**: Verifica que se pueda agregar un cliente correctamente.
  - **`test_client_enroll_in_school`**: Verifica la inscripción de un cliente en una escuela.
  - **`test_client_leave_school`**: Asegura que un cliente pueda abandonar la escuela correctamente.
  - **`test_client_remove_client`**: Verifica que un cliente sea eliminado correctamente del sistema.
  - **`test_client_assist_course`**: Verifica que un cliente pueda asistir a un curso.
  - **`test_client_join_enrollment_queue`**: Cubre el caso en que un cliente se une a la cola de inscripción de un curso.
  - **`test_client_take_exam`**: Asegura que un cliente pueda tomar un examen en un curso.
- **Cobertura parcial**:
   Las pruebas cubren adecuadamente las interacciones de los **clientes** con las escuelas, cursos, y la gestión de exámenes. Sin embargo, podría haber más pruebas para cubrir otros comportamientos relacionados con los clientes, como si el cliente intenta inscribirse en un curso que no esta en el colegio y realizar acciiones inválidas.

------

### **3. Clase `School`**

#### **Comportamiento esperado:**

- Las **escuelas** deben ser capaces de agregar cursos, agregar y retirar estudiantes, abrir y cerrar el sistema, y gestionar la cola de inscripción para los cursos.

#### **Cobertura en las pruebas:**

- **Pruebas cubiertas:**
  - **`test_school_add_school`**: Verifica la creación de una escuela.
  - **`test_school_open_close`**: Cubre la apertura y cierre de una escuela, con validaciones sobre los estudiantes inscritos.
  - **`test_school_show_list`**: Verifica la lista de escuelas en el sistema.
  - **`test_school_create_course`**: Asegura que se pueda crear un curso dentro de una escuela.
  - **`test_school_show_courses`**: Verifica que se muestren los cursos de una escuela.
  - **`test_school_show_students`**: Asegura que se muestren los estudiantes de una escuela.
  - **`test_school_show_enrollment_queue`**: Verifica que se muestre la cola de inscripción de un curso en la escuela.
  - **`test_school_admit_student_from_queue`**: Asegura que un estudiante pueda ser admitido desde la cola de inscripción.
  - **`test_school_remove_student`**: Verifica que un estudiante pueda ser retirado de la escuela.
  - **`test_school_remove_school`**: Verifica que una escuela pueda ser eliminada del sistema.
- **Cobertura parcial**:
   La cobertura de las pruebas para la clase `School` es bastante sólida. También se podrían probar escenarios más complejos relacionados con la interacción entre los cursos y las escuelas.

------

### **4. Clase `Course`**

#### **Comportamiento esperado:**

- Los **cursos** deben poder ser creados en una escuela, recibir exámenes, y gestionar las inscripciones de estudiantes.

#### **Cobertura en las pruebas:**

- **Pruebas cubiertas:**
  - **`test_school_create_course`**: Verifica que se pueda crear un curso en una escuela.
  - **`test_school_add_exam_to_course`**: Verifica que un examen pueda ser agregado a un curso.
  - **`test_school_show_exams`**: Asegura que los exámenes de un curso se muestren correctamente.
- **Cobertura parcial**:
   Aunque las pruebas cubren las funcionalidades clave, no hay pruebas explícitas sobre la **inscripción de estudiantes en los cursos**. Sería útil agregar una prueba para verificar que los estudiantes no puedan inscribirse en un curso si no están en la cola de inscripción.

------

### **5. Clase `Exam`**

#### **Comportamiento esperado:**

- Los **exámenes** deben estar asociados a los cursos, permitiendo a los estudiantes tomarlos y siendo calificados por las escuelas.

#### **Cobertura en las pruebas:**

- **Pruebas cubiertas:**
  - **`test_school_add_exam_to_course`**: Verifica que un examen sea agregado a un curso.
  - **`test_client_take_exam`**: Verifica que un cliente pueda tomar un examen.
  - **`test_school_grade_exam`**: Asegura que un examen pueda ser calificado correctamente.
  - **`test_school_remove_exam_from_course`**: Verifica que un examen pueda ser eliminado de un curso.
- **Cobertura completa:**
   Las pruebas cubren todos los aspectos importantes de los **exámenes**, desde la adición hasta la calificación y eliminación.

------

### **6. Clase `CitySimulation`**

#### **Comportamiento esperado:**

- La clase **CitySimulation** actúa como el orquestador, manejando las interacciones entre clientes, escuelas, cursos, y otros agentes del sistema.

#### **Cobertura en las pruebas:**

- Las pruebas cubren adecuadamente los **comandos** disponibles, como la adición y eliminación de agentes, la inscripción de estudiantes en cursos y escuelas, el manejo de colas de inscripción, y las interacciones entre las clases.
- **Cobertura completa:**
   Las pruebas están bien distribuidas para validar la **funcionalidad principal** de la simulación, aunque podrían probarse algunos escenarios más complejos relacionados con los **errores** o **acciones inválidas**.

------

### **Conclusión general:**

Las pruebas cubren una **gran parte** de las funcionalidades esperadas para las clases `Agent`, `AgentManager`, `Client`, `School`, `Course`, `Exam` y `CitySimulation`. Sin embargo, algunas áreas podrían beneficiarse de **más cobertura** en situaciones complejas o de **errores** (por ejemplo, al intentar inscribir un estudiante en un curso cerrado, o cuando se eliminan exámenes o cursos con estudiantes activos). En general, el sistema está bien cubierto para los **casos principales** de operación.