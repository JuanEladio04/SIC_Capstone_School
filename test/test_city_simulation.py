import unittest
from io import StringIO
import sys
from test.CitySimulation import CitySimulation
import time

class TestCitySimulation(unittest.TestCase):
    test_number = 0
    def setUp(self):
        self.simulation = CitySimulation()

    def run_command_and_assert(self,command, expected_output):
        try:
            output = StringIO()
            sys.stdout = output
            self.simulation.process_command(command)
            sys.stdout = sys.__stdout__
            result_output = output.getvalue()
            TestCitySimulation.test_number +=1
            print(f'# {TestCitySimulation.test_number}\n>{command}\n{result_output.strip()}',end='')
            self.assertIn(expected_output, result_output)
            print(' "✅ Test passsed!"')
        except AssertionError:
            print()
            print("="*40)
            print(' "❌ Test not passsed!"') 
            print("="*40)
            print(f'AssertionError: Expected output\n"{expected_output}"\nnot found in actual output:\n"{result_output.strip()}"')
            follow=input("q: quit, press other key continue...")
            if follow=='q':
                sys.exit(1)


    def test_commands(self):
        print('➡️ Testing ...')
        # Creating a client and a school
        self.run_command_and_assert("client add_client Billy", "Client 'Billy' added to the system.")
        self.run_command_and_assert("school add_school EOI", "School 'EOI' added to the system.")
        
        self.run_command_and_assert("school show_list", "Current School(s):\nEOI")
        self.run_command_and_assert("client show_list", "Current Client(s):\nBilly")
        
        # Creating a new course
        self.run_command_and_assert("school create_course Python EOI", "Course 'Python' has been created in school 'EOI'.")
        
        # Show the existing courses 
        self.run_command_and_assert("school show_courses EOI", "Courses in school 'EOI':\n- Python")
        
        # Add an exam to the course
        self.run_command_and_assert("school add_exam_to_course EOI Python Chapter01", "The exam 'Chapter01' has been added to course 'Python'.")
        
        # Client enrolls in a school
        self.run_command_and_assert("client enroll_in_school Billy EOI", "Client 'Billy' has been enrolled in school 'EOI'.")

        #Client join enrollment queue for a course
        self.run_command_and_assert("client join_enrollment_queue Billy EOI Python", "Billy joined the enrollment queue for Python in EOI.")

        # Show the enrollment queue
        
        # Client leaves the school
        self.run_command_and_assert("client leave_school Billy", "Billy exited EOI.")
        
        # Client is removed from the school
        self.run_command_and_assert("client enroll_in_school Billy EOI", "Client 'Billy' has been enrolled in school 'EOI'.")
        self.run_command_and_assert("school remove_student EOI Billy", "Student 'Billy' has been removed from school 'EOI'.")
        
        # Removing client and school
        self.run_command_and_assert("client remove_client Billy", "Agent Billy removed from the system.")
        self.run_command_and_assert("school remove_school EOI", "Agent EOI removed from the system.")

        
    def test_client_add_client(self):
        print('➡️ Testing client add_client <client_name> ...')                
        # Creating a client
        self.run_command_and_assert("client add_client Billy", "Client 'Billy' added to the system.")
        # Trying to create the same client again
        self.run_command_and_assert("client add_client Billy", "Client 'Billy' already exists.")
        
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        self.run_command_and_assert("client remove_client Billy", "Agent Billy removed from the system.")


    def test_school_add_school(self):
        print('➡️ Testing school add_school <school_name> ...')
        # Creating a school
        self.run_command_and_assert("school add_school EOI", "School 'EOI' added to the system.")
        # Trying to create the same school again
        self.run_command_and_assert("school add_school EOI", "School 'EOI' already exists.")
        
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        self.run_command_and_assert("school remove_school EOI", "Agent EOI removed from the system.")
        
    
    def test_school_show_list(self):
        print('➡️ Testing school show_list ...')
        # Show the list of school with any existing school.
        self.run_command_and_assert("school show_list", "Current School(s):")
        # Creates a new school.
        self.run_command_and_assert("school add_school EOI", "School 'EOI' added to the system.")
        # Show the list of schools.
        self.run_command_and_assert("school show_list", "Current School(s):\nEOI")
        # Removes the school from the system.
        self.run_command_and_assert("school remove_school EOI", "Agent EOI removed from the system.")
        
    
    def test_client_show_list(self):
        print('➡️ Testing client show_list ...')
        # Show the list of school with any existing school.
        self.run_command_and_assert("client show_list", "Current Client(s):")
        # Creates a new school.
        self.run_command_and_assert("client add_client Billy", "Client 'Billy' added to the system.")
        # Show the list of schools.
        self.run_command_and_assert("client show_list", "Current Client(s):\nBilly")
        # Removes the school from the system.
        self.run_command_and_assert("client remove_client Billy", "Agent Billy removed from the system.")
        
    
    def test_school_create_course(self):
        print('➡️ Testing school create_course <course_name> ...')
        self.run_command_and_assert("school add_school EOI", "School 'EOI' added to the system.")
        # --------------------------------------------------------------------------------------------------------------------------------------------------

        # Create a course        
        self.run_command_and_assert("school create_course Python EOI", "Course 'Python' has been created in school 'EOI'.")
        # Try to create the same course again
        self.run_command_and_assert("school create_course Python EOI", "Course 'Python' already exists in school 'EOI'.")
        # Create a course in a school that does not exist
        self.run_command_and_assert("school create_course Python Instituto", "Error: School 'Instituto' not found.")
        
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        self.run_command_and_assert("school remove_school EOI", "Agent EOI removed from the system")
    
    
    def test_school_show_courses(self):
        print('➡️ Testing school show_courses <school_name> ...')
        self.run_command_and_assert("school add_school EOI", "School 'EOI' added to the system.")
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        #Show courses when they are empty
        self.run_command_and_assert("school show_courses EOI", "There is no courses in school 'EOI'.")
        #Create courses
        self.run_command_and_assert("school create_course Python EOI", "'Python' has been created in school 'EOI'.")
        #Show courses
        self.run_command_and_assert("school show_courses EOI", "Courses in school 'EOI':\n- Python")
        #Show courses for a school that does not exist
        self.run_command_and_assert("school create_course Python Instituto", "Error: School 'Instituto' not found.")
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        self.run_command_and_assert("school remove_school EOI", "Agent EOI removed from the system")

    
    def test_school_add_exam_to_course(self):
        print('➡️ Testing school add_exam_to_course <school_name> <course_name> <exam_name> ...')
        self.run_command_and_assert("school add_school EOI", "School 'EOI' added to the system.")
        self.run_command_and_assert("school add_school Instituto", "School 'Instituto' added to the system.")
        self.run_command_and_assert("school create_course Python EOI", "'Python' has been created in school 'EOI'.")
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        
        #Adding a new exam to the course
        self.run_command_and_assert("school add_exam_to_course EOI Python Chapter01", "The exam 'Chapter01' has been added to course 'Python'.")
        #Adding an existing exam to the course
        self.run_command_and_assert("school add_exam_to_course EOI Python Chapter01", "The exam 'Chapter01' already exists and is associated with course 'Python'.")
        #Adding an exam to an non existing course
        self.run_command_and_assert("school add_exam_to_course Instituto Python Chapter01", "The course 'Python' is not found at the school Instituto.")
        
        
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        self.run_command_and_assert("school remove_school EOI", "Agent EOI removed from the system.")
        self.run_command_and_assert("school remove_school Instituto", "Agent Instituto removed from the system.")


    def test_client_enroll_in_school(self): 
        print('➡️ Testing client enroll_in_school <client_name> <school_name> ...')
        self.run_command_and_assert("client add_client Billy", "Client 'Billy' added to the system.") 
        self.run_command_and_assert("school add_school EOI", "School 'EOI' added to the system.")
        # --------------------------------------------------------------------------------------------------------------------------------------------------

        # Client enrolls in a school
        self.run_command_and_assert("client enroll_in_school Billy EOI", "Client 'Billy' has been enrolled in school 'EOI'.")
        # Client tries to enroll in the same school again
        self.run_command_and_assert("client enroll_in_school Billy EOI", "Client Billy is already enrolled in EOI.")
        # Client tries to enroll in a non-existent school.
        self.run_command_and_assert("client enroll_in_school Billy Instituto", "School 'Instituto' not found.")
        
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        self.run_command_and_assert("client remove_client Billy", "Agent Billy removed from the system.")
        self.run_command_and_assert("school remove_school EOI", "Agent EOI removed from the system.")
    
    
    def test_client_join_enrollment_queue(self):
        print('➡️ Testing client join_enrollment_queue <client_name> <school_name> <course_name> ...') 
        self.run_command_and_assert("client add_client Billy", "Client 'Billy' added to the system.")
        self.run_command_and_assert("school add_school EOI", "School 'EOI' added to the system.")
        self.run_command_and_assert("school add_school Carlos_Cano", "School 'Carlos_Cano' added to the system.")
        self.run_command_and_assert("client enroll_in_school Billy EOI", "Client 'Billy' has been enrolled in school 'EOI'.")
        self.run_command_and_assert("school create_course Python EOI", "Course 'Python' has been created in school 'EOI'.")
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        
        # Client joins the enrollment queue for a school
        self.run_command_and_assert("client join_enrollment_queue Billy EOI Python", "Billy joined the enrollment queue for Python in EOI.")
        # Client tries to join the same queue again
        self.run_command_and_assert("client join_enrollment_queue Billy EOI Python", "Billy is already in the enrollment queue for Python in EOI.")
        # Client tries to join a different queue in the same school
        self.run_command_and_assert("client join_enrollment_queue Billy EOI Ciencias", "Ciencias is not available in EOI.")
        # Client tries to join a queue for a different school
        self.run_command_and_assert("client join_enrollment_queue Billy Carlos_Cano Python", "Billy is not enrolled in Carlos_Cano.")
        # Client tries to join a non existing school
        self.run_command_and_assert("client join_enrollment_queue Billy Palmera Python", "School 'Palmera' do not exist.")
        
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        self.run_command_and_assert("client remove_client Billy", "Agent Billy removed from the system.")
        self.run_command_and_assert("school remove_school EOI", "Agent EOI removed from the system.")
        self.run_command_and_assert("school remove_school Carlos_Cano", "Agent Carlos_Cano removed from the system.")
    
    
    def test_school_show_enrollment_queue(self):
        pass
    
    
    def test_client_leave_school(self):
        print('➡️ Testing client leave_school <client_name> ...')
        self.run_command_and_assert("client add_client Billy", "Client 'Billy' added to the system.")
        self.run_command_and_assert("school add_school EOI", "School 'EOI' added to the system.")
        self.run_command_and_assert("client enroll_in_school Billy EOI", "Client 'Billy' has been enrolled in school 'EOI'.")
        # --------------------------------------------------------------------------------------------------------------------------------------------------

        # Client leaves the school
        self.run_command_and_assert("client leave_school Billy", "Billy exited EOI.")
        # Client tries to leave the same school again
        self.run_command_and_assert("client leave_school Billy", "Billy is not currently enrolled in any school.")
        
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        self.run_command_and_assert("client remove_client Billy", "Agent Billy removed from the system.")
        self.run_command_and_assert("school remove_school EOI", "Agent EOI removed from the system.")


    def test_client_remove_client(self):
        print('➡️ Testing client remove_client <client_name> ...')
        self.run_command_and_assert("client add_client Billy", "Client 'Billy' added to the system.")
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        # Remove client
        self.run_command_and_assert("client remove_client Billy", "Agent Billy removed from the system.")
        # Client tries to leave again
        self.run_command_and_assert("client remove_client Billy", "Client 'Billy' not found.")
        
        
    def test_school_remove_school(self):
        print('➡️ Testing school remove_school <school_name> ...')
        self.run_command_and_assert("school add_school EOI", "School 'EOI' added to the system.")
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        # Remove school
        self.run_command_and_assert("school remove_school EOI", "Agent EOI removed from the system.")
        # School tries to leave again
        self.run_command_and_assert("school remove_school EOI", "Client 'EOI' not found.")
    
    
    def test_school_remove_student(self):
        print('➡️ Testing school remove_student <school_name> <client_name> ...')
        self.run_command_and_assert("client add_client Billy", "Client 'Billy' added to the system.")
        self.run_command_and_assert("school add_school EOI", "School 'EOI' added to the system.")
        self.run_command_and_assert("client enroll_in_school Billy EOI", "Client 'Billy' has been enrolled in school 'EOI'.")
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        # Remove client from school
        self.run_command_and_assert("school remove_student EOI Billy", "Student 'Billy' has been removed from school 'EOI'.")
        # Try to remove again from school
        self.run_command_and_assert("school remove_student EOI Billy", "Student 'Billy' not found in school 'EOI'.")
        #Try to remove from a non existent school
        self.run_command_and_assert("school remove_student Palmera Billy", "Error: School 'Palmera' not found.")
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        self.run_command_and_assert("client remove_client Billy", "Agent Billy removed from the system.")
        self.run_command_and_assert("school remove_school EOI", "Agent EOI removed from the system.")

        
if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCitySimulation)
    unittest.TextTestRunner(verbosity=2).run(suite)
