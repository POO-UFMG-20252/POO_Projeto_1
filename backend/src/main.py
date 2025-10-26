from database.connection import DatabaseConnection
from controllers.main_controller import MainController

def main():
	controller = MainController()
	controller.serve()

main()