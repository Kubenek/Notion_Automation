import sys
import os
from colorama import Fore, Style
from datetime import datetime

def printException(ExceptionMessage):
    ExceptionMessage = str(ExceptionMessage)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    fpath = exc_tb.tb_frame.f_code.co_filename
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    with open("error.log", "a") as f:
        f.write(f"Exception type - {exc_type}\n")
        f.write(f"File - {fname} | Line - {exc_tb.tb_lineno}\n")
        f.write(f"Time - {formatted_datetime}\n")
        f.write(f"Message - {ExceptionMessage}\n")
        f.write("\n")  

    print(f'\n{Style.RESET_ALL}{Fore.YELLOW}] {Style.RESET_ALL}{formatted_datetime}{Style.RESET_ALL}{Fore.RED} [ERROR]      {Style.RESET_ALL}{Fore.MAGENTA}  function.error{Style.RESET_ALL} there was an error in the code! Please check the error.log file!')