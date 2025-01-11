from sanic_adapters.adapters import RESTFrameworkfrom sanic_adapters.adapters import RESTFrameworkfrom sanic_adapters.resources import RESTResource
![sanic-adapters-200](https://github.com/user-attachments/assets/c68e7b2a-7c69-4056-b5b2-17c5fd92304c)

# Sanic Adapters
Set of semi-adapters for Sanic framework.
The main idea was to autodiscovery routes defined by adapters @route decorator
instead of defining multiple resources or registering each route, resource, and blueprint in separate calls.
Currently 

# Why?
The idea of Adapters is to:
- Simplify the naming convention to be more understandable by each other
- Simplify things like registering blueprints and adding routes to blueprints
- Aggregate each Sanic Classed Based View in one Resource class which is similar to Controller from MVC
- Implement structures and frames as same as the framework helps to implement RESTfish or RESTFull routes in the current framework

# Current version
- Currently, the idea of RESTfish or RESTfull was implemented as a Sanic blueprint (called by this repo as RoutePart)
which is composed of resources called by Sanic as Classed Based Views (HTTPMethodView) but for adapters, it is renamed to RESTResource.
All binding is realized by the RESTFramework resource using the autodiscovery method which imports all routes from a defined package
and build the structure required for the Sanic app.

# Installation
### by pip 

    pip install sanic-adapters

### by poetry

    poetry add sanic-adapters

# Getting started

### Example Directories Structure
```
/project
├── /src
│   ├── /application
│   ├── /domain
│   ├── /infrastructure
│   │   └── /repositories
│   │       └── transactions.py
│   └── /interface
│       └── /sanic
│           ├── /routes
│           │   └── transaction.py
│           ├── server.py
│           └── services.yaml
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── README.md
└── ...
```

### Example `routes/transaction.py`: 
```python
# ../src/interface/sanic/routes/transaction.py
from sanic.response import text
from sanic_adapters.resources import RESTResource
from sanic_adapters.decorators import route
from project.src.infrastructure.repositories.transactions import TransactionsRepository


# [ Optional ] can be used class decorator (ResourceOverride) to change default mapping from Transaction -> /transaction
class Transactions(RESTResource):
    @route(name="list_of_transactions", path="/")
    async def get(self, name: str, transactions: TransactionsRepository):
        return text(f"Hello World my dear {name.title()} {transactions=}")

```
### Example `repositiries/transactions.py`: 
```python
# ../src/infrastructure/repositories/transactions.py
from dataclasses import dataclass


@dataclass
class TransactionsRepository:
    ...

```

### Example `server.py`
```python
# ../src/interface/sanic/server.py
from sanic import Sanic
from sanic_adapters.adapters import RESTFramework
from sanic_adapters.adapters import IoC

app = Sanic("project")

ioc = IoC(app, "services.yaml")
app.blueprint(RESTFramework.autodiscover("project.src.interface.sanic.routes"))  # argument is package path as string

```
OR 

```python
# ../src/interface/sanic/server.py
from sanic import Sanic
from sanic_adapters.adapters import RESTFramework
from sanic_adapters.adapters import IoC

app = Sanic("project")

@app.before_server_start
async def before_start(*_):
    IoC(app, "services.yaml")
    app.blueprint(RESTFramework.autodiscover("project.src.interface.sanic.routes"))  # argument is package path as string

```

### Alternative `server.py` - not tested yet
```python
# ../src/interface/sanic/server.py
from sanic import Sanic
from sanic_adapters.adapters import RESTFramework
from sanic_adapters.adapters import IoC

app = Sanic("project")

ioc = IoC(app, "services.yaml")
rest = RESTFramework(app, "project.src.interface.sanic.routes")  # argument is package path as string

```

or 

```python
# ../src/interface/sanic/server.py
from sanic import Sanic
from sanic_adapters.adapters import RESTFramework
from sanic_adapters.adapters import IoC

app = Sanic("project")

@app.before_server_start
async def before_start(*_):
    IoC(app, "services.yaml")
    RESTFramework(app, "project.src.interface.sanic.routes")  # argument is package path as string

```

### Example `services.yaml`
```yaml
transactions:
  class: "project.src.infrastructure.repositories.transactions.TransactionsRepository"
  provided_by: "Factory"

```

### Example usage out of sanic dependency scope:
```python
from sanic_adapters.adapters import IoC

transaction_repository = IoC.services.transactions()

```

# Documentation
To Be Continued...   
For current release you can use Two important decorators:
### 1. `@ResourceOverride(path=...)`
This is responsible for change default path from register route class name to your custom path   

- Each **Resource class** in `routes package` is register as Sanic `Blueprint` with default name convention of class:  
--> `CamelCase` == will be mapped to route path ==> `/camel-case` - for automatically standard convention  
--> `Classname` == will be mapped to route path ==> `/classname` - for automatically standard convention
- Each **Route** registered by `@route` decorator is annonymous Class Based View with single method 

### 2. `@route(name="...", path="...", method="...")`
This register in static fields each route as single `Class Based View` in sanic app with single method.
Reason of this forcing the user of the framework to use separate request handler as a separate method
of class and design better code with best practicies. The name of endpoint in sanic is kind of unique primary key,
and that means each method of Resource class is a single REST(fish/full) Resource.

#### 🔻 Important 🔻🔻🔻

- **_Name of method_** starting of HTTP method (i.e HTTP METHOD **GET** for function `def get(...)` or
`def get_something(...)`) is automatically mapped to route with HTTP Method "GET"    
- When you use kwargs `method="POST"` in `@route` decorator you can **override** HTTP method for this resource


# In future
- Add other adapters to be less RESTfish or RESTFull
- Add HATEOAS semi-framework (sub-framework) 
- Add decorator to wrap @inject for IoC for Dependency Injector to use injection only by class type hint   
  (maybe this will be new one project for that solution) 

```python
from dataclasses import dataclass
from pytheons.dependency_injector.decorators import service
from project.src.infrastructure.repositories.transactions import TransactionsRepository

@service
@dataclass
class MyService:
  transaction: TransactionsRepository

```  
 
- Add support for Class Based Websockets 
- Add support for Class Based Middlewares
- More Refactors and Simplifications with optimization 
- Add support for `sanic-motor` and move to Data Mapper Pattern based on @dataclass decorator and Domain Driven Design Mapping
