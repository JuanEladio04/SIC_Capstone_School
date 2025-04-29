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
            print(' "Test passsed!"')
        except AssertionError:
            print()
            print("="*40)
            print(' "Test not passsed!"') 
            print("="*40)
            print(f'AssertionError: Expected output\n"{expected_output}"\nnot found in actual output:\n"{result_output.strip()}"')
            follow=input("q: quit, press other key continue...")
            if follow=='q':
                sys.exit(1)


    def test_commands(self):
        print('-> Testing ...')
        # Creating a client and a school
        self.run_command_and_assert("client add_client Billy", "Client 'Billy' added to the system.")
        self.run_command_and_assert("school add_school EOI", "School 'EOI' added to the system.")
        
        #Creating a new course
        self.run_command_and_assert("school create_course Lengua EOI", "'Lengua' has been created in school 'EOI'.")
        
        # Client enrolls in a school
        self.run_command_and_assert("client enroll_in_school Billy EOI", "Client 'Billy' has been enrolled in school 'EOI'.")
        
        #Client joint enrollment queue for a course
        self.run_command_and_assert("client join_enrollment_queue Billy EOI Lengua", "Billy joined the enrollment queue for Lengua in EOI.")
        
        # Client leaves the school
        self.run_command_and_assert("client leave_school Billy", "Billy exited EOI.")
        
        # Removing client and school
        self.run_command_and_assert("client remove_client Billy", "Agent Billy removed from the system.")
        self.run_command_and_assert("school remove_school EOI", "Agent EOI removed from the system.")
    
        
    def test_client_add_client(self):
        print('-> Testing client add_client <client_name> ...')                
        # Creating a client
        self.run_command_and_assert("client add_client Billy", "Client 'Billy' added to the system.")
        
        # Trying to create the same client again
        self.run_command_and_assert("client add_client Billy", "Client 'Billy' already exists.")
        
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        self.run_command_and_assert("client remove_client Billy", "Agent Billy removed from the system.")
        

    def test_school_add_school(self):
        print('-> Testing school add_school <school_name> ...')
        # Creating a school
        self.run_command_and_assert("school add_school EOI", "School 'EOI' added to the system.")
        
        # Trying to create the same school again
        self.run_command_and_assert("school add_school EOI", "School 'EOI' already exists.")
        
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        self.run_command_and_assert("school remove_school EOI", "Agent EOI removed from the system.")
        
    
    def test_client_enroll_in_school(self):
        print('-> Testing client enroll_in_school <client_name> <school_name> ...')
        self.run_command_and_assert("client add_client Billy", "Client 'Billy' added to the system.")
        self.run_command_and_assert("school add_school EOI", "School 'EOI' added to the system.")
        # --------------------------------------------------------------------------------------------------------------------------------------------------

        # Client enrolls in a school
        self.run_command_and_assert("client enroll_in_school Billy EOI", "Client 'Billy' has been enrolled in school 'EOI'.")
        
        # Client tries to enroll in the same school again
        self.run_command_and_assert("client enroll_in_school Billy EOI", "Client Billy is already enrolled in EOI.")
        
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        self.run_command_and_assert("client remove_client Billy", "Agent Billy removed from the system.")
        self.run_command_and_assert("school remove_school EOI", "Agent EOI removed from the system.")
    
    
    def test_client_join_enrollment_queue(self):
        print('-> Testing client join_enrollment_queue <client_name> <school_name> <course_name> ...') 
        self.run_command_and_assert("client add_client Billy", "Client 'Billy' added to the system.")
        self.run_command_and_assert("school add_school EOI", "School 'EOI' added to the system.")
        self.run_command_and_assert("school add_school Carlos_Cano", "School 'Carlos_Cano' added to the system.")
        self.run_command_and_assert("client enroll_in_school Billy EOI", "Client 'Billy' has been enrolled in school 'EOI'.")
        self.run_command_and_assert("school create_course Lengua EOI", "'Lengua' has been created in school 'EOI'.")
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        
        # Client joins the enrollment queue for a school
        self.run_command_and_assert("client join_enrollment_queue Billy EOI Lengua", "Billy joined the enrollment queue for Lengua in EOI.")
        
        # Client tries to join the same queue again
        self.run_command_and_assert("client join_enrollment_queue Billy EOI Lengua", "Billy is already in the enrollment queue for Lengua in EOI.")
        
        # Client tries to join a different queue in the same school
        self.run_command_and_assert("client join_enrollment_queue Billy EOI Ciencias", "Ciencias is not available in EOI.")
        
        # Client tries to join a queue for a different school
        self.run_command_and_assert("client join_enrollment_queue Billy Carlos_Cano Lengua", "Billy is not enrolled in Carlos_Cano.")
        
        # Client tries to join a non existing school
        self.run_command_and_assert("client join_enrollment_queue Billy Palmera Lengua", "School 'Palmera' do not exist.")
        
        # --------------------------------------------------------------------------------------------------------------------------------------------------
        self.run_command_and_assert("client remove_client Billy", "Agent Billy removed from the system.")
        self.run_command_and_assert("school remove_school EOI", "Agent EOI removed from the system.")
    
    
    def test_client_leave_school(self):
        print('-> Testing client leave_school <client_name> ...')
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


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCitySimulation)
    unittest.TextTestRunner(verbosity=2).run(suite)
