/* Generated by Pyrex 0.9.3 on Mon Dec  6 15:39:36 2004 */

#include "Python.h"
#include "structmember.h"
#ifndef PY_LONG_LONG
  #define PY_LONG_LONG LONG_LONG
#endif
#include "stdlib.h"
#include "Numeric/arrayobject.h"


typedef struct {PyObject **p; char *s;} __Pyx_InternTabEntry; /*proto*/
typedef struct {PyObject **p; char *s; long n;} __Pyx_StringTabEntry; /*proto*/
static PyObject *__Pyx_UnpackItem(PyObject *, int); /*proto*/
static int __Pyx_EndUnpack(PyObject *, int); /*proto*/
static int __Pyx_PrintItem(PyObject *); /*proto*/
static int __Pyx_PrintNewline(void); /*proto*/
static void __Pyx_Raise(PyObject *type, PyObject *value, PyObject *tb); /*proto*/
static void __Pyx_ReRaise(void); /*proto*/
static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list); /*proto*/
static PyObject *__Pyx_GetExcValue(void); /*proto*/
static int __Pyx_ArgTypeTest(PyObject *obj, PyTypeObject *type, int none_allowed, char *name); /*proto*/
static int __Pyx_TypeTest(PyObject *obj, PyTypeObject *type); /*proto*/
static int __Pyx_GetStarArgs(PyObject **args, PyObject **kwds, char *kwd_list[], int nargs, PyObject **args2, PyObject **kwds2); /*proto*/
static void __Pyx_WriteUnraisable(char *name); /*proto*/
static void __Pyx_AddTraceback(char *funcname); /*proto*/
static PyTypeObject *__Pyx_ImportType(char *module_name, char *class_name, long size);  /*proto*/
static int __Pyx_SetVtable(PyObject *dict, void *vtable); /*proto*/
static int __Pyx_GetVtable(PyObject *dict, void *vtabptr); /*proto*/
static PyObject *__Pyx_CreateClass(PyObject *bases, PyObject *dict, PyObject *name, char *modname); /*proto*/
static int __Pyx_InternStrings(__Pyx_InternTabEntry *t); /*proto*/
static int __Pyx_InitStrings(__Pyx_StringTabEntry *t); /*proto*/
static PyObject *__Pyx_GetName(PyObject *dict, PyObject *name); /*proto*/

static PyObject *__pyx_m;
static PyObject *__pyx_b;
static int __pyx_lineno;
static char *__pyx_filename;
staticforward char **__pyx_f;

static char __pyx_mdoc[] = "\nA Pyrex extension module.  Currently this extension module allows us\nto:\n\n  1. create an empty Numeric array very efficiently,\n\n  2. Massage a 2D Numeric array into a form usable as a\n     `vtkIdTypeArray`.  This is then used to set the cells of a\n     `vtkCellArray` instance.\n\n    \n\nEric Jones provided a first cut implementation of this using weave.\n";

/* Declarations from array_ext */

static PyTypeObject *__pyx_ptype_9array_ext_ArrayType = 0;
static PyObject *__pyx_k3;
static PyObject *(__pyx_f_9array_ext_c_empty_array(PyArrayObject *,PyObject *)); /*proto*/
static PyObject *(__pyx_f_9array_ext_c_set_id_type_array(PyArrayObject *,PyArrayObject *)); /*proto*/

/* Implementation of array_ext */


static PyObject *__pyx_n_Numeric;
static PyObject *__pyx_n_empty_array;
static PyObject *__pyx_n_set_id_type_array;
static PyObject *__pyx_n_d;

static PyObject *__pyx_n_ValueError;
static PyObject *__pyx_n_MemoryError;

static PyObject *__pyx_k4p;
static PyObject *__pyx_k5p;
static PyObject *__pyx_k6p;
static PyObject *__pyx_k7p;

static char (__pyx_k4[]) = "dimension array must be 1d";
static char (__pyx_k5[]) = "Could not find descriptor from given typecode";
static char (__pyx_k6[]) = "Negative dimensions are not allowed";
static char (__pyx_k7[]) = "Can't allocate memory for array";

static PyObject *__pyx_f_9array_ext_c_empty_array(PyArrayObject *__pyx_v_dims,PyObject *__pyx_v_typecode) {
  char (*__pyx_v_real_type);
  PyArray_Descr (*__pyx_v_descr);
  int __pyx_v_nd;
  int (*__pyx_v_d);
  int __pyx_v_sd;
  int __pyx_v_i;
  char (*__pyx_v_data);
  PyArrayObject (*__pyx_v_op);
  PyObject *__pyx_v_o;
  PyObject *__pyx_r;
  int __pyx_1;
  PyObject *__pyx_2 = 0;
  Py_INCREF(__pyx_v_dims);
  Py_INCREF(__pyx_v_typecode);
  __pyx_v_o = Py_None; Py_INCREF(__pyx_v_o);

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":79 */
  __pyx_1 = (__pyx_v_dims->nd != 1);
  if (__pyx_1) {

    /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":80 */
    __pyx_2 = __Pyx_GetName(__pyx_b, __pyx_n_ValueError); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 80; goto __pyx_L1;}
    __Pyx_Raise(__pyx_2, __pyx_k4p, 0);
    Py_DECREF(__pyx_2); __pyx_2 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 80; goto __pyx_L1;}
    goto __pyx_L2;
  }
  __pyx_L2:;

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":83 */
  __pyx_v_real_type = PyString_AsString(__pyx_v_typecode);

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":87 */
  __pyx_v_descr = PyArray_DescrFromType(((int )(__pyx_v_real_type[0])));

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":88 */
  __pyx_1 = (__pyx_v_descr == 0);
  if (__pyx_1) {

    /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":89 */
    __pyx_2 = __Pyx_GetName(__pyx_b, __pyx_n_ValueError); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 89; goto __pyx_L1;}
    __Pyx_Raise(__pyx_2, __pyx_k5p, 0);
    Py_DECREF(__pyx_2); __pyx_2 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 89; goto __pyx_L1;}
    goto __pyx_L3;
  }
  __pyx_L3:;

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":95 */
  __pyx_v_nd = (__pyx_v_dims->dimensions[0]);

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":96 */
  __pyx_v_d = ((int (*))__pyx_v_dims->data);

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":97 */
  __pyx_v_sd = __pyx_v_descr->elsize;

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":98 */
  for (__pyx_v_i = 0; __pyx_v_i < __pyx_v_nd; ++__pyx_v_i) {

    /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":99 */
    __pyx_1 = ((__pyx_v_d[__pyx_v_i]) < 0);
    if (__pyx_1) {

      /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":100 */
      __pyx_2 = __Pyx_GetName(__pyx_b, __pyx_n_ValueError); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 100; goto __pyx_L1;}
      __Pyx_Raise(__pyx_2, __pyx_k6p, 0);
      Py_DECREF(__pyx_2); __pyx_2 = 0;
      {__pyx_filename = __pyx_f[0]; __pyx_lineno = 100; goto __pyx_L1;}
      goto __pyx_L6;
    }
    __pyx_L6:;

    /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":104 */
    __pyx_1 = (__pyx_v_d[__pyx_v_i]);
    if (__pyx_1) {

      /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":105 */
      __pyx_v_sd = (__pyx_v_sd * (__pyx_v_d[__pyx_v_i]));
      goto __pyx_L7;
    }
    __pyx_L7:;
    __pyx_L4:;
  }
  __pyx_L5:;

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":108 */
  __pyx_v_sd = ((__pyx_v_sd + (sizeof(int ))) - (__pyx_v_sd % (sizeof(int ))));

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":112 */
  __pyx_v_data = ((char (*))malloc(__pyx_v_sd));

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":113 */
  __pyx_1 = (__pyx_v_data == 0);
  if (__pyx_1) {

    /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":114 */
    __pyx_2 = __Pyx_GetName(__pyx_b, __pyx_n_MemoryError); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 114; goto __pyx_L1;}
    __Pyx_Raise(__pyx_2, __pyx_k7p, 0);
    Py_DECREF(__pyx_2); __pyx_2 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 114; goto __pyx_L1;}
    goto __pyx_L8;
  }
  __pyx_L8:;

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":118 */
  __pyx_v_op = PyArray_FromDimsAndDataAndDescr(__pyx_v_nd,__pyx_v_d,__pyx_v_descr,__pyx_v_data);

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":121 */
  __pyx_v_op->flags = (__pyx_v_op->flags | OWN_DATA);

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":124 */
  __pyx_2 = (PyObject *)__pyx_v_op;
  Py_INCREF(__pyx_2);
  Py_DECREF(__pyx_v_o);
  __pyx_v_o = __pyx_2;
  __pyx_2 = 0;

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":126 */
  Py_XDECREF(__pyx_v_o);

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":127 */
  Py_INCREF(__pyx_v_o);
  __pyx_r = __pyx_v_o;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(__pyx_r);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_2);
  __Pyx_AddTraceback("array_ext.c_empty_array");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_o);
  Py_DECREF(__pyx_v_dims);
  Py_DECREF(__pyx_v_typecode);
  return __pyx_r;
}

static PyObject *__pyx_f_9array_ext_c_set_id_type_array(PyArrayObject *__pyx_v_id_array,PyArrayObject *__pyx_v_out_array) {
  int __pyx_v_cell_length;
  int __pyx_v_dim0;
  int (*__pyx_v_id_data);
  int (*__pyx_v_out_data);
  int __pyx_v_stride0;
  int __pyx_v_stride1;
  int __pyx_v_i;
  int __pyx_v_j;
  int __pyx_v_in_idx;
  int __pyx_v_out_idx;
  PyObject *__pyx_r;
  Py_INCREF(__pyx_v_id_array);
  Py_INCREF(__pyx_v_out_array);

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":145 */
  __pyx_v_cell_length = (__pyx_v_id_array->dimensions[1]);

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":146 */
  __pyx_v_dim0 = (__pyx_v_id_array->dimensions[0]);

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":147 */
  __pyx_v_id_data = ((int (*))__pyx_v_id_array->data);

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":148 */
  __pyx_v_out_data = ((int (*))__pyx_v_out_array->data);

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":149 */
  __pyx_v_stride0 = ((__pyx_v_id_array->strides[0]) / (sizeof(int )));

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":150 */
  __pyx_v_stride1 = ((__pyx_v_id_array->strides[1]) / (sizeof(int )));

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":153 */
  for (__pyx_v_i = 0; __pyx_v_i < __pyx_v_dim0; ++__pyx_v_i) {

    /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":154 */
    __pyx_v_in_idx = (__pyx_v_i * __pyx_v_stride0);

    /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":155 */
    __pyx_v_out_idx = ((__pyx_v_i * __pyx_v_cell_length) + __pyx_v_i);

    /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":156 */
    (__pyx_v_out_data[__pyx_v_out_idx]) = __pyx_v_cell_length;

    /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":157 */
    for (__pyx_v_j = 0; __pyx_v_j < __pyx_v_cell_length; ++__pyx_v_j) {

      /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":158 */
      (__pyx_v_out_data[((__pyx_v_out_idx + __pyx_v_j) + 1)]) = (__pyx_v_id_data[(__pyx_v_in_idx + (__pyx_v_j * __pyx_v_stride1))]);
      __pyx_L4:;
    }
    __pyx_L5:;
    __pyx_L2:;
  }
  __pyx_L3:;

  __pyx_r = Py_None; Py_INCREF(__pyx_r);
  goto __pyx_L0;
  __pyx_L1:;
  __Pyx_AddTraceback("array_ext.c_set_id_type_array");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_id_array);
  Py_DECREF(__pyx_v_out_array);
  return __pyx_r;
}

static PyObject *__pyx_n_asarray;
static PyObject *__pyx_n_astype;
static PyObject *__pyx_n_Int;

static PyObject *__pyx_f_9array_ext_empty_array(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_9array_ext_empty_array[] = "This function creates an unitialized Numeric array of numbers\n    very quickly.  zeros() is extremely slow at creating arrays.";
static PyObject *__pyx_f_9array_ext_empty_array(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_dims = 0;
  PyObject *__pyx_v_typecode = 0;
  PyObject *__pyx_r;
  PyObject *__pyx_1 = 0;
  PyObject *__pyx_2 = 0;
  PyObject *__pyx_3 = 0;
  static char *__pyx_argnames[] = {"dims","typecode",0};
  __pyx_v_typecode = __pyx_k3;
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "O|O", __pyx_argnames, &__pyx_v_dims, &__pyx_v_typecode)) return 0;
  Py_INCREF(__pyx_v_dims);
  Py_INCREF(__pyx_v_typecode);

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":168 */
  __pyx_1 = __Pyx_GetName(__pyx_m, __pyx_n_Numeric); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 168; goto __pyx_L1;}
  __pyx_2 = PyObject_GetAttr(__pyx_1, __pyx_n_asarray); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 168; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  __pyx_1 = PyTuple_New(1); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 168; goto __pyx_L1;}
  Py_INCREF(__pyx_v_dims);
  PyTuple_SET_ITEM(__pyx_1, 0, __pyx_v_dims);
  __pyx_3 = PyObject_CallObject(__pyx_2, __pyx_1); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 168; goto __pyx_L1;}
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  __pyx_2 = PyObject_GetAttr(__pyx_3, __pyx_n_astype); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 168; goto __pyx_L1;}
  Py_DECREF(__pyx_3); __pyx_3 = 0;
  __pyx_1 = __Pyx_GetName(__pyx_m, __pyx_n_Numeric); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 168; goto __pyx_L1;}
  __pyx_3 = PyObject_GetAttr(__pyx_1, __pyx_n_Int); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 168; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  __pyx_1 = PyTuple_New(1); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 168; goto __pyx_L1;}
  PyTuple_SET_ITEM(__pyx_1, 0, __pyx_3);
  __pyx_3 = 0;
  __pyx_3 = PyObject_CallObject(__pyx_2, __pyx_1); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 168; goto __pyx_L1;}
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  Py_DECREF(__pyx_v_dims);
  __pyx_v_dims = __pyx_3;
  __pyx_3 = 0;

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":169 */
  if (!__Pyx_TypeTest(__pyx_v_dims, __pyx_ptype_9array_ext_ArrayType)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 169; goto __pyx_L1;}
  __pyx_2 = __pyx_f_9array_ext_c_empty_array(((PyArrayObject *)__pyx_v_dims),__pyx_v_typecode); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 169; goto __pyx_L1;}
  __pyx_r = __pyx_2;
  __pyx_2 = 0;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(__pyx_r);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  Py_XDECREF(__pyx_2);
  Py_XDECREF(__pyx_3);
  __Pyx_AddTraceback("array_ext.empty_array");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_dims);
  Py_DECREF(__pyx_v_typecode);
  return __pyx_r;
}

static PyObject *__pyx_n_typecode;
static PyObject *__pyx_n_l;
static PyObject *__pyx_n_iscontiguous;
static PyObject *__pyx_n_shape;
static PyObject *__pyx_n_len;
static PyObject *__pyx_n_size;

static PyObject *__pyx_k9p;
static PyObject *__pyx_k11p;
static PyObject *__pyx_k12p;
static PyObject *__pyx_k13p;
static PyObject *__pyx_k14p;

static char (__pyx_k9[]) = "id_array must have a typecode of 'l'.";
static char (__pyx_k11[]) = "out_array must have a typecode of 'l'.";
static char (__pyx_k12[]) = "out_array must be contiguous.";
static char (__pyx_k13[]) = "id_array must be a two dimensional array.";
static char (__pyx_k14[]) = "out_array size is incorrect, expected: %s, given: %s";

static PyObject *__pyx_f_9array_ext_set_id_type_array(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_9array_ext_set_id_type_array[] = "Given a 2D Int array (`id_array`), and a contiguous 1D Numeric\n    array (`out_array`) having the correct size, this function sets\n    the data from `id_array` into `out_array` so that it can be used\n    in place of a `vtkIdTypeArray` in order to set the cells of a\n    `vtkCellArray`.\n\n    Note that if `shape = id_array.shape` then `size(out_array) ==\n    shape[0]*(shape[1] + 1)` should be true.  If not you\'ll get an\n    `AssertionError`.\n\n    `id_array` need not be contiguous but `out_array` must be.\n    ";
static PyObject *__pyx_f_9array_ext_set_id_type_array(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_id_array = 0;
  PyObject *__pyx_v_out_array = 0;
  PyObject *__pyx_v_shp;
  PyObject *__pyx_v_sz;
  PyObject *__pyx_v_e_sz;
  PyObject *__pyx_r;
  PyObject *__pyx_1 = 0;
  PyObject *__pyx_2 = 0;
  PyObject *__pyx_3 = 0;
  int __pyx_4;
  PyObject *__pyx_5 = 0;
  static char *__pyx_argnames[] = {"id_array","out_array",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "OO", __pyx_argnames, &__pyx_v_id_array, &__pyx_v_out_array)) return 0;
  Py_INCREF(__pyx_v_id_array);
  Py_INCREF(__pyx_v_out_array);
  __pyx_v_shp = Py_None; Py_INCREF(__pyx_v_shp);
  __pyx_v_sz = Py_None; Py_INCREF(__pyx_v_sz);
  __pyx_v_e_sz = Py_None; Py_INCREF(__pyx_v_e_sz);

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":185 */
  __pyx_1 = PyObject_GetAttr(__pyx_v_id_array, __pyx_n_typecode); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 185; goto __pyx_L1;}
  __pyx_2 = PyTuple_New(0); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 185; goto __pyx_L1;}
  __pyx_3 = PyObject_CallObject(__pyx_1, __pyx_2); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 185; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  if (PyObject_Cmp(__pyx_3, __pyx_n_l, &__pyx_4) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 185; goto __pyx_L1;}
  __pyx_4 = __pyx_4 == 0;
  Py_DECREF(__pyx_3); __pyx_3 = 0;
  if (!__pyx_4) {
    PyErr_SetObject(PyExc_AssertionError, __pyx_k9p);
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 185; goto __pyx_L1;}
  }

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":188 */
  __pyx_1 = PyObject_GetAttr(__pyx_v_out_array, __pyx_n_typecode); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 188; goto __pyx_L1;}
  __pyx_2 = PyTuple_New(0); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 188; goto __pyx_L1;}
  __pyx_3 = PyObject_CallObject(__pyx_1, __pyx_2); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 188; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  if (PyObject_Cmp(__pyx_3, __pyx_n_l, &__pyx_4) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 188; goto __pyx_L1;}
  __pyx_4 = __pyx_4 == 0;
  Py_DECREF(__pyx_3); __pyx_3 = 0;
  if (!__pyx_4) {
    PyErr_SetObject(PyExc_AssertionError, __pyx_k11p);
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 188; goto __pyx_L1;}
  }

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":191 */
  __pyx_1 = PyObject_GetAttr(__pyx_v_out_array, __pyx_n_iscontiguous); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 191; goto __pyx_L1;}
  __pyx_2 = PyTuple_New(0); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 191; goto __pyx_L1;}
  __pyx_3 = PyObject_CallObject(__pyx_1, __pyx_2); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 191; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  __pyx_1 = PyInt_FromLong(1); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 191; goto __pyx_L1;}
  if (PyObject_Cmp(__pyx_3, __pyx_1, &__pyx_4) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 191; goto __pyx_L1;}
  __pyx_4 = __pyx_4 == 0;
  Py_DECREF(__pyx_3); __pyx_3 = 0;
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  if (!__pyx_4) {
    PyErr_SetObject(PyExc_AssertionError, __pyx_k12p);
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 191; goto __pyx_L1;}
  }

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":194 */
  __pyx_2 = PyObject_GetAttr(__pyx_v_id_array, __pyx_n_shape); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 194; goto __pyx_L1;}
  Py_DECREF(__pyx_v_shp);
  __pyx_v_shp = __pyx_2;
  __pyx_2 = 0;

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":195 */
  __pyx_3 = __Pyx_GetName(__pyx_b, __pyx_n_len); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 195; goto __pyx_L1;}
  __pyx_1 = PyTuple_New(1); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 195; goto __pyx_L1;}
  Py_INCREF(__pyx_v_shp);
  PyTuple_SET_ITEM(__pyx_1, 0, __pyx_v_shp);
  __pyx_2 = PyObject_CallObject(__pyx_3, __pyx_1); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 195; goto __pyx_L1;}
  Py_DECREF(__pyx_3); __pyx_3 = 0;
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  __pyx_3 = PyInt_FromLong(2); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 195; goto __pyx_L1;}
  if (PyObject_Cmp(__pyx_2, __pyx_3, &__pyx_4) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 195; goto __pyx_L1;}
  __pyx_4 = __pyx_4 == 0;
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  Py_DECREF(__pyx_3); __pyx_3 = 0;
  if (!__pyx_4) {
    PyErr_SetObject(PyExc_AssertionError, __pyx_k13p);
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 195; goto __pyx_L1;}
  }

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":197 */
  __pyx_1 = __Pyx_GetName(__pyx_m, __pyx_n_Numeric); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 197; goto __pyx_L1;}
  __pyx_2 = PyObject_GetAttr(__pyx_1, __pyx_n_size); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 197; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  __pyx_3 = PyTuple_New(1); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 197; goto __pyx_L1;}
  Py_INCREF(__pyx_v_out_array);
  PyTuple_SET_ITEM(__pyx_3, 0, __pyx_v_out_array);
  __pyx_1 = PyObject_CallObject(__pyx_2, __pyx_3); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 197; goto __pyx_L1;}
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  Py_DECREF(__pyx_3); __pyx_3 = 0;
  Py_DECREF(__pyx_v_sz);
  __pyx_v_sz = __pyx_1;
  __pyx_1 = 0;

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":198 */
  __pyx_2 = PyInt_FromLong(0); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 198; goto __pyx_L1;}
  __pyx_3 = PyObject_GetItem(__pyx_v_shp, __pyx_2); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 198; goto __pyx_L1;}
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  __pyx_1 = PyInt_FromLong(1); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 198; goto __pyx_L1;}
  __pyx_2 = PyObject_GetItem(__pyx_v_shp, __pyx_1); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 198; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  __pyx_1 = PyInt_FromLong(1); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 198; goto __pyx_L1;}
  __pyx_5 = PyNumber_Add(__pyx_2, __pyx_1); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 198; goto __pyx_L1;}
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  __pyx_2 = PyNumber_Multiply(__pyx_3, __pyx_5); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 198; goto __pyx_L1;}
  Py_DECREF(__pyx_3); __pyx_3 = 0;
  Py_DECREF(__pyx_5); __pyx_5 = 0;
  Py_DECREF(__pyx_v_e_sz);
  __pyx_v_e_sz = __pyx_2;
  __pyx_2 = 0;

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":199 */
  if (PyObject_Cmp(__pyx_v_sz, __pyx_v_e_sz, &__pyx_4) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 199; goto __pyx_L1;}
  __pyx_4 = __pyx_4 == 0;
  __pyx_1 = PyTuple_New(2); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 200; goto __pyx_L1;}
  Py_INCREF(__pyx_v_e_sz);
  PyTuple_SET_ITEM(__pyx_1, 0, __pyx_v_e_sz);
  Py_INCREF(__pyx_v_sz);
  PyTuple_SET_ITEM(__pyx_1, 1, __pyx_v_sz);
  __pyx_3 = PyNumber_Remainder(__pyx_k14p, __pyx_1); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 200; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  if (!__pyx_4) {
    PyErr_SetObject(PyExc_AssertionError, __pyx_3);
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 199; goto __pyx_L1;}
  }
  Py_DECREF(__pyx_3); __pyx_3 = 0;

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":202 */
  if (!__Pyx_TypeTest(__pyx_v_id_array, __pyx_ptype_9array_ext_ArrayType)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 202; goto __pyx_L1;}
  if (!__Pyx_TypeTest(__pyx_v_out_array, __pyx_ptype_9array_ext_ArrayType)) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 202; goto __pyx_L1;}
  __pyx_5 = __pyx_f_9array_ext_c_set_id_type_array(((PyArrayObject *)__pyx_v_id_array),((PyArrayObject *)__pyx_v_out_array)); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 202; goto __pyx_L1;}
  Py_DECREF(__pyx_5); __pyx_5 = 0;

  __pyx_r = Py_None; Py_INCREF(__pyx_r);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  Py_XDECREF(__pyx_2);
  Py_XDECREF(__pyx_3);
  Py_XDECREF(__pyx_5);
  __Pyx_AddTraceback("array_ext.set_id_type_array");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_shp);
  Py_DECREF(__pyx_v_sz);
  Py_DECREF(__pyx_v_e_sz);
  Py_DECREF(__pyx_v_id_array);
  Py_DECREF(__pyx_v_out_array);
  return __pyx_r;
}

static __Pyx_InternTabEntry __pyx_intern_tab[] = {
  {&__pyx_n_Int, "Int"},
  {&__pyx_n_MemoryError, "MemoryError"},
  {&__pyx_n_Numeric, "Numeric"},
  {&__pyx_n_ValueError, "ValueError"},
  {&__pyx_n_asarray, "asarray"},
  {&__pyx_n_astype, "astype"},
  {&__pyx_n_d, "d"},
  {&__pyx_n_empty_array, "empty_array"},
  {&__pyx_n_iscontiguous, "iscontiguous"},
  {&__pyx_n_l, "l"},
  {&__pyx_n_len, "len"},
  {&__pyx_n_set_id_type_array, "set_id_type_array"},
  {&__pyx_n_shape, "shape"},
  {&__pyx_n_size, "size"},
  {&__pyx_n_typecode, "typecode"},
  {0, 0}
};

static __Pyx_StringTabEntry __pyx_string_tab[] = {
  {&__pyx_k4p, __pyx_k4, sizeof(__pyx_k4)},
  {&__pyx_k5p, __pyx_k5, sizeof(__pyx_k5)},
  {&__pyx_k6p, __pyx_k6, sizeof(__pyx_k6)},
  {&__pyx_k7p, __pyx_k7, sizeof(__pyx_k7)},
  {&__pyx_k9p, __pyx_k9, sizeof(__pyx_k9)},
  {&__pyx_k11p, __pyx_k11, sizeof(__pyx_k11)},
  {&__pyx_k12p, __pyx_k12, sizeof(__pyx_k12)},
  {&__pyx_k13p, __pyx_k13, sizeof(__pyx_k13)},
  {&__pyx_k14p, __pyx_k14, sizeof(__pyx_k14)},
  {0, 0, 0}
};

static struct PyMethodDef __pyx_methods[] = {
  {"empty_array", (PyCFunction)__pyx_f_9array_ext_empty_array, METH_VARARGS|METH_KEYWORDS, __pyx_doc_9array_ext_empty_array},
  {"set_id_type_array", (PyCFunction)__pyx_f_9array_ext_set_id_type_array, METH_VARARGS|METH_KEYWORDS, __pyx_doc_9array_ext_set_id_type_array},
  {0, 0, 0, 0}
};

PyMODINIT_FUNC initarray_ext(void); /*proto*/
PyMODINIT_FUNC initarray_ext(void) {
  PyObject *__pyx_1 = 0;
  __pyx_m = Py_InitModule4("array_ext", __pyx_methods, __pyx_mdoc, 0, PYTHON_API_VERSION);
  if (!__pyx_m) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  __pyx_b = PyImport_AddModule("__builtin__");
  if (!__pyx_b) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  if (PyObject_SetAttrString(__pyx_m, "__builtins__", __pyx_b) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  if (__Pyx_InternStrings(__pyx_intern_tab) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  if (__Pyx_InitStrings(__pyx_string_tab) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  __pyx_ptype_9array_ext_ArrayType = __Pyx_ImportType("Numeric", "ArrayType", sizeof(PyArrayObject)); if (!__pyx_ptype_9array_ext_ArrayType) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 47; goto __pyx_L1;}

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":20 */
  __pyx_1 = __Pyx_Import(__pyx_n_Numeric, 0); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_Numeric, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 20; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":68 */
  import_array();

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":165 */
  Py_INCREF(__pyx_n_d);
  __pyx_k3 = __pyx_n_d;

  /* "/skratch/prabhu/svn/enthought/tvtk/src/array_ext.pyx":172 */
  return;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  __Pyx_AddTraceback("array_ext");
}

static char *__pyx_filenames[] = {
  "array_ext.pyx",
};
statichere char **__pyx_f = __pyx_filenames;

/* Runtime support code */

static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list) {
    PyObject *__import__ = 0;
    PyObject *empty_list = 0;
    PyObject *module = 0;
    PyObject *global_dict = 0;
    PyObject *empty_dict = 0;
    PyObject *list;
    __import__ = PyObject_GetAttrString(__pyx_b, "__import__");
    if (!__import__)
        goto bad;
    if (from_list)
        list = from_list;
    else {
        empty_list = PyList_New(0);
        if (!empty_list)
            goto bad;
        list = empty_list;
    }
    global_dict = PyModule_GetDict(__pyx_m);
    if (!global_dict)
        goto bad;
    empty_dict = PyDict_New();
    if (!empty_dict)
        goto bad;
    module = PyObject_CallFunction(__import__, "OOOO",
        name, global_dict, empty_dict, list);
bad:
    Py_XDECREF(empty_list);
    Py_XDECREF(__import__);
    Py_XDECREF(empty_dict);
    return module;
}

static PyObject *__Pyx_GetName(PyObject *dict, PyObject *name) {
    PyObject *result;
    result = PyObject_GetAttr(dict, name);
    if (!result)
        PyErr_SetObject(PyExc_NameError, name);
    return result;
}

static void __Pyx_Raise(PyObject *type, PyObject *value, PyObject *tb) {
    Py_XINCREF(type);
    Py_XINCREF(value);
    Py_XINCREF(tb);
    /* First, check the traceback argument, replacing None with NULL. */
    if (tb == Py_None) {
        Py_DECREF(tb);
        tb = 0;
    }
    else if (tb != NULL && !PyTraceBack_Check(tb)) {
        PyErr_SetString(PyExc_TypeError,
            "raise: arg 3 must be a traceback or None");
        goto raise_error;
    }
    /* Next, replace a missing value with None */
    if (value == NULL) {
        value = Py_None;
        Py_INCREF(value);
    }
    /* Next, repeatedly, replace a tuple exception with its first item */
    while (PyTuple_Check(type) && PyTuple_Size(type) > 0) {
        PyObject *tmp = type;
        type = PyTuple_GET_ITEM(type, 0);
        Py_INCREF(type);
        Py_DECREF(tmp);
    }
    if (PyString_Check(type))
        ;
    else if (PyClass_Check(type))
        ; /*PyErr_NormalizeException(&type, &value, &tb);*/
    else if (PyInstance_Check(type)) {
        /* Raising an instance.  The value should be a dummy. */
        if (value != Py_None) {
            PyErr_SetString(PyExc_TypeError,
              "instance exception may not have a separate value");
            goto raise_error;
        }
        else {
            /* Normalize to raise <class>, <instance> */
            Py_DECREF(value);
            value = type;
            type = (PyObject*) ((PyInstanceObject*)type)->in_class;
            Py_INCREF(type);
        }
    }
    else {
        /* Not something you can raise.  You get an exception
           anyway, just not what you specified :-) */
        PyErr_Format(PyExc_TypeError,
                 "exceptions must be strings, classes, or "
                 "instances, not %s", type->ob_type->tp_name);
        goto raise_error;
    }
    PyErr_Restore(type, value, tb);
    return;
raise_error:
    Py_XDECREF(value);
    Py_XDECREF(type);
    Py_XDECREF(tb);
    return;
}

static int __Pyx_TypeTest(PyObject *obj, PyTypeObject *type) {
    if (!type) {
        PyErr_Format(PyExc_SystemError, "Missing type object");
        return 0;
    }
    if (obj == Py_None || PyObject_TypeCheck(obj, type))
        return 1;
    PyErr_Format(PyExc_TypeError, "Cannot convert %s to %s",
        obj->ob_type->tp_name, type->tp_name);
    return 0;
}

static int __Pyx_InternStrings(__Pyx_InternTabEntry *t) {
    while (t->p) {
        *t->p = PyString_InternFromString(t->s);
        if (!*t->p)
            return -1;
        ++t;
    }
    return 0;
}

static int __Pyx_InitStrings(__Pyx_StringTabEntry *t) {
    while (t->p) {
        *t->p = PyString_FromStringAndSize(t->s, t->n - 1);
        if (!*t->p)
            return -1;
        ++t;
    }
    return 0;
}

static PyTypeObject *__Pyx_ImportType(char *module_name, char *class_name, 
    long size) 
{
    PyObject *py_module_name = 0;
    PyObject *py_class_name = 0;
    PyObject *py_name_list = 0;
    PyObject *py_module = 0;
    PyObject *result = 0;
    
    py_module_name = PyString_FromString(module_name);
    if (!py_module_name)
        goto bad;
    py_class_name = PyString_FromString(class_name);
    if (!py_class_name)
        goto bad;
    py_name_list = PyList_New(1);
    if (!py_name_list)
        goto bad;
    Py_INCREF(py_class_name);
    if (PyList_SetItem(py_name_list, 0, py_class_name) < 0)
        goto bad;
    py_module = __Pyx_Import(py_module_name, py_name_list);
    if (!py_module)
        goto bad;
    result = PyObject_GetAttr(py_module, py_class_name);
    if (!result)
        goto bad;
    if (!PyType_Check(result)) {
        PyErr_Format(PyExc_TypeError, 
            "%s.%s is not a type object",
            module_name, class_name);
        goto bad;
    }
    if (((PyTypeObject *)result)->tp_basicsize != size) {
        PyErr_Format(PyExc_ValueError, 
            "%s.%s does not appear to be the correct type object",
            module_name, class_name);
        goto bad;
    }
    goto done;
bad:
    Py_XDECREF(result);
    result = 0;
done:
    Py_XDECREF(py_module_name);
    Py_XDECREF(py_class_name);
    Py_XDECREF(py_name_list);
    return (PyTypeObject *)result;
}

#include "compile.h"
#include "frameobject.h"
#include "traceback.h"

static void __Pyx_AddTraceback(char *funcname) {
    PyObject *py_srcfile = 0;
    PyObject *py_funcname = 0;
    PyObject *py_globals = 0;
    PyObject *empty_tuple = 0;
    PyObject *empty_string = 0;
    PyCodeObject *py_code = 0;
    PyFrameObject *py_frame = 0;
    
    py_srcfile = PyString_FromString(__pyx_filename);
    if (!py_srcfile) goto bad;
    py_funcname = PyString_FromString(funcname);
    if (!py_funcname) goto bad;
    py_globals = PyModule_GetDict(__pyx_m);
    if (!py_globals) goto bad;
    empty_tuple = PyTuple_New(0);
    if (!empty_tuple) goto bad;
    empty_string = PyString_FromString("");
    if (!empty_string) goto bad;
    py_code = PyCode_New(
        0,            /*int argcount,*/
        0,            /*int nlocals,*/
        0,            /*int stacksize,*/
        0,            /*int flags,*/
        empty_string, /*PyObject *code,*/
        empty_tuple,  /*PyObject *consts,*/
        empty_tuple,  /*PyObject *names,*/
        empty_tuple,  /*PyObject *varnames,*/
        empty_tuple,  /*PyObject *freevars,*/
        empty_tuple,  /*PyObject *cellvars,*/
        py_srcfile,   /*PyObject *filename,*/
        py_funcname,  /*PyObject *name,*/
        __pyx_lineno,   /*int firstlineno,*/
        empty_string  /*PyObject *lnotab*/
    );
    if (!py_code) goto bad;
    py_frame = PyFrame_New(
        PyThreadState_Get(), /*PyThreadState *tstate,*/
        py_code,             /*PyCodeObject *code,*/
        py_globals,          /*PyObject *globals,*/
        0                    /*PyObject *locals*/
    );
    if (!py_frame) goto bad;
    py_frame->f_lineno = __pyx_lineno;
    PyTraceBack_Here(py_frame);
bad:
    Py_XDECREF(py_srcfile);
    Py_XDECREF(py_funcname);
    Py_XDECREF(empty_tuple);
    Py_XDECREF(empty_string);
    Py_XDECREF(py_code);
    Py_XDECREF(py_frame);
}
