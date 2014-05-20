#include <Python.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <readline/readline.h>
#include <readline/history.h>
 
static PyObject *dispatch_callback = NULL;

static PyObject* start(PyObject* self)
{
    char* input;

    PyObject *arglist;
    PyObject *result;
 
    // Configure readline to auto-complete paths when the tab key is hit.
    rl_bind_key('\t', rl_complete);
 
    for(;;) {

        input = readline(">> ");
 
        // Check for EOF.
        if (!input)
            break;

        // Add input to history.
        //add_history(input);

        arglist = Py_BuildValue("(s)", input);
        result = PyObject_CallObject(dispatch_callback, arglist);
        Py_DECREF(arglist);
        if (result == NULL)
            return NULL;
        Py_DECREF(result);
 
        free(input);
    }

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* set_dispatch_callback(PyObject *dummy, PyObject *args)
{
    PyObject *result = NULL;
    PyObject *temp;

    if (PyArg_ParseTuple(args, "O:set_callback", &temp)) {
        if (!PyCallable_Check(temp)) {
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
        Py_XINCREF(temp);         /* Add a reference to new callback */
        Py_XDECREF(dispatch_callback);  /* Dispose of previous callback */
        dispatch_callback = temp;       /* Remember new callback */
        /* Boilerplate to return "None" */
        Py_INCREF(Py_None);
        result = Py_None;
    }
    return result;
}

static PyMethodDef clamshellrl_funcs[] = {
    {"start", (PyCFunction)start, 
     METH_NOARGS, "Add doc here"},
    {"set_dispatch_callback", (PyCFunction)set_dispatch_callback,
     METH_VARARGS, "Callback"},
    {NULL}
};

void initclamshellrl(void)
{
    Py_InitModule3("clamshellrl", clamshellrl_funcs,
                   "Extension module example!");
}
