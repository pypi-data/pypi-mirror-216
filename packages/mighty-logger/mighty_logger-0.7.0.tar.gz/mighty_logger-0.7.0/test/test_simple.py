from time import sleep

from mighty_logger import SimpleLogger
from mighty_logger.src import LogEnvironments

if __name__ == "__main__":
	logger = SimpleLogger("Installer", LogEnvironments.PLAIN, 115)
	sleep(1)
	logger.message("Program installation started")
	sleep(1)
	logger.warning("Newer version found")
	sleep(1)
	logger.separator()
	sleep(1)
	data = logger.input("Enter password: ")
	sleep(1)
	logger.error("Incompatibility found")
	sleep(1)
	logger.fail("Program not installed")
	sleep(1)
	logger.print(data)
	sleep(1)
	logger.save("log", True)
	sleep(1)
	logger.debug("la la la")
	sleep(1)
	logger.load("log")
	sleep(1)
	logger.debug("bla bla bla")
	sleep(1)
	logger.get_logger().extractly(2)
	sleep(1)
	logger.debug("String has deleted")
	sleep(1)
	logger.print(logger.get_logger().catchy(1))
