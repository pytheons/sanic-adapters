
![sanic-adapters-200](https://github.com/user-attachments/assets/c68e7b2a-7c69-4056-b5b2-17c5fd92304c)

# Sanic Adapters
Set of semi-adapters for Sanic framework to autodiscovery routes defined by adapters @route decorator
instead of defining multiple resources or registering each route, resource, and blueprint in separate calls.


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

# In future
- Add other adapters to be less RESTfish or RESTFull
- Add support for Class Based Websockets 
- Add support for Class Based Middlewares
- More Refactors and Simplifications with optimisation 
