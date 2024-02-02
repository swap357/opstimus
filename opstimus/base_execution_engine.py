from abc import ABC, abstractmethod

class BaseExecutionEngine(ABC):
    """
    Abstract base class for execution engines.
    Defines the interface for executing configurations like playbooks, scripts, etc.
    """
    @abstractmethod
    def execute(self, task_name, *args, **kwargs):
        """
        Execute a task.
        
        Parameters:
            task_name (str): The name of the task to be executed.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
            
        Returns:
            result (dict): The result of the execution.
        """
        pass
    
    @abstractmethod
    def validate_execution(self, task_name):
        """
        Validate if a task can be executed.
        
        Parameters:
            task_name (str): The name of the task to be validated.
            
        Returns:
            is_valid (bool): True if the task is valid and can be executed, False otherwise.
        """
        pass
