from typing import Type
from xia_engine import BaseDocument
from xia_engine import BaseEngine


class Analyzer:
   @classmethod
   def compile(cls, document_class: Type[BaseDocument], engine: Type[BaseEngine],
               analytic_request: dict, acl_condition=None):
       """Compile the analysis request

       Args:
           document_class (`subclass` of `BaseDocument`): Document definition
           engine: (`subclass` of `BaseDocument`): Engine for which the analytical model should be executed
           analytic_request: analytic request
           acl_condition: Extra where condition given by user acl objects

       Returns:
           A analytic model which could be executed by the engine
       """
       return {engine: {}}
