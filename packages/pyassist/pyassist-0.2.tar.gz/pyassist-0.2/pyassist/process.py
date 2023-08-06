import subprocess
from .utils import Utilities
# Contains Process/ Subprocess related Functions
class Process(Utilities):
    def __init__(self, **kwargs):
        if "name" not in kwargs:
            kwargs["name"] = (f"{__class__}".split("'")[1])
        super().__init__(**kwargs)
        self.debug(f"Initialized: {kwargs['name']}")

    def run_process(self, process_list, stream=False):
        header = "run_process: "
        self.info(header + str(process_list))
        process = subprocess.Popen(process_list[0],
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        
        outputs = []
        errors = []
        if(stream):
            self.info(header + "Stream start")
            while True:
                # self.info(process.stdout.readline())
                output = self.decode(process.stdout.readline())
                outputs.append(output)
                errorline = self.decode(process.stderr.readline())
                errors.append(errorline)
                if((errorline) and ("SSHelper" not in errorline)):
                    # if "Connection refused" in errorline:
                    #     raise CustomError(1)
                    # if "closed" in errorline:
                    #     raise CustomError(1)
                    # else:
                    self.info("Error: " + errorline)
                if (output == '') and (process.poll() is not None) and (errorline == ''):
                    break
                if output:
                    self.info(header + output)
                    # self.info(header + output.strip())
            self.info(header + "Stream End")
            #rc = process.poll()
            return outputs, errors
        return process.communicate()
