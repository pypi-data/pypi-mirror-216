# Cypher AI Helper

A helper library for creating Cypher queries with OpenAI API.

## Installation

```bash
pip install cypher-ai-helper
```

## Usage

Start a local neo4j database:

```bash
sh infra/start_neo4j.sh
```

or

```bash
docker run \
    --name neo4j \
    -p 27474:7474 -p 27687:7687 \
    -d \
    -e NEO4J_AUTH=neo4j/pleaseletmein \
    -e NEO4J_PLUGINS=\[\"apoc\"\]  \
    neo4j:latest
```

Then you can run the following:

> Note: You need to set the `OPENAI_API_KEY` environment variable to your OpenAI API key.

```python
import functools

from neo4j import GraphDatabase
from pydantic import BaseModel, Field

from cypher_ai_helper.main import cypher_query, execute_query
from cypher_ai_helper.utils import pydantic_models_to_str


class User(BaseModel):
    """
    A User class
    """
    id: int = Field(..., description="The id of the user")
    name: str = Field(..., description="The name of the user")
    email: str = Field(..., description="The email of the user")


class Post(BaseModel):
    """
    A Post class
    """
    id: int = Field(..., description="The id of the post")
    title: str = Field(..., description="The title of the post")
    body: str = Field(..., description="The body of the post")
    user_name: str = Field(..., description="The name of the user who created the post")


_q = cypher_query("del-all", pydantic_models_to_str([User, Post]),
                  "Delete all nodes and relations",
                  input_vars=[],
                  func=functools.partial(execute_query, driver=GraphDatabase.driver("bolt://localhost:27687",
                                                                                    auth=("neo4j",
                                                                                          "pleaseletmein")),
                                         database="neo4j"))

_q = cypher_query("new-user", pydantic_models_to_str([User, Post]),
                  "Create a new user and return the created user",
                  input_vars=["id", "name", "email"],
                  func=functools.partial(execute_query, driver=GraphDatabase.driver("bolt://localhost:27687",
                                                                                    auth=("neo4j",
                                                                                          "pleaseletmein")),
                                         database="neo4j", params={"id": 2, "name": "post_user", "email": "test"}))
```