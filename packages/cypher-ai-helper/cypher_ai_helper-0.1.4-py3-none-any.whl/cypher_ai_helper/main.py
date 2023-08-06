"""
Main module for Cypher AI Helper
"""
import json
import logging
import os
from time import sleep
from typing import Any

import openai
from neo4j import Driver
from neo4j.exceptions import CypherSyntaxError

from cypher_ai_helper.utils import func_to_json

curdir = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def _send_chat_messages(messages, _model: str = "gpt-3.5-turbo-0613", functions=None) -> Any:
    """
    Send chat messages to the OpenAI API

    :param messages: Messages to send
    :param _model: Model to use
    :param functions: Functions to use
    :return: Response from the API
    """
    max_retry = 7
    retry = 0
    while True:
        try:
            if functions:
                response = openai.ChatCompletion.create(
                    model=_model,
                    messages=messages,
                    functions=functions if functions else [],
                    # auto is default, but we'll be explicit,
                    function_call="auto",
                    # we don't want creativity but consistency
                    temperature=0.0,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    max_tokens=256,
                )
            else:
                response = openai.ChatCompletion.create(
                    model=_model,
                    messages=messages,
                    temperature=0.0,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    max_tokens=256,
                )
            # decode utf-8 bytes to unicode
            return response["choices"][0]["message"]
        except Exception as oops:
            logger.warning(f'\n\nError communicating with OpenAI: "{oops}"')
            if 'maximum context length' in str(oops):
                a = messages.pop(1)
                logger.warning(f'\n\n DEBUG: Trimming oldest message: {a}')
                continue
            retry += 1
            if retry >= max_retry:
                logger.error(f"\n\nExiting due to excessive errors in API: {oops}")
                raise oops
            logger.warning(f'\n\nRetrying in {2 ** (retry - 1) * 5} seconds...')
            sleep(2 ** (retry - 1) * 5)


def execute_query(query: str, driver: Driver, database: str, params: dict[str, Any] = None) -> list[any]:
    """
    Executes Neo4j query and returns all results

    :param query: Query to run
    :param driver: Driver to use in Neo4j
    :param database: Database to use in Neo4j
    :param params: Parameters to use in the query
    :return:
    """
    _results = []
    with driver.session(database=database) as session:
        logger.debug(f"Executing query: {query} with params: {params}")
        result = session.run(query=query, parameters=params)
        for record in result:
            _results.append(record)
    return _results


query_cache = {}


def cypher_query(query_id: str, schema: str, instruction: str, input_vars: list[str], model="gpt-3.5-turbo-0613",
                 overwrite_cache: bool = False, func: callable = None) -> tuple[str, Any]:
    """
    Generate a Cypher query based on schema, input data and a question

    :param query_id: Query ID - the query ID to store in cache
    :param schema: Schema of the data - the schema of the data to use in the Cypher query
    :param instruction: Instruction from the user
    :param input_vars: Input variables - list of input variables to use in the Cypher query
    :param model: Model to use - OpenAI Model to use
    :param overwrite_cache: Overwrite cache - boolean flag to overwrite cache (e.g. if the query by id exits in the \
        cache it is removed and a new query is generated)
    :param func: Function to use to test the query
    :return:
    """
    global query_cache

    if overwrite_cache:
        del query_cache[query_id]

    if query_id in query_cache:
        logger.debug(f"Returning cached query for {query_id}")
        return query_cache[query_id]

    with open(os.path.join(curdir, "system_prompt"), "r") as f:
        _system_prompt = f.read()
    with open(os.path.join(curdir, "user_prompt"), "r") as f:
        _prompt = f.read()
    _prompt = _prompt.replace("{{schema}}", schema)
    _prompt = _prompt.replace("{{instruction}}", instruction)
    _prompt = _prompt.replace("{{input_vars}}", ", ".join(input_vars))

    _messages = [
        {"role": "system", "content": _system_prompt},
        {"role": "user", "content": _prompt},
    ]
    _functions = None

    _response_message = _send_chat_messages(_messages, _model=model, functions=_functions)
    _messages.append(json.loads(json.dumps(_response_message, ensure_ascii=False)))
    logger.debug(f"Messages: {_messages}")
    _follow_up_messages = _messages
    if func:
        _new_messages = []
        _functions = [func_to_json(func)]
        assert len(_functions[0]["parameters"]) > 0, "Function must have at least one parameter"
        _new_messages.append(
            {
                "role": "user",
                "content": f"Execute the the following query: {_response_message['content']}\n\n"
                           f"Do not attempt to generate values for placeholders, just execute the query as is.",
            }
        )
        _response_message = _send_chat_messages(_new_messages, _model=model, functions=_functions)
        _new_messages.append(json.loads(json.dumps(_response_message, ensure_ascii=False)))
        logger.debug(f"Messages: {_new_messages}")
        _follow_up_messages = _new_messages

    while "function_call" in _response_message:
        _function_to_call = func
        logger.info(f"Function to call: {_functions[0]['name']}")
        _function_args = json.loads(_response_message["function_call"]["arguments"])
        try:
            _func_response = _function_to_call(**_function_args)
            _follow_up_messages.append(
                {
                    "role": "function",
                    "name": _functions[0]["name"],
                    "content": f"{_func_response}",
                }
            )
            # Note: the below is a bit dumb but works for now
            return next(iter(_function_args.items())), _func_response
        except CypherSyntaxError as e:
            logger.error(f"Error executing query function: {e}")
            _follow_up_messages.append(
                {
                    "role": "function",
                    "name": _functions[0]["name"],
                    "content": f"Error executing query function: {repr(e)}",
                })
            _follow_up_messages.append({
                "role": "user",
                "content": "The query failed. Please consider the error and rewrite the query."
            })
            _response_message = _send_chat_messages(_follow_up_messages, _model=model, functions=_functions)

    logger.debug(f"Messages: {_follow_up_messages}")
    logger.debug(f"LLM Query Response: {_response_message}")
    query_cache[query_id] = _response_message["content"]
    return _response_message["content"], None
