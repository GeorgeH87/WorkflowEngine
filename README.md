# Workflow Engine

## introduction

**workflowengine** is a library to process processes and tasks in a standardized manner.  

## Installing WorkflowEngine and Supported Versions

The **workflowengine** is available on PyPI:

```console
$ python -m pip install workflowengine
```

## Implementation 

### Processor
A Workflow processor is the main instance which will handle a list of entities 
and passes them to the assigned tasks. The handled entities should inherit 
from the workflow model type.

Since the workflow processor is an abstract class, the following methods have 
to be implemented in the inherited class:

- **get_default_subscriptions** returns a list of unparsed entries
- **get_entry** parses the raw entries retrieved by the previous method to an 
object which inherits from the `WorkflowModel`
- **filter** define some preconditions
- **get_tasks** returns a list of instances which inherit from the workflow 
task
- **write_entry** handle a processed (successfully or unsuccessfully) entry. 
Write it to the cache or to the disk
- **close** handle the finale state of the workflow

### Model
Basic implementation of an entity. Delivers field and methods to check, wether 
the task has already been executed, if there is a related error or if the 
entry should be executed again.

### Task
Basic implementation of a task which should be executed for a workflow

## Status

The following use cases can be handled:

 flow type     | **Exception** | **StatusException** | **OnSuccess** 
---------------|---------------|---------------------|--------------------
 **skip**      | -             | -                   | x                  
 **interrupt** | x             | x                   | -                  
 **repeat**    | (-)           | x                   | x      

- **Exception** in case of an Exception which is not an instance of  
`StatusException` the workflow will be interrupted. An operator has the 
possibility to set the repeat property
- **StatusException** will interrupt the workflow and set the `Status` object 
which can contain any repeat property
- **OnSuccess** can return a `Status` can contain any repeat property. To 
*skip* the task it is not necessary to implement a dedicated status. Just 
return a `Status` to exit the task

### Exception Handling
In case of unexpected Exceptions the workflow for the handled entry will be 
cancelled. The stacktrace will be logged. An unique id is assigned to each  
exception. The error id will be persisted into your status file and into the 
logs.

