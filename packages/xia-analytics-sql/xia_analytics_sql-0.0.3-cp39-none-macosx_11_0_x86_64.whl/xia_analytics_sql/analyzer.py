from typing import Type
from xia_engine import BaseDocument, BaseEngine
from xia_analytics import Analyzer


class SqlAnalyzer(Analyzer):
   analytic_sql_template = """WITH
 data_model AS (
 {}
 )
 {}
   """

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
       sql_statement = analytic_request.get("sql", "")
       source_statement, source_values = engine.get_search_sql(document_class, False)
       if sql_statement:
           final_statement = cls.analytic_sql_template.format(source_statement, sql_statement)
           return {engine: {"sql": final_statement, "values": source_values}}
       return {engine: {}}
