#include <Python.h>

// hello_world function
static PyObject*
hello_world(PyObject *self, PyObject *args) {
    return Py_BuildValue("s", "hello, world!");
}

// module functions table
static PyMethodDef module_functions[] = {
    { "hello_world", hello_world, METH_VARARGS, "print hello world" },
    { NULL, NULL, 0, NULL } /* sentinel */
};

static struct PyModuleDef iterfun_module = {
    PyModuleDef_HEAD_INIT,
    "iterfun",
    NULL,
    -1,
    module_functions
};


// initialize module
PyMODINIT_FUNC PyInit_iterfun(void) {
    return PyModule_Create(&iterfun_module);
}
