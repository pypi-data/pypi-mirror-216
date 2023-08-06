from typing import List
from dataclasses import dataclass
from subprocess import Popen, PIPE as l
from pysimplelog import Logger
from inspect import getframeinfo, currentframe

logger = Logger(__name__)
logger.set_log_file_basename('run_cmd')
logger.set_minimum_level(logger.logLevels['info'])

@dataclass
class Script():
    
    '''
        Allows you write bash scripts in python code.
        script = Scripts()
        script.cmds = """
                        ls
                        echo "an"
                       """
        script()
    '''
    cmds:str = ''
    
    def __call__(self):
        commmand_list: List[str] = self.cmds.split('\n')
        commmand_list = [cmd.strip() for cmd in commmand_list if cmd]
        return map(run_cmd,commmand_list)

def run_cmd(cmd:str, split:bool=False) -> List[str] or str:
    """
    A simple wrapper for Popon to run shell commands from python
    
    Args:
        cmd str: The comanda you want to run
        example: ls
    Raises:
        OSError: If the command throws an error this  captures it. 
        example: ls /does_not_exist
    Returns:
        List[str] or str: This is output of the cmd, either as a string or
        as list which is the string spilt on endline.
    """    
    
    debug_msg = f"""########
                  {getframeinfo(currentframe())=}
                  {cmd=}{type(cmd)=}
                  {split=}{type(split)=}"""
    logger.debug(debug_msg)
    
    out, err = Popen(cmd,shell=True,stdout=l).communicate()
    debug_msg = f"""What is {out=}?
                    What is {err=}?"""
    logger.debug(debug_msg)
    
    if err:
        error_msg = f"""There was an error:
                        {err}
                        """
        logger.error(error_msg, stack_info= True)
        raise OSError(err)
    return [o for o in out.decode().split('\n') if o] if split else out.decode()