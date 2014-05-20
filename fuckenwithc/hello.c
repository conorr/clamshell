#include <Python.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <readline/readline.h>
#include <readline/history.h>
 
static PyObject *my_callback = NULL;

static PyObject* helloworld(PyObject* self)
{
    char* input, shell_prompt[100];

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
        result = PyObject_CallObject(my_callback, arglist);
        Py_DECREF(arglist);
 
        free(input);
    }
}

static PyObject *
my_set_callback(PyObject *dummy, PyObject *args)
{
    PyObject *result = NULL;
    PyObject *temp;

    if (PyArg_ParseTuple(args, "O:set_callback", &temp)) {
        if (!PyCallable_Check(temp)) {
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
        Py_XINCREF(temp);         /* Add a reference to new callback */
        Py_XDECREF(my_callback);  /* Dispose of previous callback */
        my_callback = temp;       /* Remember new callback */
        /* Boilerplate to return "None" */
        Py_INCREF(Py_None);
        result = Py_None;
    }
    return result;
}

static PyMethodDef helloworld_funcs[] = {
    {"helloworld", (PyCFunction)helloworld, 
     METH_NOARGS, "Add doc here"},
    {"my_set_callback", (PyCFunction)my_set_callback,
     METH_VARARGS, "Callback"},
    {NULL}
};

void inithelloworld(void)
{
    Py_InitModule3("helloworld", helloworld_funcs,
                   "Extension module example!");
}

