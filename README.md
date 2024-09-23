Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/arrayobject.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY_ARRAYOBJECT_H_
#define NUMPY_CORE_INCLUDE_NUMPY_ARRAYOBJECT_H_
#define Py_ARRAYOBJECT_H

#include "ndarrayobject.h"
#include "npy_interrupt.h"

#ifdef NPY_NO_PREFIX
#include "noprefix.h"
#endif

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_ARRAYOBJECT_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/arrayscalars.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY_ARRAYSCALARS_H_
#define NUMPY_CORE_INCLUDE_NUMPY_ARRAYSCALARS_H_

#ifndef _MULTIARRAYMODULE
typedef struct {
        PyObject_HEAD
        npy_bool obval;
} PyBoolScalarObject;
#endif


typedef struct {
        PyObject_HEAD
        signed char obval;
} PyByteScalarObject;


typedef struct {
        PyObject_HEAD
        short obval;
} PyShortScalarObject;


typedef struct {
        PyObject_HEAD
        int obval;
} PyIntScalarObject;


typedef struct {
        PyObject_HEAD
        long obval;
} PyLongScalarObject;


typedef struct {
        PyObject_HEAD
        npy_longlong obval;
} PyLongLongScalarObject;


typedef struct {
        PyObject_HEAD
        unsigned char obval;
} PyUByteScalarObject;


typedef struct {
        PyObject_HEAD
        unsigned short obval;
} PyUShortScalarObject;


typedef struct {
        PyObject_HEAD
        unsigned int obval;
} PyUIntScalarObject;


typedef struct {
        PyObject_HEAD
        unsigned long obval;
} PyULongScalarObject;


typedef struct {
        PyObject_HEAD
        npy_ulonglong obval;
} PyULongLongScalarObject;


typedef struct {
        PyObject_HEAD
        npy_half obval;
} PyHalfScalarObject;


typedef struct {
        PyObject_HEAD
        float obval;
} PyFloatScalarObject;


typedef struct {
        PyObject_HEAD
        double obval;
} PyDoubleScalarObject;


typedef struct {
        PyObject_HEAD
        npy_longdouble obval;
} PyLongDoubleScalarObject;


typedef struct {
        PyObject_HEAD
        npy_cfloat obval;
} PyCFloatScalarObject;


typedef struct {
        PyObject_HEAD
        npy_cdouble obval;
} PyCDoubleScalarObject;


typedef struct {
        PyObject_HEAD
        npy_clongdouble obval;
} PyCLongDoubleScalarObject;


typedef struct {
        PyObject_HEAD
        PyObject * obval;
} PyObjectScalarObject;

typedef struct {
        PyObject_HEAD
        npy_datetime obval;
        PyArray_DatetimeMetaData obmeta;
} PyDatetimeScalarObject;

typedef struct {
        PyObject_HEAD
        npy_timedelta obval;
        PyArray_DatetimeMetaData obmeta;
} PyTimedeltaScalarObject;


typedef struct {
        PyObject_HEAD
        char obval;
} PyScalarObject;

#define PyStringScalarObject PyBytesObject
typedef struct {
        /* note that the PyObject_HEAD macro lives right here */
        PyUnicodeObject base;
        Py_UCS4 *obval;
        char *buffer_fmt;
} PyUnicodeScalarObject;


typedef struct {
        PyObject_VAR_HEAD
        char *obval;
        PyArray_Descr *descr;
        int flags;
        PyObject *base;
        void *_buffer_info;  /* private buffer info, tagged to allow warning */
} PyVoidScalarObject;

/* Macros
     Py<Cls><bitsize>ScalarObject
     Py<Cls><bitsize>ArrType_Type
   are defined in ndarrayobject.h
*/

#define PyArrayScalar_False ((PyObject *)(&(_PyArrayScalar_BoolValues[0])))
#define PyArrayScalar_True ((PyObject *)(&(_PyArrayScalar_BoolValues[1])))
#define PyArrayScalar_FromLong(i) \
        ((PyObject *)(&(_PyArrayScalar_BoolValues[((i)!=0)])))
#define PyArrayScalar_RETURN_BOOL_FROM_LONG(i)                  \
        return Py_INCREF(PyArrayScalar_FromLong(i)), \
                PyArrayScalar_FromLong(i)
#define PyArrayScalar_RETURN_FALSE              \
        return Py_INCREF(PyArrayScalar_False),  \
                PyArrayScalar_False
#define PyArrayScalar_RETURN_TRUE               \
        return Py_INCREF(PyArrayScalar_True),   \
                PyArrayScalar_True

#define PyArrayScalar_New(cls) \
        Py##cls##ArrType_Type.tp_alloc(&Py##cls##ArrType_Type, 0)
#define PyArrayScalar_VAL(obj, cls)             \
        ((Py##cls##ScalarObject *)obj)->obval
#define PyArrayScalar_ASSIGN(obj, cls, val) \
        PyArrayScalar_VAL(obj, cls) = val

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_ARRAYSCALARS_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/experimental_dtype_api.h

```plaintext
/*
 * This header exports the new experimental DType API as proposed in
 * NEPs 41 to 43.  For background, please check these NEPs.  Otherwise,
 * this header also serves as documentation for the time being.
 *
 * Please do not hesitate to contact @seberg with questions.  This is
 * developed together with https://github.com/seberg/experimental_user_dtypes
 * and those interested in experimenting are encouraged to contribute there.
 *
 * To use the functions defined in the header, call::
 *
 *     if (import_experimental_dtype_api(version) < 0) {
 *         return NULL;
 *     }
 *
 * in your module init.  (A version mismatch will be reported, just update
 * to the correct one, this will alert you of possible changes.)
 *
 * The following lists the main symbols currently exported.  Please do not
 * hesitate to ask for help or clarification:
 *
 * - PyUFunc_AddLoopFromSpec:
 *
 *     Register a new loop for a ufunc.  This uses the `PyArrayMethod_Spec`
 *     which must be filled in (see in-line comments).
 *
 * - PyUFunc_AddWrappingLoop:
 *
 *     Register a new loop which reuses an existing one, but modifies the
 *     result dtypes.  Please search the internal NumPy docs for more info
 *     at this point.  (Used for physical units dtype.)
 *
 * - PyUFunc_AddPromoter:
 *
 *     Register a new promoter for a ufunc.  A promoter is a function stored
 *     in a PyCapsule (see in-line comments).  It is passed the operation and
 *     requested DType signatures and can mutate it to attempt a new search
 *     for a matching loop/promoter.
 *     I.e. for Numba a promoter could even add the desired loop.
 *
 * - PyArrayInitDTypeMeta_FromSpec:
 *
 *     Initialize a new DType.  It must currently be a static Python C type
 *     that is declared as `PyArray_DTypeMeta` and not `PyTypeObject`.
 *     Further, it must subclass `np.dtype` and set its type to
 *     `PyArrayDTypeMeta_Type` (before calling `PyType_Read()`).
 *
 * - PyArray_CommonDType:
 *
 *     Find the common-dtype ("promotion") for two DType classes.  Similar
 *     to `np.result_type`, but works on the classes and not instances.
 *
 * - PyArray_PromoteDTypeSequence:
 *
 *     Same as CommonDType, but works with an arbitrary number of DTypes.
 *     This function is smarter and can often return successful and unambiguous
 *     results when `common_dtype(common_dtype(dt1, dt2), dt3)` would
 *     depend on the operation order or fail.  Nevertheless, DTypes should
 *     aim to ensure that their common-dtype implementation is associative
 *     and commutative!  (Mainly, unsigned and signed integers are not.)
 *
 *     For guaranteed consistent results DTypes must implement common-Dtype
 *     "transitively".  If A promotes B and B promotes C, than A must generally
 *     also promote C; where "promotes" means implements the promotion.
 *     (There are some exceptions for abstract DTypes)
 *
 * - PyArray_GetDefaultDescr:
 *
 *     Given a DType class, returns the default instance (descriptor).
 *     This is an inline function checking for `singleton` first and only
 *     calls the `default_descr` function if necessary.
 *
 * - PyArray_DoubleDType, etc.:
 *
 *     Aliases to the DType classes for the builtin NumPy DTypes.
 *
 * WARNING
 * =======
 *
 * By using this header, you understand that this is a fully experimental
 * exposure.  Details are expected to change, and some options may have no
 * effect.  (Please contact @seberg if you have questions!)
 * If the exposure stops working, please file a bug report with NumPy.
 * Further, a DType created using this API/header should still be expected
 * to be incompatible with some functionality inside and outside of NumPy.
 * In this case crashes must be expected.  Please report any such problems
 * so that they can be fixed before final exposure.
 * Furthermore, expect missing checks for programming errors which the final
 * API is expected to have.
 *
 * Symbols with a leading underscore are likely to not be included in the
 * first public version, if these are central to your use-case, please let
 * us know, so that we can reconsider.
 *
 * "Array-like" consumer API not yet under considerations
 * ======================================================
 *
 * The new DType API is designed in a way to make it potentially useful for
 * alternative "array-like" implementations.  This will require careful
 * exposure of details and functions and is not part of this experimental API.
 *
 * Brief (incompatibility) changelog
 * =================================
 *
 * 2. None (only additions).
 * 3. New `npy_intp *view_offset` argument for `resolve_descriptors`.
 *    This replaces the `NPY_CAST_IS_VIEW` flag.  It can be set to 0 if the
 *    operation is a view, and is pre-initialized to `NPY_MIN_INTP` indicating
 *    that the operation is not a view.
 */

#ifndef NUMPY_CORE_INCLUDE_NUMPY_EXPERIMENTAL_DTYPE_API_H_
#define NUMPY_CORE_INCLUDE_NUMPY_EXPERIMENTAL_DTYPE_API_H_

#include <Python.h>
#include "ndarraytypes.h"


/*
 * There must be a better way?! -- Oh well, this is experimental
 * (my issue with it, is that I cannot undef those helpers).
 */
#if defined(PY_ARRAY_UNIQUE_SYMBOL)
    #define NPY_EXP_DTYPE_API_CONCAT_HELPER2(x, y) x ## y
    #define NPY_EXP_DTYPE_API_CONCAT_HELPER(arg) NPY_EXP_DTYPE_API_CONCAT_HELPER2(arg, __experimental_dtype_api_table)
    #define __experimental_dtype_api_table NPY_EXP_DTYPE_API_CONCAT_HELPER(PY_ARRAY_UNIQUE_SYMBOL)
#else
    #define __experimental_dtype_api_table __experimental_dtype_api_table
#endif

/* Support for correct multi-file projects: */
#if defined(NO_IMPORT) || defined(NO_IMPORT_ARRAY)
    extern void **__experimental_dtype_api_table;
#else
    /*
     * Just a hack so I don't forget importing as much myself, I spend way too
     * much time noticing it the first time around :).
     */
    static void
    __not_imported(void)
    {
        printf("*****\nCritical error, dtype API not imported\n*****\n");
    }

    static void *__uninitialized_table[] = {
            &__not_imported, &__not_imported, &__not_imported, &__not_imported,
            &__not_imported, &__not_imported, &__not_imported, &__not_imported};

    #if defined(PY_ARRAY_UNIQUE_SYMBOL)
        void **__experimental_dtype_api_table = __uninitialized_table;
    #else
        static void **__experimental_dtype_api_table = __uninitialized_table;
    #endif
#endif


/*
 * DTypeMeta struct, the content may be made fully opaque (except the size).
 * We may also move everything into a single `void *dt_slots`.
 */
typedef struct {
    PyHeapTypeObject super;
    PyArray_Descr *singleton;
    int type_num;
    PyTypeObject *scalar_type;
    npy_uint64 flags;
    void *dt_slots;
    void *reserved[3];
} PyArray_DTypeMeta;


/*
 * ******************************************************
 *         ArrayMethod API (Casting and UFuncs)
 * ******************************************************
 */
/*
 * NOTE: Expected changes:
 *       * invert logic of floating point error flag
 *       * probably split runtime and general flags into two
 *       * should possibly not use an enum for typedef for more stable ABI?
 */
typedef enum {
    /* Flag for whether the GIL is required */
    NPY_METH_REQUIRES_PYAPI = 1 << 1,
    /*
     * Some functions cannot set floating point error flags, this flag
     * gives us the option (not requirement) to skip floating point error
     * setup/check. No function should set error flags and ignore them
     * since it would interfere with chaining operations (e.g. casting).
     */
    NPY_METH_NO_FLOATINGPOINT_ERRORS = 1 << 2,
    /* Whether the method supports unaligned access (not runtime) */
    NPY_METH_SUPPORTS_UNALIGNED = 1 << 3,

    /* All flags which can change at runtime */
    NPY_METH_RUNTIME_FLAGS = (
            NPY_METH_REQUIRES_PYAPI |
            NPY_METH_NO_FLOATINGPOINT_ERRORS),
} NPY_ARRAYMETHOD_FLAGS;


/*
 * The main object for creating a new ArrayMethod. We use the typical `slots`
 * mechanism used by the Python limited API (see below for the slot defs).
 */
typedef struct {
    const char *name;
    int nin, nout;
    NPY_CASTING casting;
    NPY_ARRAYMETHOD_FLAGS flags;
    PyArray_DTypeMeta **dtypes;
    PyType_Slot *slots;
} PyArrayMethod_Spec;


typedef int _ufunc_addloop_fromspec_func(
        PyObject *ufunc, PyArrayMethod_Spec *spec);
/*
 * The main ufunc registration function.  This adds a new implementation/loop
 * to a ufunc.  It replaces `PyUFunc_RegisterLoopForType`.
 */
#define PyUFunc_AddLoopFromSpec \
    (*(_ufunc_addloop_fromspec_func *)(__experimental_dtype_api_table[0]))


/* Please see the NumPy definitions in `array_method.h` for details on these */
typedef int translate_given_descrs_func(int nin, int nout,
        PyArray_DTypeMeta *wrapped_dtypes[],
        PyArray_Descr *given_descrs[], PyArray_Descr *new_descrs[]);
typedef int translate_loop_descrs_func(int nin, int nout,
        PyArray_DTypeMeta *new_dtypes[], PyArray_Descr *given_descrs[],
        PyArray_Descr *original_descrs[], PyArray_Descr *loop_descrs[]);

typedef int _ufunc_wrapping_loop_func(PyObject *ufunc_obj,
        PyArray_DTypeMeta *new_dtypes[], PyArray_DTypeMeta *wrapped_dtypes[],
        translate_given_descrs_func *translate_given_descrs,
        translate_loop_descrs_func *translate_loop_descrs);
#define PyUFunc_AddWrappingLoop \
    (*(_ufunc_wrapping_loop_func *)(__experimental_dtype_api_table[7]))

/*
 * Type of the C promoter function, which must be wrapped into a
 * PyCapsule with name "numpy._ufunc_promoter".
 *
 * Note that currently the output dtypes are always NULL unless they are
 * also part of the signature.  This is an implementation detail and could
 * change in the future.  However, in general promoters should not have a
 * need for output dtypes.
 * (There are potential use-cases, these are currently unsupported.)
 */
typedef int promoter_function(PyObject *ufunc,
        PyArray_DTypeMeta *op_dtypes[], PyArray_DTypeMeta *signature[],
        PyArray_DTypeMeta *new_op_dtypes[]);

/*
 * Function to register a promoter.
 *
 * @param ufunc The ufunc object to register the promoter with.
 * @param DType_tuple A Python tuple containing DTypes or None matching the
 *        number of inputs and outputs of the ufunc.
 * @param promoter A PyCapsule with name "numpy._ufunc_promoter" containing
 *        a pointer to a `promoter_function`.
 */
typedef int _ufunc_addpromoter_func(
        PyObject *ufunc, PyObject *DType_tuple, PyObject *promoter);
#define PyUFunc_AddPromoter \
    (*(_ufunc_addpromoter_func *)(__experimental_dtype_api_table[1]))


/*
 * The resolve descriptors function, must be able to handle NULL values for
 * all output (but not input) `given_descrs` and fill `loop_descrs`.
 * Return -1 on error or 0 if the operation is not possible without an error
 * set.  (This may still be in flux.)
 * Otherwise must return the "casting safety", for normal functions, this is
 * almost always "safe" (or even "equivalent"?).
 *
 * `resolve_descriptors` is optional if all output DTypes are non-parametric.
 */
#define NPY_METH_resolve_descriptors 1
typedef NPY_CASTING (resolve_descriptors_function)(
        /* "method" is currently opaque (necessary e.g. to wrap Python) */
        PyObject *method,
        /* DTypes the method was created for */
        PyObject **dtypes,
        /* Input descriptors (instances).  Outputs may be NULL. */
        PyArray_Descr **given_descrs,
        /* Exact loop descriptors to use, must not hold references on error */
        PyArray_Descr **loop_descrs,
        npy_intp *view_offset);

/* NOT public yet: Signature needs adapting as external API. */
#define _NPY_METH_get_loop 2

/*
 * Current public API to define fast inner-loops.  You must provide a
 * strided loop.  If this is a cast between two "versions" of the same dtype
 * you must also provide an unaligned strided loop.
 * Other loops are useful to optimize the very common contiguous case.
 *
 * NOTE: As of now, NumPy will NOT use unaligned loops in ufuncs!
 */
#define NPY_METH_strided_loop 3
#define NPY_METH_contiguous_loop 4
#define NPY_METH_unaligned_strided_loop 5
#define NPY_METH_unaligned_contiguous_loop 6


typedef struct {
    PyObject *caller;  /* E.g. the original ufunc, may be NULL */
    PyObject *method;  /* The method "self". Currently an opaque object */

    /* Operand descriptors, filled in by resolve_descriptors */
    PyArray_Descr **descriptors;
    /* Structure may grow (this is harmless for DType authors) */
} PyArrayMethod_Context;

typedef int (PyArrayMethod_StridedLoop)(PyArrayMethod_Context *context,
        char *const *data, const npy_intp *dimensions, const npy_intp *strides,
        NpyAuxData *transferdata);



/*
 * ****************************
 *          DTYPE API
 * ****************************
 */

#define NPY_DT_ABSTRACT 1 << 1
#define NPY_DT_PARAMETRIC 1 << 2

#define NPY_DT_discover_descr_from_pyobject 1
#define _NPY_DT_is_known_scalar_type 2
#define NPY_DT_default_descr 3
#define NPY_DT_common_dtype 4
#define NPY_DT_common_instance 5
#define NPY_DT_ensure_canonical 6
#define NPY_DT_setitem 7
#define NPY_DT_getitem 8


// TODO: These slots probably still need some thought, and/or a way to "grow"?
typedef struct{
    PyTypeObject *typeobj;    /* type of python scalar or NULL */
    int flags;                /* flags, including parametric and abstract */
    /* NULL terminated cast definitions. Use NULL for the newly created DType */
    PyArrayMethod_Spec **casts;
    PyType_Slot *slots;
    /* Baseclass or NULL (will always subclass `np.dtype`) */
    PyTypeObject *baseclass;
} PyArrayDTypeMeta_Spec;


#define PyArrayDTypeMeta_Type \
    (*(PyTypeObject *)__experimental_dtype_api_table[2])
typedef int __dtypemeta_fromspec(
        PyArray_DTypeMeta *DType, PyArrayDTypeMeta_Spec *dtype_spec);
/*
 * Finalize creation of a DTypeMeta.  You must ensure that the DTypeMeta is
 * a proper subclass.  The DTypeMeta object has additional fields compared to
 * a normal PyTypeObject!
 * The only (easy) creation of a new DType is to create a static Type which
 * inherits `PyArray_DescrType`, sets its type to `PyArrayDTypeMeta_Type` and
 * uses `PyArray_DTypeMeta` defined above as the C-structure.
 */
#define PyArrayInitDTypeMeta_FromSpec \
    ((__dtypemeta_fromspec *)(__experimental_dtype_api_table[3]))


/*
 * *************************************
 *          WORKING WITH DTYPES
 * *************************************
 */

typedef PyArray_DTypeMeta *__common_dtype(
        PyArray_DTypeMeta *DType1, PyArray_DTypeMeta *DType2);
#define PyArray_CommonDType \
    ((__common_dtype *)(__experimental_dtype_api_table[4]))


typedef PyArray_DTypeMeta *__promote_dtype_sequence(
        npy_intp num, PyArray_DTypeMeta *DTypes[]);
#define PyArray_PromoteDTypeSequence \
    ((__promote_dtype_sequence *)(__experimental_dtype_api_table[5]))


typedef PyArray_Descr *__get_default_descr(
        PyArray_DTypeMeta *DType);
#define _PyArray_GetDefaultDescr \
    ((__get_default_descr *)(__experimental_dtype_api_table[6]))

static NPY_INLINE PyArray_Descr *
PyArray_GetDefaultDescr(PyArray_DTypeMeta *DType)
{
    if (DType->singleton != NULL) {
        Py_INCREF(DType->singleton);
        return DType->singleton;
    }
    return _PyArray_GetDefaultDescr(DType);
}


/*
 * NumPy's builtin DTypes:
 */
#define PyArray_BoolDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[10])
/* Integers */
#define PyArray_ByteDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[11])
#define PyArray_UByteDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[12])
#define PyArray_ShortDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[13])
#define PyArray_UShortDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[14])
#define PyArray_IntDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[15])
#define PyArray_UIntDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[16])
#define PyArray_LongDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[17])
#define PyArray_ULongDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[18])
#define PyArray_LongLongDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[19])
#define PyArray_ULongLongDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[20])
/* Integer aliases */
#define PyArray_Int8Type (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[21])
#define PyArray_UInt8DType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[22])
#define PyArray_Int16DType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[23])
#define PyArray_UInt16DType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[24])
#define PyArray_Int32DType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[25])
#define PyArray_UInt32DType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[26])
#define PyArray_Int64DType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[27])
#define PyArray_UInt64DType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[28])
#define PyArray_IntpDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[29])
#define PyArray_UIntpDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[30])
/* Floats */
#define PyArray_HalfType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[31])
#define PyArray_FloatDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[32])
#define PyArray_DoubleDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[33])
#define PyArray_LongDoubleDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[34])
/* Complex */
#define PyArray_CFloatDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[35])
#define PyArray_CDoubleDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[36])
#define PyArray_CLongDoubleDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[37])
/* String/Bytes */
#define PyArray_StringDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[38])
#define PyArray_UnicodeDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[39])
/* Datetime/Timedelta */
#define PyArray_DatetimeDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[40])
#define PyArray_TimedeltaDType (*(PyArray_DTypeMeta *)__experimental_dtype_api_table[41])


/*
 * ********************************
 *         Initialization
 * ********************************
 *
 * Import the experimental API, the version must match the one defined in
 * the header to ensure changes are taken into account. NumPy will further
 * runtime-check this.
 * You must call this function to use the symbols defined in this file.
 */
#if !defined(NO_IMPORT) && !defined(NO_IMPORT_ARRAY)

#define __EXPERIMENTAL_DTYPE_VERSION 5

static int
import_experimental_dtype_api(int version)
{
    if (version != __EXPERIMENTAL_DTYPE_VERSION) {
        PyErr_Format(PyExc_RuntimeError,
                "DType API version %d did not match header version %d. Please "
                "update the import statement and check for API changes.",
                version, __EXPERIMENTAL_DTYPE_VERSION);
        return -1;
    }
    if (__experimental_dtype_api_table != __uninitialized_table) {
        /* already imported. */
        return 0;
    }

    PyObject *multiarray = PyImport_ImportModule("numpy.core._multiarray_umath");
    if (multiarray == NULL) {
        return -1;
    }

    PyObject *api = PyObject_CallMethod(multiarray,
        "_get_experimental_dtype_api", "i", version);
    Py_DECREF(multiarray);
    if (api == NULL) {
        return -1;
    }
    __experimental_dtype_api_table = (void **)PyCapsule_GetPointer(api,
            "experimental_dtype_api_table");
    Py_DECREF(api);

    if (__experimental_dtype_api_table == NULL) {
        __experimental_dtype_api_table = __uninitialized_table;
        return -1;
    }
    return 0;
}

#endif  /* !defined(NO_IMPORT) && !defined(NO_IMPORT_ARRAY) */

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_EXPERIMENTAL_DTYPE_API_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/halffloat.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY_HALFFLOAT_H_
#define NUMPY_CORE_INCLUDE_NUMPY_HALFFLOAT_H_

#include <Python.h>
#include <numpy/npy_math.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Half-precision routines
 */

/* Conversions */
float npy_half_to_float(npy_half h);
double npy_half_to_double(npy_half h);
npy_half npy_float_to_half(float f);
npy_half npy_double_to_half(double d);
/* Comparisons */
int npy_half_eq(npy_half h1, npy_half h2);
int npy_half_ne(npy_half h1, npy_half h2);
int npy_half_le(npy_half h1, npy_half h2);
int npy_half_lt(npy_half h1, npy_half h2);
int npy_half_ge(npy_half h1, npy_half h2);
int npy_half_gt(npy_half h1, npy_half h2);
/* faster *_nonan variants for when you know h1 and h2 are not NaN */
int npy_half_eq_nonan(npy_half h1, npy_half h2);
int npy_half_lt_nonan(npy_half h1, npy_half h2);
int npy_half_le_nonan(npy_half h1, npy_half h2);
/* Miscellaneous functions */
int npy_half_iszero(npy_half h);
int npy_half_isnan(npy_half h);
int npy_half_isinf(npy_half h);
int npy_half_isfinite(npy_half h);
int npy_half_signbit(npy_half h);
npy_half npy_half_copysign(npy_half x, npy_half y);
npy_half npy_half_spacing(npy_half h);
npy_half npy_half_nextafter(npy_half x, npy_half y);
npy_half npy_half_divmod(npy_half x, npy_half y, npy_half *modulus);

/*
 * Half-precision constants
 */

#define NPY_HALF_ZERO   (0x0000u)
#define NPY_HALF_PZERO  (0x0000u)
#define NPY_HALF_NZERO  (0x8000u)
#define NPY_HALF_ONE    (0x3c00u)
#define NPY_HALF_NEGONE (0xbc00u)
#define NPY_HALF_PINF   (0x7c00u)
#define NPY_HALF_NINF   (0xfc00u)
#define NPY_HALF_NAN    (0x7e00u)

#define NPY_MAX_HALF    (0x7bffu)

/*
 * Bit-level conversions
 */

npy_uint16 npy_floatbits_to_halfbits(npy_uint32 f);
npy_uint16 npy_doublebits_to_halfbits(npy_uint64 d);
npy_uint32 npy_halfbits_to_floatbits(npy_uint16 h);
npy_uint64 npy_halfbits_to_doublebits(npy_uint16 h);

#ifdef __cplusplus
}
#endif

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_HALFFLOAT_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/libdivide/libdivide.h

```plaintext
// libdivide.h - Optimized integer division
// https://libdivide.com
//
// Copyright (C) 2010 - 2019 ridiculous_fish, <libdivide@ridiculousfish.com>
// Copyright (C) 2016 - 2019 Kim Walisch, <kim.walisch@gmail.com>
//
// libdivide is dual-licensed under the Boost or zlib licenses.
// You may use libdivide under the terms of either of these.
// See LICENSE.txt for more details.

#ifndef NUMPY_CORE_INCLUDE_NUMPY_LIBDIVIDE_LIBDIVIDE_H_
#define NUMPY_CORE_INCLUDE_NUMPY_LIBDIVIDE_LIBDIVIDE_H_

#define LIBDIVIDE_VERSION "3.0"
#define LIBDIVIDE_VERSION_MAJOR 3
#define LIBDIVIDE_VERSION_MINOR 0

#include <stdint.h>

#if defined(__cplusplus)
    #include <cstdlib>
    #include <cstdio>
    #include <type_traits>
#else
    #include <stdlib.h>
    #include <stdio.h>
#endif

#if defined(LIBDIVIDE_AVX512)
    #include <immintrin.h>
#elif defined(LIBDIVIDE_AVX2)
    #include <immintrin.h>
#elif defined(LIBDIVIDE_SSE2)
    #include <emmintrin.h>
#endif

#if defined(_MSC_VER)
    #include <intrin.h>
    // disable warning C4146: unary minus operator applied
    // to unsigned type, result still unsigned
    #pragma warning(disable: 4146)
    #define LIBDIVIDE_VC
#endif

#if !defined(__has_builtin)
    #define __has_builtin(x) 0
#endif

#if defined(__SIZEOF_INT128__)
    #define HAS_INT128_T
    // clang-cl on Windows does not yet support 128-bit division
    #if !(defined(__clang__) && defined(LIBDIVIDE_VC))
        #define HAS_INT128_DIV
    #endif
#endif

#if defined(__x86_64__) || defined(_M_X64)
    #define LIBDIVIDE_X86_64
#endif

#if defined(__i386__)
    #define LIBDIVIDE_i386
#endif

#if defined(__GNUC__) || defined(__clang__)
    #define LIBDIVIDE_GCC_STYLE_ASM
#endif

#if defined(__cplusplus) || defined(LIBDIVIDE_VC)
    #define LIBDIVIDE_FUNCTION __FUNCTION__
#else
    #define LIBDIVIDE_FUNCTION __func__
#endif

#define LIBDIVIDE_ERROR(msg) \
    do { \
        fprintf(stderr, "libdivide.h:%d: %s(): Error: %s\n", \
            __LINE__, LIBDIVIDE_FUNCTION, msg); \
        abort(); \
    } while (0)

#if defined(LIBDIVIDE_ASSERTIONS_ON)
    #define LIBDIVIDE_ASSERT(x) \
        do { \
            if (!(x)) { \
                fprintf(stderr, "libdivide.h:%d: %s(): Assertion failed: %s\n", \
                    __LINE__, LIBDIVIDE_FUNCTION, #x); \
                abort(); \
            } \
        } while (0)
#else
    #define LIBDIVIDE_ASSERT(x)
#endif

#ifdef __cplusplus
namespace libdivide {
#endif

// pack divider structs to prevent compilers from padding.
// This reduces memory usage by up to 43% when using a large
// array of libdivide dividers and improves performance
// by up to 10% because of reduced memory bandwidth.
#pragma pack(push, 1)

struct libdivide_u32_t {
    uint32_t magic;
    uint8_t more;
};

struct libdivide_s32_t {
    int32_t magic;
    uint8_t more;
};

struct libdivide_u64_t {
    uint64_t magic;
    uint8_t more;
};

struct libdivide_s64_t {
    int64_t magic;
    uint8_t more;
};

struct libdivide_u32_branchfree_t {
    uint32_t magic;
    uint8_t more;
};

struct libdivide_s32_branchfree_t {
    int32_t magic;
    uint8_t more;
};

struct libdivide_u64_branchfree_t {
    uint64_t magic;
    uint8_t more;
};

struct libdivide_s64_branchfree_t {
    int64_t magic;
    uint8_t more;
};

#pragma pack(pop)

// Explanation of the "more" field:
//
// * Bits 0-5 is the shift value (for shift path or mult path).
// * Bit 6 is the add indicator for mult path.
// * Bit 7 is set if the divisor is negative. We use bit 7 as the negative
//   divisor indicator so that we can efficiently use sign extension to
//   create a bitmask with all bits set to 1 (if the divisor is negative)
//   or 0 (if the divisor is positive).
//
// u32: [0-4] shift value
//      [5] ignored
//      [6] add indicator
//      magic number of 0 indicates shift path
//
// s32: [0-4] shift value
//      [5] ignored
//      [6] add indicator
//      [7] indicates negative divisor
//      magic number of 0 indicates shift path
//
// u64: [0-5] shift value
//      [6] add indicator
//      magic number of 0 indicates shift path
//
// s64: [0-5] shift value
//      [6] add indicator
//      [7] indicates negative divisor
//      magic number of 0 indicates shift path
//
// In s32 and s64 branchfree modes, the magic number is negated according to
// whether the divisor is negated. In branchfree strategy, it is not negated.

enum {
    LIBDIVIDE_32_SHIFT_MASK = 0x1F,
    LIBDIVIDE_64_SHIFT_MASK = 0x3F,
    LIBDIVIDE_ADD_MARKER = 0x40,
    LIBDIVIDE_NEGATIVE_DIVISOR = 0x80
};

static inline struct libdivide_s32_t libdivide_s32_gen(int32_t d);
static inline struct libdivide_u32_t libdivide_u32_gen(uint32_t d);
static inline struct libdivide_s64_t libdivide_s64_gen(int64_t d);
static inline struct libdivide_u64_t libdivide_u64_gen(uint64_t d);

static inline struct libdivide_s32_branchfree_t libdivide_s32_branchfree_gen(int32_t d);
static inline struct libdivide_u32_branchfree_t libdivide_u32_branchfree_gen(uint32_t d);
static inline struct libdivide_s64_branchfree_t libdivide_s64_branchfree_gen(int64_t d);
static inline struct libdivide_u64_branchfree_t libdivide_u64_branchfree_gen(uint64_t d);

static inline int32_t  libdivide_s32_do(int32_t numer, const struct libdivide_s32_t *denom);
static inline uint32_t libdivide_u32_do(uint32_t numer, const struct libdivide_u32_t *denom);
static inline int64_t  libdivide_s64_do(int64_t numer, const struct libdivide_s64_t *denom);
static inline uint64_t libdivide_u64_do(uint64_t numer, const struct libdivide_u64_t *denom);

static inline int32_t  libdivide_s32_branchfree_do(int32_t numer, const struct libdivide_s32_branchfree_t *denom);
static inline uint32_t libdivide_u32_branchfree_do(uint32_t numer, const struct libdivide_u32_branchfree_t *denom);
static inline int64_t  libdivide_s64_branchfree_do(int64_t numer, const struct libdivide_s64_branchfree_t *denom);
static inline uint64_t libdivide_u64_branchfree_do(uint64_t numer, const struct libdivide_u64_branchfree_t *denom);

static inline int32_t  libdivide_s32_recover(const struct libdivide_s32_t *denom);
static inline uint32_t libdivide_u32_recover(const struct libdivide_u32_t *denom);
static inline int64_t  libdivide_s64_recover(const struct libdivide_s64_t *denom);
static inline uint64_t libdivide_u64_recover(const struct libdivide_u64_t *denom);

static inline int32_t  libdivide_s32_branchfree_recover(const struct libdivide_s32_branchfree_t *denom);
static inline uint32_t libdivide_u32_branchfree_recover(const struct libdivide_u32_branchfree_t *denom);
static inline int64_t  libdivide_s64_branchfree_recover(const struct libdivide_s64_branchfree_t *denom);
static inline uint64_t libdivide_u64_branchfree_recover(const struct libdivide_u64_branchfree_t *denom);

//////// Internal Utility Functions

static inline uint32_t libdivide_mullhi_u32(uint32_t x, uint32_t y) {
    uint64_t xl = x, yl = y;
    uint64_t rl = xl * yl;
    return (uint32_t)(rl >> 32);
}

static inline int32_t libdivide_mullhi_s32(int32_t x, int32_t y) {
    int64_t xl = x, yl = y;
    int64_t rl = xl * yl;
    // needs to be arithmetic shift
    return (int32_t)(rl >> 32);
}

static inline uint64_t libdivide_mullhi_u64(uint64_t x, uint64_t y) {
#if defined(LIBDIVIDE_VC) && \
    defined(LIBDIVIDE_X86_64)
    return __umulh(x, y);
#elif defined(HAS_INT128_T)
    __uint128_t xl = x, yl = y;
    __uint128_t rl = xl * yl;
    return (uint64_t)(rl >> 64);
#else
    // full 128 bits are x0 * y0 + (x0 * y1 << 32) + (x1 * y0 << 32) + (x1 * y1 << 64)
    uint32_t mask = 0xFFFFFFFF;
    uint32_t x0 = (uint32_t)(x & mask);
    uint32_t x1 = (uint32_t)(x >> 32);
    uint32_t y0 = (uint32_t)(y & mask);
    uint32_t y1 = (uint32_t)(y >> 32);
    uint32_t x0y0_hi = libdivide_mullhi_u32(x0, y0);
    uint64_t x0y1 = x0 * (uint64_t)y1;
    uint64_t x1y0 = x1 * (uint64_t)y0;
    uint64_t x1y1 = x1 * (uint64_t)y1;
    uint64_t temp = x1y0 + x0y0_hi;
    uint64_t temp_lo = temp & mask;
    uint64_t temp_hi = temp >> 32;

    return x1y1 + temp_hi + ((temp_lo + x0y1) >> 32);
#endif
}

static inline int64_t libdivide_mullhi_s64(int64_t x, int64_t y) {
#if defined(LIBDIVIDE_VC) && \
    defined(LIBDIVIDE_X86_64)
    return __mulh(x, y);
#elif defined(HAS_INT128_T)
    __int128_t xl = x, yl = y;
    __int128_t rl = xl * yl;
    return (int64_t)(rl >> 64);
#else
    // full 128 bits are x0 * y0 + (x0 * y1 << 32) + (x1 * y0 << 32) + (x1 * y1 << 64)
    uint32_t mask = 0xFFFFFFFF;
    uint32_t x0 = (uint32_t)(x & mask);
    uint32_t y0 = (uint32_t)(y & mask);
    int32_t x1 = (int32_t)(x >> 32);
    int32_t y1 = (int32_t)(y >> 32);
    uint32_t x0y0_hi = libdivide_mullhi_u32(x0, y0);
    int64_t t = x1 * (int64_t)y0 + x0y0_hi;
    int64_t w1 = x0 * (int64_t)y1 + (t & mask);

    return x1 * (int64_t)y1 + (t >> 32) + (w1 >> 32);
#endif
}

static inline int32_t libdivide_count_leading_zeros32(uint32_t val) {
#if defined(__GNUC__) || \
    __has_builtin(__builtin_clz)
    // Fast way to count leading zeros
    return __builtin_clz(val);
#elif defined(LIBDIVIDE_VC)
    unsigned long result;
    if (_BitScanReverse(&result, val)) {
        return 31 - result;
    }
    return 0;
#else
    if (val == 0)
        return 32;
    int32_t result = 8;
    uint32_t hi = 0xFFU << 24;
    while ((val & hi) == 0) {
        hi >>= 8;
        result += 8;
    }
    while (val & hi) {
        result -= 1;
        hi <<= 1;
    }
    return result;
#endif
}

static inline int32_t libdivide_count_leading_zeros64(uint64_t val) {
#if defined(__GNUC__) || \
    __has_builtin(__builtin_clzll)
    // Fast way to count leading zeros
    return __builtin_clzll(val);
#elif defined(LIBDIVIDE_VC) && defined(_WIN64)
    unsigned long result;
    if (_BitScanReverse64(&result, val)) {
        return 63 - result;
    }
    return 0;
#else
    uint32_t hi = val >> 32;
    uint32_t lo = val & 0xFFFFFFFF;
    if (hi != 0) return libdivide_count_leading_zeros32(hi);
    return 32 + libdivide_count_leading_zeros32(lo);
#endif
}

// libdivide_64_div_32_to_32: divides a 64-bit uint {u1, u0} by a 32-bit
// uint {v}. The result must fit in 32 bits.
// Returns the quotient directly and the remainder in *r
static inline uint32_t libdivide_64_div_32_to_32(uint32_t u1, uint32_t u0, uint32_t v, uint32_t *r) {
#if (defined(LIBDIVIDE_i386) || defined(LIBDIVIDE_X86_64)) && \
     defined(LIBDIVIDE_GCC_STYLE_ASM)
    uint32_t result;
    __asm__("divl %[v]"
            : "=a"(result), "=d"(*r)
            : [v] "r"(v), "a"(u0), "d"(u1)
            );
    return result;
#else
    uint64_t n = ((uint64_t)u1 << 32) | u0;
    uint32_t result = (uint32_t)(n / v);
    *r = (uint32_t)(n - result * (uint64_t)v);
    return result;
#endif
}

// libdivide_128_div_64_to_64: divides a 128-bit uint {u1, u0} by a 64-bit
// uint {v}. The result must fit in 64 bits.
// Returns the quotient directly and the remainder in *r
static uint64_t libdivide_128_div_64_to_64(uint64_t u1, uint64_t u0, uint64_t v, uint64_t *r) {
#if defined(LIBDIVIDE_X86_64) && \
    defined(LIBDIVIDE_GCC_STYLE_ASM)
    uint64_t result;
    __asm__("divq %[v]"
            : "=a"(result), "=d"(*r)
            : [v] "r"(v), "a"(u0), "d"(u1)
            );
    return result;
#elif defined(HAS_INT128_T) && \
      defined(HAS_INT128_DIV)
    __uint128_t n = ((__uint128_t)u1 << 64) | u0;
    uint64_t result = (uint64_t)(n / v);
    *r = (uint64_t)(n - result * (__uint128_t)v);
    return result;
#else
    // Code taken from Hacker's Delight:
    // http://www.hackersdelight.org/HDcode/divlu.c.
    // License permits inclusion here per:
    // http://www.hackersdelight.org/permissions.htm

    const uint64_t b = (1ULL << 32); // Number base (32 bits)
    uint64_t un1, un0; // Norm. dividend LSD's
    uint64_t vn1, vn0; // Norm. divisor digits
    uint64_t q1, q0; // Quotient digits
    uint64_t un64, un21, un10; // Dividend digit pairs
    uint64_t rhat; // A remainder
    int32_t s; // Shift amount for norm

    // If overflow, set rem. to an impossible value,
    // and return the largest possible quotient
    if (u1 >= v) {
        *r = (uint64_t) -1;
        return (uint64_t) -1;
    }

    // count leading zeros
    s = libdivide_count_leading_zeros64(v);
    if (s > 0) {
        // Normalize divisor
        v = v << s;
        un64 = (u1 << s) | (u0 >> (64 - s));
        un10 = u0 << s; // Shift dividend left
    } else {
        // Avoid undefined behavior of (u0 >> 64).
        // The behavior is undefined if the right operand is
        // negative, or greater than or equal to the length
        // in bits of the promoted left operand.
        un64 = u1;
        un10 = u0;
    }

    // Break divisor up into two 32-bit digits
    vn1 = v >> 32;
    vn0 = v & 0xFFFFFFFF;

    // Break right half of dividend into two digits
    un1 = un10 >> 32;
    un0 = un10 & 0xFFFFFFFF;

    // Compute the first quotient digit, q1
    q1 = un64 / vn1;
    rhat = un64 - q1 * vn1;

    while (q1 >= b || q1 * vn0 > b * rhat + un1) {
        q1 = q1 - 1;
        rhat = rhat + vn1;
        if (rhat >= b)
            break;
    }

     // Multiply and subtract
    un21 = un64 * b + un1 - q1 * v;

    // Compute the second quotient digit
    q0 = un21 / vn1;
    rhat = un21 - q0 * vn1;

    while (q0 >= b || q0 * vn0 > b * rhat + un0) {
        q0 = q0 - 1;
        rhat = rhat + vn1;
        if (rhat >= b)
            break;
    }

    *r = (un21 * b + un0 - q0 * v) >> s;
    return q1 * b + q0;
#endif
}

// Bitshift a u128 in place, left (signed_shift > 0) or right (signed_shift < 0)
static inline void libdivide_u128_shift(uint64_t *u1, uint64_t *u0, int32_t signed_shift) {
    if (signed_shift > 0) {
        uint32_t shift = signed_shift;
        *u1 <<= shift;
        *u1 |= *u0 >> (64 - shift);
        *u0 <<= shift;
    }
    else if (signed_shift < 0) {
        uint32_t shift = -signed_shift;
        *u0 >>= shift;
        *u0 |= *u1 << (64 - shift);
        *u1 >>= shift;
    }
}

// Computes a 128 / 128 -> 64 bit division, with a 128 bit remainder.
static uint64_t libdivide_128_div_128_to_64(uint64_t u_hi, uint64_t u_lo, uint64_t v_hi, uint64_t v_lo, uint64_t *r_hi, uint64_t *r_lo) {
#if defined(HAS_INT128_T) && \
    defined(HAS_INT128_DIV)
    __uint128_t ufull = u_hi;
    __uint128_t vfull = v_hi;
    ufull = (ufull << 64) | u_lo;
    vfull = (vfull << 64) | v_lo;
    uint64_t res = (uint64_t)(ufull / vfull);
    __uint128_t remainder = ufull - (vfull * res);
    *r_lo = (uint64_t)remainder;
    *r_hi = (uint64_t)(remainder >> 64);
    return res;
#else
    // Adapted from "Unsigned Doubleword Division" in Hacker's Delight
    // We want to compute u / v
    typedef struct { uint64_t hi; uint64_t lo; } u128_t;
    u128_t u = {u_hi, u_lo};
    u128_t v = {v_hi, v_lo};

    if (v.hi == 0) {
        // divisor v is a 64 bit value, so we just need one 128/64 division
        // Note that we are simpler than Hacker's Delight here, because we know
        // the quotient fits in 64 bits whereas Hacker's Delight demands a full
        // 128 bit quotient
        *r_hi = 0;
        return libdivide_128_div_64_to_64(u.hi, u.lo, v.lo, r_lo);
    }
    // Here v >= 2**64
    // We know that v.hi != 0, so count leading zeros is OK
    // We have 0 <= n <= 63
    uint32_t n = libdivide_count_leading_zeros64(v.hi);

    // Normalize the divisor so its MSB is 1
    u128_t v1t = v;
    libdivide_u128_shift(&v1t.hi, &v1t.lo, n);
    uint64_t v1 = v1t.hi; // i.e. v1 = v1t >> 64

    // To ensure no overflow
    u128_t u1 = u;
    libdivide_u128_shift(&u1.hi, &u1.lo, -1);

    // Get quotient from divide unsigned insn.
    uint64_t rem_ignored;
    uint64_t q1 = libdivide_128_div_64_to_64(u1.hi, u1.lo, v1, &rem_ignored);

    // Undo normalization and division of u by 2.
    u128_t q0 = {0, q1};
    libdivide_u128_shift(&q0.hi, &q0.lo, n);
    libdivide_u128_shift(&q0.hi, &q0.lo, -63);

    // Make q0 correct or too small by 1
    // Equivalent to `if (q0 != 0) q0 = q0 - 1;`
    if (q0.hi != 0 || q0.lo != 0) {
        q0.hi -= (q0.lo == 0); // borrow
        q0.lo -= 1;
    }

    // Now q0 is correct.
    // Compute q0 * v as q0v
    // = (q0.hi << 64 + q0.lo) * (v.hi << 64 + v.lo)
    // = (q0.hi * v.hi << 128) + (q0.hi * v.lo << 64) +
    //   (q0.lo * v.hi <<  64) + q0.lo * v.lo)
    // Each term is 128 bit
    // High half of full product (upper 128 bits!) are dropped
    u128_t q0v = {0, 0};
    q0v.hi = q0.hi*v.lo + q0.lo*v.hi + libdivide_mullhi_u64(q0.lo, v.lo);
    q0v.lo = q0.lo*v.lo;

    // Compute u - q0v as u_q0v
    // This is the remainder
    u128_t u_q0v = u;
    u_q0v.hi -= q0v.hi + (u.lo < q0v.lo); // second term is borrow
    u_q0v.lo -= q0v.lo;

    // Check if u_q0v >= v
    // This checks if our remainder is larger than the divisor
    if ((u_q0v.hi > v.hi) ||
        (u_q0v.hi == v.hi && u_q0v.lo >= v.lo)) {
        // Increment q0
        q0.lo += 1;
        q0.hi += (q0.lo == 0); // carry

        // Subtract v from remainder
        u_q0v.hi -= v.hi + (u_q0v.lo < v.lo);
        u_q0v.lo -= v.lo;
    }

    *r_hi = u_q0v.hi;
    *r_lo = u_q0v.lo;

    LIBDIVIDE_ASSERT(q0.hi == 0);
    return q0.lo;
#endif
}

////////// UINT32

static inline struct libdivide_u32_t libdivide_internal_u32_gen(uint32_t d, int branchfree) {
    if (d == 0) {
        LIBDIVIDE_ERROR("divider must be != 0");
    }

    struct libdivide_u32_t result;
    uint32_t floor_log_2_d = 31 - libdivide_count_leading_zeros32(d);

    // Power of 2
    if ((d & (d - 1)) == 0) {
        // We need to subtract 1 from the shift value in case of an unsigned
        // branchfree divider because there is a hardcoded right shift by 1
        // in its division algorithm. Because of this we also need to add back
        // 1 in its recovery algorithm.
        result.magic = 0;
        result.more = (uint8_t)(floor_log_2_d - (branchfree != 0));
    } else {
        uint8_t more;
        uint32_t rem, proposed_m;
        proposed_m = libdivide_64_div_32_to_32(1U << floor_log_2_d, 0, d, &rem);

        LIBDIVIDE_ASSERT(rem > 0 && rem < d);
        const uint32_t e = d - rem;

        // This power works if e < 2**floor_log_2_d.
        if (!branchfree && (e < (1U << floor_log_2_d))) {
            // This power works
            more = floor_log_2_d;
        } else {
            // We have to use the general 33-bit algorithm.  We need to compute
            // (2**power) / d. However, we already have (2**(power-1))/d and
            // its remainder.  By doubling both, and then correcting the
            // remainder, we can compute the larger division.
            // don't care about overflow here - in fact, we expect it
            proposed_m += proposed_m;
            const uint32_t twice_rem = rem + rem;
            if (twice_rem >= d || twice_rem < rem) proposed_m += 1;
            more = floor_log_2_d | LIBDIVIDE_ADD_MARKER;
        }
        result.magic = 1 + proposed_m;
        result.more = more;
        // result.more's shift should in general be ceil_log_2_d. But if we
        // used the smaller power, we subtract one from the shift because we're
        // using the smaller power. If we're using the larger power, we
        // subtract one from the shift because it's taken care of by the add
        // indicator. So floor_log_2_d happens to be correct in both cases.
    }
    return result;
}

struct libdivide_u32_t libdivide_u32_gen(uint32_t d) {
    return libdivide_internal_u32_gen(d, 0);
}

struct libdivide_u32_branchfree_t libdivide_u32_branchfree_gen(uint32_t d) {
    if (d == 1) {
        LIBDIVIDE_ERROR("branchfree divider must be != 1");
    }
    struct libdivide_u32_t tmp = libdivide_internal_u32_gen(d, 1);
    struct libdivide_u32_branchfree_t ret = {tmp.magic, (uint8_t)(tmp.more & LIBDIVIDE_32_SHIFT_MASK)};
    return ret;
}

uint32_t libdivide_u32_do(uint32_t numer, const struct libdivide_u32_t *denom) {
    uint8_t more = denom->more;
    if (!denom->magic) {
        return numer >> more;
    }
    else {
        uint32_t q = libdivide_mullhi_u32(denom->magic, numer);
        if (more & LIBDIVIDE_ADD_MARKER) {
            uint32_t t = ((numer - q) >> 1) + q;
            return t >> (more & LIBDIVIDE_32_SHIFT_MASK);
        }
        else {
            // All upper bits are 0,
            // don't need to mask them off.
            return q >> more;
        }
    }
}

uint32_t libdivide_u32_branchfree_do(uint32_t numer, const struct libdivide_u32_branchfree_t *denom) {
    uint32_t q = libdivide_mullhi_u32(denom->magic, numer);
    uint32_t t = ((numer - q) >> 1) + q;
    return t >> denom->more;
}

uint32_t libdivide_u32_recover(const struct libdivide_u32_t *denom) {
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_32_SHIFT_MASK;

    if (!denom->magic) {
        return 1U << shift;
    } else if (!(more & LIBDIVIDE_ADD_MARKER)) {
        // We compute q = n/d = n*m / 2^(32 + shift)
        // Therefore we have d = 2^(32 + shift) / m
        // We need to ceil it.
        // We know d is not a power of 2, so m is not a power of 2,
        // so we can just add 1 to the floor
        uint32_t hi_dividend = 1U << shift;
        uint32_t rem_ignored;
        return 1 + libdivide_64_div_32_to_32(hi_dividend, 0, denom->magic, &rem_ignored);
    } else {
        // Here we wish to compute d = 2^(32+shift+1)/(m+2^32).
        // Notice (m + 2^32) is a 33 bit number. Use 64 bit division for now
        // Also note that shift may be as high as 31, so shift + 1 will
        // overflow. So we have to compute it as 2^(32+shift)/(m+2^32), and
        // then double the quotient and remainder.
        uint64_t half_n = 1ULL << (32 + shift);
        uint64_t d = (1ULL << 32) | denom->magic;
        // Note that the quotient is guaranteed <= 32 bits, but the remainder
        // may need 33!
        uint32_t half_q = (uint32_t)(half_n / d);
        uint64_t rem = half_n % d;
        // We computed 2^(32+shift)/(m+2^32)
        // Need to double it, and then add 1 to the quotient if doubling th
        // remainder would increase the quotient.
        // Note that rem<<1 cannot overflow, since rem < d and d is 33 bits
        uint32_t full_q = half_q + half_q + ((rem<<1) >= d);

        // We rounded down in gen (hence +1)
        return full_q + 1;
    }
}

uint32_t libdivide_u32_branchfree_recover(const struct libdivide_u32_branchfree_t *denom) {
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_32_SHIFT_MASK;

    if (!denom->magic) {
        return 1U << (shift + 1);
    } else {
        // Here we wish to compute d = 2^(32+shift+1)/(m+2^32).
        // Notice (m + 2^32) is a 33 bit number. Use 64 bit division for now
        // Also note that shift may be as high as 31, so shift + 1 will
        // overflow. So we have to compute it as 2^(32+shift)/(m+2^32), and
        // then double the quotient and remainder.
        uint64_t half_n = 1ULL << (32 + shift);
        uint64_t d = (1ULL << 32) | denom->magic;
        // Note that the quotient is guaranteed <= 32 bits, but the remainder
        // may need 33!
        uint32_t half_q = (uint32_t)(half_n / d);
        uint64_t rem = half_n % d;
        // We computed 2^(32+shift)/(m+2^32)
        // Need to double it, and then add 1 to the quotient if doubling th
        // remainder would increase the quotient.
        // Note that rem<<1 cannot overflow, since rem < d and d is 33 bits
        uint32_t full_q = half_q + half_q + ((rem<<1) >= d);

        // We rounded down in gen (hence +1)
        return full_q + 1;
    }
}

/////////// UINT64

static inline struct libdivide_u64_t libdivide_internal_u64_gen(uint64_t d, int branchfree) {
    if (d == 0) {
        LIBDIVIDE_ERROR("divider must be != 0");
    }

    struct libdivide_u64_t result;
    uint32_t floor_log_2_d = 63 - libdivide_count_leading_zeros64(d);

    // Power of 2
    if ((d & (d - 1)) == 0) {
        // We need to subtract 1 from the shift value in case of an unsigned
        // branchfree divider because there is a hardcoded right shift by 1
        // in its division algorithm. Because of this we also need to add back
        // 1 in its recovery algorithm.
        result.magic = 0;
        result.more = (uint8_t)(floor_log_2_d - (branchfree != 0));
    } else {
        uint64_t proposed_m, rem;
        uint8_t more;
        // (1 << (64 + floor_log_2_d)) / d
        proposed_m = libdivide_128_div_64_to_64(1ULL << floor_log_2_d, 0, d, &rem);

        LIBDIVIDE_ASSERT(rem > 0 && rem < d);
        const uint64_t e = d - rem;

        // This power works if e < 2**floor_log_2_d.
        if (!branchfree && e < (1ULL << floor_log_2_d)) {
            // This power works
            more = floor_log_2_d;
        } else {
            // We have to use the general 65-bit algorithm.  We need to compute
            // (2**power) / d. However, we already have (2**(power-1))/d and
            // its remainder. By doubling both, and then correcting the
            // remainder, we can compute the larger division.
            // don't care about overflow here - in fact, we expect it
            proposed_m += proposed_m;
            const uint64_t twice_rem = rem + rem;
            if (twice_rem >= d || twice_rem < rem) proposed_m += 1;
                more = floor_log_2_d | LIBDIVIDE_ADD_MARKER;
        }
        result.magic = 1 + proposed_m;
        result.more = more;
        // result.more's shift should in general be ceil_log_2_d. But if we
        // used the smaller power, we subtract one from the shift because we're
        // using the smaller power. If we're using the larger power, we
        // subtract one from the shift because it's taken care of by the add
        // indicator. So floor_log_2_d happens to be correct in both cases,
        // which is why we do it outside of the if statement.
    }
    return result;
}

struct libdivide_u64_t libdivide_u64_gen(uint64_t d) {
    return libdivide_internal_u64_gen(d, 0);
}

struct libdivide_u64_branchfree_t libdivide_u64_branchfree_gen(uint64_t d) {
    if (d == 1) {
        LIBDIVIDE_ERROR("branchfree divider must be != 1");
    }
    struct libdivide_u64_t tmp = libdivide_internal_u64_gen(d, 1);
    struct libdivide_u64_branchfree_t ret = {tmp.magic, (uint8_t)(tmp.more & LIBDIVIDE_64_SHIFT_MASK)};
    return ret;
}

uint64_t libdivide_u64_do(uint64_t numer, const struct libdivide_u64_t *denom) {
    uint8_t more = denom->more;
    if (!denom->magic) {
        return numer >> more;
    }
    else {
        uint64_t q = libdivide_mullhi_u64(denom->magic, numer);
        if (more & LIBDIVIDE_ADD_MARKER) {
            uint64_t t = ((numer - q) >> 1) + q;
            return t >> (more & LIBDIVIDE_64_SHIFT_MASK);
        }
        else {
             // All upper bits are 0,
             // don't need to mask them off.
            return q >> more;
        }
    }
}

uint64_t libdivide_u64_branchfree_do(uint64_t numer, const struct libdivide_u64_branchfree_t *denom) {
    uint64_t q = libdivide_mullhi_u64(denom->magic, numer);
    uint64_t t = ((numer - q) >> 1) + q;
    return t >> denom->more;
}

uint64_t libdivide_u64_recover(const struct libdivide_u64_t *denom) {
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_64_SHIFT_MASK;

    if (!denom->magic) {
        return 1ULL << shift;
    } else if (!(more & LIBDIVIDE_ADD_MARKER)) {
        // We compute q = n/d = n*m / 2^(64 + shift)
        // Therefore we have d = 2^(64 + shift) / m
        // We need to ceil it.
        // We know d is not a power of 2, so m is not a power of 2,
        // so we can just add 1 to the floor
        uint64_t hi_dividend = 1ULL << shift;
        uint64_t rem_ignored;
        return 1 + libdivide_128_div_64_to_64(hi_dividend, 0, denom->magic, &rem_ignored);
    } else {
        // Here we wish to compute d = 2^(64+shift+1)/(m+2^64).
        // Notice (m + 2^64) is a 65 bit number. This gets hairy. See
        // libdivide_u32_recover for more on what we do here.
        // TODO: do something better than 128 bit math

        // Full n is a (potentially) 129 bit value
        // half_n is a 128 bit value
        // Compute the hi half of half_n. Low half is 0.
        uint64_t half_n_hi = 1ULL << shift, half_n_lo = 0;
        // d is a 65 bit value. The high bit is always set to 1.
        const uint64_t d_hi = 1, d_lo = denom->magic;
        // Note that the quotient is guaranteed <= 64 bits,
        // but the remainder may need 65!
        uint64_t r_hi, r_lo;
        uint64_t half_q = libdivide_128_div_128_to_64(half_n_hi, half_n_lo, d_hi, d_lo, &r_hi, &r_lo);
        // We computed 2^(64+shift)/(m+2^64)
        // Double the remainder ('dr') and check if that is larger than d
        // Note that d is a 65 bit value, so r1 is small and so r1 + r1
        // cannot overflow
        uint64_t dr_lo = r_lo + r_lo;
        uint64_t dr_hi = r_hi + r_hi + (dr_lo < r_lo); // last term is carry
        int dr_exceeds_d = (dr_hi > d_hi) || (dr_hi == d_hi && dr_lo >= d_lo);
        uint64_t full_q = half_q + half_q + (dr_exceeds_d ? 1 : 0);
        return full_q + 1;
    }
}

uint64_t libdivide_u64_branchfree_recover(const struct libdivide_u64_branchfree_t *denom) {
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_64_SHIFT_MASK;

    if (!denom->magic) {
        return 1ULL << (shift + 1);
    } else {
        // Here we wish to compute d = 2^(64+shift+1)/(m+2^64).
        // Notice (m + 2^64) is a 65 bit number. This gets hairy. See
        // libdivide_u32_recover for more on what we do here.
        // TODO: do something better than 128 bit math

        // Full n is a (potentially) 129 bit value
        // half_n is a 128 bit value
        // Compute the hi half of half_n. Low half is 0.
        uint64_t half_n_hi = 1ULL << shift, half_n_lo = 0;
        // d is a 65 bit value. The high bit is always set to 1.
        const uint64_t d_hi = 1, d_lo = denom->magic;
        // Note that the quotient is guaranteed <= 64 bits,
        // but the remainder may need 65!
        uint64_t r_hi, r_lo;
        uint64_t half_q = libdivide_128_div_128_to_64(half_n_hi, half_n_lo, d_hi, d_lo, &r_hi, &r_lo);
        // We computed 2^(64+shift)/(m+2^64)
        // Double the remainder ('dr') and check if that is larger than d
        // Note that d is a 65 bit value, so r1 is small and so r1 + r1
        // cannot overflow
        uint64_t dr_lo = r_lo + r_lo;
        uint64_t dr_hi = r_hi + r_hi + (dr_lo < r_lo); // last term is carry
        int dr_exceeds_d = (dr_hi > d_hi) || (dr_hi == d_hi && dr_lo >= d_lo);
        uint64_t full_q = half_q + half_q + (dr_exceeds_d ? 1 : 0);
        return full_q + 1;
    }
}

/////////// SINT32

static inline struct libdivide_s32_t libdivide_internal_s32_gen(int32_t d, int branchfree) {
    if (d == 0) {
        LIBDIVIDE_ERROR("divider must be != 0");
    }

    struct libdivide_s32_t result;

    // If d is a power of 2, or negative a power of 2, we have to use a shift.
    // This is especially important because the magic algorithm fails for -1.
    // To check if d is a power of 2 or its inverse, it suffices to check
    // whether its absolute value has exactly one bit set. This works even for
    // INT_MIN, because abs(INT_MIN) == INT_MIN, and INT_MIN has one bit set
    // and is a power of 2.
    uint32_t ud = (uint32_t)d;
    uint32_t absD = (d < 0) ? -ud : ud;
    uint32_t floor_log_2_d = 31 - libdivide_count_leading_zeros32(absD);
    // check if exactly one bit is set,
    // don't care if absD is 0 since that's divide by zero
    if ((absD & (absD - 1)) == 0) {
        // Branchfree and normal paths are exactly the same
        result.magic = 0;
        result.more = floor_log_2_d | (d < 0 ? LIBDIVIDE_NEGATIVE_DIVISOR : 0);
    } else {
        LIBDIVIDE_ASSERT(floor_log_2_d >= 1);

        uint8_t more;
        // the dividend here is 2**(floor_log_2_d + 31), so the low 32 bit word
        // is 0 and the high word is floor_log_2_d - 1
        uint32_t rem, proposed_m;
        proposed_m = libdivide_64_div_32_to_32(1U << (floor_log_2_d - 1), 0, absD, &rem);
        const uint32_t e = absD - rem;

        // We are going to start with a power of floor_log_2_d - 1.
        // This works if works if e < 2**floor_log_2_d.
        if (!branchfree && e < (1U << floor_log_2_d)) {
            // This power works
            more = floor_log_2_d - 1;
        } else {
            // We need to go one higher. This should not make proposed_m
            // overflow, but it will make it negative when interpreted as an
            // int32_t.
            proposed_m += proposed_m;
            const uint32_t twice_rem = rem + rem;
            if (twice_rem >= absD || twice_rem < rem) proposed_m += 1;
            more = floor_log_2_d | LIBDIVIDE_ADD_MARKER;
        }

        proposed_m += 1;
        int32_t magic = (int32_t)proposed_m;

        // Mark if we are negative. Note we only negate the magic number in the
        // branchfull case.
        if (d < 0) {
            more |= LIBDIVIDE_NEGATIVE_DIVISOR;
            if (!branchfree) {
                magic = -magic;
            }
        }

        result.more = more;
        result.magic = magic;
    }
    return result;
}

struct libdivide_s32_t libdivide_s32_gen(int32_t d) {
    return libdivide_internal_s32_gen(d, 0);
}

struct libdivide_s32_branchfree_t libdivide_s32_branchfree_gen(int32_t d) {
    struct libdivide_s32_t tmp = libdivide_internal_s32_gen(d, 1);
    struct libdivide_s32_branchfree_t result = {tmp.magic, tmp.more};
    return result;
}

int32_t libdivide_s32_do(int32_t numer, const struct libdivide_s32_t *denom) {
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_32_SHIFT_MASK;

    if (!denom->magic) {
        uint32_t sign = (int8_t)more >> 7;
        uint32_t mask = (1U << shift) - 1;
        uint32_t uq = numer + ((numer >> 31) & mask);
        int32_t q = (int32_t)uq;
        q >>= shift;
        q = (q ^ sign) - sign;
        return q;
    } else {
        uint32_t uq = (uint32_t)libdivide_mullhi_s32(denom->magic, numer);
        if (more & LIBDIVIDE_ADD_MARKER) {
            // must be arithmetic shift and then sign extend
            int32_t sign = (int8_t)more >> 7;
            // q += (more < 0 ? -numer : numer)
            // cast required to avoid UB
            uq += ((uint32_t)numer ^ sign) - sign;
        }
        int32_t q = (int32_t)uq;
        q >>= shift;
        q += (q < 0);
        return q;
    }
}

int32_t libdivide_s32_branchfree_do(int32_t numer, const struct libdivide_s32_branchfree_t *denom) {
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_32_SHIFT_MASK;
    // must be arithmetic shift and then sign extend
    int32_t sign = (int8_t)more >> 7;
    int32_t magic = denom->magic;
    int32_t q = libdivide_mullhi_s32(magic, numer);
    q += numer;

    // If q is non-negative, we have nothing to do
    // If q is negative, we want to add either (2**shift)-1 if d is a power of
    // 2, or (2**shift) if it is not a power of 2
    uint32_t is_power_of_2 = (magic == 0);
    uint32_t q_sign = (uint32_t)(q >> 31);
    q += q_sign & ((1U << shift) - is_power_of_2);

    // Now arithmetic right shift
    q >>= shift;
    // Negate if needed
    q = (q ^ sign) - sign;

    return q;
}

int32_t libdivide_s32_recover(const struct libdivide_s32_t *denom) {
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_32_SHIFT_MASK;
    if (!denom->magic) {
        uint32_t absD = 1U << shift;
        if (more & LIBDIVIDE_NEGATIVE_DIVISOR) {
            absD = -absD;
        }
        return (int32_t)absD;
    } else {
        // Unsigned math is much easier
        // We negate the magic number only in the branchfull case, and we don't
        // know which case we're in. However we have enough information to
        // determine the correct sign of the magic number. The divisor was
        // negative if LIBDIVIDE_NEGATIVE_DIVISOR is set. If ADD_MARKER is set,
        // the magic number's sign is opposite that of the divisor.
        // We want to compute the positive magic number.
        int negative_divisor = (more & LIBDIVIDE_NEGATIVE_DIVISOR);
        int magic_was_negated = (more & LIBDIVIDE_ADD_MARKER)
            ? denom->magic > 0 : denom->magic < 0;

        // Handle the power of 2 case (including branchfree)
        if (denom->magic == 0) {
            int32_t result = 1U << shift;
            return negative_divisor ? -result : result;
        }

        uint32_t d = (uint32_t)(magic_was_negated ? -denom->magic : denom->magic);
        uint64_t n = 1ULL << (32 + shift); // this shift cannot exceed 30
        uint32_t q = (uint32_t)(n / d);
        int32_t result = (int32_t)q;
        result += 1;
        return negative_divisor ? -result : result;
    }
}

int32_t libdivide_s32_branchfree_recover(const struct libdivide_s32_branchfree_t *denom) {
    return libdivide_s32_recover((const struct libdivide_s32_t *)denom);
}

///////////// SINT64

static inline struct libdivide_s64_t libdivide_internal_s64_gen(int64_t d, int branchfree) {
    if (d == 0) {
        LIBDIVIDE_ERROR("divider must be != 0");
    }

    struct libdivide_s64_t result;

    // If d is a power of 2, or negative a power of 2, we have to use a shift.
    // This is especially important because the magic algorithm fails for -1.
    // To check if d is a power of 2 or its inverse, it suffices to check
    // whether its absolute value has exactly one bit set.  This works even for
    // INT_MIN, because abs(INT_MIN) == INT_MIN, and INT_MIN has one bit set
    // and is a power of 2.
    uint64_t ud = (uint64_t)d;
    uint64_t absD = (d < 0) ? -ud : ud;
    uint32_t floor_log_2_d = 63 - libdivide_count_leading_zeros64(absD);
    // check if exactly one bit is set,
    // don't care if absD is 0 since that's divide by zero
    if ((absD & (absD - 1)) == 0) {
        // Branchfree and non-branchfree cases are the same
        result.magic = 0;
        result.more = floor_log_2_d | (d < 0 ? LIBDIVIDE_NEGATIVE_DIVISOR : 0);
    } else {
        // the dividend here is 2**(floor_log_2_d + 63), so the low 64 bit word
        // is 0 and the high word is floor_log_2_d - 1
        uint8_t more;
        uint64_t rem, proposed_m;
        proposed_m = libdivide_128_div_64_to_64(1ULL << (floor_log_2_d - 1), 0, absD, &rem);
        const uint64_t e = absD - rem;

        // We are going to start with a power of floor_log_2_d - 1.
        // This works if works if e < 2**floor_log_2_d.
        if (!branchfree && e < (1ULL << floor_log_2_d)) {
            // This power works
            more = floor_log_2_d - 1;
        } else {
            // We need to go one higher. This should not make proposed_m
            // overflow, but it will make it negative when interpreted as an
            // int32_t.
            proposed_m += proposed_m;
            const uint64_t twice_rem = rem + rem;
            if (twice_rem >= absD || twice_rem < rem) proposed_m += 1;
            // note that we only set the LIBDIVIDE_NEGATIVE_DIVISOR bit if we
            // also set ADD_MARKER this is an annoying optimization that
            // enables algorithm #4 to avoid the mask. However we always set it
            // in the branchfree case
            more = floor_log_2_d | LIBDIVIDE_ADD_MARKER;
        }
        proposed_m += 1;
        int64_t magic = (int64_t)proposed_m;

        // Mark if we are negative
        if (d < 0) {
            more |= LIBDIVIDE_NEGATIVE_DIVISOR;
            if (!branchfree) {
                magic = -magic;
            }
        }

        result.more = more;
        result.magic = magic;
    }
    return result;
}

struct libdivide_s64_t libdivide_s64_gen(int64_t d) {
    return libdivide_internal_s64_gen(d, 0);
}

struct libdivide_s64_branchfree_t libdivide_s64_branchfree_gen(int64_t d) {
    struct libdivide_s64_t tmp = libdivide_internal_s64_gen(d, 1);
    struct libdivide_s64_branchfree_t ret = {tmp.magic, tmp.more};
    return ret;
}

int64_t libdivide_s64_do(int64_t numer, const struct libdivide_s64_t *denom) {
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_64_SHIFT_MASK;

    if (!denom->magic) { // shift path
        uint64_t mask = (1ULL << shift) - 1;
        uint64_t uq = numer + ((numer >> 63) & mask);
        int64_t q = (int64_t)uq;
        q >>= shift;
        // must be arithmetic shift and then sign-extend
        int64_t sign = (int8_t)more >> 7;
        q = (q ^ sign) - sign;
        return q;
    } else {
        uint64_t uq = (uint64_t)libdivide_mullhi_s64(denom->magic, numer);
        if (more & LIBDIVIDE_ADD_MARKER) {
            // must be arithmetic shift and then sign extend
            int64_t sign = (int8_t)more >> 7;
            // q += (more < 0 ? -numer : numer)
            // cast required to avoid UB
            uq += ((uint64_t)numer ^ sign) - sign;
        }
        int64_t q = (int64_t)uq;
        q >>= shift;
        q += (q < 0);
        return q;
    }
}

int64_t libdivide_s64_branchfree_do(int64_t numer, const struct libdivide_s64_branchfree_t *denom) {
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_64_SHIFT_MASK;
    // must be arithmetic shift and then sign extend
    int64_t sign = (int8_t)more >> 7;
    int64_t magic = denom->magic;
    int64_t q = libdivide_mullhi_s64(magic, numer);
    q += numer;

    // If q is non-negative, we have nothing to do.
    // If q is negative, we want to add either (2**shift)-1 if d is a power of
    // 2, or (2**shift) if it is not a power of 2.
    uint64_t is_power_of_2 = (magic == 0);
    uint64_t q_sign = (uint64_t)(q >> 63);
    q += q_sign & ((1ULL << shift) - is_power_of_2);

    // Arithmetic right shift
    q >>= shift;
    // Negate if needed
    q = (q ^ sign) - sign;

    return q;
}

int64_t libdivide_s64_recover(const struct libdivide_s64_t *denom) {
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_64_SHIFT_MASK;
    if (denom->magic == 0) { // shift path
        uint64_t absD = 1ULL << shift;
        if (more & LIBDIVIDE_NEGATIVE_DIVISOR) {
            absD = -absD;
        }
        return (int64_t)absD;
    } else {
        // Unsigned math is much easier
        int negative_divisor = (more & LIBDIVIDE_NEGATIVE_DIVISOR);
        int magic_was_negated = (more & LIBDIVIDE_ADD_MARKER)
            ? denom->magic > 0 : denom->magic < 0;

        uint64_t d = (uint64_t)(magic_was_negated ? -denom->magic : denom->magic);
        uint64_t n_hi = 1ULL << shift, n_lo = 0;
        uint64_t rem_ignored;
        uint64_t q = libdivide_128_div_64_to_64(n_hi, n_lo, d, &rem_ignored);
        int64_t result = (int64_t)(q + 1);
        if (negative_divisor) {
            result = -result;
        }
        return result;
    }
}

int64_t libdivide_s64_branchfree_recover(const struct libdivide_s64_branchfree_t *denom) {
    return libdivide_s64_recover((const struct libdivide_s64_t *)denom);
}

#if defined(LIBDIVIDE_AVX512)

static inline __m512i libdivide_u32_do_vector(__m512i numers, const struct libdivide_u32_t *denom);
static inline __m512i libdivide_s32_do_vector(__m512i numers, const struct libdivide_s32_t *denom);
static inline __m512i libdivide_u64_do_vector(__m512i numers, const struct libdivide_u64_t *denom);
static inline __m512i libdivide_s64_do_vector(__m512i numers, const struct libdivide_s64_t *denom);

static inline __m512i libdivide_u32_branchfree_do_vector(__m512i numers, const struct libdivide_u32_branchfree_t *denom);
static inline __m512i libdivide_s32_branchfree_do_vector(__m512i numers, const struct libdivide_s32_branchfree_t *denom);
static inline __m512i libdivide_u64_branchfree_do_vector(__m512i numers, const struct libdivide_u64_branchfree_t *denom);
static inline __m512i libdivide_s64_branchfree_do_vector(__m512i numers, const struct libdivide_s64_branchfree_t *denom);

//////// Internal Utility Functions

static inline __m512i libdivide_s64_signbits(__m512i v) {;
    return _mm512_srai_epi64(v, 63);
}

static inline __m512i libdivide_s64_shift_right_vector(__m512i v, int amt) {
    return _mm512_srai_epi64(v, amt);
}

// Here, b is assumed to contain one 32-bit value repeated.
static inline __m512i libdivide_mullhi_u32_vector(__m512i a, __m512i b) {
    __m512i hi_product_0Z2Z = _mm512_srli_epi64(_mm512_mul_epu32(a, b), 32);
    __m512i a1X3X = _mm512_srli_epi64(a, 32);
    __m512i mask = _mm512_set_epi32(-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0);
    __m512i hi_product_Z1Z3 = _mm512_and_si512(_mm512_mul_epu32(a1X3X, b), mask);
    return _mm512_or_si512(hi_product_0Z2Z, hi_product_Z1Z3);
}

// b is one 32-bit value repeated.
static inline __m512i libdivide_mullhi_s32_vector(__m512i a, __m512i b) {
    __m512i hi_product_0Z2Z = _mm512_srli_epi64(_mm512_mul_epi32(a, b), 32);
    __m512i a1X3X = _mm512_srli_epi64(a, 32);
    __m512i mask = _mm512_set_epi32(-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0);
    __m512i hi_product_Z1Z3 = _mm512_and_si512(_mm512_mul_epi32(a1X3X, b), mask);
    return _mm512_or_si512(hi_product_0Z2Z, hi_product_Z1Z3);
}

// Here, y is assumed to contain one 64-bit value repeated.
// https://stackoverflow.com/a/28827013
static inline __m512i libdivide_mullhi_u64_vector(__m512i x, __m512i y) {
    __m512i lomask = _mm512_set1_epi64(0xffffffff);
    __m512i xh = _mm512_shuffle_epi32(x, (_MM_PERM_ENUM) 0xB1);
    __m512i yh = _mm512_shuffle_epi32(y, (_MM_PERM_ENUM) 0xB1);
    __m512i w0 = _mm512_mul_epu32(x, y);
    __m512i w1 = _mm512_mul_epu32(x, yh);
    __m512i w2 = _mm512_mul_epu32(xh, y);
    __m512i w3 = _mm512_mul_epu32(xh, yh);
    __m512i w0h = _mm512_srli_epi64(w0, 32);
    __m512i s1 = _mm512_add_epi64(w1, w0h);
    __m512i s1l = _mm512_and_si512(s1, lomask);
    __m512i s1h = _mm512_srli_epi64(s1, 32);
    __m512i s2 = _mm512_add_epi64(w2, s1l);
    __m512i s2h = _mm512_srli_epi64(s2, 32);
    __m512i hi = _mm512_add_epi64(w3, s1h);
            hi = _mm512_add_epi64(hi, s2h);

    return hi;
}

// y is one 64-bit value repeated.
static inline __m512i libdivide_mullhi_s64_vector(__m512i x, __m512i y) {
    __m512i p = libdivide_mullhi_u64_vector(x, y);
    __m512i t1 = _mm512_and_si512(libdivide_s64_signbits(x), y);
    __m512i t2 = _mm512_and_si512(libdivide_s64_signbits(y), x);
    p = _mm512_sub_epi64(p, t1);
    p = _mm512_sub_epi64(p, t2);
    return p;
}

////////// UINT32

__m512i libdivide_u32_do_vector(__m512i numers, const struct libdivide_u32_t *denom) {
    uint8_t more = denom->more;
    if (!denom->magic) {
        return _mm512_srli_epi32(numers, more);
    }
    else {
        __m512i q = libdivide_mullhi_u32_vector(numers, _mm512_set1_epi32(denom->magic));
        if (more & LIBDIVIDE_ADD_MARKER) {
            // uint32_t t = ((numer - q) >> 1) + q;
            // return t >> denom->shift;
            uint32_t shift = more & LIBDIVIDE_32_SHIFT_MASK;
            __m512i t = _mm512_add_epi32(_mm512_srli_epi32(_mm512_sub_epi32(numers, q), 1), q);
            return _mm512_srli_epi32(t, shift);
        }
        else {
            return _mm512_srli_epi32(q, more);
        }
    }
}

__m512i libdivide_u32_branchfree_do_vector(__m512i numers, const struct libdivide_u32_branchfree_t *denom) {
    __m512i q = libdivide_mullhi_u32_vector(numers, _mm512_set1_epi32(denom->magic));
    __m512i t = _mm512_add_epi32(_mm512_srli_epi32(_mm512_sub_epi32(numers, q), 1), q);
    return _mm512_srli_epi32(t, denom->more);
}

////////// UINT64

__m512i libdivide_u64_do_vector(__m512i numers, const struct libdivide_u64_t *denom) {
    uint8_t more = denom->more;
    if (!denom->magic) {
        return _mm512_srli_epi64(numers, more);
    }
    else {
        __m512i q = libdivide_mullhi_u64_vector(numers, _mm512_set1_epi64(denom->magic));
        if (more & LIBDIVIDE_ADD_MARKER) {
            // uint32_t t = ((numer - q) >> 1) + q;
            // return t >> denom->shift;
            uint32_t shift = more & LIBDIVIDE_64_SHIFT_MASK;
            __m512i t = _mm512_add_epi64(_mm512_srli_epi64(_mm512_sub_epi64(numers, q), 1), q);
            return _mm512_srli_epi64(t, shift);
        }
        else {
            return _mm512_srli_epi64(q, more);
        }
    }
}

__m512i libdivide_u64_branchfree_do_vector(__m512i numers, const struct libdivide_u64_branchfree_t *denom) {
    __m512i q = libdivide_mullhi_u64_vector(numers, _mm512_set1_epi64(denom->magic));
    __m512i t = _mm512_add_epi64(_mm512_srli_epi64(_mm512_sub_epi64(numers, q), 1), q);
    return _mm512_srli_epi64(t, denom->more);
}

////////// SINT32

__m512i libdivide_s32_do_vector(__m512i numers, const struct libdivide_s32_t *denom) {
    uint8_t more = denom->more;
    if (!denom->magic) {
        uint32_t shift = more & LIBDIVIDE_32_SHIFT_MASK;
        uint32_t mask = (1U << shift) - 1;
        __m512i roundToZeroTweak = _mm512_set1_epi32(mask);
        // q = numer + ((numer >> 31) & roundToZeroTweak);
        __m512i q = _mm512_add_epi32(numers, _mm512_and_si512(_mm512_srai_epi32(numers, 31), roundToZeroTweak));
        q = _mm512_srai_epi32(q, shift);
        __m512i sign = _mm512_set1_epi32((int8_t)more >> 7);
        // q = (q ^ sign) - sign;
        q = _mm512_sub_epi32(_mm512_xor_si512(q, sign), sign);
        return q;
    }
    else {
        __m512i q = libdivide_mullhi_s32_vector(numers, _mm512_set1_epi32(denom->magic));
        if (more & LIBDIVIDE_ADD_MARKER) {
             // must be arithmetic shift
            __m512i sign = _mm512_set1_epi32((int8_t)more >> 7);
             // q += ((numer ^ sign) - sign);
            q = _mm512_add_epi32(q, _mm512_sub_epi32(_mm512_xor_si512(numers, sign), sign));
        }
        // q >>= shift
        q = _mm512_srai_epi32(q, more & LIBDIVIDE_32_SHIFT_MASK);
        q = _mm512_add_epi32(q, _mm512_srli_epi32(q, 31)); // q += (q < 0)
        return q;
    }
}

__m512i libdivide_s32_branchfree_do_vector(__m512i numers, const struct libdivide_s32_branchfree_t *denom) {
    int32_t magic = denom->magic;
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_32_SHIFT_MASK;
     // must be arithmetic shift
    __m512i sign = _mm512_set1_epi32((int8_t)more >> 7);
    __m512i q = libdivide_mullhi_s32_vector(numers, _mm512_set1_epi32(magic));
    q = _mm512_add_epi32(q, numers); // q += numers

    // If q is non-negative, we have nothing to do
    // If q is negative, we want to add either (2**shift)-1 if d is
    // a power of 2, or (2**shift) if it is not a power of 2
    uint32_t is_power_of_2 = (magic == 0);
    __m512i q_sign = _mm512_srai_epi32(q, 31); // q_sign = q >> 31
    __m512i mask = _mm512_set1_epi32((1U << shift) - is_power_of_2);
    q = _mm512_add_epi32(q, _mm512_and_si512(q_sign, mask)); // q = q + (q_sign & mask)
    q = _mm512_srai_epi32(q, shift); // q >>= shift
    q = _mm512_sub_epi32(_mm512_xor_si512(q, sign), sign); // q = (q ^ sign) - sign
    return q;
}

////////// SINT64

__m512i libdivide_s64_do_vector(__m512i numers, const struct libdivide_s64_t *denom) {
    uint8_t more = denom->more;
    int64_t magic = denom->magic;
    if (magic == 0) { // shift path
        uint32_t shift = more & LIBDIVIDE_64_SHIFT_MASK;
        uint64_t mask = (1ULL << shift) - 1;
        __m512i roundToZeroTweak = _mm512_set1_epi64(mask);
        // q = numer + ((numer >> 63) & roundToZeroTweak);
        __m512i q = _mm512_add_epi64(numers, _mm512_and_si512(libdivide_s64_signbits(numers), roundToZeroTweak));
        q = libdivide_s64_shift_right_vector(q, shift);
        __m512i sign = _mm512_set1_epi32((int8_t)more >> 7);
         // q = (q ^ sign) - sign;
        q = _mm512_sub_epi64(_mm512_xor_si512(q, sign), sign);
        return q;
    }
    else {
        __m512i q = libdivide_mullhi_s64_vector(numers, _mm512_set1_epi64(magic));
        if (more & LIBDIVIDE_ADD_MARKER) {
            // must be arithmetic shift
            __m512i sign = _mm512_set1_epi32((int8_t)more >> 7);
            // q += ((numer ^ sign) - sign);
            q = _mm512_add_epi64(q, _mm512_sub_epi64(_mm512_xor_si512(numers, sign), sign));
        }
        // q >>= denom->mult_path.shift
        q = libdivide_s64_shift_right_vector(q, more & LIBDIVIDE_64_SHIFT_MASK);
        q = _mm512_add_epi64(q, _mm512_srli_epi64(q, 63)); // q += (q < 0)
        return q;
    }
}

__m512i libdivide_s64_branchfree_do_vector(__m512i numers, const struct libdivide_s64_branchfree_t *denom) {
    int64_t magic = denom->magic;
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_64_SHIFT_MASK;
    // must be arithmetic shift
    __m512i sign = _mm512_set1_epi32((int8_t)more >> 7);

     // libdivide_mullhi_s64(numers, magic);
    __m512i q = libdivide_mullhi_s64_vector(numers, _mm512_set1_epi64(magic));
    q = _mm512_add_epi64(q, numers); // q += numers

    // If q is non-negative, we have nothing to do.
    // If q is negative, we want to add either (2**shift)-1 if d is
    // a power of 2, or (2**shift) if it is not a power of 2.
    uint32_t is_power_of_2 = (magic == 0);
    __m512i q_sign = libdivide_s64_signbits(q); // q_sign = q >> 63
    __m512i mask = _mm512_set1_epi64((1ULL << shift) - is_power_of_2);
    q = _mm512_add_epi64(q, _mm512_and_si512(q_sign, mask)); // q = q + (q_sign & mask)
    q = libdivide_s64_shift_right_vector(q, shift); // q >>= shift
    q = _mm512_sub_epi64(_mm512_xor_si512(q, sign), sign); // q = (q ^ sign) - sign
    return q;
}

#elif defined(LIBDIVIDE_AVX2)

static inline __m256i libdivide_u32_do_vector(__m256i numers, const struct libdivide_u32_t *denom);
static inline __m256i libdivide_s32_do_vector(__m256i numers, const struct libdivide_s32_t *denom);
static inline __m256i libdivide_u64_do_vector(__m256i numers, const struct libdivide_u64_t *denom);
static inline __m256i libdivide_s64_do_vector(__m256i numers, const struct libdivide_s64_t *denom);

static inline __m256i libdivide_u32_branchfree_do_vector(__m256i numers, const struct libdivide_u32_branchfree_t *denom);
static inline __m256i libdivide_s32_branchfree_do_vector(__m256i numers, const struct libdivide_s32_branchfree_t *denom);
static inline __m256i libdivide_u64_branchfree_do_vector(__m256i numers, const struct libdivide_u64_branchfree_t *denom);
static inline __m256i libdivide_s64_branchfree_do_vector(__m256i numers, const struct libdivide_s64_branchfree_t *denom);

//////// Internal Utility Functions

// Implementation of _mm256_srai_epi64(v, 63) (from AVX512).
static inline __m256i libdivide_s64_signbits(__m256i v) {
    __m256i hiBitsDuped = _mm256_shuffle_epi32(v, _MM_SHUFFLE(3, 3, 1, 1));
    __m256i signBits = _mm256_srai_epi32(hiBitsDuped, 31);
    return signBits;
}

// Implementation of _mm256_srai_epi64 (from AVX512).
static inline __m256i libdivide_s64_shift_right_vector(__m256i v, int amt) {
    const int b = 64 - amt;
    __m256i m = _mm256_set1_epi64x(1ULL << (b - 1));
    __m256i x = _mm256_srli_epi64(v, amt);
    __m256i result = _mm256_sub_epi64(_mm256_xor_si256(x, m), m);
    return result;
}

// Here, b is assumed to contain one 32-bit value repeated.
static inline __m256i libdivide_mullhi_u32_vector(__m256i a, __m256i b) {
    __m256i hi_product_0Z2Z = _mm256_srli_epi64(_mm256_mul_epu32(a, b), 32);
    __m256i a1X3X = _mm256_srli_epi64(a, 32);
    __m256i mask = _mm256_set_epi32(-1, 0, -1, 0, -1, 0, -1, 0);
    __m256i hi_product_Z1Z3 = _mm256_and_si256(_mm256_mul_epu32(a1X3X, b), mask);
    return _mm256_or_si256(hi_product_0Z2Z, hi_product_Z1Z3);
}

// b is one 32-bit value repeated.
static inline __m256i libdivide_mullhi_s32_vector(__m256i a, __m256i b) {
    __m256i hi_product_0Z2Z = _mm256_srli_epi64(_mm256_mul_epi32(a, b), 32);
    __m256i a1X3X = _mm256_srli_epi64(a, 32);
    __m256i mask = _mm256_set_epi32(-1, 0, -1, 0, -1, 0, -1, 0);
    __m256i hi_product_Z1Z3 = _mm256_and_si256(_mm256_mul_epi32(a1X3X, b), mask);
    return _mm256_or_si256(hi_product_0Z2Z, hi_product_Z1Z3);
}

// Here, y is assumed to contain one 64-bit value repeated.
// https://stackoverflow.com/a/28827013
static inline __m256i libdivide_mullhi_u64_vector(__m256i x, __m256i y) {
    __m256i lomask = _mm256_set1_epi64x(0xffffffff);
    __m256i xh = _mm256_shuffle_epi32(x, 0xB1);        // x0l, x0h, x1l, x1h
    __m256i yh = _mm256_shuffle_epi32(y, 0xB1);        // y0l, y0h, y1l, y1h
    __m256i w0 = _mm256_mul_epu32(x, y);               // x0l*y0l, x1l*y1l
    __m256i w1 = _mm256_mul_epu32(x, yh);              // x0l*y0h, x1l*y1h
    __m256i w2 = _mm256_mul_epu32(xh, y);              // x0h*y0l, x1h*y0l
    __m256i w3 = _mm256_mul_epu32(xh, yh);             // x0h*y0h, x1h*y1h
    __m256i w0h = _mm256_srli_epi64(w0, 32);
    __m256i s1 = _mm256_add_epi64(w1, w0h);
    __m256i s1l = _mm256_and_si256(s1, lomask);
    __m256i s1h = _mm256_srli_epi64(s1, 32);
    __m256i s2 = _mm256_add_epi64(w2, s1l);
    __m256i s2h = _mm256_srli_epi64(s2, 32);
    __m256i hi = _mm256_add_epi64(w3, s1h);
            hi = _mm256_add_epi64(hi, s2h);

    return hi;
}

// y is one 64-bit value repeated.
static inline __m256i libdivide_mullhi_s64_vector(__m256i x, __m256i y) {
    __m256i p = libdivide_mullhi_u64_vector(x, y);
    __m256i t1 = _mm256_and_si256(libdivide_s64_signbits(x), y);
    __m256i t2 = _mm256_and_si256(libdivide_s64_signbits(y), x);
    p = _mm256_sub_epi64(p, t1);
    p = _mm256_sub_epi64(p, t2);
    return p;
}

////////// UINT32

__m256i libdivide_u32_do_vector(__m256i numers, const struct libdivide_u32_t *denom) {
    uint8_t more = denom->more;
    if (!denom->magic) {
        return _mm256_srli_epi32(numers, more);
    }
    else {
        __m256i q = libdivide_mullhi_u32_vector(numers, _mm256_set1_epi32(denom->magic));
        if (more & LIBDIVIDE_ADD_MARKER) {
            // uint32_t t = ((numer - q) >> 1) + q;
            // return t >> denom->shift;
            uint32_t shift = more & LIBDIVIDE_32_SHIFT_MASK;
            __m256i t = _mm256_add_epi32(_mm256_srli_epi32(_mm256_sub_epi32(numers, q), 1), q);
            return _mm256_srli_epi32(t, shift);
        }
        else {
            return _mm256_srli_epi32(q, more);
        }
    }
}

__m256i libdivide_u32_branchfree_do_vector(__m256i numers, const struct libdivide_u32_branchfree_t *denom) {
    __m256i q = libdivide_mullhi_u32_vector(numers, _mm256_set1_epi32(denom->magic));
    __m256i t = _mm256_add_epi32(_mm256_srli_epi32(_mm256_sub_epi32(numers, q), 1), q);
    return _mm256_srli_epi32(t, denom->more);
}

////////// UINT64

__m256i libdivide_u64_do_vector(__m256i numers, const struct libdivide_u64_t *denom) {
    uint8_t more = denom->more;
    if (!denom->magic) {
        return _mm256_srli_epi64(numers, more);
    }
    else {
        __m256i q = libdivide_mullhi_u64_vector(numers, _mm256_set1_epi64x(denom->magic));
        if (more & LIBDIVIDE_ADD_MARKER) {
            // uint32_t t = ((numer - q) >> 1) + q;
            // return t >> denom->shift;
            uint32_t shift = more & LIBDIVIDE_64_SHIFT_MASK;
            __m256i t = _mm256_add_epi64(_mm256_srli_epi64(_mm256_sub_epi64(numers, q), 1), q);
            return _mm256_srli_epi64(t, shift);
        }
        else {
            return _mm256_srli_epi64(q, more);
        }
    }
}

__m256i libdivide_u64_branchfree_do_vector(__m256i numers, const struct libdivide_u64_branchfree_t *denom) {
    __m256i q = libdivide_mullhi_u64_vector(numers, _mm256_set1_epi64x(denom->magic));
    __m256i t = _mm256_add_epi64(_mm256_srli_epi64(_mm256_sub_epi64(numers, q), 1), q);
    return _mm256_srli_epi64(t, denom->more);
}

////////// SINT32

__m256i libdivide_s32_do_vector(__m256i numers, const struct libdivide_s32_t *denom) {
    uint8_t more = denom->more;
    if (!denom->magic) {
        uint32_t shift = more & LIBDIVIDE_32_SHIFT_MASK;
        uint32_t mask = (1U << shift) - 1;
        __m256i roundToZeroTweak = _mm256_set1_epi32(mask);
        // q = numer + ((numer >> 31) & roundToZeroTweak);
        __m256i q = _mm256_add_epi32(numers, _mm256_and_si256(_mm256_srai_epi32(numers, 31), roundToZeroTweak));
        q = _mm256_srai_epi32(q, shift);
        __m256i sign = _mm256_set1_epi32((int8_t)more >> 7);
        // q = (q ^ sign) - sign;
        q = _mm256_sub_epi32(_mm256_xor_si256(q, sign), sign);
        return q;
    }
    else {
        __m256i q = libdivide_mullhi_s32_vector(numers, _mm256_set1_epi32(denom->magic));
        if (more & LIBDIVIDE_ADD_MARKER) {
             // must be arithmetic shift
            __m256i sign = _mm256_set1_epi32((int8_t)more >> 7);
             // q += ((numer ^ sign) - sign);
            q = _mm256_add_epi32(q, _mm256_sub_epi32(_mm256_xor_si256(numers, sign), sign));
        }
        // q >>= shift
        q = _mm256_srai_epi32(q, more & LIBDIVIDE_32_SHIFT_MASK);
        q = _mm256_add_epi32(q, _mm256_srli_epi32(q, 31)); // q += (q < 0)
        return q;
    }
}

__m256i libdivide_s32_branchfree_do_vector(__m256i numers, const struct libdivide_s32_branchfree_t *denom) {
    int32_t magic = denom->magic;
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_32_SHIFT_MASK;
     // must be arithmetic shift
    __m256i sign = _mm256_set1_epi32((int8_t)more >> 7);
    __m256i q = libdivide_mullhi_s32_vector(numers, _mm256_set1_epi32(magic));
    q = _mm256_add_epi32(q, numers); // q += numers

    // If q is non-negative, we have nothing to do
    // If q is negative, we want to add either (2**shift)-1 if d is
    // a power of 2, or (2**shift) if it is not a power of 2
    uint32_t is_power_of_2 = (magic == 0);
    __m256i q_sign = _mm256_srai_epi32(q, 31); // q_sign = q >> 31
    __m256i mask = _mm256_set1_epi32((1U << shift) - is_power_of_2);
    q = _mm256_add_epi32(q, _mm256_and_si256(q_sign, mask)); // q = q + (q_sign & mask)
    q = _mm256_srai_epi32(q, shift); // q >>= shift
    q = _mm256_sub_epi32(_mm256_xor_si256(q, sign), sign); // q = (q ^ sign) - sign
    return q;
}

////////// SINT64

__m256i libdivide_s64_do_vector(__m256i numers, const struct libdivide_s64_t *denom) {
    uint8_t more = denom->more;
    int64_t magic = denom->magic;
    if (magic == 0) { // shift path
        uint32_t shift = more & LIBDIVIDE_64_SHIFT_MASK;
        uint64_t mask = (1ULL << shift) - 1;
        __m256i roundToZeroTweak = _mm256_set1_epi64x(mask);
        // q = numer + ((numer >> 63) & roundToZeroTweak);
        __m256i q = _mm256_add_epi64(numers, _mm256_and_si256(libdivide_s64_signbits(numers), roundToZeroTweak));
        q = libdivide_s64_shift_right_vector(q, shift);
        __m256i sign = _mm256_set1_epi32((int8_t)more >> 7);
         // q = (q ^ sign) - sign;
        q = _mm256_sub_epi64(_mm256_xor_si256(q, sign), sign);
        return q;
    }
    else {
        __m256i q = libdivide_mullhi_s64_vector(numers, _mm256_set1_epi64x(magic));
        if (more & LIBDIVIDE_ADD_MARKER) {
            // must be arithmetic shift
            __m256i sign = _mm256_set1_epi32((int8_t)more >> 7);
            // q += ((numer ^ sign) - sign);
            q = _mm256_add_epi64(q, _mm256_sub_epi64(_mm256_xor_si256(numers, sign), sign));
        }
        // q >>= denom->mult_path.shift
        q = libdivide_s64_shift_right_vector(q, more & LIBDIVIDE_64_SHIFT_MASK);
        q = _mm256_add_epi64(q, _mm256_srli_epi64(q, 63)); // q += (q < 0)
        return q;
    }
}

__m256i libdivide_s64_branchfree_do_vector(__m256i numers, const struct libdivide_s64_branchfree_t *denom) {
    int64_t magic = denom->magic;
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_64_SHIFT_MASK;
    // must be arithmetic shift
    __m256i sign = _mm256_set1_epi32((int8_t)more >> 7);

     // libdivide_mullhi_s64(numers, magic);
    __m256i q = libdivide_mullhi_s64_vector(numers, _mm256_set1_epi64x(magic));
    q = _mm256_add_epi64(q, numers); // q += numers

    // If q is non-negative, we have nothing to do.
    // If q is negative, we want to add either (2**shift)-1 if d is
    // a power of 2, or (2**shift) if it is not a power of 2.
    uint32_t is_power_of_2 = (magic == 0);
    __m256i q_sign = libdivide_s64_signbits(q); // q_sign = q >> 63
    __m256i mask = _mm256_set1_epi64x((1ULL << shift) - is_power_of_2);
    q = _mm256_add_epi64(q, _mm256_and_si256(q_sign, mask)); // q = q + (q_sign & mask)
    q = libdivide_s64_shift_right_vector(q, shift); // q >>= shift
    q = _mm256_sub_epi64(_mm256_xor_si256(q, sign), sign); // q = (q ^ sign) - sign
    return q;
}

#elif defined(LIBDIVIDE_SSE2)

static inline __m128i libdivide_u32_do_vector(__m128i numers, const struct libdivide_u32_t *denom);
static inline __m128i libdivide_s32_do_vector(__m128i numers, const struct libdivide_s32_t *denom);
static inline __m128i libdivide_u64_do_vector(__m128i numers, const struct libdivide_u64_t *denom);
static inline __m128i libdivide_s64_do_vector(__m128i numers, const struct libdivide_s64_t *denom);

static inline __m128i libdivide_u32_branchfree_do_vector(__m128i numers, const struct libdivide_u32_branchfree_t *denom);
static inline __m128i libdivide_s32_branchfree_do_vector(__m128i numers, const struct libdivide_s32_branchfree_t *denom);
static inline __m128i libdivide_u64_branchfree_do_vector(__m128i numers, const struct libdivide_u64_branchfree_t *denom);
static inline __m128i libdivide_s64_branchfree_do_vector(__m128i numers, const struct libdivide_s64_branchfree_t *denom);

//////// Internal Utility Functions

// Implementation of _mm_srai_epi64(v, 63) (from AVX512).
static inline __m128i libdivide_s64_signbits(__m128i v) {
    __m128i hiBitsDuped = _mm_shuffle_epi32(v, _MM_SHUFFLE(3, 3, 1, 1));
    __m128i signBits = _mm_srai_epi32(hiBitsDuped, 31);
    return signBits;
}

// Implementation of _mm_srai_epi64 (from AVX512).
static inline __m128i libdivide_s64_shift_right_vector(__m128i v, int amt) {
    const int b = 64 - amt;
    __m128i m = _mm_set1_epi64x(1ULL << (b - 1));
    __m128i x = _mm_srli_epi64(v, amt);
    __m128i result = _mm_sub_epi64(_mm_xor_si128(x, m), m);
    return result;
}

// Here, b is assumed to contain one 32-bit value repeated.
static inline __m128i libdivide_mullhi_u32_vector(__m128i a, __m128i b) {
    __m128i hi_product_0Z2Z = _mm_srli_epi64(_mm_mul_epu32(a, b), 32);
    __m128i a1X3X = _mm_srli_epi64(a, 32);
    __m128i mask = _mm_set_epi32(-1, 0, -1, 0);
    __m128i hi_product_Z1Z3 = _mm_and_si128(_mm_mul_epu32(a1X3X, b), mask);
    return _mm_or_si128(hi_product_0Z2Z, hi_product_Z1Z3);
}

// SSE2 does not have a signed multiplication instruction, but we can convert
// unsigned to signed pretty efficiently. Again, b is just a 32 bit value
// repeated four times.
static inline __m128i libdivide_mullhi_s32_vector(__m128i a, __m128i b) {
    __m128i p = libdivide_mullhi_u32_vector(a, b);
    // t1 = (a >> 31) & y, arithmetic shift
    __m128i t1 = _mm_and_si128(_mm_srai_epi32(a, 31), b);
    __m128i t2 = _mm_and_si128(_mm_srai_epi32(b, 31), a);
    p = _mm_sub_epi32(p, t1);
    p = _mm_sub_epi32(p, t2);
    return p;
}

// Here, y is assumed to contain one 64-bit value repeated.
// https://stackoverflow.com/a/28827013
static inline __m128i libdivide_mullhi_u64_vector(__m128i x, __m128i y) {
    __m128i lomask = _mm_set1_epi64x(0xffffffff);
    __m128i xh = _mm_shuffle_epi32(x, 0xB1);        // x0l, x0h, x1l, x1h
    __m128i yh = _mm_shuffle_epi32(y, 0xB1);        // y0l, y0h, y1l, y1h
    __m128i w0 = _mm_mul_epu32(x, y);               // x0l*y0l, x1l*y1l
    __m128i w1 = _mm_mul_epu32(x, yh);              // x0l*y0h, x1l*y1h
    __m128i w2 = _mm_mul_epu32(xh, y);              // x0h*y0l, x1h*y0l
    __m128i w3 = _mm_mul_epu32(xh, yh);             // x0h*y0h, x1h*y1h
    __m128i w0h = _mm_srli_epi64(w0, 32);
    __m128i s1 = _mm_add_epi64(w1, w0h);
    __m128i s1l = _mm_and_si128(s1, lomask);
    __m128i s1h = _mm_srli_epi64(s1, 32);
    __m128i s2 = _mm_add_epi64(w2, s1l);
    __m128i s2h = _mm_srli_epi64(s2, 32);
    __m128i hi = _mm_add_epi64(w3, s1h);
            hi = _mm_add_epi64(hi, s2h);

    return hi;
}

// y is one 64-bit value repeated.
static inline __m128i libdivide_mullhi_s64_vector(__m128i x, __m128i y) {
    __m128i p = libdivide_mullhi_u64_vector(x, y);
    __m128i t1 = _mm_and_si128(libdivide_s64_signbits(x), y);
    __m128i t2 = _mm_and_si128(libdivide_s64_signbits(y), x);
    p = _mm_sub_epi64(p, t1);
    p = _mm_sub_epi64(p, t2);
    return p;
}

////////// UINT32

__m128i libdivide_u32_do_vector(__m128i numers, const struct libdivide_u32_t *denom) {
    uint8_t more = denom->more;
    if (!denom->magic) {
        return _mm_srli_epi32(numers, more);
    }
    else {
        __m128i q = libdivide_mullhi_u32_vector(numers, _mm_set1_epi32(denom->magic));
        if (more & LIBDIVIDE_ADD_MARKER) {
            // uint32_t t = ((numer - q) >> 1) + q;
            // return t >> denom->shift;
            uint32_t shift = more & LIBDIVIDE_32_SHIFT_MASK;
            __m128i t = _mm_add_epi32(_mm_srli_epi32(_mm_sub_epi32(numers, q), 1), q);
            return _mm_srli_epi32(t, shift);
        }
        else {
            return _mm_srli_epi32(q, more);
        }
    }
}

__m128i libdivide_u32_branchfree_do_vector(__m128i numers, const struct libdivide_u32_branchfree_t *denom) {
    __m128i q = libdivide_mullhi_u32_vector(numers, _mm_set1_epi32(denom->magic));
    __m128i t = _mm_add_epi32(_mm_srli_epi32(_mm_sub_epi32(numers, q), 1), q);
    return _mm_srli_epi32(t, denom->more);
}

////////// UINT64

__m128i libdivide_u64_do_vector(__m128i numers, const struct libdivide_u64_t *denom) {
    uint8_t more = denom->more;
    if (!denom->magic) {
        return _mm_srli_epi64(numers, more);
    }
    else {
        __m128i q = libdivide_mullhi_u64_vector(numers, _mm_set1_epi64x(denom->magic));
        if (more & LIBDIVIDE_ADD_MARKER) {
            // uint32_t t = ((numer - q) >> 1) + q;
            // return t >> denom->shift;
            uint32_t shift = more & LIBDIVIDE_64_SHIFT_MASK;
            __m128i t = _mm_add_epi64(_mm_srli_epi64(_mm_sub_epi64(numers, q), 1), q);
            return _mm_srli_epi64(t, shift);
        }
        else {
            return _mm_srli_epi64(q, more);
        }
    }
}

__m128i libdivide_u64_branchfree_do_vector(__m128i numers, const struct libdivide_u64_branchfree_t *denom) {
    __m128i q = libdivide_mullhi_u64_vector(numers, _mm_set1_epi64x(denom->magic));
    __m128i t = _mm_add_epi64(_mm_srli_epi64(_mm_sub_epi64(numers, q), 1), q);
    return _mm_srli_epi64(t, denom->more);
}

////////// SINT32

__m128i libdivide_s32_do_vector(__m128i numers, const struct libdivide_s32_t *denom) {
    uint8_t more = denom->more;
    if (!denom->magic) {
        uint32_t shift = more & LIBDIVIDE_32_SHIFT_MASK;
        uint32_t mask = (1U << shift) - 1;
        __m128i roundToZeroTweak = _mm_set1_epi32(mask);
        // q = numer + ((numer >> 31) & roundToZeroTweak);
        __m128i q = _mm_add_epi32(numers, _mm_and_si128(_mm_srai_epi32(numers, 31), roundToZeroTweak));
        q = _mm_srai_epi32(q, shift);
        __m128i sign = _mm_set1_epi32((int8_t)more >> 7);
        // q = (q ^ sign) - sign;
        q = _mm_sub_epi32(_mm_xor_si128(q, sign), sign);
        return q;
    }
    else {
        __m128i q = libdivide_mullhi_s32_vector(numers, _mm_set1_epi32(denom->magic));
        if (more & LIBDIVIDE_ADD_MARKER) {
             // must be arithmetic shift
            __m128i sign = _mm_set1_epi32((int8_t)more >> 7);
             // q += ((numer ^ sign) - sign);
            q = _mm_add_epi32(q, _mm_sub_epi32(_mm_xor_si128(numers, sign), sign));
        }
        // q >>= shift
        q = _mm_srai_epi32(q, more & LIBDIVIDE_32_SHIFT_MASK);
        q = _mm_add_epi32(q, _mm_srli_epi32(q, 31)); // q += (q < 0)
        return q;
    }
}

__m128i libdivide_s32_branchfree_do_vector(__m128i numers, const struct libdivide_s32_branchfree_t *denom) {
    int32_t magic = denom->magic;
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_32_SHIFT_MASK;
     // must be arithmetic shift
    __m128i sign = _mm_set1_epi32((int8_t)more >> 7);
    __m128i q = libdivide_mullhi_s32_vector(numers, _mm_set1_epi32(magic));
    q = _mm_add_epi32(q, numers); // q += numers

    // If q is non-negative, we have nothing to do
    // If q is negative, we want to add either (2**shift)-1 if d is
    // a power of 2, or (2**shift) if it is not a power of 2
    uint32_t is_power_of_2 = (magic == 0);
    __m128i q_sign = _mm_srai_epi32(q, 31); // q_sign = q >> 31
    __m128i mask = _mm_set1_epi32((1U << shift) - is_power_of_2);
    q = _mm_add_epi32(q, _mm_and_si128(q_sign, mask)); // q = q + (q_sign & mask)
    q = _mm_srai_epi32(q, shift); // q >>= shift
    q = _mm_sub_epi32(_mm_xor_si128(q, sign), sign); // q = (q ^ sign) - sign
    return q;
}

////////// SINT64

__m128i libdivide_s64_do_vector(__m128i numers, const struct libdivide_s64_t *denom) {
    uint8_t more = denom->more;
    int64_t magic = denom->magic;
    if (magic == 0) { // shift path
        uint32_t shift = more & LIBDIVIDE_64_SHIFT_MASK;
        uint64_t mask = (1ULL << shift) - 1;
        __m128i roundToZeroTweak = _mm_set1_epi64x(mask);
        // q = numer + ((numer >> 63) & roundToZeroTweak);
        __m128i q = _mm_add_epi64(numers, _mm_and_si128(libdivide_s64_signbits(numers), roundToZeroTweak));
        q = libdivide_s64_shift_right_vector(q, shift);
        __m128i sign = _mm_set1_epi32((int8_t)more >> 7);
         // q = (q ^ sign) - sign;
        q = _mm_sub_epi64(_mm_xor_si128(q, sign), sign);
        return q;
    }
    else {
        __m128i q = libdivide_mullhi_s64_vector(numers, _mm_set1_epi64x(magic));
        if (more & LIBDIVIDE_ADD_MARKER) {
            // must be arithmetic shift
            __m128i sign = _mm_set1_epi32((int8_t)more >> 7);
            // q += ((numer ^ sign) - sign);
            q = _mm_add_epi64(q, _mm_sub_epi64(_mm_xor_si128(numers, sign), sign));
        }
        // q >>= denom->mult_path.shift
        q = libdivide_s64_shift_right_vector(q, more & LIBDIVIDE_64_SHIFT_MASK);
        q = _mm_add_epi64(q, _mm_srli_epi64(q, 63)); // q += (q < 0)
        return q;
    }
}

__m128i libdivide_s64_branchfree_do_vector(__m128i numers, const struct libdivide_s64_branchfree_t *denom) {
    int64_t magic = denom->magic;
    uint8_t more = denom->more;
    uint8_t shift = more & LIBDIVIDE_64_SHIFT_MASK;
    // must be arithmetic shift
    __m128i sign = _mm_set1_epi32((int8_t)more >> 7);

     // libdivide_mullhi_s64(numers, magic);
    __m128i q = libdivide_mullhi_s64_vector(numers, _mm_set1_epi64x(magic));
    q = _mm_add_epi64(q, numers); // q += numers

    // If q is non-negative, we have nothing to do.
    // If q is negative, we want to add either (2**shift)-1 if d is
    // a power of 2, or (2**shift) if it is not a power of 2.
    uint32_t is_power_of_2 = (magic == 0);
    __m128i q_sign = libdivide_s64_signbits(q); // q_sign = q >> 63
    __m128i mask = _mm_set1_epi64x((1ULL << shift) - is_power_of_2);
    q = _mm_add_epi64(q, _mm_and_si128(q_sign, mask)); // q = q + (q_sign & mask)
    q = libdivide_s64_shift_right_vector(q, shift); // q >>= shift
    q = _mm_sub_epi64(_mm_xor_si128(q, sign), sign); // q = (q ^ sign) - sign
    return q;
}

#endif

/////////// C++ stuff

#ifdef __cplusplus

// The C++ divider class is templated on both an integer type
// (like uint64_t) and an algorithm type.
// * BRANCHFULL is the default algorithm type.
// * BRANCHFREE is the branchfree algorithm type.
enum {
    BRANCHFULL,
    BRANCHFREE
};

#if defined(LIBDIVIDE_AVX512)
    #define LIBDIVIDE_VECTOR_TYPE __m512i
#elif defined(LIBDIVIDE_AVX2)
    #define LIBDIVIDE_VECTOR_TYPE __m256i
#elif defined(LIBDIVIDE_SSE2)
    #define LIBDIVIDE_VECTOR_TYPE __m128i
#endif

#if !defined(LIBDIVIDE_VECTOR_TYPE)
    #define LIBDIVIDE_DIVIDE_VECTOR(ALGO)
#else
    #define LIBDIVIDE_DIVIDE_VECTOR(ALGO) \
        LIBDIVIDE_VECTOR_TYPE divide(LIBDIVIDE_VECTOR_TYPE n) const { \
            return libdivide_##ALGO##_do_vector(n, &denom); \
        }
#endif

// The DISPATCHER_GEN() macro generates C++ methods (for the given integer
// and algorithm types) that redirect to libdivide's C API.
#define DISPATCHER_GEN(T, ALGO) \
    libdivide_##ALGO##_t denom; \
    dispatcher() { } \
    dispatcher(T d) \
        : denom(libdivide_##ALGO##_gen(d)) \
    { } \
    T divide(T n) const { \
        return libdivide_##ALGO##_do(n, &denom); \
    } \
    LIBDIVIDE_DIVIDE_VECTOR(ALGO) \
    T recover() const { \
        return libdivide_##ALGO##_recover(&denom); \
    }

// The dispatcher selects a specific division algorithm for a given
// type and ALGO using partial template specialization.
template<bool IS_INTEGRAL, bool IS_SIGNED, int SIZEOF, int ALGO> struct dispatcher { };

template<> struct dispatcher<true, true, sizeof(int32_t), BRANCHFULL> { DISPATCHER_GEN(int32_t, s32) };
template<> struct dispatcher<true, true, sizeof(int32_t), BRANCHFREE> { DISPATCHER_GEN(int32_t, s32_branchfree) };
template<> struct dispatcher<true, false, sizeof(uint32_t), BRANCHFULL> { DISPATCHER_GEN(uint32_t, u32) };
template<> struct dispatcher<true, false, sizeof(uint32_t), BRANCHFREE> { DISPATCHER_GEN(uint32_t, u32_branchfree) };
template<> struct dispatcher<true, true, sizeof(int64_t), BRANCHFULL> { DISPATCHER_GEN(int64_t, s64) };
template<> struct dispatcher<true, true, sizeof(int64_t), BRANCHFREE> { DISPATCHER_GEN(int64_t, s64_branchfree) };
template<> struct dispatcher<true, false, sizeof(uint64_t), BRANCHFULL> { DISPATCHER_GEN(uint64_t, u64) };
template<> struct dispatcher<true, false, sizeof(uint64_t), BRANCHFREE> { DISPATCHER_GEN(uint64_t, u64_branchfree) };

// This is the main divider class for use by the user (C++ API).
// The actual division algorithm is selected using the dispatcher struct
// based on the integer and algorithm template parameters.
template<typename T, int ALGO = BRANCHFULL>
class divider {
public:
    // We leave the default constructor empty so that creating
    // an array of dividers and then initializing them
    // later doesn't slow us down.
    divider() { }

    // Constructor that takes the divisor as a parameter
    divider(T d) : div(d) { }

    // Divides n by the divisor
    T divide(T n) const {
        return div.divide(n);
    }

    // Recovers the divisor, returns the value that was
    // used to initialize this divider object.
    T recover() const {
        return div.recover();
    }

    bool operator==(const divider<T, ALGO>& other) const {
        return div.denom.magic == other.denom.magic &&
               div.denom.more == other.denom.more;
    }

    bool operator!=(const divider<T, ALGO>& other) const {
        return !(*this == other);
    }

#if defined(LIBDIVIDE_VECTOR_TYPE)
    // Treats the vector as packed integer values with the same type as
    // the divider (e.g. s32, u32, s64, u64) and divides each of
    // them by the divider, returning the packed quotients.
    LIBDIVIDE_VECTOR_TYPE divide(LIBDIVIDE_VECTOR_TYPE n) const {
        return div.divide(n);
    }
#endif

private:
    // Storage for the actual divisor
    dispatcher<std::is_integral<T>::value,
               std::is_signed<T>::value, sizeof(T), ALGO> div;
};

// Overload of operator / for scalar division
template<typename T, int ALGO>
T operator/(T n, const divider<T, ALGO>& div) {
    return div.divide(n);
}

// Overload of operator /= for scalar division
template<typename T, int ALGO>
T& operator/=(T& n, const divider<T, ALGO>& div) {
    n = div.divide(n);
    return n;
}

#if defined(LIBDIVIDE_VECTOR_TYPE)
    // Overload of operator / for vector division
    template<typename T, int ALGO>
    LIBDIVIDE_VECTOR_TYPE operator/(LIBDIVIDE_VECTOR_TYPE n, const divider<T, ALGO>& div) {
        return div.divide(n);
    }
    // Overload of operator /= for vector division
    template<typename T, int ALGO>
    LIBDIVIDE_VECTOR_TYPE& operator/=(LIBDIVIDE_VECTOR_TYPE& n, const divider<T, ALGO>& div) {
        n = div.divide(n);
        return n;
    }
#endif

// libdivdie::branchfree_divider<T>
template <typename T>
using branchfree_divider = divider<T, BRANCHFREE>;

}  // namespace libdivide

#endif  // __cplusplus

#endif  // NUMPY_CORE_INCLUDE_NUMPY_LIBDIVIDE_LIBDIVIDE_H_
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/__multiarray_api.h

```plaintext

#if defined(_MULTIARRAYMODULE) || defined(WITH_CPYCHECKER_STEALS_REFERENCE_TO_ARG_ATTRIBUTE)

typedef struct {
        PyObject_HEAD
        npy_bool obval;
} PyBoolScalarObject;

extern NPY_NO_EXPORT PyTypeObject PyArrayMapIter_Type;
extern NPY_NO_EXPORT PyTypeObject PyArrayNeighborhoodIter_Type;
extern NPY_NO_EXPORT PyBoolScalarObject _PyArrayScalar_BoolValues[2];

NPY_NO_EXPORT  unsigned int PyArray_GetNDArrayCVersion \
       (void);
extern NPY_NO_EXPORT PyTypeObject PyBigArray_Type;

extern NPY_NO_EXPORT PyTypeObject PyArray_Type;

extern NPY_NO_EXPORT PyArray_DTypeMeta PyArrayDescr_TypeFull;
#define PyArrayDescr_Type (*(PyTypeObject *)(&PyArrayDescr_TypeFull))

extern NPY_NO_EXPORT PyTypeObject PyArrayFlags_Type;

extern NPY_NO_EXPORT PyTypeObject PyArrayIter_Type;

extern NPY_NO_EXPORT PyTypeObject PyArrayMultiIter_Type;

extern NPY_NO_EXPORT int NPY_NUMUSERTYPES;

extern NPY_NO_EXPORT PyTypeObject PyBoolArrType_Type;

extern NPY_NO_EXPORT PyBoolScalarObject _PyArrayScalar_BoolValues[2];

extern NPY_NO_EXPORT PyTypeObject PyGenericArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyNumberArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyIntegerArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PySignedIntegerArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyUnsignedIntegerArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyInexactArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyFloatingArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyComplexFloatingArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyFlexibleArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyCharacterArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyByteArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyShortArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyIntArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyLongArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyLongLongArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyUByteArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyUShortArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyUIntArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyULongArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyULongLongArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyFloatArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyDoubleArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyLongDoubleArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyCFloatArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyCDoubleArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyCLongDoubleArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyObjectArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyStringArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyUnicodeArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyVoidArrType_Type;

NPY_NO_EXPORT  int PyArray_SetNumericOps \
       (PyObject *);
NPY_NO_EXPORT  PyObject * PyArray_GetNumericOps \
       (void);
NPY_NO_EXPORT  int PyArray_INCREF \
       (PyArrayObject *);
NPY_NO_EXPORT  int PyArray_XDECREF \
       (PyArrayObject *);
NPY_NO_EXPORT  void PyArray_SetStringFunction \
       (PyObject *, int);
NPY_NO_EXPORT  PyArray_Descr * PyArray_DescrFromType \
       (int);
NPY_NO_EXPORT  PyObject * PyArray_TypeObjectFromType \
       (int);
NPY_NO_EXPORT  char * PyArray_Zero \
       (PyArrayObject *);
NPY_NO_EXPORT  char * PyArray_One \
       (PyArrayObject *);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(2) PyObject * PyArray_CastToType \
       (PyArrayObject *, PyArray_Descr *, int);
NPY_NO_EXPORT  int PyArray_CastTo \
       (PyArrayObject *, PyArrayObject *);
NPY_NO_EXPORT  int PyArray_CastAnyTo \
       (PyArrayObject *, PyArrayObject *);
NPY_NO_EXPORT  int PyArray_CanCastSafely \
       (int, int);
NPY_NO_EXPORT  npy_bool PyArray_CanCastTo \
       (PyArray_Descr *, PyArray_Descr *);
NPY_NO_EXPORT  int PyArray_ObjectType \
       (PyObject *, int);
NPY_NO_EXPORT  PyArray_Descr * PyArray_DescrFromObject \
       (PyObject *, PyArray_Descr *);
NPY_NO_EXPORT  PyArrayObject ** PyArray_ConvertToCommonType \
       (PyObject *, int *);
NPY_NO_EXPORT  PyArray_Descr * PyArray_DescrFromScalar \
       (PyObject *);
NPY_NO_EXPORT  PyArray_Descr * PyArray_DescrFromTypeObject \
       (PyObject *);
NPY_NO_EXPORT  npy_intp PyArray_Size \
       (PyObject *);
NPY_NO_EXPORT  PyObject * PyArray_Scalar \
       (void *, PyArray_Descr *, PyObject *);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(2) PyObject * PyArray_FromScalar \
       (PyObject *, PyArray_Descr *);
NPY_NO_EXPORT  void PyArray_ScalarAsCtype \
       (PyObject *, void *);
NPY_NO_EXPORT  int PyArray_CastScalarToCtype \
       (PyObject *, void *, PyArray_Descr *);
NPY_NO_EXPORT  int PyArray_CastScalarDirect \
       (PyObject *, PyArray_Descr *, void *, int);
NPY_NO_EXPORT  PyObject * PyArray_ScalarFromObject \
       (PyObject *);
NPY_NO_EXPORT  PyArray_VectorUnaryFunc * PyArray_GetCastFunc \
       (PyArray_Descr *, int);
NPY_NO_EXPORT  PyObject * PyArray_FromDims \
       (int NPY_UNUSED(nd), int *NPY_UNUSED(d), int NPY_UNUSED(type));
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(3) PyObject * PyArray_FromDimsAndDataAndDescr \
       (int NPY_UNUSED(nd), int *NPY_UNUSED(d), PyArray_Descr *, char *NPY_UNUSED(data));
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(2) PyObject * PyArray_FromAny \
       (PyObject *, PyArray_Descr *, int, int, int, PyObject *);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(1) PyObject * PyArray_EnsureArray \
       (PyObject *);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(1) PyObject * PyArray_EnsureAnyArray \
       (PyObject *);
NPY_NO_EXPORT  PyObject * PyArray_FromFile \
       (FILE *, PyArray_Descr *, npy_intp, char *);
NPY_NO_EXPORT  PyObject * PyArray_FromString \
       (char *, npy_intp, PyArray_Descr *, npy_intp, char *);
NPY_NO_EXPORT  PyObject * PyArray_FromBuffer \
       (PyObject *, PyArray_Descr *, npy_intp, npy_intp);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(2) PyObject * PyArray_FromIter \
       (PyObject *, PyArray_Descr *, npy_intp);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(1) PyObject * PyArray_Return \
       (PyArrayObject *);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(2) PyObject * PyArray_GetField \
       (PyArrayObject *, PyArray_Descr *, int);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(2) int PyArray_SetField \
       (PyArrayObject *, PyArray_Descr *, int, PyObject *);
NPY_NO_EXPORT  PyObject * PyArray_Byteswap \
       (PyArrayObject *, npy_bool);
NPY_NO_EXPORT  PyObject * PyArray_Resize \
       (PyArrayObject *, PyArray_Dims *, int, NPY_ORDER NPY_UNUSED(order));
NPY_NO_EXPORT  int PyArray_MoveInto \
       (PyArrayObject *, PyArrayObject *);
NPY_NO_EXPORT  int PyArray_CopyInto \
       (PyArrayObject *, PyArrayObject *);
NPY_NO_EXPORT  int PyArray_CopyAnyInto \
       (PyArrayObject *, PyArrayObject *);
NPY_NO_EXPORT  int PyArray_CopyObject \
       (PyArrayObject *, PyObject *);
NPY_NO_EXPORT  PyObject * PyArray_NewCopy \
       (PyArrayObject *, NPY_ORDER);
NPY_NO_EXPORT  PyObject * PyArray_ToList \
       (PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_ToString \
       (PyArrayObject *, NPY_ORDER);
NPY_NO_EXPORT  int PyArray_ToFile \
       (PyArrayObject *, FILE *, char *, char *);
NPY_NO_EXPORT  int PyArray_Dump \
       (PyObject *, PyObject *, int);
NPY_NO_EXPORT  PyObject * PyArray_Dumps \
       (PyObject *, int);
NPY_NO_EXPORT  int PyArray_ValidType \
       (int);
NPY_NO_EXPORT  void PyArray_UpdateFlags \
       (PyArrayObject *, int);
NPY_NO_EXPORT  PyObject * PyArray_New \
       (PyTypeObject *, int, npy_intp const *, int, npy_intp const *, void *, int, int, PyObject *);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(2) PyObject * PyArray_NewFromDescr \
       (PyTypeObject *, PyArray_Descr *, int, npy_intp const *, npy_intp const *, void *, int, PyObject *);
NPY_NO_EXPORT  PyArray_Descr * PyArray_DescrNew \
       (PyArray_Descr *);
NPY_NO_EXPORT  PyArray_Descr * PyArray_DescrNewFromType \
       (int);
NPY_NO_EXPORT  double PyArray_GetPriority \
       (PyObject *, double);
NPY_NO_EXPORT  PyObject * PyArray_IterNew \
       (PyObject *);
NPY_NO_EXPORT  PyObject* PyArray_MultiIterNew \
       (int, ...);
NPY_NO_EXPORT  int PyArray_PyIntAsInt \
       (PyObject *);
NPY_NO_EXPORT  npy_intp PyArray_PyIntAsIntp \
       (PyObject *);
NPY_NO_EXPORT  int PyArray_Broadcast \
       (PyArrayMultiIterObject *);
NPY_NO_EXPORT  void PyArray_FillObjectArray \
       (PyArrayObject *, PyObject *);
NPY_NO_EXPORT  int PyArray_FillWithScalar \
       (PyArrayObject *, PyObject *);
NPY_NO_EXPORT  npy_bool PyArray_CheckStrides \
       (int, int, npy_intp, npy_intp, npy_intp const *, npy_intp const *);
NPY_NO_EXPORT  PyArray_Descr * PyArray_DescrNewByteorder \
       (PyArray_Descr *, char);
NPY_NO_EXPORT  PyObject * PyArray_IterAllButAxis \
       (PyObject *, int *);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(2) PyObject * PyArray_CheckFromAny \
       (PyObject *, PyArray_Descr *, int, int, int, PyObject *);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(2) PyObject * PyArray_FromArray \
       (PyArrayObject *, PyArray_Descr *, int);
NPY_NO_EXPORT  PyObject * PyArray_FromInterface \
       (PyObject *);
NPY_NO_EXPORT  PyObject * PyArray_FromStructInterface \
       (PyObject *);
NPY_NO_EXPORT  PyObject * PyArray_FromArrayAttr \
       (PyObject *, PyArray_Descr *, PyObject *);
NPY_NO_EXPORT  NPY_SCALARKIND PyArray_ScalarKind \
       (int, PyArrayObject **);
NPY_NO_EXPORT  int PyArray_CanCoerceScalar \
       (int, int, NPY_SCALARKIND);
NPY_NO_EXPORT  PyObject * PyArray_NewFlagsObject \
       (PyObject *);
NPY_NO_EXPORT  npy_bool PyArray_CanCastScalar \
       (PyTypeObject *, PyTypeObject *);
NPY_NO_EXPORT  int PyArray_CompareUCS4 \
       (npy_ucs4 const *, npy_ucs4 const *, size_t);
NPY_NO_EXPORT  int PyArray_RemoveSmallest \
       (PyArrayMultiIterObject *);
NPY_NO_EXPORT  int PyArray_ElementStrides \
       (PyObject *);
NPY_NO_EXPORT  void PyArray_Item_INCREF \
       (char *, PyArray_Descr *);
NPY_NO_EXPORT  void PyArray_Item_XDECREF \
       (char *, PyArray_Descr *);
NPY_NO_EXPORT  PyObject * PyArray_FieldNames \
       (PyObject *);
NPY_NO_EXPORT  PyObject * PyArray_Transpose \
       (PyArrayObject *, PyArray_Dims *);
NPY_NO_EXPORT  PyObject * PyArray_TakeFrom \
       (PyArrayObject *, PyObject *, int, PyArrayObject *, NPY_CLIPMODE);
NPY_NO_EXPORT  PyObject * PyArray_PutTo \
       (PyArrayObject *, PyObject*, PyObject *, NPY_CLIPMODE);
NPY_NO_EXPORT  PyObject * PyArray_PutMask \
       (PyArrayObject *, PyObject*, PyObject*);
NPY_NO_EXPORT  PyObject * PyArray_Repeat \
       (PyArrayObject *, PyObject *, int);
NPY_NO_EXPORT  PyObject * PyArray_Choose \
       (PyArrayObject *, PyObject *, PyArrayObject *, NPY_CLIPMODE);
NPY_NO_EXPORT  int PyArray_Sort \
       (PyArrayObject *, int, NPY_SORTKIND);
NPY_NO_EXPORT  PyObject * PyArray_ArgSort \
       (PyArrayObject *, int, NPY_SORTKIND);
NPY_NO_EXPORT  PyObject * PyArray_SearchSorted \
       (PyArrayObject *, PyObject *, NPY_SEARCHSIDE, PyObject *);
NPY_NO_EXPORT  PyObject * PyArray_ArgMax \
       (PyArrayObject *, int, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_ArgMin \
       (PyArrayObject *, int, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_Reshape \
       (PyArrayObject *, PyObject *);
NPY_NO_EXPORT  PyObject * PyArray_Newshape \
       (PyArrayObject *, PyArray_Dims *, NPY_ORDER);
NPY_NO_EXPORT  PyObject * PyArray_Squeeze \
       (PyArrayObject *);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(2) PyObject * PyArray_View \
       (PyArrayObject *, PyArray_Descr *, PyTypeObject *);
NPY_NO_EXPORT  PyObject * PyArray_SwapAxes \
       (PyArrayObject *, int, int);
NPY_NO_EXPORT  PyObject * PyArray_Max \
       (PyArrayObject *, int, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_Min \
       (PyArrayObject *, int, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_Ptp \
       (PyArrayObject *, int, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_Mean \
       (PyArrayObject *, int, int, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_Trace \
       (PyArrayObject *, int, int, int, int, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_Diagonal \
       (PyArrayObject *, int, int, int);
NPY_NO_EXPORT  PyObject * PyArray_Clip \
       (PyArrayObject *, PyObject *, PyObject *, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_Conjugate \
       (PyArrayObject *, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_Nonzero \
       (PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_Std \
       (PyArrayObject *, int, int, PyArrayObject *, int);
NPY_NO_EXPORT  PyObject * PyArray_Sum \
       (PyArrayObject *, int, int, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_CumSum \
       (PyArrayObject *, int, int, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_Prod \
       (PyArrayObject *, int, int, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_CumProd \
       (PyArrayObject *, int, int, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_All \
       (PyArrayObject *, int, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_Any \
       (PyArrayObject *, int, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_Compress \
       (PyArrayObject *, PyObject *, int, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyArray_Flatten \
       (PyArrayObject *, NPY_ORDER);
NPY_NO_EXPORT  PyObject * PyArray_Ravel \
       (PyArrayObject *, NPY_ORDER);
NPY_NO_EXPORT  npy_intp PyArray_MultiplyList \
       (npy_intp const *, int);
NPY_NO_EXPORT  int PyArray_MultiplyIntList \
       (int const *, int);
NPY_NO_EXPORT  void * PyArray_GetPtr \
       (PyArrayObject *, npy_intp const*);
NPY_NO_EXPORT  int PyArray_CompareLists \
       (npy_intp const *, npy_intp const *, int);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(5) int PyArray_AsCArray \
       (PyObject **, void *, npy_intp *, int, PyArray_Descr*);
NPY_NO_EXPORT  int PyArray_As1D \
       (PyObject **NPY_UNUSED(op), char **NPY_UNUSED(ptr), int *NPY_UNUSED(d1), int NPY_UNUSED(typecode));
NPY_NO_EXPORT  int PyArray_As2D \
       (PyObject **NPY_UNUSED(op), char ***NPY_UNUSED(ptr), int *NPY_UNUSED(d1), int *NPY_UNUSED(d2), int NPY_UNUSED(typecode));
NPY_NO_EXPORT  int PyArray_Free \
       (PyObject *, void *);
NPY_NO_EXPORT  int PyArray_Converter \
       (PyObject *, PyObject **);
NPY_NO_EXPORT  int PyArray_IntpFromSequence \
       (PyObject *, npy_intp *, int);
NPY_NO_EXPORT  PyObject * PyArray_Concatenate \
       (PyObject *, int);
NPY_NO_EXPORT  PyObject * PyArray_InnerProduct \
       (PyObject *, PyObject *);
NPY_NO_EXPORT  PyObject * PyArray_MatrixProduct \
       (PyObject *, PyObject *);
NPY_NO_EXPORT  PyObject * PyArray_CopyAndTranspose \
       (PyObject *);
NPY_NO_EXPORT  PyObject * PyArray_Correlate \
       (PyObject *, PyObject *, int);
NPY_NO_EXPORT  int PyArray_TypestrConvert \
       (int, int);
NPY_NO_EXPORT  int PyArray_DescrConverter \
       (PyObject *, PyArray_Descr **);
NPY_NO_EXPORT  int PyArray_DescrConverter2 \
       (PyObject *, PyArray_Descr **);
NPY_NO_EXPORT  int PyArray_IntpConverter \
       (PyObject *, PyArray_Dims *);
NPY_NO_EXPORT  int PyArray_BufferConverter \
       (PyObject *, PyArray_Chunk *);
NPY_NO_EXPORT  int PyArray_AxisConverter \
       (PyObject *, int *);
NPY_NO_EXPORT  int PyArray_BoolConverter \
       (PyObject *, npy_bool *);
NPY_NO_EXPORT  int PyArray_ByteorderConverter \
       (PyObject *, char *);
NPY_NO_EXPORT  int PyArray_OrderConverter \
       (PyObject *, NPY_ORDER *);
NPY_NO_EXPORT  unsigned char PyArray_EquivTypes \
       (PyArray_Descr *, PyArray_Descr *);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(3) PyObject * PyArray_Zeros \
       (int, npy_intp const *, PyArray_Descr *, int);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(3) PyObject * PyArray_Empty \
       (int, npy_intp const *, PyArray_Descr *, int);
NPY_NO_EXPORT  PyObject * PyArray_Where \
       (PyObject *, PyObject *, PyObject *);
NPY_NO_EXPORT  PyObject * PyArray_Arange \
       (double, double, double, int);
NPY_NO_EXPORT  PyObject * PyArray_ArangeObj \
       (PyObject *, PyObject *, PyObject *, PyArray_Descr *);
NPY_NO_EXPORT  int PyArray_SortkindConverter \
       (PyObject *, NPY_SORTKIND *);
NPY_NO_EXPORT  PyObject * PyArray_LexSort \
       (PyObject *, int);
NPY_NO_EXPORT  PyObject * PyArray_Round \
       (PyArrayObject *, int, PyArrayObject *);
NPY_NO_EXPORT  unsigned char PyArray_EquivTypenums \
       (int, int);
NPY_NO_EXPORT  int PyArray_RegisterDataType \
       (PyArray_Descr *);
NPY_NO_EXPORT  int PyArray_RegisterCastFunc \
       (PyArray_Descr *, int, PyArray_VectorUnaryFunc *);
NPY_NO_EXPORT  int PyArray_RegisterCanCast \
       (PyArray_Descr *, int, NPY_SCALARKIND);
NPY_NO_EXPORT  void PyArray_InitArrFuncs \
       (PyArray_ArrFuncs *);
NPY_NO_EXPORT  PyObject * PyArray_IntTupleFromIntp \
       (int, npy_intp const *);
NPY_NO_EXPORT  int PyArray_TypeNumFromName \
       (char const *);
NPY_NO_EXPORT  int PyArray_ClipmodeConverter \
       (PyObject *, NPY_CLIPMODE *);
NPY_NO_EXPORT  int PyArray_OutputConverter \
       (PyObject *, PyArrayObject **);
NPY_NO_EXPORT  PyObject * PyArray_BroadcastToShape \
       (PyObject *, npy_intp *, int);
NPY_NO_EXPORT  void _PyArray_SigintHandler \
       (int);
NPY_NO_EXPORT  void* _PyArray_GetSigintBuf \
       (void);
NPY_NO_EXPORT  int PyArray_DescrAlignConverter \
       (PyObject *, PyArray_Descr **);
NPY_NO_EXPORT  int PyArray_DescrAlignConverter2 \
       (PyObject *, PyArray_Descr **);
NPY_NO_EXPORT  int PyArray_SearchsideConverter \
       (PyObject *, void *);
NPY_NO_EXPORT  PyObject * PyArray_CheckAxis \
       (PyArrayObject *, int *, int);
NPY_NO_EXPORT  npy_intp PyArray_OverflowMultiplyList \
       (npy_intp const *, int);
NPY_NO_EXPORT  int PyArray_CompareString \
       (const char *, const char *, size_t);
NPY_NO_EXPORT  PyObject* PyArray_MultiIterFromObjects \
       (PyObject **, int, int, ...);
NPY_NO_EXPORT  int PyArray_GetEndianness \
       (void);
NPY_NO_EXPORT  unsigned int PyArray_GetNDArrayCFeatureVersion \
       (void);
NPY_NO_EXPORT  PyObject * PyArray_Correlate2 \
       (PyObject *, PyObject *, int);
NPY_NO_EXPORT  PyObject* PyArray_NeighborhoodIterNew \
       (PyArrayIterObject *, const npy_intp *, int, PyArrayObject*);
extern NPY_NO_EXPORT PyTypeObject PyTimeIntegerArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyDatetimeArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyTimedeltaArrType_Type;

extern NPY_NO_EXPORT PyTypeObject PyHalfArrType_Type;

extern NPY_NO_EXPORT PyTypeObject NpyIter_Type;

NPY_NO_EXPORT  void PyArray_SetDatetimeParseFunction \
       (PyObject *NPY_UNUSED(op));
NPY_NO_EXPORT  void PyArray_DatetimeToDatetimeStruct \
       (npy_datetime NPY_UNUSED(val), NPY_DATETIMEUNIT NPY_UNUSED(fr), npy_datetimestruct *);
NPY_NO_EXPORT  void PyArray_TimedeltaToTimedeltaStruct \
       (npy_timedelta NPY_UNUSED(val), NPY_DATETIMEUNIT NPY_UNUSED(fr), npy_timedeltastruct *);
NPY_NO_EXPORT  npy_datetime PyArray_DatetimeStructToDatetime \
       (NPY_DATETIMEUNIT NPY_UNUSED(fr), npy_datetimestruct *NPY_UNUSED(d));
NPY_NO_EXPORT  npy_datetime PyArray_TimedeltaStructToTimedelta \
       (NPY_DATETIMEUNIT NPY_UNUSED(fr), npy_timedeltastruct *NPY_UNUSED(d));
NPY_NO_EXPORT  NpyIter * NpyIter_New \
       (PyArrayObject *, npy_uint32, NPY_ORDER, NPY_CASTING, PyArray_Descr*);
NPY_NO_EXPORT  NpyIter * NpyIter_MultiNew \
       (int, PyArrayObject **, npy_uint32, NPY_ORDER, NPY_CASTING, npy_uint32 *, PyArray_Descr **);
NPY_NO_EXPORT  NpyIter * NpyIter_AdvancedNew \
       (int, PyArrayObject **, npy_uint32, NPY_ORDER, NPY_CASTING, npy_uint32 *, PyArray_Descr **, int, int **, npy_intp *, npy_intp);
NPY_NO_EXPORT  NpyIter * NpyIter_Copy \
       (NpyIter *);
NPY_NO_EXPORT  int NpyIter_Deallocate \
       (NpyIter *);
NPY_NO_EXPORT  npy_bool NpyIter_HasDelayedBufAlloc \
       (NpyIter *);
NPY_NO_EXPORT  npy_bool NpyIter_HasExternalLoop \
       (NpyIter *);
NPY_NO_EXPORT  int NpyIter_EnableExternalLoop \
       (NpyIter *);
NPY_NO_EXPORT  npy_intp * NpyIter_GetInnerStrideArray \
       (NpyIter *);
NPY_NO_EXPORT  npy_intp * NpyIter_GetInnerLoopSizePtr \
       (NpyIter *);
NPY_NO_EXPORT  int NpyIter_Reset \
       (NpyIter *, char **);
NPY_NO_EXPORT  int NpyIter_ResetBasePointers \
       (NpyIter *, char **, char **);
NPY_NO_EXPORT  int NpyIter_ResetToIterIndexRange \
       (NpyIter *, npy_intp, npy_intp, char **);
NPY_NO_EXPORT  int NpyIter_GetNDim \
       (NpyIter *);
NPY_NO_EXPORT  int NpyIter_GetNOp \
       (NpyIter *);
NPY_NO_EXPORT  NpyIter_IterNextFunc * NpyIter_GetIterNext \
       (NpyIter *, char **);
NPY_NO_EXPORT  npy_intp NpyIter_GetIterSize \
       (NpyIter *);
NPY_NO_EXPORT  void NpyIter_GetIterIndexRange \
       (NpyIter *, npy_intp *, npy_intp *);
NPY_NO_EXPORT  npy_intp NpyIter_GetIterIndex \
       (NpyIter *);
NPY_NO_EXPORT  int NpyIter_GotoIterIndex \
       (NpyIter *, npy_intp);
NPY_NO_EXPORT  npy_bool NpyIter_HasMultiIndex \
       (NpyIter *);
NPY_NO_EXPORT  int NpyIter_GetShape \
       (NpyIter *, npy_intp *);
NPY_NO_EXPORT  NpyIter_GetMultiIndexFunc * NpyIter_GetGetMultiIndex \
       (NpyIter *, char **);
NPY_NO_EXPORT  int NpyIter_GotoMultiIndex \
       (NpyIter *, npy_intp const *);
NPY_NO_EXPORT  int NpyIter_RemoveMultiIndex \
       (NpyIter *);
NPY_NO_EXPORT  npy_bool NpyIter_HasIndex \
       (NpyIter *);
NPY_NO_EXPORT  npy_bool NpyIter_IsBuffered \
       (NpyIter *);
NPY_NO_EXPORT  npy_bool NpyIter_IsGrowInner \
       (NpyIter *);
NPY_NO_EXPORT  npy_intp NpyIter_GetBufferSize \
       (NpyIter *);
NPY_NO_EXPORT  npy_intp * NpyIter_GetIndexPtr \
       (NpyIter *);
NPY_NO_EXPORT  int NpyIter_GotoIndex \
       (NpyIter *, npy_intp);
NPY_NO_EXPORT  char ** NpyIter_GetDataPtrArray \
       (NpyIter *);
NPY_NO_EXPORT  PyArray_Descr ** NpyIter_GetDescrArray \
       (NpyIter *);
NPY_NO_EXPORT  PyArrayObject ** NpyIter_GetOperandArray \
       (NpyIter *);
NPY_NO_EXPORT  PyArrayObject * NpyIter_GetIterView \
       (NpyIter *, npy_intp);
NPY_NO_EXPORT  void NpyIter_GetReadFlags \
       (NpyIter *, char *);
NPY_NO_EXPORT  void NpyIter_GetWriteFlags \
       (NpyIter *, char *);
NPY_NO_EXPORT  void NpyIter_DebugPrint \
       (NpyIter *);
NPY_NO_EXPORT  npy_bool NpyIter_IterationNeedsAPI \
       (NpyIter *);
NPY_NO_EXPORT  void NpyIter_GetInnerFixedStrideArray \
       (NpyIter *, npy_intp *);
NPY_NO_EXPORT  int NpyIter_RemoveAxis \
       (NpyIter *, int);
NPY_NO_EXPORT  npy_intp * NpyIter_GetAxisStrideArray \
       (NpyIter *, int);
NPY_NO_EXPORT  npy_bool NpyIter_RequiresBuffering \
       (NpyIter *);
NPY_NO_EXPORT  char ** NpyIter_GetInitialDataPtrArray \
       (NpyIter *);
NPY_NO_EXPORT  int NpyIter_CreateCompatibleStrides \
       (NpyIter *, npy_intp, npy_intp *);
NPY_NO_EXPORT  int PyArray_CastingConverter \
       (PyObject *, NPY_CASTING *);
NPY_NO_EXPORT  npy_intp PyArray_CountNonzero \
       (PyArrayObject *);
NPY_NO_EXPORT  PyArray_Descr * PyArray_PromoteTypes \
       (PyArray_Descr *, PyArray_Descr *);
NPY_NO_EXPORT  PyArray_Descr * PyArray_MinScalarType \
       (PyArrayObject *);
NPY_NO_EXPORT  PyArray_Descr * PyArray_ResultType \
       (npy_intp, PyArrayObject *arrs[], npy_intp, PyArray_Descr *descrs[]);
NPY_NO_EXPORT  npy_bool PyArray_CanCastArrayTo \
       (PyArrayObject *, PyArray_Descr *, NPY_CASTING);
NPY_NO_EXPORT  npy_bool PyArray_CanCastTypeTo \
       (PyArray_Descr *, PyArray_Descr *, NPY_CASTING);
NPY_NO_EXPORT  PyArrayObject * PyArray_EinsteinSum \
       (char *, npy_intp, PyArrayObject **, PyArray_Descr *, NPY_ORDER, NPY_CASTING, PyArrayObject *);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(3) PyObject * PyArray_NewLikeArray \
       (PyArrayObject *, NPY_ORDER, PyArray_Descr *, int);
NPY_NO_EXPORT  int PyArray_GetArrayParamsFromObject \
       (PyObject *NPY_UNUSED(op), PyArray_Descr *NPY_UNUSED(requested_dtype), npy_bool NPY_UNUSED(writeable), PyArray_Descr **NPY_UNUSED(out_dtype), int *NPY_UNUSED(out_ndim), npy_intp *NPY_UNUSED(out_dims), PyArrayObject **NPY_UNUSED(out_arr), PyObject *NPY_UNUSED(context));
NPY_NO_EXPORT  int PyArray_ConvertClipmodeSequence \
       (PyObject *, NPY_CLIPMODE *, int);
NPY_NO_EXPORT  PyObject * PyArray_MatrixProduct2 \
       (PyObject *, PyObject *, PyArrayObject*);
NPY_NO_EXPORT  npy_bool NpyIter_IsFirstVisit \
       (NpyIter *, int);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(2) int PyArray_SetBaseObject \
       (PyArrayObject *, PyObject *);
NPY_NO_EXPORT  void PyArray_CreateSortedStridePerm \
       (int, npy_intp const *, npy_stride_sort_item *);
NPY_NO_EXPORT  void PyArray_RemoveAxesInPlace \
       (PyArrayObject *, const npy_bool *);
NPY_NO_EXPORT  void PyArray_DebugPrint \
       (PyArrayObject *);
NPY_NO_EXPORT  int PyArray_FailUnlessWriteable \
       (PyArrayObject *, const char *);
NPY_NO_EXPORT NPY_STEALS_REF_TO_ARG(2) int PyArray_SetUpdateIfCopyBase \
       (PyArrayObject *, PyArrayObject *);
NPY_NO_EXPORT  void * PyDataMem_NEW \
       (size_t);
NPY_NO_EXPORT  void PyDataMem_FREE \
       (void *);
NPY_NO_EXPORT  void * PyDataMem_RENEW \
       (void *, size_t);
NPY_NO_EXPORT  PyDataMem_EventHookFunc * PyDataMem_SetEventHook \
       (PyDataMem_EventHookFunc *, void *, void **);
extern NPY_NO_EXPORT NPY_CASTING NPY_DEFAULT_ASSIGN_CASTING;

NPY_NO_EXPORT  void PyArray_MapIterSwapAxes \
       (PyArrayMapIterObject *, PyArrayObject **, int);
NPY_NO_EXPORT  PyObject * PyArray_MapIterArray \
       (PyArrayObject *, PyObject *);
NPY_NO_EXPORT  void PyArray_MapIterNext \
       (PyArrayMapIterObject *);
NPY_NO_EXPORT  int PyArray_Partition \
       (PyArrayObject *, PyArrayObject *, int, NPY_SELECTKIND);
NPY_NO_EXPORT  PyObject * PyArray_ArgPartition \
       (PyArrayObject *, PyArrayObject *, int, NPY_SELECTKIND);
NPY_NO_EXPORT  int PyArray_SelectkindConverter \
       (PyObject *, NPY_SELECTKIND *);
NPY_NO_EXPORT  void * PyDataMem_NEW_ZEROED \
       (size_t, size_t);
NPY_NO_EXPORT  int PyArray_CheckAnyScalarExact \
       (PyObject *);
NPY_NO_EXPORT  PyObject * PyArray_MapIterArrayCopyIfOverlap \
       (PyArrayObject *, PyObject *, int, PyArrayObject *);
NPY_NO_EXPORT  int PyArray_ResolveWritebackIfCopy \
       (PyArrayObject *);
NPY_NO_EXPORT  int PyArray_SetWritebackIfCopyBase \
       (PyArrayObject *, PyArrayObject *);
NPY_NO_EXPORT  PyObject * PyDataMem_SetHandler \
       (PyObject *);
NPY_NO_EXPORT  PyObject * PyDataMem_GetHandler \
       (void);
extern NPY_NO_EXPORT PyObject* PyDataMem_DefaultHandler;


#else

#if defined(PY_ARRAY_UNIQUE_SYMBOL)
#define PyArray_API PY_ARRAY_UNIQUE_SYMBOL
#endif

#if defined(NO_IMPORT) || defined(NO_IMPORT_ARRAY)
extern void **PyArray_API;
#else
#if defined(PY_ARRAY_UNIQUE_SYMBOL)
void **PyArray_API;
#else
static void **PyArray_API=NULL;
#endif
#endif

#define PyArray_GetNDArrayCVersion \
        (*(unsigned int (*)(void)) \
         PyArray_API[0])
#define PyBigArray_Type (*(PyTypeObject *)PyArray_API[1])
#define PyArray_Type (*(PyTypeObject *)PyArray_API[2])
#define PyArrayDescr_Type (*(PyTypeObject *)PyArray_API[3])
#define PyArrayFlags_Type (*(PyTypeObject *)PyArray_API[4])
#define PyArrayIter_Type (*(PyTypeObject *)PyArray_API[5])
#define PyArrayMultiIter_Type (*(PyTypeObject *)PyArray_API[6])
#define NPY_NUMUSERTYPES (*(int *)PyArray_API[7])
#define PyBoolArrType_Type (*(PyTypeObject *)PyArray_API[8])
#define _PyArrayScalar_BoolValues ((PyBoolScalarObject *)PyArray_API[9])
#define PyGenericArrType_Type (*(PyTypeObject *)PyArray_API[10])
#define PyNumberArrType_Type (*(PyTypeObject *)PyArray_API[11])
#define PyIntegerArrType_Type (*(PyTypeObject *)PyArray_API[12])
#define PySignedIntegerArrType_Type (*(PyTypeObject *)PyArray_API[13])
#define PyUnsignedIntegerArrType_Type (*(PyTypeObject *)PyArray_API[14])
#define PyInexactArrType_Type (*(PyTypeObject *)PyArray_API[15])
#define PyFloatingArrType_Type (*(PyTypeObject *)PyArray_API[16])
#define PyComplexFloatingArrType_Type (*(PyTypeObject *)PyArray_API[17])
#define PyFlexibleArrType_Type (*(PyTypeObject *)PyArray_API[18])
#define PyCharacterArrType_Type (*(PyTypeObject *)PyArray_API[19])
#define PyByteArrType_Type (*(PyTypeObject *)PyArray_API[20])
#define PyShortArrType_Type (*(PyTypeObject *)PyArray_API[21])
#define PyIntArrType_Type (*(PyTypeObject *)PyArray_API[22])
#define PyLongArrType_Type (*(PyTypeObject *)PyArray_API[23])
#define PyLongLongArrType_Type (*(PyTypeObject *)PyArray_API[24])
#define PyUByteArrType_Type (*(PyTypeObject *)PyArray_API[25])
#define PyUShortArrType_Type (*(PyTypeObject *)PyArray_API[26])
#define PyUIntArrType_Type (*(PyTypeObject *)PyArray_API[27])
#define PyULongArrType_Type (*(PyTypeObject *)PyArray_API[28])
#define PyULongLongArrType_Type (*(PyTypeObject *)PyArray_API[29])
#define PyFloatArrType_Type (*(PyTypeObject *)PyArray_API[30])
#define PyDoubleArrType_Type (*(PyTypeObject *)PyArray_API[31])
#define PyLongDoubleArrType_Type (*(PyTypeObject *)PyArray_API[32])
#define PyCFloatArrType_Type (*(PyTypeObject *)PyArray_API[33])
#define PyCDoubleArrType_Type (*(PyTypeObject *)PyArray_API[34])
#define PyCLongDoubleArrType_Type (*(PyTypeObject *)PyArray_API[35])
#define PyObjectArrType_Type (*(PyTypeObject *)PyArray_API[36])
#define PyStringArrType_Type (*(PyTypeObject *)PyArray_API[37])
#define PyUnicodeArrType_Type (*(PyTypeObject *)PyArray_API[38])
#define PyVoidArrType_Type (*(PyTypeObject *)PyArray_API[39])
#define PyArray_SetNumericOps \
        (*(int (*)(PyObject *)) \
         PyArray_API[40])
#define PyArray_GetNumericOps \
        (*(PyObject * (*)(void)) \
         PyArray_API[41])
#define PyArray_INCREF \
        (*(int (*)(PyArrayObject *)) \
         PyArray_API[42])
#define PyArray_XDECREF \
        (*(int (*)(PyArrayObject *)) \
         PyArray_API[43])
#define PyArray_SetStringFunction \
        (*(void (*)(PyObject *, int)) \
         PyArray_API[44])
#define PyArray_DescrFromType \
        (*(PyArray_Descr * (*)(int)) \
         PyArray_API[45])
#define PyArray_TypeObjectFromType \
        (*(PyObject * (*)(int)) \
         PyArray_API[46])
#define PyArray_Zero \
        (*(char * (*)(PyArrayObject *)) \
         PyArray_API[47])
#define PyArray_One \
        (*(char * (*)(PyArrayObject *)) \
         PyArray_API[48])
#define PyArray_CastToType \
        (*(PyObject * (*)(PyArrayObject *, PyArray_Descr *, int)) \
         PyArray_API[49])
#define PyArray_CastTo \
        (*(int (*)(PyArrayObject *, PyArrayObject *)) \
         PyArray_API[50])
#define PyArray_CastAnyTo \
        (*(int (*)(PyArrayObject *, PyArrayObject *)) \
         PyArray_API[51])
#define PyArray_CanCastSafely \
        (*(int (*)(int, int)) \
         PyArray_API[52])
#define PyArray_CanCastTo \
        (*(npy_bool (*)(PyArray_Descr *, PyArray_Descr *)) \
         PyArray_API[53])
#define PyArray_ObjectType \
        (*(int (*)(PyObject *, int)) \
         PyArray_API[54])
#define PyArray_DescrFromObject \
        (*(PyArray_Descr * (*)(PyObject *, PyArray_Descr *)) \
         PyArray_API[55])
#define PyArray_ConvertToCommonType \
        (*(PyArrayObject ** (*)(PyObject *, int *)) \
         PyArray_API[56])
#define PyArray_DescrFromScalar \
        (*(PyArray_Descr * (*)(PyObject *)) \
         PyArray_API[57])
#define PyArray_DescrFromTypeObject \
        (*(PyArray_Descr * (*)(PyObject *)) \
         PyArray_API[58])
#define PyArray_Size \
        (*(npy_intp (*)(PyObject *)) \
         PyArray_API[59])
#define PyArray_Scalar \
        (*(PyObject * (*)(void *, PyArray_Descr *, PyObject *)) \
         PyArray_API[60])
#define PyArray_FromScalar \
        (*(PyObject * (*)(PyObject *, PyArray_Descr *)) \
         PyArray_API[61])
#define PyArray_ScalarAsCtype \
        (*(void (*)(PyObject *, void *)) \
         PyArray_API[62])
#define PyArray_CastScalarToCtype \
        (*(int (*)(PyObject *, void *, PyArray_Descr *)) \
         PyArray_API[63])
#define PyArray_CastScalarDirect \
        (*(int (*)(PyObject *, PyArray_Descr *, void *, int)) \
         PyArray_API[64])
#define PyArray_ScalarFromObject \
        (*(PyObject * (*)(PyObject *)) \
         PyArray_API[65])
#define PyArray_GetCastFunc \
        (*(PyArray_VectorUnaryFunc * (*)(PyArray_Descr *, int)) \
         PyArray_API[66])
#define PyArray_FromDims \
        (*(PyObject * (*)(int NPY_UNUSED(nd), int *NPY_UNUSED(d), int NPY_UNUSED(type))) \
         PyArray_API[67])
#define PyArray_FromDimsAndDataAndDescr \
        (*(PyObject * (*)(int NPY_UNUSED(nd), int *NPY_UNUSED(d), PyArray_Descr *, char *NPY_UNUSED(data))) \
         PyArray_API[68])
#define PyArray_FromAny \
        (*(PyObject * (*)(PyObject *, PyArray_Descr *, int, int, int, PyObject *)) \
         PyArray_API[69])
#define PyArray_EnsureArray \
        (*(PyObject * (*)(PyObject *)) \
         PyArray_API[70])
#define PyArray_EnsureAnyArray \
        (*(PyObject * (*)(PyObject *)) \
         PyArray_API[71])
#define PyArray_FromFile \
        (*(PyObject * (*)(FILE *, PyArray_Descr *, npy_intp, char *)) \
         PyArray_API[72])
#define PyArray_FromString \
        (*(PyObject * (*)(char *, npy_intp, PyArray_Descr *, npy_intp, char *)) \
         PyArray_API[73])
#define PyArray_FromBuffer \
        (*(PyObject * (*)(PyObject *, PyArray_Descr *, npy_intp, npy_intp)) \
         PyArray_API[74])
#define PyArray_FromIter \
        (*(PyObject * (*)(PyObject *, PyArray_Descr *, npy_intp)) \
         PyArray_API[75])
#define PyArray_Return \
        (*(PyObject * (*)(PyArrayObject *)) \
         PyArray_API[76])
#define PyArray_GetField \
        (*(PyObject * (*)(PyArrayObject *, PyArray_Descr *, int)) \
         PyArray_API[77])
#define PyArray_SetField \
        (*(int (*)(PyArrayObject *, PyArray_Descr *, int, PyObject *)) \
         PyArray_API[78])
#define PyArray_Byteswap \
        (*(PyObject * (*)(PyArrayObject *, npy_bool)) \
         PyArray_API[79])
#define PyArray_Resize \
        (*(PyObject * (*)(PyArrayObject *, PyArray_Dims *, int, NPY_ORDER NPY_UNUSED(order))) \
         PyArray_API[80])
#define PyArray_MoveInto \
        (*(int (*)(PyArrayObject *, PyArrayObject *)) \
         PyArray_API[81])
#define PyArray_CopyInto \
        (*(int (*)(PyArrayObject *, PyArrayObject *)) \
         PyArray_API[82])
#define PyArray_CopyAnyInto \
        (*(int (*)(PyArrayObject *, PyArrayObject *)) \
         PyArray_API[83])
#define PyArray_CopyObject \
        (*(int (*)(PyArrayObject *, PyObject *)) \
         PyArray_API[84])
#define PyArray_NewCopy \
        (*(PyObject * (*)(PyArrayObject *, NPY_ORDER)) \
         PyArray_API[85])
#define PyArray_ToList \
        (*(PyObject * (*)(PyArrayObject *)) \
         PyArray_API[86])
#define PyArray_ToString \
        (*(PyObject * (*)(PyArrayObject *, NPY_ORDER)) \
         PyArray_API[87])
#define PyArray_ToFile \
        (*(int (*)(PyArrayObject *, FILE *, char *, char *)) \
         PyArray_API[88])
#define PyArray_Dump \
        (*(int (*)(PyObject *, PyObject *, int)) \
         PyArray_API[89])
#define PyArray_Dumps \
        (*(PyObject * (*)(PyObject *, int)) \
         PyArray_API[90])
#define PyArray_ValidType \
        (*(int (*)(int)) \
         PyArray_API[91])
#define PyArray_UpdateFlags \
        (*(void (*)(PyArrayObject *, int)) \
         PyArray_API[92])
#define PyArray_New \
        (*(PyObject * (*)(PyTypeObject *, int, npy_intp const *, int, npy_intp const *, void *, int, int, PyObject *)) \
         PyArray_API[93])
#define PyArray_NewFromDescr \
        (*(PyObject * (*)(PyTypeObject *, PyArray_Descr *, int, npy_intp const *, npy_intp const *, void *, int, PyObject *)) \
         PyArray_API[94])
#define PyArray_DescrNew \
        (*(PyArray_Descr * (*)(PyArray_Descr *)) \
         PyArray_API[95])
#define PyArray_DescrNewFromType \
        (*(PyArray_Descr * (*)(int)) \
         PyArray_API[96])
#define PyArray_GetPriority \
        (*(double (*)(PyObject *, double)) \
         PyArray_API[97])
#define PyArray_IterNew \
        (*(PyObject * (*)(PyObject *)) \
         PyArray_API[98])
#define PyArray_MultiIterNew \
        (*(PyObject* (*)(int, ...)) \
         PyArray_API[99])
#define PyArray_PyIntAsInt \
        (*(int (*)(PyObject *)) \
         PyArray_API[100])
#define PyArray_PyIntAsIntp \
        (*(npy_intp (*)(PyObject *)) \
         PyArray_API[101])
#define PyArray_Broadcast \
        (*(int (*)(PyArrayMultiIterObject *)) \
         PyArray_API[102])
#define PyArray_FillObjectArray \
        (*(void (*)(PyArrayObject *, PyObject *)) \
         PyArray_API[103])
#define PyArray_FillWithScalar \
        (*(int (*)(PyArrayObject *, PyObject *)) \
         PyArray_API[104])
#define PyArray_CheckStrides \
        (*(npy_bool (*)(int, int, npy_intp, npy_intp, npy_intp const *, npy_intp const *)) \
         PyArray_API[105])
#define PyArray_DescrNewByteorder \
        (*(PyArray_Descr * (*)(PyArray_Descr *, char)) \
         PyArray_API[106])
#define PyArray_IterAllButAxis \
        (*(PyObject * (*)(PyObject *, int *)) \
         PyArray_API[107])
#define PyArray_CheckFromAny \
        (*(PyObject * (*)(PyObject *, PyArray_Descr *, int, int, int, PyObject *)) \
         PyArray_API[108])
#define PyArray_FromArray \
        (*(PyObject * (*)(PyArrayObject *, PyArray_Descr *, int)) \
         PyArray_API[109])
#define PyArray_FromInterface \
        (*(PyObject * (*)(PyObject *)) \
         PyArray_API[110])
#define PyArray_FromStructInterface \
        (*(PyObject * (*)(PyObject *)) \
         PyArray_API[111])
#define PyArray_FromArrayAttr \
        (*(PyObject * (*)(PyObject *, PyArray_Descr *, PyObject *)) \
         PyArray_API[112])
#define PyArray_ScalarKind \
        (*(NPY_SCALARKIND (*)(int, PyArrayObject **)) \
         PyArray_API[113])
#define PyArray_CanCoerceScalar \
        (*(int (*)(int, int, NPY_SCALARKIND)) \
         PyArray_API[114])
#define PyArray_NewFlagsObject \
        (*(PyObject * (*)(PyObject *)) \
         PyArray_API[115])
#define PyArray_CanCastScalar \
        (*(npy_bool (*)(PyTypeObject *, PyTypeObject *)) \
         PyArray_API[116])
#define PyArray_CompareUCS4 \
        (*(int (*)(npy_ucs4 const *, npy_ucs4 const *, size_t)) \
         PyArray_API[117])
#define PyArray_RemoveSmallest \
        (*(int (*)(PyArrayMultiIterObject *)) \
         PyArray_API[118])
#define PyArray_ElementStrides \
        (*(int (*)(PyObject *)) \
         PyArray_API[119])
#define PyArray_Item_INCREF \
        (*(void (*)(char *, PyArray_Descr *)) \
         PyArray_API[120])
#define PyArray_Item_XDECREF \
        (*(void (*)(char *, PyArray_Descr *)) \
         PyArray_API[121])
#define PyArray_FieldNames \
        (*(PyObject * (*)(PyObject *)) \
         PyArray_API[122])
#define PyArray_Transpose \
        (*(PyObject * (*)(PyArrayObject *, PyArray_Dims *)) \
         PyArray_API[123])
#define PyArray_TakeFrom \
        (*(PyObject * (*)(PyArrayObject *, PyObject *, int, PyArrayObject *, NPY_CLIPMODE)) \
         PyArray_API[124])
#define PyArray_PutTo \
        (*(PyObject * (*)(PyArrayObject *, PyObject*, PyObject *, NPY_CLIPMODE)) \
         PyArray_API[125])
#define PyArray_PutMask \
        (*(PyObject * (*)(PyArrayObject *, PyObject*, PyObject*)) \
         PyArray_API[126])
#define PyArray_Repeat \
        (*(PyObject * (*)(PyArrayObject *, PyObject *, int)) \
         PyArray_API[127])
#define PyArray_Choose \
        (*(PyObject * (*)(PyArrayObject *, PyObject *, PyArrayObject *, NPY_CLIPMODE)) \
         PyArray_API[128])
#define PyArray_Sort \
        (*(int (*)(PyArrayObject *, int, NPY_SORTKIND)) \
         PyArray_API[129])
#define PyArray_ArgSort \
        (*(PyObject * (*)(PyArrayObject *, int, NPY_SORTKIND)) \
         PyArray_API[130])
#define PyArray_SearchSorted \
        (*(PyObject * (*)(PyArrayObject *, PyObject *, NPY_SEARCHSIDE, PyObject *)) \
         PyArray_API[131])
#define PyArray_ArgMax \
        (*(PyObject * (*)(PyArrayObject *, int, PyArrayObject *)) \
         PyArray_API[132])
#define PyArray_ArgMin \
        (*(PyObject * (*)(PyArrayObject *, int, PyArrayObject *)) \
         PyArray_API[133])
#define PyArray_Reshape \
        (*(PyObject * (*)(PyArrayObject *, PyObject *)) \
         PyArray_API[134])
#define PyArray_Newshape \
        (*(PyObject * (*)(PyArrayObject *, PyArray_Dims *, NPY_ORDER)) \
         PyArray_API[135])
#define PyArray_Squeeze \
        (*(PyObject * (*)(PyArrayObject *)) \
         PyArray_API[136])
#define PyArray_View \
        (*(PyObject * (*)(PyArrayObject *, PyArray_Descr *, PyTypeObject *)) \
         PyArray_API[137])
#define PyArray_SwapAxes \
        (*(PyObject * (*)(PyArrayObject *, int, int)) \
         PyArray_API[138])
#define PyArray_Max \
        (*(PyObject * (*)(PyArrayObject *, int, PyArrayObject *)) \
         PyArray_API[139])
#define PyArray_Min \
        (*(PyObject * (*)(PyArrayObject *, int, PyArrayObject *)) \
         PyArray_API[140])
#define PyArray_Ptp \
        (*(PyObject * (*)(PyArrayObject *, int, PyArrayObject *)) \
         PyArray_API[141])
#define PyArray_Mean \
        (*(PyObject * (*)(PyArrayObject *, int, int, PyArrayObject *)) \
         PyArray_API[142])
#define PyArray_Trace \
        (*(PyObject * (*)(PyArrayObject *, int, int, int, int, PyArrayObject *)) \
         PyArray_API[143])
#define PyArray_Diagonal \
        (*(PyObject * (*)(PyArrayObject *, int, int, int)) \
         PyArray_API[144])
#define PyArray_Clip \
        (*(PyObject * (*)(PyArrayObject *, PyObject *, PyObject *, PyArrayObject *)) \
         PyArray_API[145])
#define PyArray_Conjugate \
        (*(PyObject * (*)(PyArrayObject *, PyArrayObject *)) \
         PyArray_API[146])
#define PyArray_Nonzero \
        (*(PyObject * (*)(PyArrayObject *)) \
         PyArray_API[147])
#define PyArray_Std \
        (*(PyObject * (*)(PyArrayObject *, int, int, PyArrayObject *, int)) \
         PyArray_API[148])
#define PyArray_Sum \
        (*(PyObject * (*)(PyArrayObject *, int, int, PyArrayObject *)) \
         PyArray_API[149])
#define PyArray_CumSum \
        (*(PyObject * (*)(PyArrayObject *, int, int, PyArrayObject *)) \
         PyArray_API[150])
#define PyArray_Prod \
        (*(PyObject * (*)(PyArrayObject *, int, int, PyArrayObject *)) \
         PyArray_API[151])
#define PyArray_CumProd \
        (*(PyObject * (*)(PyArrayObject *, int, int, PyArrayObject *)) \
         PyArray_API[152])
#define PyArray_All \
        (*(PyObject * (*)(PyArrayObject *, int, PyArrayObject *)) \
         PyArray_API[153])
#define PyArray_Any \
        (*(PyObject * (*)(PyArrayObject *, int, PyArrayObject *)) \
         PyArray_API[154])
#define PyArray_Compress \
        (*(PyObject * (*)(PyArrayObject *, PyObject *, int, PyArrayObject *)) \
         PyArray_API[155])
#define PyArray_Flatten \
        (*(PyObject * (*)(PyArrayObject *, NPY_ORDER)) \
         PyArray_API[156])
#define PyArray_Ravel \
        (*(PyObject * (*)(PyArrayObject *, NPY_ORDER)) \
         PyArray_API[157])
#define PyArray_MultiplyList \
        (*(npy_intp (*)(npy_intp const *, int)) \
         PyArray_API[158])
#define PyArray_MultiplyIntList \
        (*(int (*)(int const *, int)) \
         PyArray_API[159])
#define PyArray_GetPtr \
        (*(void * (*)(PyArrayObject *, npy_intp const*)) \
         PyArray_API[160])
#define PyArray_CompareLists \
        (*(int (*)(npy_intp const *, npy_intp const *, int)) \
         PyArray_API[161])
#define PyArray_AsCArray \
        (*(int (*)(PyObject **, void *, npy_intp *, int, PyArray_Descr*)) \
         PyArray_API[162])
#define PyArray_As1D \
        (*(int (*)(PyObject **NPY_UNUSED(op), char **NPY_UNUSED(ptr), int *NPY_UNUSED(d1), int NPY_UNUSED(typecode))) \
         PyArray_API[163])
#define PyArray_As2D \
        (*(int (*)(PyObject **NPY_UNUSED(op), char ***NPY_UNUSED(ptr), int *NPY_UNUSED(d1), int *NPY_UNUSED(d2), int NPY_UNUSED(typecode))) \
         PyArray_API[164])
#define PyArray_Free \
        (*(int (*)(PyObject *, void *)) \
         PyArray_API[165])
#define PyArray_Converter \
        (*(int (*)(PyObject *, PyObject **)) \
         PyArray_API[166])
#define PyArray_IntpFromSequence \
        (*(int (*)(PyObject *, npy_intp *, int)) \
         PyArray_API[167])
#define PyArray_Concatenate \
        (*(PyObject * (*)(PyObject *, int)) \
         PyArray_API[168])
#define PyArray_InnerProduct \
        (*(PyObject * (*)(PyObject *, PyObject *)) \
         PyArray_API[169])
#define PyArray_MatrixProduct \
        (*(PyObject * (*)(PyObject *, PyObject *)) \
         PyArray_API[170])
#define PyArray_CopyAndTranspose \
        (*(PyObject * (*)(PyObject *)) \
         PyArray_API[171])
#define PyArray_Correlate \
        (*(PyObject * (*)(PyObject *, PyObject *, int)) \
         PyArray_API[172])
#define PyArray_TypestrConvert \
        (*(int (*)(int, int)) \
         PyArray_API[173])
#define PyArray_DescrConverter \
        (*(int (*)(PyObject *, PyArray_Descr **)) \
         PyArray_API[174])
#define PyArray_DescrConverter2 \
        (*(int (*)(PyObject *, PyArray_Descr **)) \
         PyArray_API[175])
#define PyArray_IntpConverter \
        (*(int (*)(PyObject *, PyArray_Dims *)) \
         PyArray_API[176])
#define PyArray_BufferConverter \
        (*(int (*)(PyObject *, PyArray_Chunk *)) \
         PyArray_API[177])
#define PyArray_AxisConverter \
        (*(int (*)(PyObject *, int *)) \
         PyArray_API[178])
#define PyArray_BoolConverter \
        (*(int (*)(PyObject *, npy_bool *)) \
         PyArray_API[179])
#define PyArray_ByteorderConverter \
        (*(int (*)(PyObject *, char *)) \
         PyArray_API[180])
#define PyArray_OrderConverter \
        (*(int (*)(PyObject *, NPY_ORDER *)) \
         PyArray_API[181])
#define PyArray_EquivTypes \
        (*(unsigned char (*)(PyArray_Descr *, PyArray_Descr *)) \
         PyArray_API[182])
#define PyArray_Zeros \
        (*(PyObject * (*)(int, npy_intp const *, PyArray_Descr *, int)) \
         PyArray_API[183])
#define PyArray_Empty \
        (*(PyObject * (*)(int, npy_intp const *, PyArray_Descr *, int)) \
         PyArray_API[184])
#define PyArray_Where \
        (*(PyObject * (*)(PyObject *, PyObject *, PyObject *)) \
         PyArray_API[185])
#define PyArray_Arange \
        (*(PyObject * (*)(double, double, double, int)) \
         PyArray_API[186])
#define PyArray_ArangeObj \
        (*(PyObject * (*)(PyObject *, PyObject *, PyObject *, PyArray_Descr *)) \
         PyArray_API[187])
#define PyArray_SortkindConverter \
        (*(int (*)(PyObject *, NPY_SORTKIND *)) \
         PyArray_API[188])
#define PyArray_LexSort \
        (*(PyObject * (*)(PyObject *, int)) \
         PyArray_API[189])
#define PyArray_Round \
        (*(PyObject * (*)(PyArrayObject *, int, PyArrayObject *)) \
         PyArray_API[190])
#define PyArray_EquivTypenums \
        (*(unsigned char (*)(int, int)) \
         PyArray_API[191])
#define PyArray_RegisterDataType \
        (*(int (*)(PyArray_Descr *)) \
         PyArray_API[192])
#define PyArray_RegisterCastFunc \
        (*(int (*)(PyArray_Descr *, int, PyArray_VectorUnaryFunc *)) \
         PyArray_API[193])
#define PyArray_RegisterCanCast \
        (*(int (*)(PyArray_Descr *, int, NPY_SCALARKIND)) \
         PyArray_API[194])
#define PyArray_InitArrFuncs \
        (*(void (*)(PyArray_ArrFuncs *)) \
         PyArray_API[195])
#define PyArray_IntTupleFromIntp \
        (*(PyObject * (*)(int, npy_intp const *)) \
         PyArray_API[196])
#define PyArray_TypeNumFromName \
        (*(int (*)(char const *)) \
         PyArray_API[197])
#define PyArray_ClipmodeConverter \
        (*(int (*)(PyObject *, NPY_CLIPMODE *)) \
         PyArray_API[198])
#define PyArray_OutputConverter \
        (*(int (*)(PyObject *, PyArrayObject **)) \
         PyArray_API[199])
#define PyArray_BroadcastToShape \
        (*(PyObject * (*)(PyObject *, npy_intp *, int)) \
         PyArray_API[200])
#define _PyArray_SigintHandler \
        (*(void (*)(int)) \
         PyArray_API[201])
#define _PyArray_GetSigintBuf \
        (*(void* (*)(void)) \
         PyArray_API[202])
#define PyArray_DescrAlignConverter \
        (*(int (*)(PyObject *, PyArray_Descr **)) \
         PyArray_API[203])
#define PyArray_DescrAlignConverter2 \
        (*(int (*)(PyObject *, PyArray_Descr **)) \
         PyArray_API[204])
#define PyArray_SearchsideConverter \
        (*(int (*)(PyObject *, void *)) \
         PyArray_API[205])
#define PyArray_CheckAxis \
        (*(PyObject * (*)(PyArrayObject *, int *, int)) \
         PyArray_API[206])
#define PyArray_OverflowMultiplyList \
        (*(npy_intp (*)(npy_intp const *, int)) \
         PyArray_API[207])
#define PyArray_CompareString \
        (*(int (*)(const char *, const char *, size_t)) \
         PyArray_API[208])
#define PyArray_MultiIterFromObjects \
        (*(PyObject* (*)(PyObject **, int, int, ...)) \
         PyArray_API[209])
#define PyArray_GetEndianness \
        (*(int (*)(void)) \
         PyArray_API[210])
#define PyArray_GetNDArrayCFeatureVersion \
        (*(unsigned int (*)(void)) \
         PyArray_API[211])
#define PyArray_Correlate2 \
        (*(PyObject * (*)(PyObject *, PyObject *, int)) \
         PyArray_API[212])
#define PyArray_NeighborhoodIterNew \
        (*(PyObject* (*)(PyArrayIterObject *, const npy_intp *, int, PyArrayObject*)) \
         PyArray_API[213])
#define PyTimeIntegerArrType_Type (*(PyTypeObject *)PyArray_API[214])
#define PyDatetimeArrType_Type (*(PyTypeObject *)PyArray_API[215])
#define PyTimedeltaArrType_Type (*(PyTypeObject *)PyArray_API[216])
#define PyHalfArrType_Type (*(PyTypeObject *)PyArray_API[217])
#define NpyIter_Type (*(PyTypeObject *)PyArray_API[218])
#define PyArray_SetDatetimeParseFunction \
        (*(void (*)(PyObject *NPY_UNUSED(op))) \
         PyArray_API[219])
#define PyArray_DatetimeToDatetimeStruct \
        (*(void (*)(npy_datetime NPY_UNUSED(val), NPY_DATETIMEUNIT NPY_UNUSED(fr), npy_datetimestruct *)) \
         PyArray_API[220])
#define PyArray_TimedeltaToTimedeltaStruct \
        (*(void (*)(npy_timedelta NPY_UNUSED(val), NPY_DATETIMEUNIT NPY_UNUSED(fr), npy_timedeltastruct *)) \
         PyArray_API[221])
#define PyArray_DatetimeStructToDatetime \
        (*(npy_datetime (*)(NPY_DATETIMEUNIT NPY_UNUSED(fr), npy_datetimestruct *NPY_UNUSED(d))) \
         PyArray_API[222])
#define PyArray_TimedeltaStructToTimedelta \
        (*(npy_datetime (*)(NPY_DATETIMEUNIT NPY_UNUSED(fr), npy_timedeltastruct *NPY_UNUSED(d))) \
         PyArray_API[223])
#define NpyIter_New \
        (*(NpyIter * (*)(PyArrayObject *, npy_uint32, NPY_ORDER, NPY_CASTING, PyArray_Descr*)) \
         PyArray_API[224])
#define NpyIter_MultiNew \
        (*(NpyIter * (*)(int, PyArrayObject **, npy_uint32, NPY_ORDER, NPY_CASTING, npy_uint32 *, PyArray_Descr **)) \
         PyArray_API[225])
#define NpyIter_AdvancedNew \
        (*(NpyIter * (*)(int, PyArrayObject **, npy_uint32, NPY_ORDER, NPY_CASTING, npy_uint32 *, PyArray_Descr **, int, int **, npy_intp *, npy_intp)) \
         PyArray_API[226])
#define NpyIter_Copy \
        (*(NpyIter * (*)(NpyIter *)) \
         PyArray_API[227])
#define NpyIter_Deallocate \
        (*(int (*)(NpyIter *)) \
         PyArray_API[228])
#define NpyIter_HasDelayedBufAlloc \
        (*(npy_bool (*)(NpyIter *)) \
         PyArray_API[229])
#define NpyIter_HasExternalLoop \
        (*(npy_bool (*)(NpyIter *)) \
         PyArray_API[230])
#define NpyIter_EnableExternalLoop \
        (*(int (*)(NpyIter *)) \
         PyArray_API[231])
#define NpyIter_GetInnerStrideArray \
        (*(npy_intp * (*)(NpyIter *)) \
         PyArray_API[232])
#define NpyIter_GetInnerLoopSizePtr \
        (*(npy_intp * (*)(NpyIter *)) \
         PyArray_API[233])
#define NpyIter_Reset \
        (*(int (*)(NpyIter *, char **)) \
         PyArray_API[234])
#define NpyIter_ResetBasePointers \
        (*(int (*)(NpyIter *, char **, char **)) \
         PyArray_API[235])
#define NpyIter_ResetToIterIndexRange \
        (*(int (*)(NpyIter *, npy_intp, npy_intp, char **)) \
         PyArray_API[236])
#define NpyIter_GetNDim \
        (*(int (*)(NpyIter *)) \
         PyArray_API[237])
#define NpyIter_GetNOp \
        (*(int (*)(NpyIter *)) \
         PyArray_API[238])
#define NpyIter_GetIterNext \
        (*(NpyIter_IterNextFunc * (*)(NpyIter *, char **)) \
         PyArray_API[239])
#define NpyIter_GetIterSize \
        (*(npy_intp (*)(NpyIter *)) \
         PyArray_API[240])
#define NpyIter_GetIterIndexRange \
        (*(void (*)(NpyIter *, npy_intp *, npy_intp *)) \
         PyArray_API[241])
#define NpyIter_GetIterIndex \
        (*(npy_intp (*)(NpyIter *)) \
         PyArray_API[242])
#define NpyIter_GotoIterIndex \
        (*(int (*)(NpyIter *, npy_intp)) \
         PyArray_API[243])
#define NpyIter_HasMultiIndex \
        (*(npy_bool (*)(NpyIter *)) \
         PyArray_API[244])
#define NpyIter_GetShape \
        (*(int (*)(NpyIter *, npy_intp *)) \
         PyArray_API[245])
#define NpyIter_GetGetMultiIndex \
        (*(NpyIter_GetMultiIndexFunc * (*)(NpyIter *, char **)) \
         PyArray_API[246])
#define NpyIter_GotoMultiIndex \
        (*(int (*)(NpyIter *, npy_intp const *)) \
         PyArray_API[247])
#define NpyIter_RemoveMultiIndex \
        (*(int (*)(NpyIter *)) \
         PyArray_API[248])
#define NpyIter_HasIndex \
        (*(npy_bool (*)(NpyIter *)) \
         PyArray_API[249])
#define NpyIter_IsBuffered \
        (*(npy_bool (*)(NpyIter *)) \
         PyArray_API[250])
#define NpyIter_IsGrowInner \
        (*(npy_bool (*)(NpyIter *)) \
         PyArray_API[251])
#define NpyIter_GetBufferSize \
        (*(npy_intp (*)(NpyIter *)) \
         PyArray_API[252])
#define NpyIter_GetIndexPtr \
        (*(npy_intp * (*)(NpyIter *)) \
         PyArray_API[253])
#define NpyIter_GotoIndex \
        (*(int (*)(NpyIter *, npy_intp)) \
         PyArray_API[254])
#define NpyIter_GetDataPtrArray \
        (*(char ** (*)(NpyIter *)) \
         PyArray_API[255])
#define NpyIter_GetDescrArray \
        (*(PyArray_Descr ** (*)(NpyIter *)) \
         PyArray_API[256])
#define NpyIter_GetOperandArray \
        (*(PyArrayObject ** (*)(NpyIter *)) \
         PyArray_API[257])
#define NpyIter_GetIterView \
        (*(PyArrayObject * (*)(NpyIter *, npy_intp)) \
         PyArray_API[258])
#define NpyIter_GetReadFlags \
        (*(void (*)(NpyIter *, char *)) \
         PyArray_API[259])
#define NpyIter_GetWriteFlags \
        (*(void (*)(NpyIter *, char *)) \
         PyArray_API[260])
#define NpyIter_DebugPrint \
        (*(void (*)(NpyIter *)) \
         PyArray_API[261])
#define NpyIter_IterationNeedsAPI \
        (*(npy_bool (*)(NpyIter *)) \
         PyArray_API[262])
#define NpyIter_GetInnerFixedStrideArray \
        (*(void (*)(NpyIter *, npy_intp *)) \
         PyArray_API[263])
#define NpyIter_RemoveAxis \
        (*(int (*)(NpyIter *, int)) \
         PyArray_API[264])
#define NpyIter_GetAxisStrideArray \
        (*(npy_intp * (*)(NpyIter *, int)) \
         PyArray_API[265])
#define NpyIter_RequiresBuffering \
        (*(npy_bool (*)(NpyIter *)) \
         PyArray_API[266])
#define NpyIter_GetInitialDataPtrArray \
        (*(char ** (*)(NpyIter *)) \
         PyArray_API[267])
#define NpyIter_CreateCompatibleStrides \
        (*(int (*)(NpyIter *, npy_intp, npy_intp *)) \
         PyArray_API[268])
#define PyArray_CastingConverter \
        (*(int (*)(PyObject *, NPY_CASTING *)) \
         PyArray_API[269])
#define PyArray_CountNonzero \
        (*(npy_intp (*)(PyArrayObject *)) \
         PyArray_API[270])
#define PyArray_PromoteTypes \
        (*(PyArray_Descr * (*)(PyArray_Descr *, PyArray_Descr *)) \
         PyArray_API[271])
#define PyArray_MinScalarType \
        (*(PyArray_Descr * (*)(PyArrayObject *)) \
         PyArray_API[272])
#define PyArray_ResultType \
        (*(PyArray_Descr * (*)(npy_intp, PyArrayObject *arrs[], npy_intp, PyArray_Descr *descrs[])) \
         PyArray_API[273])
#define PyArray_CanCastArrayTo \
        (*(npy_bool (*)(PyArrayObject *, PyArray_Descr *, NPY_CASTING)) \
         PyArray_API[274])
#define PyArray_CanCastTypeTo \
        (*(npy_bool (*)(PyArray_Descr *, PyArray_Descr *, NPY_CASTING)) \
         PyArray_API[275])
#define PyArray_EinsteinSum \
        (*(PyArrayObject * (*)(char *, npy_intp, PyArrayObject **, PyArray_Descr *, NPY_ORDER, NPY_CASTING, PyArrayObject *)) \
         PyArray_API[276])
#define PyArray_NewLikeArray \
        (*(PyObject * (*)(PyArrayObject *, NPY_ORDER, PyArray_Descr *, int)) \
         PyArray_API[277])
#define PyArray_GetArrayParamsFromObject \
        (*(int (*)(PyObject *NPY_UNUSED(op), PyArray_Descr *NPY_UNUSED(requested_dtype), npy_bool NPY_UNUSED(writeable), PyArray_Descr **NPY_UNUSED(out_dtype), int *NPY_UNUSED(out_ndim), npy_intp *NPY_UNUSED(out_dims), PyArrayObject **NPY_UNUSED(out_arr), PyObject *NPY_UNUSED(context))) \
         PyArray_API[278])
#define PyArray_ConvertClipmodeSequence \
        (*(int (*)(PyObject *, NPY_CLIPMODE *, int)) \
         PyArray_API[279])
#define PyArray_MatrixProduct2 \
        (*(PyObject * (*)(PyObject *, PyObject *, PyArrayObject*)) \
         PyArray_API[280])
#define NpyIter_IsFirstVisit \
        (*(npy_bool (*)(NpyIter *, int)) \
         PyArray_API[281])
#define PyArray_SetBaseObject \
        (*(int (*)(PyArrayObject *, PyObject *)) \
         PyArray_API[282])
#define PyArray_CreateSortedStridePerm \
        (*(void (*)(int, npy_intp const *, npy_stride_sort_item *)) \
         PyArray_API[283])
#define PyArray_RemoveAxesInPlace \
        (*(void (*)(PyArrayObject *, const npy_bool *)) \
         PyArray_API[284])
#define PyArray_DebugPrint \
        (*(void (*)(PyArrayObject *)) \
         PyArray_API[285])
#define PyArray_FailUnlessWriteable \
        (*(int (*)(PyArrayObject *, const char *)) \
         PyArray_API[286])
#define PyArray_SetUpdateIfCopyBase \
        (*(int (*)(PyArrayObject *, PyArrayObject *)) \
         PyArray_API[287])
#define PyDataMem_NEW \
        (*(void * (*)(size_t)) \
         PyArray_API[288])
#define PyDataMem_FREE \
        (*(void (*)(void *)) \
         PyArray_API[289])
#define PyDataMem_RENEW \
        (*(void * (*)(void *, size_t)) \
         PyArray_API[290])
#define PyDataMem_SetEventHook \
        (*(PyDataMem_EventHookFunc * (*)(PyDataMem_EventHookFunc *, void *, void **)) \
         PyArray_API[291])
#define NPY_DEFAULT_ASSIGN_CASTING (*(NPY_CASTING *)PyArray_API[292])
#define PyArray_MapIterSwapAxes \
        (*(void (*)(PyArrayMapIterObject *, PyArrayObject **, int)) \
         PyArray_API[293])
#define PyArray_MapIterArray \
        (*(PyObject * (*)(PyArrayObject *, PyObject *)) \
         PyArray_API[294])
#define PyArray_MapIterNext \
        (*(void (*)(PyArrayMapIterObject *)) \
         PyArray_API[295])
#define PyArray_Partition \
        (*(int (*)(PyArrayObject *, PyArrayObject *, int, NPY_SELECTKIND)) \
         PyArray_API[296])
#define PyArray_ArgPartition \
        (*(PyObject * (*)(PyArrayObject *, PyArrayObject *, int, NPY_SELECTKIND)) \
         PyArray_API[297])
#define PyArray_SelectkindConverter \
        (*(int (*)(PyObject *, NPY_SELECTKIND *)) \
         PyArray_API[298])
#define PyDataMem_NEW_ZEROED \
        (*(void * (*)(size_t, size_t)) \
         PyArray_API[299])
#define PyArray_CheckAnyScalarExact \
        (*(int (*)(PyObject *)) \
         PyArray_API[300])
#define PyArray_MapIterArrayCopyIfOverlap \
        (*(PyObject * (*)(PyArrayObject *, PyObject *, int, PyArrayObject *)) \
         PyArray_API[301])
#define PyArray_ResolveWritebackIfCopy \
        (*(int (*)(PyArrayObject *)) \
         PyArray_API[302])
#define PyArray_SetWritebackIfCopyBase \
        (*(int (*)(PyArrayObject *, PyArrayObject *)) \
         PyArray_API[303])
#define PyDataMem_SetHandler \
        (*(PyObject * (*)(PyObject *)) \
         PyArray_API[304])
#define PyDataMem_GetHandler \
        (*(PyObject * (*)(void)) \
         PyArray_API[305])
#define PyDataMem_DefaultHandler (*(PyObject* *)PyArray_API[306])

#if !defined(NO_IMPORT_ARRAY) && !defined(NO_IMPORT)
static int
_import_array(void)
{
  int st;
  PyObject *numpy = PyImport_ImportModule("numpy.core._multiarray_umath");
  PyObject *c_api = NULL;

  if (numpy == NULL) {
      return -1;
  }
  c_api = PyObject_GetAttrString(numpy, "_ARRAY_API");
  Py_DECREF(numpy);
  if (c_api == NULL) {
      PyErr_SetString(PyExc_AttributeError, "_ARRAY_API not found");
      return -1;
  }

  if (!PyCapsule_CheckExact(c_api)) {
      PyErr_SetString(PyExc_RuntimeError, "_ARRAY_API is not PyCapsule object");
      Py_DECREF(c_api);
      return -1;
  }
  PyArray_API = (void **)PyCapsule_GetPointer(c_api, NULL);
  Py_DECREF(c_api);
  if (PyArray_API == NULL) {
      PyErr_SetString(PyExc_RuntimeError, "_ARRAY_API is NULL pointer");
      return -1;
  }

  /* Perform runtime check of C API version */
  if (NPY_VERSION != PyArray_GetNDArrayCVersion()) {
      PyErr_Format(PyExc_RuntimeError, "module compiled against "\
             "ABI version 0x%x but this version of numpy is 0x%x", \
             (int) NPY_VERSION, (int) PyArray_GetNDArrayCVersion());
      return -1;
  }
  if (NPY_FEATURE_VERSION > PyArray_GetNDArrayCFeatureVersion()) {
      PyErr_Format(PyExc_RuntimeError, "module compiled against "\
             "API version 0x%x but this version of numpy is 0x%x . "\
             "Check the section C-API incompatibility at the "\
             "Troubleshooting ImportError section at "\
             "https://numpy.org/devdocs/user/troubleshooting-importerror.html"\
             "#c-api-incompatibility "\
              "for indications on how to solve this problem .", \
             (int) NPY_FEATURE_VERSION, (int) PyArray_GetNDArrayCFeatureVersion());
      return -1;
  }

  /*
   * Perform runtime check of endianness and check it matches the one set by
   * the headers (npy_endian.h) as a safeguard
   */
  st = PyArray_GetEndianness();
  if (st == NPY_CPU_UNKNOWN_ENDIAN) {
      PyErr_SetString(PyExc_RuntimeError,
                      "FATAL: module compiled as unknown endian");
      return -1;
  }
#if NPY_BYTE_ORDER == NPY_BIG_ENDIAN
  if (st != NPY_CPU_BIG) {
      PyErr_SetString(PyExc_RuntimeError,
                      "FATAL: module compiled as big endian, but "
                      "detected different endianness at runtime");
      return -1;
  }
#elif NPY_BYTE_ORDER == NPY_LITTLE_ENDIAN
  if (st != NPY_CPU_LITTLE) {
      PyErr_SetString(PyExc_RuntimeError,
                      "FATAL: module compiled as little endian, but "
                      "detected different endianness at runtime");
      return -1;
  }
#endif

  return 0;
}

#define import_array() {if (_import_array() < 0) {PyErr_Print(); PyErr_SetString(PyExc_ImportError, "numpy.core.multiarray failed to import"); return NULL; } }

#define import_array1(ret) {if (_import_array() < 0) {PyErr_Print(); PyErr_SetString(PyExc_ImportError, "numpy.core.multiarray failed to import"); return ret; } }

#define import_array2(msg, ret) {if (_import_array() < 0) {PyErr_Print(); PyErr_SetString(PyExc_ImportError, msg); return ret; } }

#endif

#endif
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/ndarrayobject.h

```plaintext
/*
 * DON'T INCLUDE THIS DIRECTLY.
 */
#ifndef NUMPY_CORE_INCLUDE_NUMPY_NDARRAYOBJECT_H_
#define NUMPY_CORE_INCLUDE_NUMPY_NDARRAYOBJECT_H_

#ifdef __cplusplus
extern "C" {
#endif

#include <Python.h>
#include "ndarraytypes.h"

/* Includes the "function" C-API -- these are all stored in a
   list of pointers --- one for each file
   The two lists are concatenated into one in multiarray.

   They are available as import_array()
*/

#include "__multiarray_api.h"


/* C-API that requires previous API to be defined */

#define PyArray_DescrCheck(op) PyObject_TypeCheck(op, &PyArrayDescr_Type)

#define PyArray_Check(op) PyObject_TypeCheck(op, &PyArray_Type)
#define PyArray_CheckExact(op) (((PyObject*)(op))->ob_type == &PyArray_Type)

#define PyArray_HasArrayInterfaceType(op, type, context, out)                 \
        ((((out)=PyArray_FromStructInterface(op)) != Py_NotImplemented) ||    \
         (((out)=PyArray_FromInterface(op)) != Py_NotImplemented) ||          \
         (((out)=PyArray_FromArrayAttr(op, type, context)) !=                 \
          Py_NotImplemented))

#define PyArray_HasArrayInterface(op, out)                                    \
        PyArray_HasArrayInterfaceType(op, NULL, NULL, out)

#define PyArray_IsZeroDim(op) (PyArray_Check(op) && \
                               (PyArray_NDIM((PyArrayObject *)op) == 0))

#define PyArray_IsScalar(obj, cls)                                            \
        (PyObject_TypeCheck(obj, &Py##cls##ArrType_Type))

#define PyArray_CheckScalar(m) (PyArray_IsScalar(m, Generic) ||               \
                                PyArray_IsZeroDim(m))
#define PyArray_IsPythonNumber(obj)                                           \
        (PyFloat_Check(obj) || PyComplex_Check(obj) ||                        \
         PyLong_Check(obj) || PyBool_Check(obj))
#define PyArray_IsIntegerScalar(obj) (PyLong_Check(obj)                       \
              || PyArray_IsScalar((obj), Integer))
#define PyArray_IsPythonScalar(obj)                                           \
        (PyArray_IsPythonNumber(obj) || PyBytes_Check(obj) ||                 \
         PyUnicode_Check(obj))

#define PyArray_IsAnyScalar(obj)                                              \
        (PyArray_IsScalar(obj, Generic) || PyArray_IsPythonScalar(obj))

#define PyArray_CheckAnyScalar(obj) (PyArray_IsPythonScalar(obj) ||           \
                                     PyArray_CheckScalar(obj))


#define PyArray_GETCONTIGUOUS(m) (PyArray_ISCONTIGUOUS(m) ?                   \
                                  Py_INCREF(m), (m) :                         \
                                  (PyArrayObject *)(PyArray_Copy(m)))

#define PyArray_SAMESHAPE(a1,a2) ((PyArray_NDIM(a1) == PyArray_NDIM(a2)) &&   \
                                  PyArray_CompareLists(PyArray_DIMS(a1),      \
                                                       PyArray_DIMS(a2),      \
                                                       PyArray_NDIM(a1)))

#define PyArray_SIZE(m) PyArray_MultiplyList(PyArray_DIMS(m), PyArray_NDIM(m))
#define PyArray_NBYTES(m) (PyArray_ITEMSIZE(m) * PyArray_SIZE(m))
#define PyArray_FROM_O(m) PyArray_FromAny(m, NULL, 0, 0, 0, NULL)

#define PyArray_FROM_OF(m,flags) PyArray_CheckFromAny(m, NULL, 0, 0, flags,   \
                                                      NULL)

#define PyArray_FROM_OT(m,type) PyArray_FromAny(m,                            \
                                PyArray_DescrFromType(type), 0, 0, 0, NULL)

#define PyArray_FROM_OTF(m, type, flags) \
        PyArray_FromAny(m, PyArray_DescrFromType(type), 0, 0, \
                        (((flags) & NPY_ARRAY_ENSURECOPY) ? \
                         ((flags) | NPY_ARRAY_DEFAULT) : (flags)), NULL)

#define PyArray_FROMANY(m, type, min, max, flags) \
        PyArray_FromAny(m, PyArray_DescrFromType(type), min, max, \
                        (((flags) & NPY_ARRAY_ENSURECOPY) ? \
                         (flags) | NPY_ARRAY_DEFAULT : (flags)), NULL)

#define PyArray_ZEROS(m, dims, type, is_f_order) \
        PyArray_Zeros(m, dims, PyArray_DescrFromType(type), is_f_order)

#define PyArray_EMPTY(m, dims, type, is_f_order) \
        PyArray_Empty(m, dims, PyArray_DescrFromType(type), is_f_order)

#define PyArray_FILLWBYTE(obj, val) memset(PyArray_DATA(obj), val, \
                                           PyArray_NBYTES(obj))
#ifndef PYPY_VERSION
#define PyArray_REFCOUNT(obj) (((PyObject *)(obj))->ob_refcnt)
#define NPY_REFCOUNT PyArray_REFCOUNT
#endif
#define NPY_MAX_ELSIZE (2 * NPY_SIZEOF_LONGDOUBLE)

#define PyArray_ContiguousFromAny(op, type, min_depth, max_depth) \
        PyArray_FromAny(op, PyArray_DescrFromType(type), min_depth, \
                              max_depth, NPY_ARRAY_DEFAULT, NULL)

#define PyArray_EquivArrTypes(a1, a2) \
        PyArray_EquivTypes(PyArray_DESCR(a1), PyArray_DESCR(a2))

#define PyArray_EquivByteorders(b1, b2) \
        (((b1) == (b2)) || (PyArray_ISNBO(b1) == PyArray_ISNBO(b2)))

#define PyArray_SimpleNew(nd, dims, typenum) \
        PyArray_New(&PyArray_Type, nd, dims, typenum, NULL, NULL, 0, 0, NULL)

#define PyArray_SimpleNewFromData(nd, dims, typenum, data) \
        PyArray_New(&PyArray_Type, nd, dims, typenum, NULL, \
                    data, 0, NPY_ARRAY_CARRAY, NULL)

#define PyArray_SimpleNewFromDescr(nd, dims, descr) \
        PyArray_NewFromDescr(&PyArray_Type, descr, nd, dims, \
                             NULL, NULL, 0, NULL)

#define PyArray_ToScalar(data, arr) \
        PyArray_Scalar(data, PyArray_DESCR(arr), (PyObject *)arr)


/* These might be faster without the dereferencing of obj
   going on inside -- of course an optimizing compiler should
   inline the constants inside a for loop making it a moot point
*/

#define PyArray_GETPTR1(obj, i) ((void *)(PyArray_BYTES(obj) + \
                                         (i)*PyArray_STRIDES(obj)[0]))

#define PyArray_GETPTR2(obj, i, j) ((void *)(PyArray_BYTES(obj) + \
                                            (i)*PyArray_STRIDES(obj)[0] + \
                                            (j)*PyArray_STRIDES(obj)[1]))

#define PyArray_GETPTR3(obj, i, j, k) ((void *)(PyArray_BYTES(obj) + \
                                            (i)*PyArray_STRIDES(obj)[0] + \
                                            (j)*PyArray_STRIDES(obj)[1] + \
                                            (k)*PyArray_STRIDES(obj)[2]))

#define PyArray_GETPTR4(obj, i, j, k, l) ((void *)(PyArray_BYTES(obj) + \
                                            (i)*PyArray_STRIDES(obj)[0] + \
                                            (j)*PyArray_STRIDES(obj)[1] + \
                                            (k)*PyArray_STRIDES(obj)[2] + \
                                            (l)*PyArray_STRIDES(obj)[3]))

static NPY_INLINE void
PyArray_DiscardWritebackIfCopy(PyArrayObject *arr)
{
    PyArrayObject_fields *fa = (PyArrayObject_fields *)arr;
    if (fa && fa->base) {
        if (fa->flags & NPY_ARRAY_WRITEBACKIFCOPY) {
            PyArray_ENABLEFLAGS((PyArrayObject*)fa->base, NPY_ARRAY_WRITEABLE);
            Py_DECREF(fa->base);
            fa->base = NULL;
            PyArray_CLEARFLAGS(arr, NPY_ARRAY_WRITEBACKIFCOPY);
        }
    }
}

#define PyArray_DESCR_REPLACE(descr) do { \
                PyArray_Descr *_new_; \
                _new_ = PyArray_DescrNew(descr); \
                Py_XDECREF(descr); \
                descr = _new_; \
        } while(0)

/* Copy should always return contiguous array */
#define PyArray_Copy(obj) PyArray_NewCopy(obj, NPY_CORDER)

#define PyArray_FromObject(op, type, min_depth, max_depth) \
        PyArray_FromAny(op, PyArray_DescrFromType(type), min_depth, \
                              max_depth, NPY_ARRAY_BEHAVED | \
                                         NPY_ARRAY_ENSUREARRAY, NULL)

#define PyArray_ContiguousFromObject(op, type, min_depth, max_depth) \
        PyArray_FromAny(op, PyArray_DescrFromType(type), min_depth, \
                              max_depth, NPY_ARRAY_DEFAULT | \
                                         NPY_ARRAY_ENSUREARRAY, NULL)

#define PyArray_CopyFromObject(op, type, min_depth, max_depth) \
        PyArray_FromAny(op, PyArray_DescrFromType(type), min_depth, \
                        max_depth, NPY_ARRAY_ENSURECOPY | \
                                   NPY_ARRAY_DEFAULT | \
                                   NPY_ARRAY_ENSUREARRAY, NULL)

#define PyArray_Cast(mp, type_num)                                            \
        PyArray_CastToType(mp, PyArray_DescrFromType(type_num), 0)

#define PyArray_Take(ap, items, axis)                                         \
        PyArray_TakeFrom(ap, items, axis, NULL, NPY_RAISE)

#define PyArray_Put(ap, items, values)                                        \
        PyArray_PutTo(ap, items, values, NPY_RAISE)

/* Compatibility with old Numeric stuff -- don't use in new code */

#define PyArray_FromDimsAndData(nd, d, type, data)                            \
        PyArray_FromDimsAndDataAndDescr(nd, d, PyArray_DescrFromType(type),   \
                                        data)


/*
   Check to see if this key in the dictionary is the "title"
   entry of the tuple (i.e. a duplicate dictionary entry in the fields
   dict).
*/

static NPY_INLINE int
NPY_TITLE_KEY_check(PyObject *key, PyObject *value)
{
    PyObject *title;
    if (PyTuple_Size(value) != 3) {
        return 0;
    }
    title = PyTuple_GetItem(value, 2);
    if (key == title) {
        return 1;
    }
#ifdef PYPY_VERSION
    /*
     * On PyPy, dictionary keys do not always preserve object identity.
     * Fall back to comparison by value.
     */
    if (PyUnicode_Check(title) && PyUnicode_Check(key)) {
        return PyUnicode_Compare(title, key) == 0 ? 1 : 0;
    }
#endif
    return 0;
}

/* Macro, for backward compat with "if NPY_TITLE_KEY(key, value) { ..." */
#define NPY_TITLE_KEY(key, value) (NPY_TITLE_KEY_check((key), (value)))

#define DEPRECATE(msg) PyErr_WarnEx(PyExc_DeprecationWarning,msg,1)
#define DEPRECATE_FUTUREWARNING(msg) PyErr_WarnEx(PyExc_FutureWarning,msg,1)

#ifdef __cplusplus
}
#endif


#endif  /* NUMPY_CORE_INCLUDE_NUMPY_NDARRAYOBJECT_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/ndarraytypes.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY_NDARRAYTYPES_H_
#define NUMPY_CORE_INCLUDE_NUMPY_NDARRAYTYPES_H_

#include "npy_common.h"
#include "npy_endian.h"
#include "npy_cpu.h"
#include "utils.h"

#define NPY_NO_EXPORT NPY_VISIBILITY_HIDDEN

/* Only use thread if configured in config and python supports it */
#if defined WITH_THREAD && !NPY_NO_SMP
        #define NPY_ALLOW_THREADS 1
#else
        #define NPY_ALLOW_THREADS 0
#endif

#ifndef __has_extension
#define __has_extension(x) 0
#endif

#if !defined(_NPY_NO_DEPRECATIONS) && \
    ((defined(__GNUC__)&& __GNUC__ >= 6) || \
     __has_extension(attribute_deprecated_with_message))
#define NPY_ATTR_DEPRECATE(text) __attribute__ ((deprecated (text)))
#else
#define NPY_ATTR_DEPRECATE(text)
#endif

/*
 * There are several places in the code where an array of dimensions
 * is allocated statically.  This is the size of that static
 * allocation.
 *
 * The array creation itself could have arbitrary dimensions but all
 * the places where static allocation is used would need to be changed
 * to dynamic (including inside of several structures)
 */

#define NPY_MAXDIMS 32
#define NPY_MAXARGS 32

/* Used for Converter Functions "O&" code in ParseTuple */
#define NPY_FAIL 0
#define NPY_SUCCEED 1

/*
 * Binary compatibility version number.  This number is increased
 * whenever the C-API is changed such that binary compatibility is
 * broken, i.e. whenever a recompile of extension modules is needed.
 */
#define NPY_VERSION NPY_ABI_VERSION

/*
 * Minor API version.  This number is increased whenever a change is
 * made to the C-API -- whether it breaks binary compatibility or not.
 * Some changes, such as adding a function pointer to the end of the
 * function table, can be made without breaking binary compatibility.
 * In this case, only the NPY_FEATURE_VERSION (*not* NPY_VERSION)
 * would be increased.  Whenever binary compatibility is broken, both
 * NPY_VERSION and NPY_FEATURE_VERSION should be increased.
 */
#define NPY_FEATURE_VERSION NPY_API_VERSION

enum NPY_TYPES {    NPY_BOOL=0,
                    NPY_BYTE, NPY_UBYTE,
                    NPY_SHORT, NPY_USHORT,
                    NPY_INT, NPY_UINT,
                    NPY_LONG, NPY_ULONG,
                    NPY_LONGLONG, NPY_ULONGLONG,
                    NPY_FLOAT, NPY_DOUBLE, NPY_LONGDOUBLE,
                    NPY_CFLOAT, NPY_CDOUBLE, NPY_CLONGDOUBLE,
                    NPY_OBJECT=17,
                    NPY_STRING, NPY_UNICODE,
                    NPY_VOID,
                    /*
                     * New 1.6 types appended, may be integrated
                     * into the above in 2.0.
                     */
                    NPY_DATETIME, NPY_TIMEDELTA, NPY_HALF,

                    NPY_NTYPES,
                    NPY_NOTYPE,
                    NPY_CHAR NPY_ATTR_DEPRECATE("Use NPY_STRING"),
                    NPY_USERDEF=256,  /* leave room for characters */

                    /* The number of types not including the new 1.6 types */
                    NPY_NTYPES_ABI_COMPATIBLE=21
};
#if defined(_MSC_VER) && !defined(__clang__)
#pragma deprecated(NPY_CHAR)
#endif

/* basetype array priority */
#define NPY_PRIORITY 0.0

/* default subtype priority */
#define NPY_SUBTYPE_PRIORITY 1.0

/* default scalar priority */
#define NPY_SCALAR_PRIORITY -1000000.0

/* How many floating point types are there (excluding half) */
#define NPY_NUM_FLOATTYPE 3

/*
 * These characters correspond to the array type and the struct
 * module
 */

enum NPY_TYPECHAR {
        NPY_BOOLLTR = '?',
        NPY_BYTELTR = 'b',
        NPY_UBYTELTR = 'B',
        NPY_SHORTLTR = 'h',
        NPY_USHORTLTR = 'H',
        NPY_INTLTR = 'i',
        NPY_UINTLTR = 'I',
        NPY_LONGLTR = 'l',
        NPY_ULONGLTR = 'L',
        NPY_LONGLONGLTR = 'q',
        NPY_ULONGLONGLTR = 'Q',
        NPY_HALFLTR = 'e',
        NPY_FLOATLTR = 'f',
        NPY_DOUBLELTR = 'd',
        NPY_LONGDOUBLELTR = 'g',
        NPY_CFLOATLTR = 'F',
        NPY_CDOUBLELTR = 'D',
        NPY_CLONGDOUBLELTR = 'G',
        NPY_OBJECTLTR = 'O',
        NPY_STRINGLTR = 'S',
        NPY_STRINGLTR2 = 'a',
        NPY_UNICODELTR = 'U',
        NPY_VOIDLTR = 'V',
        NPY_DATETIMELTR = 'M',
        NPY_TIMEDELTALTR = 'm',
        NPY_CHARLTR = 'c',

        /*
         * No Descriptor, just a define -- this let's
         * Python users specify an array of integers
         * large enough to hold a pointer on the
         * platform
         */
        NPY_INTPLTR = 'p',
        NPY_UINTPLTR = 'P',

        /*
         * These are for dtype 'kinds', not dtype 'typecodes'
         * as the above are for.
         */
        NPY_GENBOOLLTR ='b',
        NPY_SIGNEDLTR = 'i',
        NPY_UNSIGNEDLTR = 'u',
        NPY_FLOATINGLTR = 'f',
        NPY_COMPLEXLTR = 'c'
};

/*
 * Changing this may break Numpy API compatibility
 * due to changing offsets in PyArray_ArrFuncs, so be
 * careful. Here we have reused the mergesort slot for
 * any kind of stable sort, the actual implementation will
 * depend on the data type.
 */
typedef enum {
        NPY_QUICKSORT=0,
        NPY_HEAPSORT=1,
        NPY_MERGESORT=2,
        NPY_STABLESORT=2,
} NPY_SORTKIND;
#define NPY_NSORTS (NPY_STABLESORT + 1)


typedef enum {
        NPY_INTROSELECT=0
} NPY_SELECTKIND;
#define NPY_NSELECTS (NPY_INTROSELECT + 1)


typedef enum {
        NPY_SEARCHLEFT=0,
        NPY_SEARCHRIGHT=1
} NPY_SEARCHSIDE;
#define NPY_NSEARCHSIDES (NPY_SEARCHRIGHT + 1)


typedef enum {
        NPY_NOSCALAR=-1,
        NPY_BOOL_SCALAR,
        NPY_INTPOS_SCALAR,
        NPY_INTNEG_SCALAR,
        NPY_FLOAT_SCALAR,
        NPY_COMPLEX_SCALAR,
        NPY_OBJECT_SCALAR
} NPY_SCALARKIND;
#define NPY_NSCALARKINDS (NPY_OBJECT_SCALAR + 1)

/* For specifying array memory layout or iteration order */
typedef enum {
        /* Fortran order if inputs are all Fortran, C otherwise */
        NPY_ANYORDER=-1,
        /* C order */
        NPY_CORDER=0,
        /* Fortran order */
        NPY_FORTRANORDER=1,
        /* An order as close to the inputs as possible */
        NPY_KEEPORDER=2
} NPY_ORDER;

/* For specifying allowed casting in operations which support it */
typedef enum {
        _NPY_ERROR_OCCURRED_IN_CAST = -1,
        /* Only allow identical types */
        NPY_NO_CASTING=0,
        /* Allow identical and byte swapped types */
        NPY_EQUIV_CASTING=1,
        /* Only allow safe casts */
        NPY_SAFE_CASTING=2,
        /* Allow safe casts or casts within the same kind */
        NPY_SAME_KIND_CASTING=3,
        /* Allow any casts */
        NPY_UNSAFE_CASTING=4,
} NPY_CASTING;

typedef enum {
        NPY_CLIP=0,
        NPY_WRAP=1,
        NPY_RAISE=2
} NPY_CLIPMODE;

typedef enum {
        NPY_VALID=0,
        NPY_SAME=1,
        NPY_FULL=2
} NPY_CORRELATEMODE;

/* The special not-a-time (NaT) value */
#define NPY_DATETIME_NAT NPY_MIN_INT64

/*
 * Upper bound on the length of a DATETIME ISO 8601 string
 *   YEAR: 21 (64-bit year)
 *   MONTH: 3
 *   DAY: 3
 *   HOURS: 3
 *   MINUTES: 3
 *   SECONDS: 3
 *   ATTOSECONDS: 1 + 3*6
 *   TIMEZONE: 5
 *   NULL TERMINATOR: 1
 */
#define NPY_DATETIME_MAX_ISO8601_STRLEN (21 + 3*5 + 1 + 3*6 + 6 + 1)

/* The FR in the unit names stands for frequency */
typedef enum {
        /* Force signed enum type, must be -1 for code compatibility */
        NPY_FR_ERROR = -1,      /* error or undetermined */

        /* Start of valid units */
        NPY_FR_Y = 0,           /* Years */
        NPY_FR_M = 1,           /* Months */
        NPY_FR_W = 2,           /* Weeks */
        /* Gap where 1.6 NPY_FR_B (value 3) was */
        NPY_FR_D = 4,           /* Days */
        NPY_FR_h = 5,           /* hours */
        NPY_FR_m = 6,           /* minutes */
        NPY_FR_s = 7,           /* seconds */
        NPY_FR_ms = 8,          /* milliseconds */
        NPY_FR_us = 9,          /* microseconds */
        NPY_FR_ns = 10,         /* nanoseconds */
        NPY_FR_ps = 11,         /* picoseconds */
        NPY_FR_fs = 12,         /* femtoseconds */
        NPY_FR_as = 13,         /* attoseconds */
        NPY_FR_GENERIC = 14     /* unbound units, can convert to anything */
} NPY_DATETIMEUNIT;

/*
 * NOTE: With the NPY_FR_B gap for 1.6 ABI compatibility, NPY_DATETIME_NUMUNITS
 * is technically one more than the actual number of units.
 */
#define NPY_DATETIME_NUMUNITS (NPY_FR_GENERIC + 1)
#define NPY_DATETIME_DEFAULTUNIT NPY_FR_GENERIC

/*
 * Business day conventions for mapping invalid business
 * days to valid business days.
 */
typedef enum {
    /* Go forward in time to the following business day. */
    NPY_BUSDAY_FORWARD,
    NPY_BUSDAY_FOLLOWING = NPY_BUSDAY_FORWARD,
    /* Go backward in time to the preceding business day. */
    NPY_BUSDAY_BACKWARD,
    NPY_BUSDAY_PRECEDING = NPY_BUSDAY_BACKWARD,
    /*
     * Go forward in time to the following business day, unless it
     * crosses a month boundary, in which case go backward
     */
    NPY_BUSDAY_MODIFIEDFOLLOWING,
    /*
     * Go backward in time to the preceding business day, unless it
     * crosses a month boundary, in which case go forward.
     */
    NPY_BUSDAY_MODIFIEDPRECEDING,
    /* Produce a NaT for non-business days. */
    NPY_BUSDAY_NAT,
    /* Raise an exception for non-business days. */
    NPY_BUSDAY_RAISE
} NPY_BUSDAY_ROLL;

/************************************************************
 * NumPy Auxiliary Data for inner loops, sort functions, etc.
 ************************************************************/

/*
 * When creating an auxiliary data struct, this should always appear
 * as the first member, like this:
 *
 * typedef struct {
 *     NpyAuxData base;
 *     double constant;
 * } constant_multiplier_aux_data;
 */
typedef struct NpyAuxData_tag NpyAuxData;

/* Function pointers for freeing or cloning auxiliary data */
typedef void (NpyAuxData_FreeFunc) (NpyAuxData *);
typedef NpyAuxData *(NpyAuxData_CloneFunc) (NpyAuxData *);

struct NpyAuxData_tag {
    NpyAuxData_FreeFunc *free;
    NpyAuxData_CloneFunc *clone;
    /* To allow for a bit of expansion without breaking the ABI */
    void *reserved[2];
};

/* Macros to use for freeing and cloning auxiliary data */
#define NPY_AUXDATA_FREE(auxdata) \
    do { \
        if ((auxdata) != NULL) { \
            (auxdata)->free(auxdata); \
        } \
    } while(0)
#define NPY_AUXDATA_CLONE(auxdata) \
    ((auxdata)->clone(auxdata))

#define NPY_ERR(str) fprintf(stderr, #str); fflush(stderr);
#define NPY_ERR2(str) fprintf(stderr, str); fflush(stderr);

/*
* Macros to define how array, and dimension/strides data is
* allocated. These should be made private
*/

#define NPY_USE_PYMEM 1


#if NPY_USE_PYMEM == 1
/* use the Raw versions which are safe to call with the GIL released */
#define PyArray_malloc PyMem_RawMalloc
#define PyArray_free PyMem_RawFree
#define PyArray_realloc PyMem_RawRealloc
#else
#define PyArray_malloc malloc
#define PyArray_free free
#define PyArray_realloc realloc
#endif

/* Dimensions and strides */
#define PyDimMem_NEW(size)                                         \
    ((npy_intp *)PyArray_malloc(size*sizeof(npy_intp)))

#define PyDimMem_FREE(ptr) PyArray_free(ptr)

#define PyDimMem_RENEW(ptr,size)                                   \
        ((npy_intp *)PyArray_realloc(ptr,size*sizeof(npy_intp)))

/* forward declaration */
struct _PyArray_Descr;

/* These must deal with unaligned and swapped data if necessary */
typedef PyObject * (PyArray_GetItemFunc) (void *, void *);
typedef int (PyArray_SetItemFunc)(PyObject *, void *, void *);

typedef void (PyArray_CopySwapNFunc)(void *, npy_intp, void *, npy_intp,
                                     npy_intp, int, void *);

typedef void (PyArray_CopySwapFunc)(void *, void *, int, void *);
typedef npy_bool (PyArray_NonzeroFunc)(void *, void *);


/*
 * These assume aligned and notswapped data -- a buffer will be used
 * before or contiguous data will be obtained
 */

typedef int (PyArray_CompareFunc)(const void *, const void *, void *);
typedef int (PyArray_ArgFunc)(void*, npy_intp, npy_intp*, void *);

typedef void (PyArray_DotFunc)(void *, npy_intp, void *, npy_intp, void *,
                               npy_intp, void *);

typedef void (PyArray_VectorUnaryFunc)(void *, void *, npy_intp, void *,
                                       void *);

/*
 * XXX the ignore argument should be removed next time the API version
 * is bumped. It used to be the separator.
 */
typedef int (PyArray_ScanFunc)(FILE *fp, void *dptr,
                               char *ignore, struct _PyArray_Descr *);
typedef int (PyArray_FromStrFunc)(char *s, void *dptr, char **endptr,
                                  struct _PyArray_Descr *);

typedef int (PyArray_FillFunc)(void *, npy_intp, void *);

typedef int (PyArray_SortFunc)(void *, npy_intp, void *);
typedef int (PyArray_ArgSortFunc)(void *, npy_intp *, npy_intp, void *);
typedef int (PyArray_PartitionFunc)(void *, npy_intp, npy_intp,
                                    npy_intp *, npy_intp *,
                                    void *);
typedef int (PyArray_ArgPartitionFunc)(void *, npy_intp *, npy_intp, npy_intp,
                                       npy_intp *, npy_intp *,
                                       void *);

typedef int (PyArray_FillWithScalarFunc)(void *, npy_intp, void *, void *);

typedef int (PyArray_ScalarKindFunc)(void *);

typedef void (PyArray_FastClipFunc)(void *in, npy_intp n_in, void *min,
                                    void *max, void *out);
typedef void (PyArray_FastPutmaskFunc)(void *in, void *mask, npy_intp n_in,
                                       void *values, npy_intp nv);
typedef int  (PyArray_FastTakeFunc)(void *dest, void *src, npy_intp *indarray,
                                       npy_intp nindarray, npy_intp n_outer,
                                       npy_intp m_middle, npy_intp nelem,
                                       NPY_CLIPMODE clipmode);

typedef struct {
        npy_intp *ptr;
        int len;
} PyArray_Dims;

typedef struct {
        /*
         * Functions to cast to most other standard types
         * Can have some NULL entries. The types
         * DATETIME, TIMEDELTA, and HALF go into the castdict
         * even though they are built-in.
         */
        PyArray_VectorUnaryFunc *cast[NPY_NTYPES_ABI_COMPATIBLE];

        /* The next four functions *cannot* be NULL */

        /*
         * Functions to get and set items with standard Python types
         * -- not array scalars
         */
        PyArray_GetItemFunc *getitem;
        PyArray_SetItemFunc *setitem;

        /*
         * Copy and/or swap data.  Memory areas may not overlap
         * Use memmove first if they might
         */
        PyArray_CopySwapNFunc *copyswapn;
        PyArray_CopySwapFunc *copyswap;

        /*
         * Function to compare items
         * Can be NULL
         */
        PyArray_CompareFunc *compare;

        /*
         * Function to select largest
         * Can be NULL
         */
        PyArray_ArgFunc *argmax;

        /*
         * Function to compute dot product
         * Can be NULL
         */
        PyArray_DotFunc *dotfunc;

        /*
         * Function to scan an ASCII file and
         * place a single value plus possible separator
         * Can be NULL
         */
        PyArray_ScanFunc *scanfunc;

        /*
         * Function to read a single value from a string
         * and adjust the pointer; Can be NULL
         */
        PyArray_FromStrFunc *fromstr;

        /*
         * Function to determine if data is zero or not
         * If NULL a default version is
         * used at Registration time.
         */
        PyArray_NonzeroFunc *nonzero;

        /*
         * Used for arange. Should return 0 on success
         * and -1 on failure.
         * Can be NULL.
         */
        PyArray_FillFunc *fill;

        /*
         * Function to fill arrays with scalar values
         * Can be NULL
         */
        PyArray_FillWithScalarFunc *fillwithscalar;

        /*
         * Sorting functions
         * Can be NULL
         */
        PyArray_SortFunc *sort[NPY_NSORTS];
        PyArray_ArgSortFunc *argsort[NPY_NSORTS];

        /*
         * Dictionary of additional casting functions
         * PyArray_VectorUnaryFuncs
         * which can be populated to support casting
         * to other registered types. Can be NULL
         */
        PyObject *castdict;

        /*
         * Functions useful for generalizing
         * the casting rules.
         * Can be NULL;
         */
        PyArray_ScalarKindFunc *scalarkind;
        int **cancastscalarkindto;
        int *cancastto;

        PyArray_FastClipFunc *fastclip;
        PyArray_FastPutmaskFunc *fastputmask;
        PyArray_FastTakeFunc *fasttake;

        /*
         * Function to select smallest
         * Can be NULL
         */
        PyArray_ArgFunc *argmin;

} PyArray_ArrFuncs;

/* The item must be reference counted when it is inserted or extracted. */
#define NPY_ITEM_REFCOUNT   0x01
/* Same as needing REFCOUNT */
#define NPY_ITEM_HASOBJECT  0x01
/* Convert to list for pickling */
#define NPY_LIST_PICKLE     0x02
/* The item is a POINTER  */
#define NPY_ITEM_IS_POINTER 0x04
/* memory needs to be initialized for this data-type */
#define NPY_NEEDS_INIT      0x08
/* operations need Python C-API so don't give-up thread. */
#define NPY_NEEDS_PYAPI     0x10
/* Use f.getitem when extracting elements of this data-type */
#define NPY_USE_GETITEM     0x20
/* Use f.setitem when setting creating 0-d array from this data-type.*/
#define NPY_USE_SETITEM     0x40
/* A sticky flag specifically for structured arrays */
#define NPY_ALIGNED_STRUCT  0x80

/*
 *These are inherited for global data-type if any data-types in the
 * field have them
 */
#define NPY_FROM_FIELDS    (NPY_NEEDS_INIT | NPY_LIST_PICKLE | \
                            NPY_ITEM_REFCOUNT | NPY_NEEDS_PYAPI)

#define NPY_OBJECT_DTYPE_FLAGS (NPY_LIST_PICKLE | NPY_USE_GETITEM | \
                                NPY_ITEM_IS_POINTER | NPY_ITEM_REFCOUNT | \
                                NPY_NEEDS_INIT | NPY_NEEDS_PYAPI)

#define PyDataType_FLAGCHK(dtype, flag) \
        (((dtype)->flags & (flag)) == (flag))

#define PyDataType_REFCHK(dtype) \
        PyDataType_FLAGCHK(dtype, NPY_ITEM_REFCOUNT)

typedef struct _PyArray_Descr {
        PyObject_HEAD
        /*
         * the type object representing an
         * instance of this type -- should not
         * be two type_numbers with the same type
         * object.
         */
        PyTypeObject *typeobj;
        /* kind for this type */
        char kind;
        /* unique-character representing this type */
        char type;
        /*
         * '>' (big), '<' (little), '|'
         * (not-applicable), or '=' (native).
         */
        char byteorder;
        /* flags describing data type */
        char flags;
        /* number representing this type */
        int type_num;
        /* element size (itemsize) for this type */
        int elsize;
        /* alignment needed for this type */
        int alignment;
        /*
         * Non-NULL if this type is
         * is an array (C-contiguous)
         * of some other type
         */
        struct _arr_descr *subarray;
        /*
         * The fields dictionary for this type
         * For statically defined descr this
         * is always Py_None
         */
        PyObject *fields;
        /*
         * An ordered tuple of field names or NULL
         * if no fields are defined
         */
        PyObject *names;
        /*
         * a table of functions specific for each
         * basic data descriptor
         */
        PyArray_ArrFuncs *f;
        /* Metadata about this dtype */
        PyObject *metadata;
        /*
         * Metadata specific to the C implementation
         * of the particular dtype. This was added
         * for NumPy 1.7.0.
         */
        NpyAuxData *c_metadata;
        /* Cached hash value (-1 if not yet computed).
         * This was added for NumPy 2.0.0.
         */
        npy_hash_t hash;
} PyArray_Descr;

typedef struct _arr_descr {
        PyArray_Descr *base;
        PyObject *shape;       /* a tuple */
} PyArray_ArrayDescr;

/*
 * Memory handler structure for array data.
 */
/* The declaration of free differs from PyMemAllocatorEx */
typedef struct {
    void *ctx;
    void* (*malloc) (void *ctx, size_t size);
    void* (*calloc) (void *ctx, size_t nelem, size_t elsize);
    void* (*realloc) (void *ctx, void *ptr, size_t new_size);
    void (*free) (void *ctx, void *ptr, size_t size);
    /*
     * This is the end of the version=1 struct. Only add new fields after
     * this line
     */
} PyDataMemAllocator;

typedef struct {
    char name[127];  /* multiple of 64 to keep the struct aligned */
    uint8_t version; /* currently 1 */
    PyDataMemAllocator allocator;
} PyDataMem_Handler;


/*
 * The main array object structure.
 *
 * It has been recommended to use the inline functions defined below
 * (PyArray_DATA and friends) to access fields here for a number of
 * releases. Direct access to the members themselves is deprecated.
 * To ensure that your code does not use deprecated access,
 * #define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
 * (or NPY_1_8_API_VERSION or higher as required).
 */
/* This struct will be moved to a private header in a future release */
typedef struct tagPyArrayObject_fields {
    PyObject_HEAD
    /* Pointer to the raw data buffer */
    char *data;
    /* The number of dimensions, also called 'ndim' */
    int nd;
    /* The size in each dimension, also called 'shape' */
    npy_intp *dimensions;
    /*
     * Number of bytes to jump to get to the
     * next element in each dimension
     */
    npy_intp *strides;
    /*
     * This object is decref'd upon
     * deletion of array. Except in the
     * case of WRITEBACKIFCOPY which has
     * special handling.
     *
     * For views it points to the original
     * array, collapsed so no chains of
     * views occur.
     *
     * For creation from buffer object it
     * points to an object that should be
     * decref'd on deletion
     *
     * For WRITEBACKIFCOPY flag this is an
     * array to-be-updated upon calling
     * PyArray_ResolveWritebackIfCopy
     */
    PyObject *base;
    /* Pointer to type structure */
    PyArray_Descr *descr;
    /* Flags describing array -- see below */
    int flags;
    /* For weak references */
    PyObject *weakreflist;
    void *_buffer_info;  /* private buffer info, tagged to allow warning */
    /*
     * For malloc/calloc/realloc/free per object
     */
    PyObject *mem_handler;
} PyArrayObject_fields;

/*
 * To hide the implementation details, we only expose
 * the Python struct HEAD.
 */
#if !defined(NPY_NO_DEPRECATED_API) || \
    (NPY_NO_DEPRECATED_API < NPY_1_7_API_VERSION)
/*
 * Can't put this in npy_deprecated_api.h like the others.
 * PyArrayObject field access is deprecated as of NumPy 1.7.
 */
typedef PyArrayObject_fields PyArrayObject;
#else
typedef struct tagPyArrayObject {
        PyObject_HEAD
} PyArrayObject;
#endif

/*
 * Removed 2020-Nov-25, NumPy 1.20
 * #define NPY_SIZEOF_PYARRAYOBJECT (sizeof(PyArrayObject_fields))
 *
 * The above macro was removed as it gave a false sense of a stable ABI
 * with respect to the structures size.  If you require a runtime constant,
 * you can use `PyArray_Type.tp_basicsize` instead.  Otherwise, please
 * see the PyArrayObject documentation or ask the NumPy developers for
 * information on how to correctly replace the macro in a way that is
 * compatible with multiple NumPy versions.
 */


/* Array Flags Object */
typedef struct PyArrayFlagsObject {
        PyObject_HEAD
        PyObject *arr;
        int flags;
} PyArrayFlagsObject;

/* Mirrors buffer object to ptr */

typedef struct {
        PyObject_HEAD
        PyObject *base;
        void *ptr;
        npy_intp len;
        int flags;
} PyArray_Chunk;

typedef struct {
    NPY_DATETIMEUNIT base;
    int num;
} PyArray_DatetimeMetaData;

typedef struct {
    NpyAuxData base;
    PyArray_DatetimeMetaData meta;
} PyArray_DatetimeDTypeMetaData;

/*
 * This structure contains an exploded view of a date-time value.
 * NaT is represented by year == NPY_DATETIME_NAT.
 */
typedef struct {
        npy_int64 year;
        npy_int32 month, day, hour, min, sec, us, ps, as;
} npy_datetimestruct;

/* This is not used internally. */
typedef struct {
        npy_int64 day;
        npy_int32 sec, us, ps, as;
} npy_timedeltastruct;

typedef int (PyArray_FinalizeFunc)(PyArrayObject *, PyObject *);

/*
 * Means c-style contiguous (last index varies the fastest). The data
 * elements right after each other.
 *
 * This flag may be requested in constructor functions.
 * This flag may be tested for in PyArray_FLAGS(arr).
 */
#define NPY_ARRAY_C_CONTIGUOUS    0x0001

/*
 * Set if array is a contiguous Fortran array: the first index varies
 * the fastest in memory (strides array is reverse of C-contiguous
 * array)
 *
 * This flag may be requested in constructor functions.
 * This flag may be tested for in PyArray_FLAGS(arr).
 */
#define NPY_ARRAY_F_CONTIGUOUS    0x0002

/*
 * Note: all 0-d arrays are C_CONTIGUOUS and F_CONTIGUOUS. If a
 * 1-d array is C_CONTIGUOUS it is also F_CONTIGUOUS. Arrays with
 * more then one dimension can be C_CONTIGUOUS and F_CONTIGUOUS
 * at the same time if they have either zero or one element.
 * A higher dimensional array always has the same contiguity flags as
 * `array.squeeze()`; dimensions with `array.shape[dimension] == 1` are
 * effectively ignored when checking for contiguity.
 */

/*
 * If set, the array owns the data: it will be free'd when the array
 * is deleted.
 *
 * This flag may be tested for in PyArray_FLAGS(arr).
 */
#define NPY_ARRAY_OWNDATA         0x0004

/*
 * An array never has the next four set; they're only used as parameter
 * flags to the various FromAny functions
 *
 * This flag may be requested in constructor functions.
 */

/* Cause a cast to occur regardless of whether or not it is safe. */
#define NPY_ARRAY_FORCECAST       0x0010

/*
 * Always copy the array. Returned arrays are always CONTIGUOUS,
 * ALIGNED, and WRITEABLE. See also: NPY_ARRAY_ENSURENOCOPY = 0x4000.
 *
 * This flag may be requested in constructor functions.
 */
#define NPY_ARRAY_ENSURECOPY      0x0020

/*
 * Make sure the returned array is a base-class ndarray
 *
 * This flag may be requested in constructor functions.
 */
#define NPY_ARRAY_ENSUREARRAY     0x0040

/*
 * Make sure that the strides are in units of the element size Needed
 * for some operations with record-arrays.
 *
 * This flag may be requested in constructor functions.
 */
#define NPY_ARRAY_ELEMENTSTRIDES  0x0080

/*
 * Array data is aligned on the appropriate memory address for the type
 * stored according to how the compiler would align things (e.g., an
 * array of integers (4 bytes each) starts on a memory address that's
 * a multiple of 4)
 *
 * This flag may be requested in constructor functions.
 * This flag may be tested for in PyArray_FLAGS(arr).
 */
#define NPY_ARRAY_ALIGNED         0x0100

/*
 * Array data has the native endianness
 *
 * This flag may be requested in constructor functions.
 */
#define NPY_ARRAY_NOTSWAPPED      0x0200

/*
 * Array data is writeable
 *
 * This flag may be requested in constructor functions.
 * This flag may be tested for in PyArray_FLAGS(arr).
 */
#define NPY_ARRAY_WRITEABLE       0x0400

/*
 * If this flag is set, then base contains a pointer to an array of
 * the same size that should be updated with the current contents of
 * this array when PyArray_ResolveWritebackIfCopy is called.
 *
 * This flag may be requested in constructor functions.
 * This flag may be tested for in PyArray_FLAGS(arr).
 */
#define NPY_ARRAY_WRITEBACKIFCOPY 0x2000

/*
 * No copy may be made while converting from an object/array (result is a view)
 *
 * This flag may be requested in constructor functions.
 */
#define NPY_ARRAY_ENSURENOCOPY 0x4000

/*
 * NOTE: there are also internal flags defined in multiarray/arrayobject.h,
 * which start at bit 31 and work down.
 */

#define NPY_ARRAY_BEHAVED      (NPY_ARRAY_ALIGNED | \
                                NPY_ARRAY_WRITEABLE)
#define NPY_ARRAY_BEHAVED_NS   (NPY_ARRAY_ALIGNED | \
                                NPY_ARRAY_WRITEABLE | \
                                NPY_ARRAY_NOTSWAPPED)
#define NPY_ARRAY_CARRAY       (NPY_ARRAY_C_CONTIGUOUS | \
                                NPY_ARRAY_BEHAVED)
#define NPY_ARRAY_CARRAY_RO    (NPY_ARRAY_C_CONTIGUOUS | \
                                NPY_ARRAY_ALIGNED)
#define NPY_ARRAY_FARRAY       (NPY_ARRAY_F_CONTIGUOUS | \
                                NPY_ARRAY_BEHAVED)
#define NPY_ARRAY_FARRAY_RO    (NPY_ARRAY_F_CONTIGUOUS | \
                                NPY_ARRAY_ALIGNED)
#define NPY_ARRAY_DEFAULT      (NPY_ARRAY_CARRAY)
#define NPY_ARRAY_IN_ARRAY     (NPY_ARRAY_CARRAY_RO)
#define NPY_ARRAY_OUT_ARRAY    (NPY_ARRAY_CARRAY)
#define NPY_ARRAY_INOUT_ARRAY  (NPY_ARRAY_CARRAY)
#define NPY_ARRAY_INOUT_ARRAY2 (NPY_ARRAY_CARRAY | \
                                NPY_ARRAY_WRITEBACKIFCOPY)
#define NPY_ARRAY_IN_FARRAY    (NPY_ARRAY_FARRAY_RO)
#define NPY_ARRAY_OUT_FARRAY   (NPY_ARRAY_FARRAY)
#define NPY_ARRAY_INOUT_FARRAY (NPY_ARRAY_FARRAY)
#define NPY_ARRAY_INOUT_FARRAY2 (NPY_ARRAY_FARRAY | \
                                NPY_ARRAY_WRITEBACKIFCOPY)

#define NPY_ARRAY_UPDATE_ALL   (NPY_ARRAY_C_CONTIGUOUS | \
                                NPY_ARRAY_F_CONTIGUOUS | \
                                NPY_ARRAY_ALIGNED)

/* This flag is for the array interface, not PyArrayObject */
#define NPY_ARR_HAS_DESCR  0x0800




/*
 * Size of internal buffers used for alignment Make BUFSIZE a multiple
 * of sizeof(npy_cdouble) -- usually 16 so that ufunc buffers are aligned
 */
#define NPY_MIN_BUFSIZE ((int)sizeof(npy_cdouble))
#define NPY_MAX_BUFSIZE (((int)sizeof(npy_cdouble))*1000000)
#define NPY_BUFSIZE 8192
/* buffer stress test size: */
/*#define NPY_BUFSIZE 17*/

#define PyArray_MAX(a,b) (((a)>(b))?(a):(b))
#define PyArray_MIN(a,b) (((a)<(b))?(a):(b))
#define PyArray_CLT(p,q) ((((p).real==(q).real) ? ((p).imag < (q).imag) : \
                               ((p).real < (q).real)))
#define PyArray_CGT(p,q) ((((p).real==(q).real) ? ((p).imag > (q).imag) : \
                               ((p).real > (q).real)))
#define PyArray_CLE(p,q) ((((p).real==(q).real) ? ((p).imag <= (q).imag) : \
                               ((p).real <= (q).real)))
#define PyArray_CGE(p,q) ((((p).real==(q).real) ? ((p).imag >= (q).imag) : \
                               ((p).real >= (q).real)))
#define PyArray_CEQ(p,q) (((p).real==(q).real) && ((p).imag == (q).imag))
#define PyArray_CNE(p,q) (((p).real!=(q).real) || ((p).imag != (q).imag))

/*
 * C API: consists of Macros and functions.  The MACROS are defined
 * here.
 */


#define PyArray_ISCONTIGUOUS(m) PyArray_CHKFLAGS((m), NPY_ARRAY_C_CONTIGUOUS)
#define PyArray_ISWRITEABLE(m) PyArray_CHKFLAGS((m), NPY_ARRAY_WRITEABLE)
#define PyArray_ISALIGNED(m) PyArray_CHKFLAGS((m), NPY_ARRAY_ALIGNED)

#define PyArray_IS_C_CONTIGUOUS(m) PyArray_CHKFLAGS((m), NPY_ARRAY_C_CONTIGUOUS)
#define PyArray_IS_F_CONTIGUOUS(m) PyArray_CHKFLAGS((m), NPY_ARRAY_F_CONTIGUOUS)

/* the variable is used in some places, so always define it */
#define NPY_BEGIN_THREADS_DEF PyThreadState *_save=NULL;
#if NPY_ALLOW_THREADS
#define NPY_BEGIN_ALLOW_THREADS Py_BEGIN_ALLOW_THREADS
#define NPY_END_ALLOW_THREADS Py_END_ALLOW_THREADS
#define NPY_BEGIN_THREADS do {_save = PyEval_SaveThread();} while (0);
#define NPY_END_THREADS   do { if (_save) \
                { PyEval_RestoreThread(_save); _save = NULL;} } while (0);
#define NPY_BEGIN_THREADS_THRESHOLDED(loop_size) do { if ((loop_size) > 500) \
                { _save = PyEval_SaveThread();} } while (0);

#define NPY_BEGIN_THREADS_DESCR(dtype) \
        do {if (!(PyDataType_FLAGCHK((dtype), NPY_NEEDS_PYAPI))) \
                NPY_BEGIN_THREADS;} while (0);

#define NPY_END_THREADS_DESCR(dtype) \
        do {if (!(PyDataType_FLAGCHK((dtype), NPY_NEEDS_PYAPI))) \
                NPY_END_THREADS; } while (0);

#define NPY_ALLOW_C_API_DEF  PyGILState_STATE __save__;
#define NPY_ALLOW_C_API      do {__save__ = PyGILState_Ensure();} while (0);
#define NPY_DISABLE_C_API    do {PyGILState_Release(__save__);} while (0);
#else
#define NPY_BEGIN_ALLOW_THREADS
#define NPY_END_ALLOW_THREADS
#define NPY_BEGIN_THREADS
#define NPY_END_THREADS
#define NPY_BEGIN_THREADS_THRESHOLDED(loop_size)
#define NPY_BEGIN_THREADS_DESCR(dtype)
#define NPY_END_THREADS_DESCR(dtype)
#define NPY_ALLOW_C_API_DEF
#define NPY_ALLOW_C_API
#define NPY_DISABLE_C_API
#endif

/**********************************
 * The nditer object, added in 1.6
 **********************************/

/* The actual structure of the iterator is an internal detail */
typedef struct NpyIter_InternalOnly NpyIter;

/* Iterator function pointers that may be specialized */
typedef int (NpyIter_IterNextFunc)(NpyIter *iter);
typedef void (NpyIter_GetMultiIndexFunc)(NpyIter *iter,
                                      npy_intp *outcoords);

/*** Global flags that may be passed to the iterator constructors ***/

/* Track an index representing C order */
#define NPY_ITER_C_INDEX                    0x00000001
/* Track an index representing Fortran order */
#define NPY_ITER_F_INDEX                    0x00000002
/* Track a multi-index */
#define NPY_ITER_MULTI_INDEX                0x00000004
/* User code external to the iterator does the 1-dimensional innermost loop */
#define NPY_ITER_EXTERNAL_LOOP              0x00000008
/* Convert all the operands to a common data type */
#define NPY_ITER_COMMON_DTYPE               0x00000010
/* Operands may hold references, requiring API access during iteration */
#define NPY_ITER_REFS_OK                    0x00000020
/* Zero-sized operands should be permitted, iteration checks IterSize for 0 */
#define NPY_ITER_ZEROSIZE_OK                0x00000040
/* Permits reductions (size-0 stride with dimension size > 1) */
#define NPY_ITER_REDUCE_OK                  0x00000080
/* Enables sub-range iteration */
#define NPY_ITER_RANGED                     0x00000100
/* Enables buffering */
#define NPY_ITER_BUFFERED                   0x00000200
/* When buffering is enabled, grows the inner loop if possible */
#define NPY_ITER_GROWINNER                  0x00000400
/* Delay allocation of buffers until first Reset* call */
#define NPY_ITER_DELAY_BUFALLOC             0x00000800
/* When NPY_KEEPORDER is specified, disable reversing negative-stride axes */
#define NPY_ITER_DONT_NEGATE_STRIDES        0x00001000
/*
 * If output operands overlap with other operands (based on heuristics that
 * has false positives but no false negatives), make temporary copies to
 * eliminate overlap.
 */
#define NPY_ITER_COPY_IF_OVERLAP            0x00002000

/*** Per-operand flags that may be passed to the iterator constructors ***/

/* The operand will be read from and written to */
#define NPY_ITER_READWRITE                  0x00010000
/* The operand will only be read from */
#define NPY_ITER_READONLY                   0x00020000
/* The operand will only be written to */
#define NPY_ITER_WRITEONLY                  0x00040000
/* The operand's data must be in native byte order */
#define NPY_ITER_NBO                        0x00080000
/* The operand's data must be aligned */
#define NPY_ITER_ALIGNED                    0x00100000
/* The operand's data must be contiguous (within the inner loop) */
#define NPY_ITER_CONTIG                     0x00200000
/* The operand may be copied to satisfy requirements */
#define NPY_ITER_COPY                       0x00400000
/* The operand may be copied with WRITEBACKIFCOPY to satisfy requirements */
#define NPY_ITER_UPDATEIFCOPY               0x00800000
/* Allocate the operand if it is NULL */
#define NPY_ITER_ALLOCATE                   0x01000000
/* If an operand is allocated, don't use any subtype */
#define NPY_ITER_NO_SUBTYPE                 0x02000000
/* This is a virtual array slot, operand is NULL but temporary data is there */
#define NPY_ITER_VIRTUAL                    0x04000000
/* Require that the dimension match the iterator dimensions exactly */
#define NPY_ITER_NO_BROADCAST               0x08000000
/* A mask is being used on this array, affects buffer -> array copy */
#define NPY_ITER_WRITEMASKED                0x10000000
/* This array is the mask for all WRITEMASKED operands */
#define NPY_ITER_ARRAYMASK                  0x20000000
/* Assume iterator order data access for COPY_IF_OVERLAP */
#define NPY_ITER_OVERLAP_ASSUME_ELEMENTWISE 0x40000000

#define NPY_ITER_GLOBAL_FLAGS               0x0000ffff
#define NPY_ITER_PER_OP_FLAGS               0xffff0000


/*****************************
 * Basic iterator object
 *****************************/

/* FWD declaration */
typedef struct PyArrayIterObject_tag PyArrayIterObject;

/*
 * type of the function which translates a set of coordinates to a
 * pointer to the data
 */
typedef char* (*npy_iter_get_dataptr_t)(
        PyArrayIterObject* iter, const npy_intp*);

struct PyArrayIterObject_tag {
        PyObject_HEAD
        int               nd_m1;            /* number of dimensions - 1 */
        npy_intp          index, size;
        npy_intp          coordinates[NPY_MAXDIMS];/* N-dimensional loop */
        npy_intp          dims_m1[NPY_MAXDIMS];    /* ao->dimensions - 1 */
        npy_intp          strides[NPY_MAXDIMS];    /* ao->strides or fake */
        npy_intp          backstrides[NPY_MAXDIMS];/* how far to jump back */
        npy_intp          factors[NPY_MAXDIMS];     /* shape factors */
        PyArrayObject     *ao;
        char              *dataptr;        /* pointer to current item*/
        npy_bool          contiguous;

        npy_intp          bounds[NPY_MAXDIMS][2];
        npy_intp          limits[NPY_MAXDIMS][2];
        npy_intp          limits_sizes[NPY_MAXDIMS];
        npy_iter_get_dataptr_t translate;
} ;


/* Iterator API */
#define PyArrayIter_Check(op) PyObject_TypeCheck((op), &PyArrayIter_Type)

#define _PyAIT(it) ((PyArrayIterObject *)(it))
#define PyArray_ITER_RESET(it) do { \
        _PyAIT(it)->index = 0; \
        _PyAIT(it)->dataptr = PyArray_BYTES(_PyAIT(it)->ao); \
        memset(_PyAIT(it)->coordinates, 0, \
               (_PyAIT(it)->nd_m1+1)*sizeof(npy_intp)); \
} while (0)

#define _PyArray_ITER_NEXT1(it) do { \
        (it)->dataptr += _PyAIT(it)->strides[0]; \
        (it)->coordinates[0]++; \
} while (0)

#define _PyArray_ITER_NEXT2(it) do { \
        if ((it)->coordinates[1] < (it)->dims_m1[1]) { \
                (it)->coordinates[1]++; \
                (it)->dataptr += (it)->strides[1]; \
        } \
        else { \
                (it)->coordinates[1] = 0; \
                (it)->coordinates[0]++; \
                (it)->dataptr += (it)->strides[0] - \
                        (it)->backstrides[1]; \
        } \
} while (0)

#define PyArray_ITER_NEXT(it) do { \
        _PyAIT(it)->index++; \
        if (_PyAIT(it)->nd_m1 == 0) { \
                _PyArray_ITER_NEXT1(_PyAIT(it)); \
        } \
        else if (_PyAIT(it)->contiguous) \
                _PyAIT(it)->dataptr += PyArray_DESCR(_PyAIT(it)->ao)->elsize; \
        else if (_PyAIT(it)->nd_m1 == 1) { \
                _PyArray_ITER_NEXT2(_PyAIT(it)); \
        } \
        else { \
                int __npy_i; \
                for (__npy_i=_PyAIT(it)->nd_m1; __npy_i >= 0; __npy_i--) { \
                        if (_PyAIT(it)->coordinates[__npy_i] < \
                            _PyAIT(it)->dims_m1[__npy_i]) { \
                                _PyAIT(it)->coordinates[__npy_i]++; \
                                _PyAIT(it)->dataptr += \
                                        _PyAIT(it)->strides[__npy_i]; \
                                break; \
                        } \
                        else { \
                                _PyAIT(it)->coordinates[__npy_i] = 0; \
                                _PyAIT(it)->dataptr -= \
                                        _PyAIT(it)->backstrides[__npy_i]; \
                        } \
                } \
        } \
} while (0)

#define PyArray_ITER_GOTO(it, destination) do { \
        int __npy_i; \
        _PyAIT(it)->index = 0; \
        _PyAIT(it)->dataptr = PyArray_BYTES(_PyAIT(it)->ao); \
        for (__npy_i = _PyAIT(it)->nd_m1; __npy_i>=0; __npy_i--) { \
                if (destination[__npy_i] < 0) { \
                        destination[__npy_i] += \
                                _PyAIT(it)->dims_m1[__npy_i]+1; \
                } \
                _PyAIT(it)->dataptr += destination[__npy_i] * \
                        _PyAIT(it)->strides[__npy_i]; \
                _PyAIT(it)->coordinates[__npy_i] = \
                        destination[__npy_i]; \
                _PyAIT(it)->index += destination[__npy_i] * \
                        ( __npy_i==_PyAIT(it)->nd_m1 ? 1 : \
                          _PyAIT(it)->dims_m1[__npy_i+1]+1) ; \
        } \
} while (0)

#define PyArray_ITER_GOTO1D(it, ind) do { \
        int __npy_i; \
        npy_intp __npy_ind = (npy_intp)(ind); \
        if (__npy_ind < 0) __npy_ind += _PyAIT(it)->size; \
        _PyAIT(it)->index = __npy_ind; \
        if (_PyAIT(it)->nd_m1 == 0) { \
                _PyAIT(it)->dataptr = PyArray_BYTES(_PyAIT(it)->ao) + \
                        __npy_ind * _PyAIT(it)->strides[0]; \
        } \
        else if (_PyAIT(it)->contiguous) \
                _PyAIT(it)->dataptr = PyArray_BYTES(_PyAIT(it)->ao) + \
                        __npy_ind * PyArray_DESCR(_PyAIT(it)->ao)->elsize; \
        else { \
                _PyAIT(it)->dataptr = PyArray_BYTES(_PyAIT(it)->ao); \
                for (__npy_i = 0; __npy_i<=_PyAIT(it)->nd_m1; \
                     __npy_i++) { \
                        _PyAIT(it)->coordinates[__npy_i] = \
                                (__npy_ind / _PyAIT(it)->factors[__npy_i]); \
                        _PyAIT(it)->dataptr += \
                                (__npy_ind / _PyAIT(it)->factors[__npy_i]) \
                                * _PyAIT(it)->strides[__npy_i]; \
                        __npy_ind %= _PyAIT(it)->factors[__npy_i]; \
                } \
        } \
} while (0)

#define PyArray_ITER_DATA(it) ((void *)(_PyAIT(it)->dataptr))

#define PyArray_ITER_NOTDONE(it) (_PyAIT(it)->index < _PyAIT(it)->size)


/*
 * Any object passed to PyArray_Broadcast must be binary compatible
 * with this structure.
 */

typedef struct {
        PyObject_HEAD
        int                  numiter;                 /* number of iters */
        npy_intp             size;                    /* broadcasted size */
        npy_intp             index;                   /* current index */
        int                  nd;                      /* number of dims */
        npy_intp             dimensions[NPY_MAXDIMS]; /* dimensions */
        PyArrayIterObject    *iters[NPY_MAXARGS];     /* iterators */
} PyArrayMultiIterObject;

#define _PyMIT(m) ((PyArrayMultiIterObject *)(m))
#define PyArray_MultiIter_RESET(multi) do {                                   \
        int __npy_mi;                                                         \
        _PyMIT(multi)->index = 0;                                             \
        for (__npy_mi=0; __npy_mi < _PyMIT(multi)->numiter;  __npy_mi++) {    \
                PyArray_ITER_RESET(_PyMIT(multi)->iters[__npy_mi]);           \
        }                                                                     \
} while (0)

#define PyArray_MultiIter_NEXT(multi) do {                                    \
        int __npy_mi;                                                         \
        _PyMIT(multi)->index++;                                               \
        for (__npy_mi=0; __npy_mi < _PyMIT(multi)->numiter;   __npy_mi++) {   \
                PyArray_ITER_NEXT(_PyMIT(multi)->iters[__npy_mi]);            \
        }                                                                     \
} while (0)

#define PyArray_MultiIter_GOTO(multi, dest) do {                            \
        int __npy_mi;                                                       \
        for (__npy_mi=0; __npy_mi < _PyMIT(multi)->numiter; __npy_mi++) {   \
                PyArray_ITER_GOTO(_PyMIT(multi)->iters[__npy_mi], dest);    \
        }                                                                   \
        _PyMIT(multi)->index = _PyMIT(multi)->iters[0]->index;              \
} while (0)

#define PyArray_MultiIter_GOTO1D(multi, ind) do {                          \
        int __npy_mi;                                                      \
        for (__npy_mi=0; __npy_mi < _PyMIT(multi)->numiter; __npy_mi++) {  \
                PyArray_ITER_GOTO1D(_PyMIT(multi)->iters[__npy_mi], ind);  \
        }                                                                  \
        _PyMIT(multi)->index = _PyMIT(multi)->iters[0]->index;             \
} while (0)

#define PyArray_MultiIter_DATA(multi, i)                \
        ((void *)(_PyMIT(multi)->iters[i]->dataptr))

#define PyArray_MultiIter_NEXTi(multi, i)               \
        PyArray_ITER_NEXT(_PyMIT(multi)->iters[i])

#define PyArray_MultiIter_NOTDONE(multi)                \
        (_PyMIT(multi)->index < _PyMIT(multi)->size)

/*
 * Store the information needed for fancy-indexing over an array. The
 * fields are slightly unordered to keep consec, dataptr and subspace
 * where they were originally.
 */
typedef struct {
        PyObject_HEAD
        /*
         * Multi-iterator portion --- needs to be present in this
         * order to work with PyArray_Broadcast
         */

        int                   numiter;                 /* number of index-array
                                                          iterators */
        npy_intp              size;                    /* size of broadcasted
                                                          result */
        npy_intp              index;                   /* current index */
        int                   nd;                      /* number of dims */
        npy_intp              dimensions[NPY_MAXDIMS]; /* dimensions */
        NpyIter               *outer;                  /* index objects
                                                          iterator */
        void                  *unused[NPY_MAXDIMS - 2];
        PyArrayObject         *array;
        /* Flat iterator for the indexed array. For compatibility solely. */
        PyArrayIterObject     *ait;

        /*
         * Subspace array. For binary compatibility (was an iterator,
         * but only the check for NULL should be used).
         */
        PyArrayObject         *subspace;

        /*
         * if subspace iteration, then this is the array of axes in
         * the underlying array represented by the index objects
         */
        int                   iteraxes[NPY_MAXDIMS];
        npy_intp              fancy_strides[NPY_MAXDIMS];

        /* pointer when all fancy indices are 0 */
        char                  *baseoffset;

        /*
         * after binding consec denotes at which axis the fancy axes
         * are inserted.
         */
        int                   consec;
        char                  *dataptr;

        int                   nd_fancy;
        npy_intp              fancy_dims[NPY_MAXDIMS];

        /*
         * Whether the iterator (any of the iterators) requires API.  This is
         * unused by NumPy itself; ArrayMethod flags are more precise.
         */
        int                   needs_api;

        /*
         * Extra op information.
         */
        PyArrayObject         *extra_op;
        PyArray_Descr         *extra_op_dtype;         /* desired dtype */
        npy_uint32            *extra_op_flags;         /* Iterator flags */

        NpyIter               *extra_op_iter;
        NpyIter_IterNextFunc  *extra_op_next;
        char                  **extra_op_ptrs;

        /*
         * Information about the iteration state.
         */
        NpyIter_IterNextFunc  *outer_next;
        char                  **outer_ptrs;
        npy_intp              *outer_strides;

        /*
         * Information about the subspace iterator.
         */
        NpyIter               *subspace_iter;
        NpyIter_IterNextFunc  *subspace_next;
        char                  **subspace_ptrs;
        npy_intp              *subspace_strides;

        /* Count for the external loop (which ever it is) for API iteration */
        npy_intp              iter_count;

} PyArrayMapIterObject;

enum {
    NPY_NEIGHBORHOOD_ITER_ZERO_PADDING,
    NPY_NEIGHBORHOOD_ITER_ONE_PADDING,
    NPY_NEIGHBORHOOD_ITER_CONSTANT_PADDING,
    NPY_NEIGHBORHOOD_ITER_CIRCULAR_PADDING,
    NPY_NEIGHBORHOOD_ITER_MIRROR_PADDING
};

typedef struct {
    PyObject_HEAD

    /*
     * PyArrayIterObject part: keep this in this exact order
     */
    int               nd_m1;            /* number of dimensions - 1 */
    npy_intp          index, size;
    npy_intp          coordinates[NPY_MAXDIMS];/* N-dimensional loop */
    npy_intp          dims_m1[NPY_MAXDIMS];    /* ao->dimensions - 1 */
    npy_intp          strides[NPY_MAXDIMS];    /* ao->strides or fake */
    npy_intp          backstrides[NPY_MAXDIMS];/* how far to jump back */
    npy_intp          factors[NPY_MAXDIMS];     /* shape factors */
    PyArrayObject     *ao;
    char              *dataptr;        /* pointer to current item*/
    npy_bool          contiguous;

    npy_intp          bounds[NPY_MAXDIMS][2];
    npy_intp          limits[NPY_MAXDIMS][2];
    npy_intp          limits_sizes[NPY_MAXDIMS];
    npy_iter_get_dataptr_t translate;

    /*
     * New members
     */
    npy_intp nd;

    /* Dimensions is the dimension of the array */
    npy_intp dimensions[NPY_MAXDIMS];

    /*
     * Neighborhood points coordinates are computed relatively to the
     * point pointed by _internal_iter
     */
    PyArrayIterObject* _internal_iter;
    /*
     * To keep a reference to the representation of the constant value
     * for constant padding
     */
    char* constant;

    int mode;
} PyArrayNeighborhoodIterObject;

/*
 * Neighborhood iterator API
 */

/* General: those work for any mode */
static NPY_INLINE int
PyArrayNeighborhoodIter_Reset(PyArrayNeighborhoodIterObject* iter);
static NPY_INLINE int
PyArrayNeighborhoodIter_Next(PyArrayNeighborhoodIterObject* iter);
#if 0
static NPY_INLINE int
PyArrayNeighborhoodIter_Next2D(PyArrayNeighborhoodIterObject* iter);
#endif

/*
 * Include inline implementations - functions defined there are not
 * considered public API
 */
#define NUMPY_CORE_INCLUDE_NUMPY__NEIGHBORHOOD_IMP_H_
#include "_neighborhood_iterator_imp.h"
#undef NUMPY_CORE_INCLUDE_NUMPY__NEIGHBORHOOD_IMP_H_



/* The default array type */
#define NPY_DEFAULT_TYPE NPY_DOUBLE

/*
 * All sorts of useful ways to look into a PyArrayObject. It is recommended
 * to use PyArrayObject * objects instead of always casting from PyObject *,
 * for improved type checking.
 *
 * In many cases here the macro versions of the accessors are deprecated,
 * but can't be immediately changed to inline functions because the
 * preexisting macros accept PyObject * and do automatic casts. Inline
 * functions accepting PyArrayObject * provides for some compile-time
 * checking of correctness when working with these objects in C.
 */

#define PyArray_ISONESEGMENT(m) (PyArray_CHKFLAGS(m, NPY_ARRAY_C_CONTIGUOUS) || \
                                 PyArray_CHKFLAGS(m, NPY_ARRAY_F_CONTIGUOUS))

#define PyArray_ISFORTRAN(m) (PyArray_CHKFLAGS(m, NPY_ARRAY_F_CONTIGUOUS) && \
                             (!PyArray_CHKFLAGS(m, NPY_ARRAY_C_CONTIGUOUS)))

#define PyArray_FORTRAN_IF(m) ((PyArray_CHKFLAGS(m, NPY_ARRAY_F_CONTIGUOUS) ? \
                               NPY_ARRAY_F_CONTIGUOUS : 0))

#if (defined(NPY_NO_DEPRECATED_API) && (NPY_1_7_API_VERSION <= NPY_NO_DEPRECATED_API))
/*
 * Changing access macros into functions, to allow for future hiding
 * of the internal memory layout. This later hiding will allow the 2.x series
 * to change the internal representation of arrays without affecting
 * ABI compatibility.
 */

static NPY_INLINE int
PyArray_NDIM(const PyArrayObject *arr)
{
    return ((PyArrayObject_fields *)arr)->nd;
}

static NPY_INLINE void *
PyArray_DATA(PyArrayObject *arr)
{
    return ((PyArrayObject_fields *)arr)->data;
}

static NPY_INLINE char *
PyArray_BYTES(PyArrayObject *arr)
{
    return ((PyArrayObject_fields *)arr)->data;
}

static NPY_INLINE npy_intp *
PyArray_DIMS(PyArrayObject *arr)
{
    return ((PyArrayObject_fields *)arr)->dimensions;
}

static NPY_INLINE npy_intp *
PyArray_STRIDES(PyArrayObject *arr)
{
    return ((PyArrayObject_fields *)arr)->strides;
}

static NPY_INLINE npy_intp
PyArray_DIM(const PyArrayObject *arr, int idim)
{
    return ((PyArrayObject_fields *)arr)->dimensions[idim];
}

static NPY_INLINE npy_intp
PyArray_STRIDE(const PyArrayObject *arr, int istride)
{
    return ((PyArrayObject_fields *)arr)->strides[istride];
}

static NPY_INLINE NPY_RETURNS_BORROWED_REF PyObject *
PyArray_BASE(PyArrayObject *arr)
{
    return ((PyArrayObject_fields *)arr)->base;
}

static NPY_INLINE NPY_RETURNS_BORROWED_REF PyArray_Descr *
PyArray_DESCR(PyArrayObject *arr)
{
    return ((PyArrayObject_fields *)arr)->descr;
}

static NPY_INLINE int
PyArray_FLAGS(const PyArrayObject *arr)
{
    return ((PyArrayObject_fields *)arr)->flags;
}

static NPY_INLINE npy_intp
PyArray_ITEMSIZE(const PyArrayObject *arr)
{
    return ((PyArrayObject_fields *)arr)->descr->elsize;
}

static NPY_INLINE int
PyArray_TYPE(const PyArrayObject *arr)
{
    return ((PyArrayObject_fields *)arr)->descr->type_num;
}

static NPY_INLINE int
PyArray_CHKFLAGS(const PyArrayObject *arr, int flags)
{
    return (PyArray_FLAGS(arr) & flags) == flags;
}

static NPY_INLINE PyObject *
PyArray_GETITEM(const PyArrayObject *arr, const char *itemptr)
{
    return ((PyArrayObject_fields *)arr)->descr->f->getitem(
                                        (void *)itemptr, (PyArrayObject *)arr);
}

/*
 * SETITEM should only be used if it is known that the value is a scalar
 * and of a type understood by the arrays dtype.
 * Use `PyArray_Pack` if the value may be of a different dtype.
 */
static NPY_INLINE int
PyArray_SETITEM(PyArrayObject *arr, char *itemptr, PyObject *v)
{
    return ((PyArrayObject_fields *)arr)->descr->f->setitem(v, itemptr, arr);
}

#else

/* These macros are deprecated as of NumPy 1.7. */
#define PyArray_NDIM(obj) (((PyArrayObject_fields *)(obj))->nd)
#define PyArray_BYTES(obj) (((PyArrayObject_fields *)(obj))->data)
#define PyArray_DATA(obj) ((void *)((PyArrayObject_fields *)(obj))->data)
#define PyArray_DIMS(obj) (((PyArrayObject_fields *)(obj))->dimensions)
#define PyArray_STRIDES(obj) (((PyArrayObject_fields *)(obj))->strides)
#define PyArray_DIM(obj,n) (PyArray_DIMS(obj)[n])
#define PyArray_STRIDE(obj,n) (PyArray_STRIDES(obj)[n])
#define PyArray_BASE(obj) (((PyArrayObject_fields *)(obj))->base)
#define PyArray_DESCR(obj) (((PyArrayObject_fields *)(obj))->descr)
#define PyArray_FLAGS(obj) (((PyArrayObject_fields *)(obj))->flags)
#define PyArray_CHKFLAGS(m, FLAGS) \
        ((((PyArrayObject_fields *)(m))->flags & (FLAGS)) == (FLAGS))
#define PyArray_ITEMSIZE(obj) \
                    (((PyArrayObject_fields *)(obj))->descr->elsize)
#define PyArray_TYPE(obj) \
                    (((PyArrayObject_fields *)(obj))->descr->type_num)
#define PyArray_GETITEM(obj,itemptr) \
        PyArray_DESCR(obj)->f->getitem((char *)(itemptr), \
                                     (PyArrayObject *)(obj))

#define PyArray_SETITEM(obj,itemptr,v) \
        PyArray_DESCR(obj)->f->setitem((PyObject *)(v), \
                                     (char *)(itemptr), \
                                     (PyArrayObject *)(obj))
#endif

static NPY_INLINE PyArray_Descr *
PyArray_DTYPE(PyArrayObject *arr)
{
    return ((PyArrayObject_fields *)arr)->descr;
}

static NPY_INLINE npy_intp *
PyArray_SHAPE(PyArrayObject *arr)
{
    return ((PyArrayObject_fields *)arr)->dimensions;
}

/*
 * Enables the specified array flags. Does no checking,
 * assumes you know what you're doing.
 */
static NPY_INLINE void
PyArray_ENABLEFLAGS(PyArrayObject *arr, int flags)
{
    ((PyArrayObject_fields *)arr)->flags |= flags;
}

/*
 * Clears the specified array flags. Does no checking,
 * assumes you know what you're doing.
 */
static NPY_INLINE void
PyArray_CLEARFLAGS(PyArrayObject *arr, int flags)
{
    ((PyArrayObject_fields *)arr)->flags &= ~flags;
}

static NPY_INLINE NPY_RETURNS_BORROWED_REF PyObject *
PyArray_HANDLER(PyArrayObject *arr)
{
    return ((PyArrayObject_fields *)arr)->mem_handler;
}

#define PyTypeNum_ISBOOL(type) ((type) == NPY_BOOL)

#define PyTypeNum_ISUNSIGNED(type) (((type) == NPY_UBYTE) ||   \
                                 ((type) == NPY_USHORT) ||     \
                                 ((type) == NPY_UINT) ||       \
                                 ((type) == NPY_ULONG) ||      \
                                 ((type) == NPY_ULONGLONG))

#define PyTypeNum_ISSIGNED(type) (((type) == NPY_BYTE) ||      \
                               ((type) == NPY_SHORT) ||        \
                               ((type) == NPY_INT) ||          \
                               ((type) == NPY_LONG) ||         \
                               ((type) == NPY_LONGLONG))

#define PyTypeNum_ISINTEGER(type) (((type) >= NPY_BYTE) &&     \
                                ((type) <= NPY_ULONGLONG))

#define PyTypeNum_ISFLOAT(type) ((((type) >= NPY_FLOAT) && \
                              ((type) <= NPY_LONGDOUBLE)) || \
                              ((type) == NPY_HALF))

#define PyTypeNum_ISNUMBER(type) (((type) <= NPY_CLONGDOUBLE) || \
                                  ((type) == NPY_HALF))

#define PyTypeNum_ISSTRING(type) (((type) == NPY_STRING) ||    \
                                  ((type) == NPY_UNICODE))

#define PyTypeNum_ISCOMPLEX(type) (((type) >= NPY_CFLOAT) &&   \
                                ((type) <= NPY_CLONGDOUBLE))

#define PyTypeNum_ISPYTHON(type) (((type) == NPY_LONG) ||      \
                                  ((type) == NPY_DOUBLE) ||    \
                                  ((type) == NPY_CDOUBLE) ||   \
                                  ((type) == NPY_BOOL) ||      \
                                  ((type) == NPY_OBJECT ))

#define PyTypeNum_ISFLEXIBLE(type) (((type) >=NPY_STRING) &&  \
                                    ((type) <=NPY_VOID))

#define PyTypeNum_ISDATETIME(type) (((type) >=NPY_DATETIME) &&  \
                                    ((type) <=NPY_TIMEDELTA))

#define PyTypeNum_ISUSERDEF(type) (((type) >= NPY_USERDEF) && \
                                   ((type) < NPY_USERDEF+     \
                                    NPY_NUMUSERTYPES))

#define PyTypeNum_ISEXTENDED(type) (PyTypeNum_ISFLEXIBLE(type) ||  \
                                    PyTypeNum_ISUSERDEF(type))

#define PyTypeNum_ISOBJECT(type) ((type) == NPY_OBJECT)


#define PyDataType_ISBOOL(obj) PyTypeNum_ISBOOL(((PyArray_Descr*)(obj))->type_num)
#define PyDataType_ISUNSIGNED(obj) PyTypeNum_ISUNSIGNED(((PyArray_Descr*)(obj))->type_num)
#define PyDataType_ISSIGNED(obj) PyTypeNum_ISSIGNED(((PyArray_Descr*)(obj))->type_num)
#define PyDataType_ISINTEGER(obj) PyTypeNum_ISINTEGER(((PyArray_Descr*)(obj))->type_num )
#define PyDataType_ISFLOAT(obj) PyTypeNum_ISFLOAT(((PyArray_Descr*)(obj))->type_num)
#define PyDataType_ISNUMBER(obj) PyTypeNum_ISNUMBER(((PyArray_Descr*)(obj))->type_num)
#define PyDataType_ISSTRING(obj) PyTypeNum_ISSTRING(((PyArray_Descr*)(obj))->type_num)
#define PyDataType_ISCOMPLEX(obj) PyTypeNum_ISCOMPLEX(((PyArray_Descr*)(obj))->type_num)
#define PyDataType_ISPYTHON(obj) PyTypeNum_ISPYTHON(((PyArray_Descr*)(obj))->type_num)
#define PyDataType_ISFLEXIBLE(obj) PyTypeNum_ISFLEXIBLE(((PyArray_Descr*)(obj))->type_num)
#define PyDataType_ISDATETIME(obj) PyTypeNum_ISDATETIME(((PyArray_Descr*)(obj))->type_num)
#define PyDataType_ISUSERDEF(obj) PyTypeNum_ISUSERDEF(((PyArray_Descr*)(obj))->type_num)
#define PyDataType_ISEXTENDED(obj) PyTypeNum_ISEXTENDED(((PyArray_Descr*)(obj))->type_num)
#define PyDataType_ISOBJECT(obj) PyTypeNum_ISOBJECT(((PyArray_Descr*)(obj))->type_num)
#define PyDataType_HASFIELDS(obj) (((PyArray_Descr *)(obj))->names != NULL)
#define PyDataType_HASSUBARRAY(dtype) ((dtype)->subarray != NULL)
#define PyDataType_ISUNSIZED(dtype) ((dtype)->elsize == 0 && \
                                      !PyDataType_HASFIELDS(dtype))
#define PyDataType_MAKEUNSIZED(dtype) ((dtype)->elsize = 0)

#define PyArray_ISBOOL(obj) PyTypeNum_ISBOOL(PyArray_TYPE(obj))
#define PyArray_ISUNSIGNED(obj) PyTypeNum_ISUNSIGNED(PyArray_TYPE(obj))
#define PyArray_ISSIGNED(obj) PyTypeNum_ISSIGNED(PyArray_TYPE(obj))
#define PyArray_ISINTEGER(obj) PyTypeNum_ISINTEGER(PyArray_TYPE(obj))
#define PyArray_ISFLOAT(obj) PyTypeNum_ISFLOAT(PyArray_TYPE(obj))
#define PyArray_ISNUMBER(obj) PyTypeNum_ISNUMBER(PyArray_TYPE(obj))
#define PyArray_ISSTRING(obj) PyTypeNum_ISSTRING(PyArray_TYPE(obj))
#define PyArray_ISCOMPLEX(obj) PyTypeNum_ISCOMPLEX(PyArray_TYPE(obj))
#define PyArray_ISPYTHON(obj) PyTypeNum_ISPYTHON(PyArray_TYPE(obj))
#define PyArray_ISFLEXIBLE(obj) PyTypeNum_ISFLEXIBLE(PyArray_TYPE(obj))
#define PyArray_ISDATETIME(obj) PyTypeNum_ISDATETIME(PyArray_TYPE(obj))
#define PyArray_ISUSERDEF(obj) PyTypeNum_ISUSERDEF(PyArray_TYPE(obj))
#define PyArray_ISEXTENDED(obj) PyTypeNum_ISEXTENDED(PyArray_TYPE(obj))
#define PyArray_ISOBJECT(obj) PyTypeNum_ISOBJECT(PyArray_TYPE(obj))
#define PyArray_HASFIELDS(obj) PyDataType_HASFIELDS(PyArray_DESCR(obj))

    /*
     * FIXME: This should check for a flag on the data-type that
     * states whether or not it is variable length.  Because the
     * ISFLEXIBLE check is hard-coded to the built-in data-types.
     */
#define PyArray_ISVARIABLE(obj) PyTypeNum_ISFLEXIBLE(PyArray_TYPE(obj))

#define PyArray_SAFEALIGNEDCOPY(obj) (PyArray_ISALIGNED(obj) && !PyArray_ISVARIABLE(obj))


#define NPY_LITTLE '<'
#define NPY_BIG '>'
#define NPY_NATIVE '='
#define NPY_SWAP 's'
#define NPY_IGNORE '|'

#if NPY_BYTE_ORDER == NPY_BIG_ENDIAN
#define NPY_NATBYTE NPY_BIG
#define NPY_OPPBYTE NPY_LITTLE
#else
#define NPY_NATBYTE NPY_LITTLE
#define NPY_OPPBYTE NPY_BIG
#endif

#define PyArray_ISNBO(arg) ((arg) != NPY_OPPBYTE)
#define PyArray_IsNativeByteOrder PyArray_ISNBO
#define PyArray_ISNOTSWAPPED(m) PyArray_ISNBO(PyArray_DESCR(m)->byteorder)
#define PyArray_ISBYTESWAPPED(m) (!PyArray_ISNOTSWAPPED(m))

#define PyArray_FLAGSWAP(m, flags) (PyArray_CHKFLAGS(m, flags) &&       \
                                    PyArray_ISNOTSWAPPED(m))

#define PyArray_ISCARRAY(m) PyArray_FLAGSWAP(m, NPY_ARRAY_CARRAY)
#define PyArray_ISCARRAY_RO(m) PyArray_FLAGSWAP(m, NPY_ARRAY_CARRAY_RO)
#define PyArray_ISFARRAY(m) PyArray_FLAGSWAP(m, NPY_ARRAY_FARRAY)
#define PyArray_ISFARRAY_RO(m) PyArray_FLAGSWAP(m, NPY_ARRAY_FARRAY_RO)
#define PyArray_ISBEHAVED(m) PyArray_FLAGSWAP(m, NPY_ARRAY_BEHAVED)
#define PyArray_ISBEHAVED_RO(m) PyArray_FLAGSWAP(m, NPY_ARRAY_ALIGNED)


#define PyDataType_ISNOTSWAPPED(d) PyArray_ISNBO(((PyArray_Descr *)(d))->byteorder)
#define PyDataType_ISBYTESWAPPED(d) (!PyDataType_ISNOTSWAPPED(d))

/************************************************************
 * A struct used by PyArray_CreateSortedStridePerm, new in 1.7.
 ************************************************************/

typedef struct {
    npy_intp perm, stride;
} npy_stride_sort_item;

/************************************************************
 * This is the form of the struct that's stored in the
 * PyCapsule returned by an array's __array_struct__ attribute. See
 * https://docs.scipy.org/doc/numpy/reference/arrays.interface.html for the full
 * documentation.
 ************************************************************/
typedef struct {
    int two;              /*
                           * contains the integer 2 as a sanity
                           * check
                           */

    int nd;               /* number of dimensions */

    char typekind;        /*
                           * kind in array --- character code of
                           * typestr
                           */

    int itemsize;         /* size of each element */

    int flags;            /*
                           * how should be data interpreted. Valid
                           * flags are CONTIGUOUS (1), F_CONTIGUOUS (2),
                           * ALIGNED (0x100), NOTSWAPPED (0x200), and
                           * WRITEABLE (0x400).  ARR_HAS_DESCR (0x800)
                           * states that arrdescr field is present in
                           * structure
                           */

    npy_intp *shape;       /*
                            * A length-nd array of shape
                            * information
                            */

    npy_intp *strides;    /* A length-nd array of stride information */

    void *data;           /* A pointer to the first element of the array */

    PyObject *descr;      /*
                           * A list of fields or NULL (ignored if flags
                           * does not have ARR_HAS_DESCR flag set)
                           */
} PyArrayInterface;

/*
 * This is a function for hooking into the PyDataMem_NEW/FREE/RENEW functions.
 * See the documentation for PyDataMem_SetEventHook.
 */
typedef void (PyDataMem_EventHookFunc)(void *inp, void *outp, size_t size,
                                       void *user_data);


/*
 * PyArray_DTypeMeta related definitions.
 *
 * As of now, this API is preliminary and will be extended as necessary.
 */
#if defined(NPY_INTERNAL_BUILD) && NPY_INTERNAL_BUILD
    /*
     * The Structures defined in this block are currently considered
     * private API and may change without warning!
     * Part of this (at least the size) is expected to be public API without
     * further modifications.
     */
    /* TODO: Make this definition public in the API, as soon as its settled */
    NPY_NO_EXPORT extern PyTypeObject PyArrayDTypeMeta_Type;

    /*
     * While NumPy DTypes would not need to be heap types the plan is to
     * make DTypes available in Python at which point they will be heap types.
     * Since we also wish to add fields to the DType class, this looks like
     * a typical instance definition, but with PyHeapTypeObject instead of
     * only the PyObject_HEAD.
     * This must only be exposed very extremely careful consideration, since
     * it is a fairly complex construct which may be better to allow
     * refactoring of.
     */
    typedef struct {
        PyHeapTypeObject super;

        /*
         * Most DTypes will have a singleton default instance, for the
         * parametric legacy DTypes (bytes, string, void, datetime) this
         * may be a pointer to the *prototype* instance?
         */
        PyArray_Descr *singleton;
        /* Copy of the legacy DTypes type number, usually invalid. */
        int type_num;

        /* The type object of the scalar instances (may be NULL?) */
        PyTypeObject *scalar_type;
        /*
         * DType flags to signal legacy, parametric, or
         * abstract.  But plenty of space for additional information/flags.
         */
        npy_uint64 flags;

        /*
         * Use indirection in order to allow a fixed size for this struct.
         * A stable ABI size makes creating a static DType less painful
         * while also ensuring flexibility for all opaque API (with one
         * indirection due the pointer lookup).
         */
        void *dt_slots;
        void *reserved[3];
    } PyArray_DTypeMeta;

#endif  /* NPY_INTERNAL_BUILD */


/*
 * Use the keyword NPY_DEPRECATED_INCLUDES to ensure that the header files
 * npy_*_*_deprecated_api.h are only included from here and nowhere else.
 */
#ifdef NPY_DEPRECATED_INCLUDES
#error "Do not use the reserved keyword NPY_DEPRECATED_INCLUDES."
#endif
#define NPY_DEPRECATED_INCLUDES
#if !defined(NPY_NO_DEPRECATED_API) || \
    (NPY_NO_DEPRECATED_API < NPY_1_7_API_VERSION)
#include "npy_1_7_deprecated_api.h"
#endif
/*
 * There is no file npy_1_8_deprecated_api.h since there are no additional
 * deprecated API features in NumPy 1.8.
 *
 * Note to maintainers: insert code like the following in future NumPy
 * versions.
 *
 * #if !defined(NPY_NO_DEPRECATED_API) || \
 *     (NPY_NO_DEPRECATED_API < NPY_1_9_API_VERSION)
 * #include "npy_1_9_deprecated_api.h"
 * #endif
 */
#undef NPY_DEPRECATED_INCLUDES

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_NDARRAYTYPES_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/_neighborhood_iterator_imp.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY__NEIGHBORHOOD_IMP_H_
#error You should not include this header directly
#endif
/*
 * Private API (here for inline)
 */
static NPY_INLINE int
_PyArrayNeighborhoodIter_IncrCoord(PyArrayNeighborhoodIterObject* iter);

/*
 * Update to next item of the iterator
 *
 * Note: this simply increment the coordinates vector, last dimension
 * incremented first , i.e, for dimension 3
 * ...
 * -1, -1, -1
 * -1, -1,  0
 * -1, -1,  1
 *  ....
 * -1,  0, -1
 * -1,  0,  0
 *  ....
 * 0,  -1, -1
 * 0,  -1,  0
 *  ....
 */
#define _UPDATE_COORD_ITER(c) \
    wb = iter->coordinates[c] < iter->bounds[c][1]; \
    if (wb) { \
        iter->coordinates[c] += 1; \
        return 0; \
    } \
    else { \
        iter->coordinates[c] = iter->bounds[c][0]; \
    }

static NPY_INLINE int
_PyArrayNeighborhoodIter_IncrCoord(PyArrayNeighborhoodIterObject* iter)
{
    npy_intp i, wb;

    for (i = iter->nd - 1; i >= 0; --i) {
        _UPDATE_COORD_ITER(i)
    }

    return 0;
}

/*
 * Version optimized for 2d arrays, manual loop unrolling
 */
static NPY_INLINE int
_PyArrayNeighborhoodIter_IncrCoord2D(PyArrayNeighborhoodIterObject* iter)
{
    npy_intp wb;

    _UPDATE_COORD_ITER(1)
    _UPDATE_COORD_ITER(0)

    return 0;
}
#undef _UPDATE_COORD_ITER

/*
 * Advance to the next neighbour
 */
static NPY_INLINE int
PyArrayNeighborhoodIter_Next(PyArrayNeighborhoodIterObject* iter)
{
    _PyArrayNeighborhoodIter_IncrCoord (iter);
    iter->dataptr = iter->translate((PyArrayIterObject*)iter, iter->coordinates);

    return 0;
}

/*
 * Reset functions
 */
static NPY_INLINE int
PyArrayNeighborhoodIter_Reset(PyArrayNeighborhoodIterObject* iter)
{
    npy_intp i;

    for (i = 0; i < iter->nd; ++i) {
        iter->coordinates[i] = iter->bounds[i][0];
    }
    iter->dataptr = iter->translate((PyArrayIterObject*)iter, iter->coordinates);

    return 0;
}
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/noprefix.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY_NOPREFIX_H_
#define NUMPY_CORE_INCLUDE_NUMPY_NOPREFIX_H_

/*
 * You can directly include noprefix.h as a backward
 * compatibility measure
 */
#ifndef NPY_NO_PREFIX
#include "ndarrayobject.h"
#include "npy_interrupt.h"
#endif

#define SIGSETJMP   NPY_SIGSETJMP
#define SIGLONGJMP  NPY_SIGLONGJMP
#define SIGJMP_BUF  NPY_SIGJMP_BUF

#define MAX_DIMS NPY_MAXDIMS

#define longlong    npy_longlong
#define ulonglong   npy_ulonglong
#define Bool        npy_bool
#define longdouble  npy_longdouble
#define byte        npy_byte

#ifndef _BSD_SOURCE
#define ushort      npy_ushort
#define uint        npy_uint
#define ulong       npy_ulong
#endif

#define ubyte       npy_ubyte
#define ushort      npy_ushort
#define uint        npy_uint
#define ulong       npy_ulong
#define cfloat      npy_cfloat
#define cdouble     npy_cdouble
#define clongdouble npy_clongdouble
#define Int8        npy_int8
#define UInt8       npy_uint8
#define Int16       npy_int16
#define UInt16      npy_uint16
#define Int32       npy_int32
#define UInt32      npy_uint32
#define Int64       npy_int64
#define UInt64      npy_uint64
#define Int128      npy_int128
#define UInt128     npy_uint128
#define Int256      npy_int256
#define UInt256     npy_uint256
#define Float16     npy_float16
#define Complex32   npy_complex32
#define Float32     npy_float32
#define Complex64   npy_complex64
#define Float64     npy_float64
#define Complex128  npy_complex128
#define Float80     npy_float80
#define Complex160  npy_complex160
#define Float96     npy_float96
#define Complex192  npy_complex192
#define Float128    npy_float128
#define Complex256  npy_complex256
#define intp        npy_intp
#define uintp       npy_uintp
#define datetime    npy_datetime
#define timedelta   npy_timedelta

#define SIZEOF_LONGLONG         NPY_SIZEOF_LONGLONG
#define SIZEOF_INTP             NPY_SIZEOF_INTP
#define SIZEOF_UINTP            NPY_SIZEOF_UINTP
#define SIZEOF_HALF             NPY_SIZEOF_HALF
#define SIZEOF_LONGDOUBLE       NPY_SIZEOF_LONGDOUBLE
#define SIZEOF_DATETIME         NPY_SIZEOF_DATETIME
#define SIZEOF_TIMEDELTA        NPY_SIZEOF_TIMEDELTA

#define LONGLONG_FMT NPY_LONGLONG_FMT
#define ULONGLONG_FMT NPY_ULONGLONG_FMT
#define LONGLONG_SUFFIX NPY_LONGLONG_SUFFIX
#define ULONGLONG_SUFFIX NPY_ULONGLONG_SUFFIX

#define MAX_INT8 127
#define MIN_INT8 -128
#define MAX_UINT8 255
#define MAX_INT16 32767
#define MIN_INT16 -32768
#define MAX_UINT16 65535
#define MAX_INT32 2147483647
#define MIN_INT32 (-MAX_INT32 - 1)
#define MAX_UINT32 4294967295U
#define MAX_INT64 LONGLONG_SUFFIX(9223372036854775807)
#define MIN_INT64 (-MAX_INT64 - LONGLONG_SUFFIX(1))
#define MAX_UINT64 ULONGLONG_SUFFIX(18446744073709551615)
#define MAX_INT128 LONGLONG_SUFFIX(85070591730234615865843651857942052864)
#define MIN_INT128 (-MAX_INT128 - LONGLONG_SUFFIX(1))
#define MAX_UINT128 ULONGLONG_SUFFIX(170141183460469231731687303715884105728)
#define MAX_INT256 LONGLONG_SUFFIX(57896044618658097711785492504343953926634992332820282019728792003956564819967)
#define MIN_INT256 (-MAX_INT256 - LONGLONG_SUFFIX(1))
#define MAX_UINT256 ULONGLONG_SUFFIX(115792089237316195423570985008687907853269984665640564039457584007913129639935)

#define MAX_BYTE NPY_MAX_BYTE
#define MIN_BYTE NPY_MIN_BYTE
#define MAX_UBYTE NPY_MAX_UBYTE
#define MAX_SHORT NPY_MAX_SHORT
#define MIN_SHORT NPY_MIN_SHORT
#define MAX_USHORT NPY_MAX_USHORT
#define MAX_INT   NPY_MAX_INT
#define MIN_INT   NPY_MIN_INT
#define MAX_UINT  NPY_MAX_UINT
#define MAX_LONG  NPY_MAX_LONG
#define MIN_LONG  NPY_MIN_LONG
#define MAX_ULONG  NPY_MAX_ULONG
#define MAX_LONGLONG NPY_MAX_LONGLONG
#define MIN_LONGLONG NPY_MIN_LONGLONG
#define MAX_ULONGLONG NPY_MAX_ULONGLONG
#define MIN_DATETIME NPY_MIN_DATETIME
#define MAX_DATETIME NPY_MAX_DATETIME
#define MIN_TIMEDELTA NPY_MIN_TIMEDELTA
#define MAX_TIMEDELTA NPY_MAX_TIMEDELTA

#define BITSOF_BOOL       NPY_BITSOF_BOOL
#define BITSOF_CHAR       NPY_BITSOF_CHAR
#define BITSOF_SHORT      NPY_BITSOF_SHORT
#define BITSOF_INT        NPY_BITSOF_INT
#define BITSOF_LONG       NPY_BITSOF_LONG
#define BITSOF_LONGLONG   NPY_BITSOF_LONGLONG
#define BITSOF_HALF       NPY_BITSOF_HALF
#define BITSOF_FLOAT      NPY_BITSOF_FLOAT
#define BITSOF_DOUBLE     NPY_BITSOF_DOUBLE
#define BITSOF_LONGDOUBLE NPY_BITSOF_LONGDOUBLE
#define BITSOF_DATETIME   NPY_BITSOF_DATETIME
#define BITSOF_TIMEDELTA   NPY_BITSOF_TIMEDELTA

#define _pya_malloc PyArray_malloc
#define _pya_free PyArray_free
#define _pya_realloc PyArray_realloc

#define BEGIN_THREADS_DEF NPY_BEGIN_THREADS_DEF
#define BEGIN_THREADS     NPY_BEGIN_THREADS
#define END_THREADS       NPY_END_THREADS
#define ALLOW_C_API_DEF   NPY_ALLOW_C_API_DEF
#define ALLOW_C_API       NPY_ALLOW_C_API
#define DISABLE_C_API     NPY_DISABLE_C_API

#define PY_FAIL NPY_FAIL
#define PY_SUCCEED NPY_SUCCEED

#ifndef TRUE
#define TRUE NPY_TRUE
#endif

#ifndef FALSE
#define FALSE NPY_FALSE
#endif

#define LONGDOUBLE_FMT NPY_LONGDOUBLE_FMT

#define CONTIGUOUS         NPY_CONTIGUOUS
#define C_CONTIGUOUS       NPY_C_CONTIGUOUS
#define FORTRAN            NPY_FORTRAN
#define F_CONTIGUOUS       NPY_F_CONTIGUOUS
#define OWNDATA            NPY_OWNDATA
#define FORCECAST          NPY_FORCECAST
#define ENSURECOPY         NPY_ENSURECOPY
#define ENSUREARRAY        NPY_ENSUREARRAY
#define ELEMENTSTRIDES     NPY_ELEMENTSTRIDES
#define ALIGNED            NPY_ALIGNED
#define NOTSWAPPED         NPY_NOTSWAPPED
#define WRITEABLE          NPY_WRITEABLE
#define WRITEBACKIFCOPY    NPY_ARRAY_WRITEBACKIFCOPY
#define ARR_HAS_DESCR      NPY_ARR_HAS_DESCR
#define BEHAVED            NPY_BEHAVED
#define BEHAVED_NS         NPY_BEHAVED_NS
#define CARRAY             NPY_CARRAY
#define CARRAY_RO          NPY_CARRAY_RO
#define FARRAY             NPY_FARRAY
#define FARRAY_RO          NPY_FARRAY_RO
#define DEFAULT            NPY_DEFAULT
#define IN_ARRAY           NPY_IN_ARRAY
#define OUT_ARRAY          NPY_OUT_ARRAY
#define INOUT_ARRAY        NPY_INOUT_ARRAY
#define IN_FARRAY          NPY_IN_FARRAY
#define OUT_FARRAY         NPY_OUT_FARRAY
#define INOUT_FARRAY       NPY_INOUT_FARRAY
#define UPDATE_ALL         NPY_UPDATE_ALL

#define OWN_DATA          NPY_OWNDATA
#define BEHAVED_FLAGS     NPY_BEHAVED
#define BEHAVED_FLAGS_NS  NPY_BEHAVED_NS
#define CARRAY_FLAGS_RO   NPY_CARRAY_RO
#define CARRAY_FLAGS      NPY_CARRAY
#define FARRAY_FLAGS      NPY_FARRAY
#define FARRAY_FLAGS_RO   NPY_FARRAY_RO
#define DEFAULT_FLAGS     NPY_DEFAULT
#define UPDATE_ALL_FLAGS  NPY_UPDATE_ALL_FLAGS

#ifndef MIN
#define MIN PyArray_MIN
#endif
#ifndef MAX
#define MAX PyArray_MAX
#endif
#define MAX_INTP NPY_MAX_INTP
#define MIN_INTP NPY_MIN_INTP
#define MAX_UINTP NPY_MAX_UINTP
#define INTP_FMT NPY_INTP_FMT

#ifndef PYPY_VERSION
#define REFCOUNT PyArray_REFCOUNT
#define MAX_ELSIZE NPY_MAX_ELSIZE
#endif

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_NOPREFIX_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h

```plaintext
#ifndef NPY_DEPRECATED_INCLUDES
#error "Should never include npy_*_*_deprecated_api directly."
#endif

#ifndef NUMPY_CORE_INCLUDE_NUMPY_NPY_1_7_DEPRECATED_API_H_
#define NUMPY_CORE_INCLUDE_NUMPY_NPY_1_7_DEPRECATED_API_H_

/* Emit a warning if the user did not specifically request the old API */
#ifndef NPY_NO_DEPRECATED_API
#if defined(_WIN32)
#define _WARN___STR2__(x) #x
#define _WARN___STR1__(x) _WARN___STR2__(x)
#define _WARN___LOC__ __FILE__ "(" _WARN___STR1__(__LINE__) ") : Warning Msg: "
#pragma message(_WARN___LOC__"Using deprecated NumPy API, disable it with " \
                         "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION")
#else
#warning "Using deprecated NumPy API, disable it with " \
         "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION"
#endif
#endif

/*
 * This header exists to collect all dangerous/deprecated NumPy API
 * as of NumPy 1.7.
 *
 * This is an attempt to remove bad API, the proliferation of macros,
 * and namespace pollution currently produced by the NumPy headers.
 */

/* These array flags are deprecated as of NumPy 1.7 */
#define NPY_CONTIGUOUS NPY_ARRAY_C_CONTIGUOUS
#define NPY_FORTRAN NPY_ARRAY_F_CONTIGUOUS

/*
 * The consistent NPY_ARRAY_* names which don't pollute the NPY_*
 * namespace were added in NumPy 1.7.
 *
 * These versions of the carray flags are deprecated, but
 * probably should only be removed after two releases instead of one.
 */
#define NPY_C_CONTIGUOUS   NPY_ARRAY_C_CONTIGUOUS
#define NPY_F_CONTIGUOUS   NPY_ARRAY_F_CONTIGUOUS
#define NPY_OWNDATA        NPY_ARRAY_OWNDATA
#define NPY_FORCECAST      NPY_ARRAY_FORCECAST
#define NPY_ENSURECOPY     NPY_ARRAY_ENSURECOPY
#define NPY_ENSUREARRAY    NPY_ARRAY_ENSUREARRAY
#define NPY_ELEMENTSTRIDES NPY_ARRAY_ELEMENTSTRIDES
#define NPY_ALIGNED        NPY_ARRAY_ALIGNED
#define NPY_NOTSWAPPED     NPY_ARRAY_NOTSWAPPED
#define NPY_WRITEABLE      NPY_ARRAY_WRITEABLE
#define NPY_BEHAVED        NPY_ARRAY_BEHAVED
#define NPY_BEHAVED_NS     NPY_ARRAY_BEHAVED_NS
#define NPY_CARRAY         NPY_ARRAY_CARRAY
#define NPY_CARRAY_RO      NPY_ARRAY_CARRAY_RO
#define NPY_FARRAY         NPY_ARRAY_FARRAY
#define NPY_FARRAY_RO      NPY_ARRAY_FARRAY_RO
#define NPY_DEFAULT        NPY_ARRAY_DEFAULT
#define NPY_IN_ARRAY       NPY_ARRAY_IN_ARRAY
#define NPY_OUT_ARRAY      NPY_ARRAY_OUT_ARRAY
#define NPY_INOUT_ARRAY    NPY_ARRAY_INOUT_ARRAY
#define NPY_IN_FARRAY      NPY_ARRAY_IN_FARRAY
#define NPY_OUT_FARRAY     NPY_ARRAY_OUT_FARRAY
#define NPY_INOUT_FARRAY   NPY_ARRAY_INOUT_FARRAY
#define NPY_UPDATE_ALL     NPY_ARRAY_UPDATE_ALL

/* This way of accessing the default type is deprecated as of NumPy 1.7 */
#define PyArray_DEFAULT NPY_DEFAULT_TYPE

/* These DATETIME bits aren't used internally */
#define PyDataType_GetDatetimeMetaData(descr)                                 \
    ((descr->metadata == NULL) ? NULL :                                       \
        ((PyArray_DatetimeMetaData *)(PyCapsule_GetPointer(                   \
                PyDict_GetItemString(                                         \
                    descr->metadata, NPY_METADATA_DTSTR), NULL))))

/*
 * Deprecated as of NumPy 1.7, this kind of shortcut doesn't
 * belong in the public API.
 */
#define NPY_AO PyArrayObject

/*
 * Deprecated as of NumPy 1.7, an all-lowercase macro doesn't
 * belong in the public API.
 */
#define fortran fortran_

/*
 * Deprecated as of NumPy 1.7, as it is a namespace-polluting
 * macro.
 */
#define FORTRAN_IF PyArray_FORTRAN_IF

/* Deprecated as of NumPy 1.7, datetime64 uses c_metadata instead */
#define NPY_METADATA_DTSTR "__timeunit__"

/*
 * Deprecated as of NumPy 1.7.
 * The reasoning:
 *  - These are for datetime, but there's no datetime "namespace".
 *  - They just turn NPY_STR_<x> into "<x>", which is just
 *    making something simple be indirected.
 */
#define NPY_STR_Y "Y"
#define NPY_STR_M "M"
#define NPY_STR_W "W"
#define NPY_STR_D "D"
#define NPY_STR_h "h"
#define NPY_STR_m "m"
#define NPY_STR_s "s"
#define NPY_STR_ms "ms"
#define NPY_STR_us "us"
#define NPY_STR_ns "ns"
#define NPY_STR_ps "ps"
#define NPY_STR_fs "fs"
#define NPY_STR_as "as"

/*
 * The macros in old_defines.h are Deprecated as of NumPy 1.7 and will be
 * removed in the next major release.
 */
#include "old_defines.h"

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_NPY_1_7_DEPRECATED_API_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/npy_3kcompat.h

```plaintext
/*
 * This is a convenience header file providing compatibility utilities
 * for supporting different minor versions of Python 3.
 * It was originally used to support the transition from Python 2,
 * hence the "3k" naming.
 *
 * If you want to use this for your own projects, it's recommended to make a
 * copy of it. Although the stuff below is unlikely to change, we don't provide
 * strong backwards compatibility guarantees at the moment.
 */

#ifndef NUMPY_CORE_INCLUDE_NUMPY_NPY_3KCOMPAT_H_
#define NUMPY_CORE_INCLUDE_NUMPY_NPY_3KCOMPAT_H_

#include <Python.h>
#include <stdio.h>

#ifndef NPY_PY3K
#define NPY_PY3K 1
#endif

#include "numpy/npy_common.h"
#include "numpy/ndarrayobject.h"

#ifdef __cplusplus
extern "C" {
#endif

/*
 * PyInt -> PyLong
 */


/*
 * This is a renamed copy of the Python non-limited API function _PyLong_AsInt. It is
 * included here because it is missing from the PyPy API. It completes the PyLong_As*
 * group of functions and can be useful in replacing PyInt_Check.
 */
static NPY_INLINE int
Npy__PyLong_AsInt(PyObject *obj)
{
    int overflow;
    long result = PyLong_AsLongAndOverflow(obj, &overflow);

    /* INT_MAX and INT_MIN are defined in Python.h */
    if (overflow || result > INT_MAX || result < INT_MIN) {
        /* XXX: could be cute and give a different
           message for overflow == -1 */
        PyErr_SetString(PyExc_OverflowError,
                        "Python int too large to convert to C int");
        return -1;
    }
    return (int)result;
}


#if defined(NPY_PY3K)
/* Return True only if the long fits in a C long */
static NPY_INLINE int PyInt_Check(PyObject *op) {
    int overflow = 0;
    if (!PyLong_Check(op)) {
        return 0;
    }
    PyLong_AsLongAndOverflow(op, &overflow);
    return (overflow == 0);
}


#define PyInt_FromLong PyLong_FromLong
#define PyInt_AsLong PyLong_AsLong
#define PyInt_AS_LONG PyLong_AsLong
#define PyInt_AsSsize_t PyLong_AsSsize_t
#define PyNumber_Int PyNumber_Long

/* NOTE:
 *
 * Since the PyLong type is very different from the fixed-range PyInt,
 * we don't define PyInt_Type -> PyLong_Type.
 */
#endif /* NPY_PY3K */

/* Py3 changes PySlice_GetIndicesEx' first argument's type to PyObject* */
#ifdef NPY_PY3K
#  define NpySlice_GetIndicesEx PySlice_GetIndicesEx
#else
#  define NpySlice_GetIndicesEx(op, nop, start, end, step, slicelength) \
    PySlice_GetIndicesEx((PySliceObject *)op, nop, start, end, step, slicelength)
#endif

#if PY_VERSION_HEX < 0x030900a4
    /* Introduced in https://github.com/python/cpython/commit/d2ec81a8c99796b51fb8c49b77a7fe369863226f */
    #define Py_SET_TYPE(obj, type) ((Py_TYPE(obj) = (type)), (void)0)
    /* Introduced in https://github.com/python/cpython/commit/b10dc3e7a11fcdb97e285882eba6da92594f90f9 */
    #define Py_SET_SIZE(obj, size) ((Py_SIZE(obj) = (size)), (void)0)
    /* Introduced in https://github.com/python/cpython/commit/c86a11221df7e37da389f9c6ce6e47ea22dc44ff */
    #define Py_SET_REFCNT(obj, refcnt) ((Py_REFCNT(obj) = (refcnt)), (void)0)
#endif


#define Npy_EnterRecursiveCall(x) Py_EnterRecursiveCall(x)

/* Py_SETREF was added in 3.5.2, and only if Py_LIMITED_API is absent */
#if PY_VERSION_HEX < 0x03050200
    #define Py_SETREF(op, op2)                      \
        do {                                        \
            PyObject *_py_tmp = (PyObject *)(op);   \
            (op) = (op2);                           \
            Py_DECREF(_py_tmp);                     \
        } while (0)
#endif

/* introduced in https://github.com/python/cpython/commit/a24107b04c1277e3c1105f98aff5bfa3a98b33a0 */
#if PY_VERSION_HEX < 0x030800A3
    static NPY_INLINE PyObject *
    _PyDict_GetItemStringWithError(PyObject *v, const char *key)
    {
        PyObject *kv, *rv;
        kv = PyUnicode_FromString(key);
        if (kv == NULL) {
            return NULL;
        }
        rv = PyDict_GetItemWithError(v, kv);
        Py_DECREF(kv);
        return rv;
    }
#endif

/*
 * PyString -> PyBytes
 */

#if defined(NPY_PY3K)

#define PyString_Type PyBytes_Type
#define PyString_Check PyBytes_Check
#define PyStringObject PyBytesObject
#define PyString_FromString PyBytes_FromString
#define PyString_FromStringAndSize PyBytes_FromStringAndSize
#define PyString_AS_STRING PyBytes_AS_STRING
#define PyString_AsStringAndSize PyBytes_AsStringAndSize
#define PyString_FromFormat PyBytes_FromFormat
#define PyString_Concat PyBytes_Concat
#define PyString_ConcatAndDel PyBytes_ConcatAndDel
#define PyString_AsString PyBytes_AsString
#define PyString_GET_SIZE PyBytes_GET_SIZE
#define PyString_Size PyBytes_Size

#define PyUString_Type PyUnicode_Type
#define PyUString_Check PyUnicode_Check
#define PyUStringObject PyUnicodeObject
#define PyUString_FromString PyUnicode_FromString
#define PyUString_FromStringAndSize PyUnicode_FromStringAndSize
#define PyUString_FromFormat PyUnicode_FromFormat
#define PyUString_Concat PyUnicode_Concat2
#define PyUString_ConcatAndDel PyUnicode_ConcatAndDel
#define PyUString_GET_SIZE PyUnicode_GET_SIZE
#define PyUString_Size PyUnicode_Size
#define PyUString_InternFromString PyUnicode_InternFromString
#define PyUString_Format PyUnicode_Format

#define PyBaseString_Check(obj) (PyUnicode_Check(obj))

#else

#define PyBytes_Type PyString_Type
#define PyBytes_Check PyString_Check
#define PyBytesObject PyStringObject
#define PyBytes_FromString PyString_FromString
#define PyBytes_FromStringAndSize PyString_FromStringAndSize
#define PyBytes_AS_STRING PyString_AS_STRING
#define PyBytes_AsStringAndSize PyString_AsStringAndSize
#define PyBytes_FromFormat PyString_FromFormat
#define PyBytes_Concat PyString_Concat
#define PyBytes_ConcatAndDel PyString_ConcatAndDel
#define PyBytes_AsString PyString_AsString
#define PyBytes_GET_SIZE PyString_GET_SIZE
#define PyBytes_Size PyString_Size

#define PyUString_Type PyString_Type
#define PyUString_Check PyString_Check
#define PyUStringObject PyStringObject
#define PyUString_FromString PyString_FromString
#define PyUString_FromStringAndSize PyString_FromStringAndSize
#define PyUString_FromFormat PyString_FromFormat
#define PyUString_Concat PyString_Concat
#define PyUString_ConcatAndDel PyString_ConcatAndDel
#define PyUString_GET_SIZE PyString_GET_SIZE
#define PyUString_Size PyString_Size
#define PyUString_InternFromString PyString_InternFromString
#define PyUString_Format PyString_Format

#define PyBaseString_Check(obj) (PyBytes_Check(obj) || PyUnicode_Check(obj))

#endif /* NPY_PY3K */


static NPY_INLINE void
PyUnicode_ConcatAndDel(PyObject **left, PyObject *right)
{
    Py_SETREF(*left, PyUnicode_Concat(*left, right));
    Py_DECREF(right);
}

static NPY_INLINE void
PyUnicode_Concat2(PyObject **left, PyObject *right)
{
    Py_SETREF(*left, PyUnicode_Concat(*left, right));
}

/*
 * PyFile_* compatibility
 */

/*
 * Get a FILE* handle to the file represented by the Python object
 */
static NPY_INLINE FILE*
npy_PyFile_Dup2(PyObject *file, char *mode, npy_off_t *orig_pos)
{
    int fd, fd2, unbuf;
    Py_ssize_t fd2_tmp;
    PyObject *ret, *os, *io, *io_raw;
    npy_off_t pos;
    FILE *handle;

    /* For Python 2 PyFileObject, use PyFile_AsFile */
#if !defined(NPY_PY3K)
    if (PyFile_Check(file)) {
        return PyFile_AsFile(file);
    }
#endif

    /* Flush first to ensure things end up in the file in the correct order */
    ret = PyObject_CallMethod(file, "flush", "");
    if (ret == NULL) {
        return NULL;
    }
    Py_DECREF(ret);
    fd = PyObject_AsFileDescriptor(file);
    if (fd == -1) {
        return NULL;
    }

    /*
     * The handle needs to be dup'd because we have to call fclose
     * at the end
     */
    os = PyImport_ImportModule("os");
    if (os == NULL) {
        return NULL;
    }
    ret = PyObject_CallMethod(os, "dup", "i", fd);
    Py_DECREF(os);
    if (ret == NULL) {
        return NULL;
    }
    fd2_tmp = PyNumber_AsSsize_t(ret, PyExc_IOError);
    Py_DECREF(ret);
    if (fd2_tmp == -1 && PyErr_Occurred()) {
        return NULL;
    }
    if (fd2_tmp < INT_MIN || fd2_tmp > INT_MAX) {
        PyErr_SetString(PyExc_IOError,
                        "Getting an 'int' from os.dup() failed");
        return NULL;
    }
    fd2 = (int)fd2_tmp;

    /* Convert to FILE* handle */
#ifdef _WIN32
    handle = _fdopen(fd2, mode);
#else
    handle = fdopen(fd2, mode);
#endif
    if (handle == NULL) {
        PyErr_SetString(PyExc_IOError,
                        "Getting a FILE* from a Python file object failed");
        return NULL;
    }

    /* Record the original raw file handle position */
    *orig_pos = npy_ftell(handle);
    if (*orig_pos == -1) {
        /* The io module is needed to determine if buffering is used */
        io = PyImport_ImportModule("io");
        if (io == NULL) {
            fclose(handle);
            return NULL;
        }
        /* File object instances of RawIOBase are unbuffered */
        io_raw = PyObject_GetAttrString(io, "RawIOBase");
        Py_DECREF(io);
        if (io_raw == NULL) {
            fclose(handle);
            return NULL;
        }
        unbuf = PyObject_IsInstance(file, io_raw);
        Py_DECREF(io_raw);
        if (unbuf == 1) {
            /* Succeed if the IO is unbuffered */
            return handle;
        }
        else {
            PyErr_SetString(PyExc_IOError, "obtaining file position failed");
            fclose(handle);
            return NULL;
        }
    }

    /* Seek raw handle to the Python-side position */
    ret = PyObject_CallMethod(file, "tell", "");
    if (ret == NULL) {
        fclose(handle);
        return NULL;
    }
    pos = PyLong_AsLongLong(ret);
    Py_DECREF(ret);
    if (PyErr_Occurred()) {
        fclose(handle);
        return NULL;
    }
    if (npy_fseek(handle, pos, SEEK_SET) == -1) {
        PyErr_SetString(PyExc_IOError, "seeking file failed");
        fclose(handle);
        return NULL;
    }
    return handle;
}

/*
 * Close the dup-ed file handle, and seek the Python one to the current position
 */
static NPY_INLINE int
npy_PyFile_DupClose2(PyObject *file, FILE* handle, npy_off_t orig_pos)
{
    int fd, unbuf;
    PyObject *ret, *io, *io_raw;
    npy_off_t position;

    /* For Python 2 PyFileObject, do nothing */
#if !defined(NPY_PY3K)
    if (PyFile_Check(file)) {
        return 0;
    }
#endif

    position = npy_ftell(handle);

    /* Close the FILE* handle */
    fclose(handle);

    /*
     * Restore original file handle position, in order to not confuse
     * Python-side data structures
     */
    fd = PyObject_AsFileDescriptor(file);
    if (fd == -1) {
        return -1;
    }

    if (npy_lseek(fd, orig_pos, SEEK_SET) == -1) {

        /* The io module is needed to determine if buffering is used */
        io = PyImport_ImportModule("io");
        if (io == NULL) {
            return -1;
        }
        /* File object instances of RawIOBase are unbuffered */
        io_raw = PyObject_GetAttrString(io, "RawIOBase");
        Py_DECREF(io);
        if (io_raw == NULL) {
            return -1;
        }
        unbuf = PyObject_IsInstance(file, io_raw);
        Py_DECREF(io_raw);
        if (unbuf == 1) {
            /* Succeed if the IO is unbuffered */
            return 0;
        }
        else {
            PyErr_SetString(PyExc_IOError, "seeking file failed");
            return -1;
        }
    }

    if (position == -1) {
        PyErr_SetString(PyExc_IOError, "obtaining file position failed");
        return -1;
    }

    /* Seek Python-side handle to the FILE* handle position */
    ret = PyObject_CallMethod(file, "seek", NPY_OFF_T_PYFMT "i", position, 0);
    if (ret == NULL) {
        return -1;
    }
    Py_DECREF(ret);
    return 0;
}

static NPY_INLINE int
npy_PyFile_Check(PyObject *file)
{
    int fd;
    /* For Python 2, check if it is a PyFileObject */
#if !defined(NPY_PY3K)
    if (PyFile_Check(file)) {
        return 1;
    }
#endif
    fd = PyObject_AsFileDescriptor(file);
    if (fd == -1) {
        PyErr_Clear();
        return 0;
    }
    return 1;
}

static NPY_INLINE PyObject*
npy_PyFile_OpenFile(PyObject *filename, const char *mode)
{
    PyObject *open;
    open = PyDict_GetItemString(PyEval_GetBuiltins(), "open");
    if (open == NULL) {
        return NULL;
    }
    return PyObject_CallFunction(open, "Os", filename, mode);
}

static NPY_INLINE int
npy_PyFile_CloseFile(PyObject *file)
{
    PyObject *ret;

    ret = PyObject_CallMethod(file, "close", NULL);
    if (ret == NULL) {
        return -1;
    }
    Py_DECREF(ret);
    return 0;
}


/* This is a copy of _PyErr_ChainExceptions
 */
static NPY_INLINE void
npy_PyErr_ChainExceptions(PyObject *exc, PyObject *val, PyObject *tb)
{
    if (exc == NULL)
        return;

    if (PyErr_Occurred()) {
        /* only py3 supports this anyway */
        #ifdef NPY_PY3K
            PyObject *exc2, *val2, *tb2;
            PyErr_Fetch(&exc2, &val2, &tb2);
            PyErr_NormalizeException(&exc, &val, &tb);
            if (tb != NULL) {
                PyException_SetTraceback(val, tb);
                Py_DECREF(tb);
            }
            Py_DECREF(exc);
            PyErr_NormalizeException(&exc2, &val2, &tb2);
            PyException_SetContext(val2, val);
            PyErr_Restore(exc2, val2, tb2);
        #endif
    }
    else {
        PyErr_Restore(exc, val, tb);
    }
}


/* This is a copy of _PyErr_ChainExceptions, with:
 *  - a minimal implementation for python 2
 *  - __cause__ used instead of __context__
 */
static NPY_INLINE void
npy_PyErr_ChainExceptionsCause(PyObject *exc, PyObject *val, PyObject *tb)
{
    if (exc == NULL)
        return;

    if (PyErr_Occurred()) {
        /* only py3 supports this anyway */
        #ifdef NPY_PY3K
            PyObject *exc2, *val2, *tb2;
            PyErr_Fetch(&exc2, &val2, &tb2);
            PyErr_NormalizeException(&exc, &val, &tb);
            if (tb != NULL) {
                PyException_SetTraceback(val, tb);
                Py_DECREF(tb);
            }
            Py_DECREF(exc);
            PyErr_NormalizeException(&exc2, &val2, &tb2);
            PyException_SetCause(val2, val);
            PyErr_Restore(exc2, val2, tb2);
        #endif
    }
    else {
        PyErr_Restore(exc, val, tb);
    }
}

/*
 * PyObject_Cmp
 */
#if defined(NPY_PY3K)
static NPY_INLINE int
PyObject_Cmp(PyObject *i1, PyObject *i2, int *cmp)
{
    int v;
    v = PyObject_RichCompareBool(i1, i2, Py_LT);
    if (v == 1) {
        *cmp = -1;
        return 1;
    }
    else if (v == -1) {
        return -1;
    }

    v = PyObject_RichCompareBool(i1, i2, Py_GT);
    if (v == 1) {
        *cmp = 1;
        return 1;
    }
    else if (v == -1) {
        return -1;
    }

    v = PyObject_RichCompareBool(i1, i2, Py_EQ);
    if (v == 1) {
        *cmp = 0;
        return 1;
    }
    else {
        *cmp = 0;
        return -1;
    }
}
#endif

/*
 * PyCObject functions adapted to PyCapsules.
 *
 * The main job here is to get rid of the improved error handling
 * of PyCapsules. It's a shame...
 */
static NPY_INLINE PyObject *
NpyCapsule_FromVoidPtr(void *ptr, void (*dtor)(PyObject *))
{
    PyObject *ret = PyCapsule_New(ptr, NULL, dtor);
    if (ret == NULL) {
        PyErr_Clear();
    }
    return ret;
}

static NPY_INLINE PyObject *
NpyCapsule_FromVoidPtrAndDesc(void *ptr, void* context, void (*dtor)(PyObject *))
{
    PyObject *ret = NpyCapsule_FromVoidPtr(ptr, dtor);
    if (ret != NULL && PyCapsule_SetContext(ret, context) != 0) {
        PyErr_Clear();
        Py_DECREF(ret);
        ret = NULL;
    }
    return ret;
}

static NPY_INLINE void *
NpyCapsule_AsVoidPtr(PyObject *obj)
{
    void *ret = PyCapsule_GetPointer(obj, NULL);
    if (ret == NULL) {
        PyErr_Clear();
    }
    return ret;
}

static NPY_INLINE void *
NpyCapsule_GetDesc(PyObject *obj)
{
    return PyCapsule_GetContext(obj);
}

static NPY_INLINE int
NpyCapsule_Check(PyObject *ptr)
{
    return PyCapsule_CheckExact(ptr);
}

#ifdef __cplusplus
}
#endif


#endif  /* NUMPY_CORE_INCLUDE_NUMPY_NPY_3KCOMPAT_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/npy_common.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY_NPY_COMMON_H_
#define NUMPY_CORE_INCLUDE_NUMPY_NPY_COMMON_H_

/* need Python.h for npy_intp, npy_uintp */
#include <Python.h>

/* numpconfig.h is auto-generated */
#include "numpyconfig.h"
#ifdef HAVE_NPY_CONFIG_H
#include <npy_config.h>
#endif

/*
 * using static inline modifiers when defining npy_math functions
 * allows the compiler to make optimizations when possible
 */
#ifndef NPY_INLINE_MATH
#if defined(NPY_INTERNAL_BUILD) && NPY_INTERNAL_BUILD
    #define NPY_INLINE_MATH 1
#else
    #define NPY_INLINE_MATH 0
#endif
#endif

/*
 * gcc does not unroll even with -O3
 * use with care, unrolling on modern cpus rarely speeds things up
 */
#ifdef HAVE_ATTRIBUTE_OPTIMIZE_UNROLL_LOOPS
#define NPY_GCC_UNROLL_LOOPS \
    __attribute__((optimize("unroll-loops")))
#else
#define NPY_GCC_UNROLL_LOOPS
#endif

/* highest gcc optimization level, enabled autovectorizer */
#ifdef HAVE_ATTRIBUTE_OPTIMIZE_OPT_3
#define NPY_GCC_OPT_3 __attribute__((optimize("O3")))
#else
#define NPY_GCC_OPT_3
#endif

/* compile target attributes */
#if defined HAVE_ATTRIBUTE_TARGET_AVX && defined HAVE_LINK_AVX
#define NPY_GCC_TARGET_AVX __attribute__((target("avx")))
#else
#define NPY_GCC_TARGET_AVX
#endif

#if defined HAVE_ATTRIBUTE_TARGET_AVX2_WITH_INTRINSICS
#define HAVE_ATTRIBUTE_TARGET_FMA
#define NPY_GCC_TARGET_FMA __attribute__((target("avx2,fma")))
#endif

#if defined HAVE_ATTRIBUTE_TARGET_AVX2 && defined HAVE_LINK_AVX2
#define NPY_GCC_TARGET_AVX2 __attribute__((target("avx2")))
#else
#define NPY_GCC_TARGET_AVX2
#endif

#if defined HAVE_ATTRIBUTE_TARGET_AVX512F && defined HAVE_LINK_AVX512F
#define NPY_GCC_TARGET_AVX512F __attribute__((target("avx512f")))
#elif defined HAVE_ATTRIBUTE_TARGET_AVX512F_WITH_INTRINSICS
#define NPY_GCC_TARGET_AVX512F __attribute__((target("avx512f")))
#else
#define NPY_GCC_TARGET_AVX512F
#endif

#if defined HAVE_ATTRIBUTE_TARGET_AVX512_SKX && defined HAVE_LINK_AVX512_SKX
#define NPY_GCC_TARGET_AVX512_SKX __attribute__((target("avx512f,avx512dq,avx512vl,avx512bw,avx512cd")))
#elif defined HAVE_ATTRIBUTE_TARGET_AVX512_SKX_WITH_INTRINSICS
#define NPY_GCC_TARGET_AVX512_SKX __attribute__((target("avx512f,avx512dq,avx512vl,avx512bw,avx512cd")))
#else
#define NPY_GCC_TARGET_AVX512_SKX
#endif
/*
 * mark an argument (starting from 1) that must not be NULL and is not checked
 * DO NOT USE IF FUNCTION CHECKS FOR NULL!! the compiler will remove the check
 */
#ifdef HAVE_ATTRIBUTE_NONNULL
#define NPY_GCC_NONNULL(n) __attribute__((nonnull(n)))
#else
#define NPY_GCC_NONNULL(n)
#endif

#if defined HAVE_XMMINTRIN_H && defined HAVE__MM_LOAD_PS
#define NPY_HAVE_SSE_INTRINSICS
#endif

#if defined HAVE_EMMINTRIN_H && defined HAVE__MM_LOAD_PD
#define NPY_HAVE_SSE2_INTRINSICS
#endif

#if defined HAVE_IMMINTRIN_H && defined HAVE_LINK_AVX2
#define NPY_HAVE_AVX2_INTRINSICS
#endif

#if defined HAVE_IMMINTRIN_H && defined HAVE_LINK_AVX512F
#define NPY_HAVE_AVX512F_INTRINSICS
#endif
/*
 * give a hint to the compiler which branch is more likely or unlikely
 * to occur, e.g. rare error cases:
 *
 * if (NPY_UNLIKELY(failure == 0))
 *    return NULL;
 *
 * the double !! is to cast the expression (e.g. NULL) to a boolean required by
 * the intrinsic
 */
#ifdef HAVE___BUILTIN_EXPECT
#define NPY_LIKELY(x) __builtin_expect(!!(x), 1)
#define NPY_UNLIKELY(x) __builtin_expect(!!(x), 0)
#else
#define NPY_LIKELY(x) (x)
#define NPY_UNLIKELY(x) (x)
#endif

#ifdef HAVE___BUILTIN_PREFETCH
/* unlike _mm_prefetch also works on non-x86 */
#define NPY_PREFETCH(x, rw, loc) __builtin_prefetch((x), (rw), (loc))
#else
#ifdef HAVE__MM_PREFETCH
/* _MM_HINT_ET[01] (rw = 1) unsupported, only available in gcc >= 4.9 */
#define NPY_PREFETCH(x, rw, loc) _mm_prefetch((x), loc == 0 ? _MM_HINT_NTA : \
                                             (loc == 1 ? _MM_HINT_T2 : \
                                              (loc == 2 ? _MM_HINT_T1 : \
                                               (loc == 3 ? _MM_HINT_T0 : -1))))
#else
#define NPY_PREFETCH(x, rw,loc)
#endif
#endif

#if defined(_MSC_VER) && !defined(__clang__)
    #define NPY_INLINE __inline
/* clang included here to handle clang-cl on Windows */
#elif defined(__GNUC__) || defined(__clang__)
    #if defined(__STRICT_ANSI__)
         #define NPY_INLINE __inline__
    #else
         #define NPY_INLINE inline
    #endif
#else
    #define NPY_INLINE
#endif

#ifdef _MSC_VER
    #define NPY_FINLINE static __forceinline
#elif defined(__GNUC__)
    #define NPY_FINLINE static NPY_INLINE __attribute__((always_inline))
#else
    #define NPY_FINLINE static
#endif

#ifdef HAVE___THREAD
    #define NPY_TLS __thread
#else
    #ifdef HAVE___DECLSPEC_THREAD_
        #define NPY_TLS __declspec(thread)
    #else
        #define NPY_TLS
    #endif
#endif

#ifdef WITH_CPYCHECKER_RETURNS_BORROWED_REF_ATTRIBUTE
  #define NPY_RETURNS_BORROWED_REF \
    __attribute__((cpychecker_returns_borrowed_ref))
#else
  #define NPY_RETURNS_BORROWED_REF
#endif

#ifdef WITH_CPYCHECKER_STEALS_REFERENCE_TO_ARG_ATTRIBUTE
  #define NPY_STEALS_REF_TO_ARG(n) \
   __attribute__((cpychecker_steals_reference_to_arg(n)))
#else
 #define NPY_STEALS_REF_TO_ARG(n)
#endif

/* 64 bit file position support, also on win-amd64. Ticket #1660 */
#if defined(_MSC_VER) && defined(_WIN64) && (_MSC_VER > 1400) || \
    defined(__MINGW32__) || defined(__MINGW64__)
    #include <io.h>

    #define npy_fseek _fseeki64
    #define npy_ftell _ftelli64
    #define npy_lseek _lseeki64
    #define npy_off_t npy_int64

    #if NPY_SIZEOF_INT == 8
        #define NPY_OFF_T_PYFMT "i"
    #elif NPY_SIZEOF_LONG == 8
        #define NPY_OFF_T_PYFMT "l"
    #elif NPY_SIZEOF_LONGLONG == 8
        #define NPY_OFF_T_PYFMT "L"
    #else
        #error Unsupported size for type off_t
    #endif
#else
#ifdef HAVE_FSEEKO
    #define npy_fseek fseeko
#else
    #define npy_fseek fseek
#endif
#ifdef HAVE_FTELLO
    #define npy_ftell ftello
#else
    #define npy_ftell ftell
#endif
    #include <sys/types.h>
    #define npy_lseek lseek
    #define npy_off_t off_t

    #if NPY_SIZEOF_OFF_T == NPY_SIZEOF_SHORT
        #define NPY_OFF_T_PYFMT "h"
    #elif NPY_SIZEOF_OFF_T == NPY_SIZEOF_INT
        #define NPY_OFF_T_PYFMT "i"
    #elif NPY_SIZEOF_OFF_T == NPY_SIZEOF_LONG
        #define NPY_OFF_T_PYFMT "l"
    #elif NPY_SIZEOF_OFF_T == NPY_SIZEOF_LONGLONG
        #define NPY_OFF_T_PYFMT "L"
    #else
        #error Unsupported size for type off_t
    #endif
#endif

/* enums for detected endianness */
enum {
        NPY_CPU_UNKNOWN_ENDIAN,
        NPY_CPU_LITTLE,
        NPY_CPU_BIG
};

/*
 * This is to typedef npy_intp to the appropriate pointer size for this
 * platform.  Py_intptr_t, Py_uintptr_t are defined in pyport.h.
 */
typedef Py_intptr_t npy_intp;
typedef Py_uintptr_t npy_uintp;

/*
 * Define sizes that were not defined in numpyconfig.h.
 */
#define NPY_SIZEOF_CHAR 1
#define NPY_SIZEOF_BYTE 1
#define NPY_SIZEOF_DATETIME 8
#define NPY_SIZEOF_TIMEDELTA 8
#define NPY_SIZEOF_INTP NPY_SIZEOF_PY_INTPTR_T
#define NPY_SIZEOF_UINTP NPY_SIZEOF_PY_INTPTR_T
#define NPY_SIZEOF_HALF 2
#define NPY_SIZEOF_CFLOAT NPY_SIZEOF_COMPLEX_FLOAT
#define NPY_SIZEOF_CDOUBLE NPY_SIZEOF_COMPLEX_DOUBLE
#define NPY_SIZEOF_CLONGDOUBLE NPY_SIZEOF_COMPLEX_LONGDOUBLE

#ifdef constchar
#undef constchar
#endif

#define NPY_SSIZE_T_PYFMT "n"
#define constchar char

/* NPY_INTP_FMT Note:
 *      Unlike the other NPY_*_FMT macros, which are used with PyOS_snprintf,
 *      NPY_INTP_FMT is used with PyErr_Format and PyUnicode_FromFormat. Those
 *      functions use different formatting codes that are portably specified
 *      according to the Python documentation. See issue gh-2388.
 */
#if NPY_SIZEOF_PY_INTPTR_T == NPY_SIZEOF_INT
        #define NPY_INTP NPY_INT
        #define NPY_UINTP NPY_UINT
        #define PyIntpArrType_Type PyIntArrType_Type
        #define PyUIntpArrType_Type PyUIntArrType_Type
        #define NPY_MAX_INTP NPY_MAX_INT
        #define NPY_MIN_INTP NPY_MIN_INT
        #define NPY_MAX_UINTP NPY_MAX_UINT
        #define NPY_INTP_FMT "d"
#elif NPY_SIZEOF_PY_INTPTR_T == NPY_SIZEOF_LONG
        #define NPY_INTP NPY_LONG
        #define NPY_UINTP NPY_ULONG
        #define PyIntpArrType_Type PyLongArrType_Type
        #define PyUIntpArrType_Type PyULongArrType_Type
        #define NPY_MAX_INTP NPY_MAX_LONG
        #define NPY_MIN_INTP NPY_MIN_LONG
        #define NPY_MAX_UINTP NPY_MAX_ULONG
        #define NPY_INTP_FMT "ld"
#elif defined(PY_LONG_LONG) && (NPY_SIZEOF_PY_INTPTR_T == NPY_SIZEOF_LONGLONG)
        #define NPY_INTP NPY_LONGLONG
        #define NPY_UINTP NPY_ULONGLONG
        #define PyIntpArrType_Type PyLongLongArrType_Type
        #define PyUIntpArrType_Type PyULongLongArrType_Type
        #define NPY_MAX_INTP NPY_MAX_LONGLONG
        #define NPY_MIN_INTP NPY_MIN_LONGLONG
        #define NPY_MAX_UINTP NPY_MAX_ULONGLONG
        #define NPY_INTP_FMT "lld"
#endif

/*
 * We can only use C99 formats for npy_int_p if it is the same as
 * intp_t, hence the condition on HAVE_UNITPTR_T
 */
#if (NPY_USE_C99_FORMATS) == 1 \
        && (defined HAVE_UINTPTR_T) \
        && (defined HAVE_INTTYPES_H)
        #include <inttypes.h>
        #undef NPY_INTP_FMT
        #define NPY_INTP_FMT PRIdPTR
#endif


/*
 * Some platforms don't define bool, long long, or long double.
 * Handle that here.
 */
#define NPY_BYTE_FMT "hhd"
#define NPY_UBYTE_FMT "hhu"
#define NPY_SHORT_FMT "hd"
#define NPY_USHORT_FMT "hu"
#define NPY_INT_FMT "d"
#define NPY_UINT_FMT "u"
#define NPY_LONG_FMT "ld"
#define NPY_ULONG_FMT "lu"
#define NPY_HALF_FMT "g"
#define NPY_FLOAT_FMT "g"
#define NPY_DOUBLE_FMT "g"


#ifdef PY_LONG_LONG
typedef PY_LONG_LONG npy_longlong;
typedef unsigned PY_LONG_LONG npy_ulonglong;
#  ifdef _MSC_VER
#    define NPY_LONGLONG_FMT         "I64d"
#    define NPY_ULONGLONG_FMT        "I64u"
#  else
#    define NPY_LONGLONG_FMT         "lld"
#    define NPY_ULONGLONG_FMT        "llu"
#  endif
#  ifdef _MSC_VER
#    define NPY_LONGLONG_SUFFIX(x)   (x##i64)
#    define NPY_ULONGLONG_SUFFIX(x)  (x##Ui64)
#  else
#    define NPY_LONGLONG_SUFFIX(x)   (x##LL)
#    define NPY_ULONGLONG_SUFFIX(x)  (x##ULL)
#  endif
#else
typedef long npy_longlong;
typedef unsigned long npy_ulonglong;
#  define NPY_LONGLONG_SUFFIX(x)  (x##L)
#  define NPY_ULONGLONG_SUFFIX(x) (x##UL)
#endif


typedef unsigned char npy_bool;
#define NPY_FALSE 0
#define NPY_TRUE 1
/*
 * `NPY_SIZEOF_LONGDOUBLE` isn't usually equal to sizeof(long double).
 * In some certain cases, it may forced to be equal to sizeof(double)
 * even against the compiler implementation and the same goes for
 * `complex long double`.
 *
 * Therefore, avoid `long double`, use `npy_longdouble` instead,
 * and when it comes to standard math functions make sure of using
 * the double version when `NPY_SIZEOF_LONGDOUBLE` == `NPY_SIZEOF_DOUBLE`.
 * For example:
 *   npy_longdouble *ptr, x;
 *   #if NPY_SIZEOF_LONGDOUBLE == NPY_SIZEOF_DOUBLE
 *       npy_longdouble r = modf(x, ptr);
 *   #else
 *       npy_longdouble r = modfl(x, ptr);
 *   #endif
 *
 * See https://github.com/numpy/numpy/issues/20348
 */
#if NPY_SIZEOF_LONGDOUBLE == NPY_SIZEOF_DOUBLE
    #define NPY_LONGDOUBLE_FMT "g"
    typedef double npy_longdouble;
#else
    #define NPY_LONGDOUBLE_FMT "Lg"
    typedef long double npy_longdouble;
#endif

#ifndef Py_USING_UNICODE
#error Must use Python with unicode enabled.
#endif


typedef signed char npy_byte;
typedef unsigned char npy_ubyte;
typedef unsigned short npy_ushort;
typedef unsigned int npy_uint;
typedef unsigned long npy_ulong;

/* These are for completeness */
typedef char npy_char;
typedef short npy_short;
typedef int npy_int;
typedef long npy_long;
typedef float npy_float;
typedef double npy_double;

typedef Py_hash_t npy_hash_t;
#define NPY_SIZEOF_HASH_T NPY_SIZEOF_INTP

/*
 * Disabling C99 complex usage: a lot of C code in numpy/scipy rely on being
 * able to do .real/.imag. Will have to convert code first.
 */
#if 0
#if defined(NPY_USE_C99_COMPLEX) && defined(NPY_HAVE_COMPLEX_DOUBLE)
typedef complex npy_cdouble;
#else
typedef struct { double real, imag; } npy_cdouble;
#endif

#if defined(NPY_USE_C99_COMPLEX) && defined(NPY_HAVE_COMPLEX_FLOAT)
typedef complex float npy_cfloat;
#else
typedef struct { float real, imag; } npy_cfloat;
#endif

#if defined(NPY_USE_C99_COMPLEX) && defined(NPY_HAVE_COMPLEX_LONG_DOUBLE)
typedef complex long double npy_clongdouble;
#else
typedef struct {npy_longdouble real, imag;} npy_clongdouble;
#endif
#endif
#if NPY_SIZEOF_COMPLEX_DOUBLE != 2 * NPY_SIZEOF_DOUBLE
#error npy_cdouble definition is not compatible with C99 complex definition ! \
        Please contact NumPy maintainers and give detailed information about your \
        compiler and platform
#endif
typedef struct { double real, imag; } npy_cdouble;

#if NPY_SIZEOF_COMPLEX_FLOAT != 2 * NPY_SIZEOF_FLOAT
#error npy_cfloat definition is not compatible with C99 complex definition ! \
        Please contact NumPy maintainers and give detailed information about your \
        compiler and platform
#endif
typedef struct { float real, imag; } npy_cfloat;

#if NPY_SIZEOF_COMPLEX_LONGDOUBLE != 2 * NPY_SIZEOF_LONGDOUBLE
#error npy_clongdouble definition is not compatible with C99 complex definition ! \
        Please contact NumPy maintainers and give detailed information about your \
        compiler and platform
#endif
typedef struct { npy_longdouble real, imag; } npy_clongdouble;

/*
 * numarray-style bit-width typedefs
 */
#define NPY_MAX_INT8 127
#define NPY_MIN_INT8 -128
#define NPY_MAX_UINT8 255
#define NPY_MAX_INT16 32767
#define NPY_MIN_INT16 -32768
#define NPY_MAX_UINT16 65535
#define NPY_MAX_INT32 2147483647
#define NPY_MIN_INT32 (-NPY_MAX_INT32 - 1)
#define NPY_MAX_UINT32 4294967295U
#define NPY_MAX_INT64 NPY_LONGLONG_SUFFIX(9223372036854775807)
#define NPY_MIN_INT64 (-NPY_MAX_INT64 - NPY_LONGLONG_SUFFIX(1))
#define NPY_MAX_UINT64 NPY_ULONGLONG_SUFFIX(18446744073709551615)
#define NPY_MAX_INT128 NPY_LONGLONG_SUFFIX(85070591730234615865843651857942052864)
#define NPY_MIN_INT128 (-NPY_MAX_INT128 - NPY_LONGLONG_SUFFIX(1))
#define NPY_MAX_UINT128 NPY_ULONGLONG_SUFFIX(170141183460469231731687303715884105728)
#define NPY_MAX_INT256 NPY_LONGLONG_SUFFIX(57896044618658097711785492504343953926634992332820282019728792003956564819967)
#define NPY_MIN_INT256 (-NPY_MAX_INT256 - NPY_LONGLONG_SUFFIX(1))
#define NPY_MAX_UINT256 NPY_ULONGLONG_SUFFIX(115792089237316195423570985008687907853269984665640564039457584007913129639935)
#define NPY_MIN_DATETIME NPY_MIN_INT64
#define NPY_MAX_DATETIME NPY_MAX_INT64
#define NPY_MIN_TIMEDELTA NPY_MIN_INT64
#define NPY_MAX_TIMEDELTA NPY_MAX_INT64

        /* Need to find the number of bits for each type and
           make definitions accordingly.

           C states that sizeof(char) == 1 by definition

           So, just using the sizeof keyword won't help.

           It also looks like Python itself uses sizeof(char) quite a
           bit, which by definition should be 1 all the time.

           Idea: Make Use of CHAR_BIT which should tell us how many
           BITS per CHARACTER
        */

        /* Include platform definitions -- These are in the C89/90 standard */
#include <limits.h>
#define NPY_MAX_BYTE SCHAR_MAX
#define NPY_MIN_BYTE SCHAR_MIN
#define NPY_MAX_UBYTE UCHAR_MAX
#define NPY_MAX_SHORT SHRT_MAX
#define NPY_MIN_SHORT SHRT_MIN
#define NPY_MAX_USHORT USHRT_MAX
#define NPY_MAX_INT   INT_MAX
#ifndef INT_MIN
#define INT_MIN (-INT_MAX - 1)
#endif
#define NPY_MIN_INT   INT_MIN
#define NPY_MAX_UINT  UINT_MAX
#define NPY_MAX_LONG  LONG_MAX
#define NPY_MIN_LONG  LONG_MIN
#define NPY_MAX_ULONG  ULONG_MAX

#define NPY_BITSOF_BOOL (sizeof(npy_bool) * CHAR_BIT)
#define NPY_BITSOF_CHAR CHAR_BIT
#define NPY_BITSOF_BYTE (NPY_SIZEOF_BYTE * CHAR_BIT)
#define NPY_BITSOF_SHORT (NPY_SIZEOF_SHORT * CHAR_BIT)
#define NPY_BITSOF_INT (NPY_SIZEOF_INT * CHAR_BIT)
#define NPY_BITSOF_LONG (NPY_SIZEOF_LONG * CHAR_BIT)
#define NPY_BITSOF_LONGLONG (NPY_SIZEOF_LONGLONG * CHAR_BIT)
#define NPY_BITSOF_INTP (NPY_SIZEOF_INTP * CHAR_BIT)
#define NPY_BITSOF_HALF (NPY_SIZEOF_HALF * CHAR_BIT)
#define NPY_BITSOF_FLOAT (NPY_SIZEOF_FLOAT * CHAR_BIT)
#define NPY_BITSOF_DOUBLE (NPY_SIZEOF_DOUBLE * CHAR_BIT)
#define NPY_BITSOF_LONGDOUBLE (NPY_SIZEOF_LONGDOUBLE * CHAR_BIT)
#define NPY_BITSOF_CFLOAT (NPY_SIZEOF_CFLOAT * CHAR_BIT)
#define NPY_BITSOF_CDOUBLE (NPY_SIZEOF_CDOUBLE * CHAR_BIT)
#define NPY_BITSOF_CLONGDOUBLE (NPY_SIZEOF_CLONGDOUBLE * CHAR_BIT)
#define NPY_BITSOF_DATETIME (NPY_SIZEOF_DATETIME * CHAR_BIT)
#define NPY_BITSOF_TIMEDELTA (NPY_SIZEOF_TIMEDELTA * CHAR_BIT)

#if NPY_BITSOF_LONG == 8
#define NPY_INT8 NPY_LONG
#define NPY_UINT8 NPY_ULONG
        typedef long npy_int8;
        typedef unsigned long npy_uint8;
#define PyInt8ScalarObject PyLongScalarObject
#define PyInt8ArrType_Type PyLongArrType_Type
#define PyUInt8ScalarObject PyULongScalarObject
#define PyUInt8ArrType_Type PyULongArrType_Type
#define NPY_INT8_FMT NPY_LONG_FMT
#define NPY_UINT8_FMT NPY_ULONG_FMT
#elif NPY_BITSOF_LONG == 16
#define NPY_INT16 NPY_LONG
#define NPY_UINT16 NPY_ULONG
        typedef long npy_int16;
        typedef unsigned long npy_uint16;
#define PyInt16ScalarObject PyLongScalarObject
#define PyInt16ArrType_Type PyLongArrType_Type
#define PyUInt16ScalarObject PyULongScalarObject
#define PyUInt16ArrType_Type PyULongArrType_Type
#define NPY_INT16_FMT NPY_LONG_FMT
#define NPY_UINT16_FMT NPY_ULONG_FMT
#elif NPY_BITSOF_LONG == 32
#define NPY_INT32 NPY_LONG
#define NPY_UINT32 NPY_ULONG
        typedef long npy_int32;
        typedef unsigned long npy_uint32;
        typedef unsigned long npy_ucs4;
#define PyInt32ScalarObject PyLongScalarObject
#define PyInt32ArrType_Type PyLongArrType_Type
#define PyUInt32ScalarObject PyULongScalarObject
#define PyUInt32ArrType_Type PyULongArrType_Type
#define NPY_INT32_FMT NPY_LONG_FMT
#define NPY_UINT32_FMT NPY_ULONG_FMT
#elif NPY_BITSOF_LONG == 64
#define NPY_INT64 NPY_LONG
#define NPY_UINT64 NPY_ULONG
        typedef long npy_int64;
        typedef unsigned long npy_uint64;
#define PyInt64ScalarObject PyLongScalarObject
#define PyInt64ArrType_Type PyLongArrType_Type
#define PyUInt64ScalarObject PyULongScalarObject
#define PyUInt64ArrType_Type PyULongArrType_Type
#define NPY_INT64_FMT NPY_LONG_FMT
#define NPY_UINT64_FMT NPY_ULONG_FMT
#define MyPyLong_FromInt64 PyLong_FromLong
#define MyPyLong_AsInt64 PyLong_AsLong
#elif NPY_BITSOF_LONG == 128
#define NPY_INT128 NPY_LONG
#define NPY_UINT128 NPY_ULONG
        typedef long npy_int128;
        typedef unsigned long npy_uint128;
#define PyInt128ScalarObject PyLongScalarObject
#define PyInt128ArrType_Type PyLongArrType_Type
#define PyUInt128ScalarObject PyULongScalarObject
#define PyUInt128ArrType_Type PyULongArrType_Type
#define NPY_INT128_FMT NPY_LONG_FMT
#define NPY_UINT128_FMT NPY_ULONG_FMT
#endif

#if NPY_BITSOF_LONGLONG == 8
#  ifndef NPY_INT8
#    define NPY_INT8 NPY_LONGLONG
#    define NPY_UINT8 NPY_ULONGLONG
        typedef npy_longlong npy_int8;
        typedef npy_ulonglong npy_uint8;
#    define PyInt8ScalarObject PyLongLongScalarObject
#    define PyInt8ArrType_Type PyLongLongArrType_Type
#    define PyUInt8ScalarObject PyULongLongScalarObject
#    define PyUInt8ArrType_Type PyULongLongArrType_Type
#define NPY_INT8_FMT NPY_LONGLONG_FMT
#define NPY_UINT8_FMT NPY_ULONGLONG_FMT
#  endif
#  define NPY_MAX_LONGLONG NPY_MAX_INT8
#  define NPY_MIN_LONGLONG NPY_MIN_INT8
#  define NPY_MAX_ULONGLONG NPY_MAX_UINT8
#elif NPY_BITSOF_LONGLONG == 16
#  ifndef NPY_INT16
#    define NPY_INT16 NPY_LONGLONG
#    define NPY_UINT16 NPY_ULONGLONG
        typedef npy_longlong npy_int16;
        typedef npy_ulonglong npy_uint16;
#    define PyInt16ScalarObject PyLongLongScalarObject
#    define PyInt16ArrType_Type PyLongLongArrType_Type
#    define PyUInt16ScalarObject PyULongLongScalarObject
#    define PyUInt16ArrType_Type PyULongLongArrType_Type
#define NPY_INT16_FMT NPY_LONGLONG_FMT
#define NPY_UINT16_FMT NPY_ULONGLONG_FMT
#  endif
#  define NPY_MAX_LONGLONG NPY_MAX_INT16
#  define NPY_MIN_LONGLONG NPY_MIN_INT16
#  define NPY_MAX_ULONGLONG NPY_MAX_UINT16
#elif NPY_BITSOF_LONGLONG == 32
#  ifndef NPY_INT32
#    define NPY_INT32 NPY_LONGLONG
#    define NPY_UINT32 NPY_ULONGLONG
        typedef npy_longlong npy_int32;
        typedef npy_ulonglong npy_uint32;
        typedef npy_ulonglong npy_ucs4;
#    define PyInt32ScalarObject PyLongLongScalarObject
#    define PyInt32ArrType_Type PyLongLongArrType_Type
#    define PyUInt32ScalarObject PyULongLongScalarObject
#    define PyUInt32ArrType_Type PyULongLongArrType_Type
#define NPY_INT32_FMT NPY_LONGLONG_FMT
#define NPY_UINT32_FMT NPY_ULONGLONG_FMT
#  endif
#  define NPY_MAX_LONGLONG NPY_MAX_INT32
#  define NPY_MIN_LONGLONG NPY_MIN_INT32
#  define NPY_MAX_ULONGLONG NPY_MAX_UINT32
#elif NPY_BITSOF_LONGLONG == 64
#  ifndef NPY_INT64
#    define NPY_INT64 NPY_LONGLONG
#    define NPY_UINT64 NPY_ULONGLONG
        typedef npy_longlong npy_int64;
        typedef npy_ulonglong npy_uint64;
#    define PyInt64ScalarObject PyLongLongScalarObject
#    define PyInt64ArrType_Type PyLongLongArrType_Type
#    define PyUInt64ScalarObject PyULongLongScalarObject
#    define PyUInt64ArrType_Type PyULongLongArrType_Type
#define NPY_INT64_FMT NPY_LONGLONG_FMT
#define NPY_UINT64_FMT NPY_ULONGLONG_FMT
#    define MyPyLong_FromInt64 PyLong_FromLongLong
#    define MyPyLong_AsInt64 PyLong_AsLongLong
#  endif
#  define NPY_MAX_LONGLONG NPY_MAX_INT64
#  define NPY_MIN_LONGLONG NPY_MIN_INT64
#  define NPY_MAX_ULONGLONG NPY_MAX_UINT64
#elif NPY_BITSOF_LONGLONG == 128
#  ifndef NPY_INT128
#    define NPY_INT128 NPY_LONGLONG
#    define NPY_UINT128 NPY_ULONGLONG
        typedef npy_longlong npy_int128;
        typedef npy_ulonglong npy_uint128;
#    define PyInt128ScalarObject PyLongLongScalarObject
#    define PyInt128ArrType_Type PyLongLongArrType_Type
#    define PyUInt128ScalarObject PyULongLongScalarObject
#    define PyUInt128ArrType_Type PyULongLongArrType_Type
#define NPY_INT128_FMT NPY_LONGLONG_FMT
#define NPY_UINT128_FMT NPY_ULONGLONG_FMT
#  endif
#  define NPY_MAX_LONGLONG NPY_MAX_INT128
#  define NPY_MIN_LONGLONG NPY_MIN_INT128
#  define NPY_MAX_ULONGLONG NPY_MAX_UINT128
#elif NPY_BITSOF_LONGLONG == 256
#  define NPY_INT256 NPY_LONGLONG
#  define NPY_UINT256 NPY_ULONGLONG
        typedef npy_longlong npy_int256;
        typedef npy_ulonglong npy_uint256;
#  define PyInt256ScalarObject PyLongLongScalarObject
#  define PyInt256ArrType_Type PyLongLongArrType_Type
#  define PyUInt256ScalarObject PyULongLongScalarObject
#  define PyUInt256ArrType_Type PyULongLongArrType_Type
#define NPY_INT256_FMT NPY_LONGLONG_FMT
#define NPY_UINT256_FMT NPY_ULONGLONG_FMT
#  define NPY_MAX_LONGLONG NPY_MAX_INT256
#  define NPY_MIN_LONGLONG NPY_MIN_INT256
#  define NPY_MAX_ULONGLONG NPY_MAX_UINT256
#endif

#if NPY_BITSOF_INT == 8
#ifndef NPY_INT8
#define NPY_INT8 NPY_INT
#define NPY_UINT8 NPY_UINT
        typedef int npy_int8;
        typedef unsigned int npy_uint8;
#    define PyInt8ScalarObject PyIntScalarObject
#    define PyInt8ArrType_Type PyIntArrType_Type
#    define PyUInt8ScalarObject PyUIntScalarObject
#    define PyUInt8ArrType_Type PyUIntArrType_Type
#define NPY_INT8_FMT NPY_INT_FMT
#define NPY_UINT8_FMT NPY_UINT_FMT
#endif
#elif NPY_BITSOF_INT == 16
#ifndef NPY_INT16
#define NPY_INT16 NPY_INT
#define NPY_UINT16 NPY_UINT
        typedef int npy_int16;
        typedef unsigned int npy_uint16;
#    define PyInt16ScalarObject PyIntScalarObject
#    define PyInt16ArrType_Type PyIntArrType_Type
#    define PyUInt16ScalarObject PyIntUScalarObject
#    define PyUInt16ArrType_Type PyIntUArrType_Type
#define NPY_INT16_FMT NPY_INT_FMT
#define NPY_UINT16_FMT NPY_UINT_FMT
#endif
#elif NPY_BITSOF_INT == 32
#ifndef NPY_INT32
#define NPY_INT32 NPY_INT
#define NPY_UINT32 NPY_UINT
        typedef int npy_int32;
        typedef unsigned int npy_uint32;
        typedef unsigned int npy_ucs4;
#    define PyInt32ScalarObject PyIntScalarObject
#    define PyInt32ArrType_Type PyIntArrType_Type
#    define PyUInt32ScalarObject PyUIntScalarObject
#    define PyUInt32ArrType_Type PyUIntArrType_Type
#define NPY_INT32_FMT NPY_INT_FMT
#define NPY_UINT32_FMT NPY_UINT_FMT
#endif
#elif NPY_BITSOF_INT == 64
#ifndef NPY_INT64
#define NPY_INT64 NPY_INT
#define NPY_UINT64 NPY_UINT
        typedef int npy_int64;
        typedef unsigned int npy_uint64;
#    define PyInt64ScalarObject PyIntScalarObject
#    define PyInt64ArrType_Type PyIntArrType_Type
#    define PyUInt64ScalarObject PyUIntScalarObject
#    define PyUInt64ArrType_Type PyUIntArrType_Type
#define NPY_INT64_FMT NPY_INT_FMT
#define NPY_UINT64_FMT NPY_UINT_FMT
#    define MyPyLong_FromInt64 PyLong_FromLong
#    define MyPyLong_AsInt64 PyLong_AsLong
#endif
#elif NPY_BITSOF_INT == 128
#ifndef NPY_INT128
#define NPY_INT128 NPY_INT
#define NPY_UINT128 NPY_UINT
        typedef int npy_int128;
        typedef unsigned int npy_uint128;
#    define PyInt128ScalarObject PyIntScalarObject
#    define PyInt128ArrType_Type PyIntArrType_Type
#    define PyUInt128ScalarObject PyUIntScalarObject
#    define PyUInt128ArrType_Type PyUIntArrType_Type
#define NPY_INT128_FMT NPY_INT_FMT
#define NPY_UINT128_FMT NPY_UINT_FMT
#endif
#endif

#if NPY_BITSOF_SHORT == 8
#ifndef NPY_INT8
#define NPY_INT8 NPY_SHORT
#define NPY_UINT8 NPY_USHORT
        typedef short npy_int8;
        typedef unsigned short npy_uint8;
#    define PyInt8ScalarObject PyShortScalarObject
#    define PyInt8ArrType_Type PyShortArrType_Type
#    define PyUInt8ScalarObject PyUShortScalarObject
#    define PyUInt8ArrType_Type PyUShortArrType_Type
#define NPY_INT8_FMT NPY_SHORT_FMT
#define NPY_UINT8_FMT NPY_USHORT_FMT
#endif
#elif NPY_BITSOF_SHORT == 16
#ifndef NPY_INT16
#define NPY_INT16 NPY_SHORT
#define NPY_UINT16 NPY_USHORT
        typedef short npy_int16;
        typedef unsigned short npy_uint16;
#    define PyInt16ScalarObject PyShortScalarObject
#    define PyInt16ArrType_Type PyShortArrType_Type
#    define PyUInt16ScalarObject PyUShortScalarObject
#    define PyUInt16ArrType_Type PyUShortArrType_Type
#define NPY_INT16_FMT NPY_SHORT_FMT
#define NPY_UINT16_FMT NPY_USHORT_FMT
#endif
#elif NPY_BITSOF_SHORT == 32
#ifndef NPY_INT32
#define NPY_INT32 NPY_SHORT
#define NPY_UINT32 NPY_USHORT
        typedef short npy_int32;
        typedef unsigned short npy_uint32;
        typedef unsigned short npy_ucs4;
#    define PyInt32ScalarObject PyShortScalarObject
#    define PyInt32ArrType_Type PyShortArrType_Type
#    define PyUInt32ScalarObject PyUShortScalarObject
#    define PyUInt32ArrType_Type PyUShortArrType_Type
#define NPY_INT32_FMT NPY_SHORT_FMT
#define NPY_UINT32_FMT NPY_USHORT_FMT
#endif
#elif NPY_BITSOF_SHORT == 64
#ifndef NPY_INT64
#define NPY_INT64 NPY_SHORT
#define NPY_UINT64 NPY_USHORT
        typedef short npy_int64;
        typedef unsigned short npy_uint64;
#    define PyInt64ScalarObject PyShortScalarObject
#    define PyInt64ArrType_Type PyShortArrType_Type
#    define PyUInt64ScalarObject PyUShortScalarObject
#    define PyUInt64ArrType_Type PyUShortArrType_Type
#define NPY_INT64_FMT NPY_SHORT_FMT
#define NPY_UINT64_FMT NPY_USHORT_FMT
#    define MyPyLong_FromInt64 PyLong_FromLong
#    define MyPyLong_AsInt64 PyLong_AsLong
#endif
#elif NPY_BITSOF_SHORT == 128
#ifndef NPY_INT128
#define NPY_INT128 NPY_SHORT
#define NPY_UINT128 NPY_USHORT
        typedef short npy_int128;
        typedef unsigned short npy_uint128;
#    define PyInt128ScalarObject PyShortScalarObject
#    define PyInt128ArrType_Type PyShortArrType_Type
#    define PyUInt128ScalarObject PyUShortScalarObject
#    define PyUInt128ArrType_Type PyUShortArrType_Type
#define NPY_INT128_FMT NPY_SHORT_FMT
#define NPY_UINT128_FMT NPY_USHORT_FMT
#endif
#endif


#if NPY_BITSOF_CHAR == 8
#ifndef NPY_INT8
#define NPY_INT8 NPY_BYTE
#define NPY_UINT8 NPY_UBYTE
        typedef signed char npy_int8;
        typedef unsigned char npy_uint8;
#    define PyInt8ScalarObject PyByteScalarObject
#    define PyInt8ArrType_Type PyByteArrType_Type
#    define PyUInt8ScalarObject PyUByteScalarObject
#    define PyUInt8ArrType_Type PyUByteArrType_Type
#define NPY_INT8_FMT NPY_BYTE_FMT
#define NPY_UINT8_FMT NPY_UBYTE_FMT
#endif
#elif NPY_BITSOF_CHAR == 16
#ifndef NPY_INT16
#define NPY_INT16 NPY_BYTE
#define NPY_UINT16 NPY_UBYTE
        typedef signed char npy_int16;
        typedef unsigned char npy_uint16;
#    define PyInt16ScalarObject PyByteScalarObject
#    define PyInt16ArrType_Type PyByteArrType_Type
#    define PyUInt16ScalarObject PyUByteScalarObject
#    define PyUInt16ArrType_Type PyUByteArrType_Type
#define NPY_INT16_FMT NPY_BYTE_FMT
#define NPY_UINT16_FMT NPY_UBYTE_FMT
#endif
#elif NPY_BITSOF_CHAR == 32
#ifndef NPY_INT32
#define NPY_INT32 NPY_BYTE
#define NPY_UINT32 NPY_UBYTE
        typedef signed char npy_int32;
        typedef unsigned char npy_uint32;
        typedef unsigned char npy_ucs4;
#    define PyInt32ScalarObject PyByteScalarObject
#    define PyInt32ArrType_Type PyByteArrType_Type
#    define PyUInt32ScalarObject PyUByteScalarObject
#    define PyUInt32ArrType_Type PyUByteArrType_Type
#define NPY_INT32_FMT NPY_BYTE_FMT
#define NPY_UINT32_FMT NPY_UBYTE_FMT
#endif
#elif NPY_BITSOF_CHAR == 64
#ifndef NPY_INT64
#define NPY_INT64 NPY_BYTE
#define NPY_UINT64 NPY_UBYTE
        typedef signed char npy_int64;
        typedef unsigned char npy_uint64;
#    define PyInt64ScalarObject PyByteScalarObject
#    define PyInt64ArrType_Type PyByteArrType_Type
#    define PyUInt64ScalarObject PyUByteScalarObject
#    define PyUInt64ArrType_Type PyUByteArrType_Type
#define NPY_INT64_FMT NPY_BYTE_FMT
#define NPY_UINT64_FMT NPY_UBYTE_FMT
#    define MyPyLong_FromInt64 PyLong_FromLong
#    define MyPyLong_AsInt64 PyLong_AsLong
#endif
#elif NPY_BITSOF_CHAR == 128
#ifndef NPY_INT128
#define NPY_INT128 NPY_BYTE
#define NPY_UINT128 NPY_UBYTE
        typedef signed char npy_int128;
        typedef unsigned char npy_uint128;
#    define PyInt128ScalarObject PyByteScalarObject
#    define PyInt128ArrType_Type PyByteArrType_Type
#    define PyUInt128ScalarObject PyUByteScalarObject
#    define PyUInt128ArrType_Type PyUByteArrType_Type
#define NPY_INT128_FMT NPY_BYTE_FMT
#define NPY_UINT128_FMT NPY_UBYTE_FMT
#endif
#endif



#if NPY_BITSOF_DOUBLE == 32
#ifndef NPY_FLOAT32
#define NPY_FLOAT32 NPY_DOUBLE
#define NPY_COMPLEX64 NPY_CDOUBLE
        typedef double npy_float32;
        typedef npy_cdouble npy_complex64;
#    define PyFloat32ScalarObject PyDoubleScalarObject
#    define PyComplex64ScalarObject PyCDoubleScalarObject
#    define PyFloat32ArrType_Type PyDoubleArrType_Type
#    define PyComplex64ArrType_Type PyCDoubleArrType_Type
#define NPY_FLOAT32_FMT NPY_DOUBLE_FMT
#define NPY_COMPLEX64_FMT NPY_CDOUBLE_FMT
#endif
#elif NPY_BITSOF_DOUBLE == 64
#ifndef NPY_FLOAT64
#define NPY_FLOAT64 NPY_DOUBLE
#define NPY_COMPLEX128 NPY_CDOUBLE
        typedef double npy_float64;
        typedef npy_cdouble npy_complex128;
#    define PyFloat64ScalarObject PyDoubleScalarObject
#    define PyComplex128ScalarObject PyCDoubleScalarObject
#    define PyFloat64ArrType_Type PyDoubleArrType_Type
#    define PyComplex128ArrType_Type PyCDoubleArrType_Type
#define NPY_FLOAT64_FMT NPY_DOUBLE_FMT
#define NPY_COMPLEX128_FMT NPY_CDOUBLE_FMT
#endif
#elif NPY_BITSOF_DOUBLE == 80
#ifndef NPY_FLOAT80
#define NPY_FLOAT80 NPY_DOUBLE
#define NPY_COMPLEX160 NPY_CDOUBLE
        typedef double npy_float80;
        typedef npy_cdouble npy_complex160;
#    define PyFloat80ScalarObject PyDoubleScalarObject
#    define PyComplex160ScalarObject PyCDoubleScalarObject
#    define PyFloat80ArrType_Type PyDoubleArrType_Type
#    define PyComplex160ArrType_Type PyCDoubleArrType_Type
#define NPY_FLOAT80_FMT NPY_DOUBLE_FMT
#define NPY_COMPLEX160_FMT NPY_CDOUBLE_FMT
#endif
#elif NPY_BITSOF_DOUBLE == 96
#ifndef NPY_FLOAT96
#define NPY_FLOAT96 NPY_DOUBLE
#define NPY_COMPLEX192 NPY_CDOUBLE
        typedef double npy_float96;
        typedef npy_cdouble npy_complex192;
#    define PyFloat96ScalarObject PyDoubleScalarObject
#    define PyComplex192ScalarObject PyCDoubleScalarObject
#    define PyFloat96ArrType_Type PyDoubleArrType_Type
#    define PyComplex192ArrType_Type PyCDoubleArrType_Type
#define NPY_FLOAT96_FMT NPY_DOUBLE_FMT
#define NPY_COMPLEX192_FMT NPY_CDOUBLE_FMT
#endif
#elif NPY_BITSOF_DOUBLE == 128
#ifndef NPY_FLOAT128
#define NPY_FLOAT128 NPY_DOUBLE
#define NPY_COMPLEX256 NPY_CDOUBLE
        typedef double npy_float128;
        typedef npy_cdouble npy_complex256;
#    define PyFloat128ScalarObject PyDoubleScalarObject
#    define PyComplex256ScalarObject PyCDoubleScalarObject
#    define PyFloat128ArrType_Type PyDoubleArrType_Type
#    define PyComplex256ArrType_Type PyCDoubleArrType_Type
#define NPY_FLOAT128_FMT NPY_DOUBLE_FMT
#define NPY_COMPLEX256_FMT NPY_CDOUBLE_FMT
#endif
#endif



#if NPY_BITSOF_FLOAT == 32
#ifndef NPY_FLOAT32
#define NPY_FLOAT32 NPY_FLOAT
#define NPY_COMPLEX64 NPY_CFLOAT
        typedef float npy_float32;
        typedef npy_cfloat npy_complex64;
#    define PyFloat32ScalarObject PyFloatScalarObject
#    define PyComplex64ScalarObject PyCFloatScalarObject
#    define PyFloat32ArrType_Type PyFloatArrType_Type
#    define PyComplex64ArrType_Type PyCFloatArrType_Type
#define NPY_FLOAT32_FMT NPY_FLOAT_FMT
#define NPY_COMPLEX64_FMT NPY_CFLOAT_FMT
#endif
#elif NPY_BITSOF_FLOAT == 64
#ifndef NPY_FLOAT64
#define NPY_FLOAT64 NPY_FLOAT
#define NPY_COMPLEX128 NPY_CFLOAT
        typedef float npy_float64;
        typedef npy_cfloat npy_complex128;
#    define PyFloat64ScalarObject PyFloatScalarObject
#    define PyComplex128ScalarObject PyCFloatScalarObject
#    define PyFloat64ArrType_Type PyFloatArrType_Type
#    define PyComplex128ArrType_Type PyCFloatArrType_Type
#define NPY_FLOAT64_FMT NPY_FLOAT_FMT
#define NPY_COMPLEX128_FMT NPY_CFLOAT_FMT
#endif
#elif NPY_BITSOF_FLOAT == 80
#ifndef NPY_FLOAT80
#define NPY_FLOAT80 NPY_FLOAT
#define NPY_COMPLEX160 NPY_CFLOAT
        typedef float npy_float80;
        typedef npy_cfloat npy_complex160;
#    define PyFloat80ScalarObject PyFloatScalarObject
#    define PyComplex160ScalarObject PyCFloatScalarObject
#    define PyFloat80ArrType_Type PyFloatArrType_Type
#    define PyComplex160ArrType_Type PyCFloatArrType_Type
#define NPY_FLOAT80_FMT NPY_FLOAT_FMT
#define NPY_COMPLEX160_FMT NPY_CFLOAT_FMT
#endif
#elif NPY_BITSOF_FLOAT == 96
#ifndef NPY_FLOAT96
#define NPY_FLOAT96 NPY_FLOAT
#define NPY_COMPLEX192 NPY_CFLOAT
        typedef float npy_float96;
        typedef npy_cfloat npy_complex192;
#    define PyFloat96ScalarObject PyFloatScalarObject
#    define PyComplex192ScalarObject PyCFloatScalarObject
#    define PyFloat96ArrType_Type PyFloatArrType_Type
#    define PyComplex192ArrType_Type PyCFloatArrType_Type
#define NPY_FLOAT96_FMT NPY_FLOAT_FMT
#define NPY_COMPLEX192_FMT NPY_CFLOAT_FMT
#endif
#elif NPY_BITSOF_FLOAT == 128
#ifndef NPY_FLOAT128
#define NPY_FLOAT128 NPY_FLOAT
#define NPY_COMPLEX256 NPY_CFLOAT
        typedef float npy_float128;
        typedef npy_cfloat npy_complex256;
#    define PyFloat128ScalarObject PyFloatScalarObject
#    define PyComplex256ScalarObject PyCFloatScalarObject
#    define PyFloat128ArrType_Type PyFloatArrType_Type
#    define PyComplex256ArrType_Type PyCFloatArrType_Type
#define NPY_FLOAT128_FMT NPY_FLOAT_FMT
#define NPY_COMPLEX256_FMT NPY_CFLOAT_FMT
#endif
#endif

/* half/float16 isn't a floating-point type in C */
#define NPY_FLOAT16 NPY_HALF
typedef npy_uint16 npy_half;
typedef npy_half npy_float16;

#if NPY_BITSOF_LONGDOUBLE == 32
#ifndef NPY_FLOAT32
#define NPY_FLOAT32 NPY_LONGDOUBLE
#define NPY_COMPLEX64 NPY_CLONGDOUBLE
        typedef npy_longdouble npy_float32;
        typedef npy_clongdouble npy_complex64;
#    define PyFloat32ScalarObject PyLongDoubleScalarObject
#    define PyComplex64ScalarObject PyCLongDoubleScalarObject
#    define PyFloat32ArrType_Type PyLongDoubleArrType_Type
#    define PyComplex64ArrType_Type PyCLongDoubleArrType_Type
#define NPY_FLOAT32_FMT NPY_LONGDOUBLE_FMT
#define NPY_COMPLEX64_FMT NPY_CLONGDOUBLE_FMT
#endif
#elif NPY_BITSOF_LONGDOUBLE == 64
#ifndef NPY_FLOAT64
#define NPY_FLOAT64 NPY_LONGDOUBLE
#define NPY_COMPLEX128 NPY_CLONGDOUBLE
        typedef npy_longdouble npy_float64;
        typedef npy_clongdouble npy_complex128;
#    define PyFloat64ScalarObject PyLongDoubleScalarObject
#    define PyComplex128ScalarObject PyCLongDoubleScalarObject
#    define PyFloat64ArrType_Type PyLongDoubleArrType_Type
#    define PyComplex128ArrType_Type PyCLongDoubleArrType_Type
#define NPY_FLOAT64_FMT NPY_LONGDOUBLE_FMT
#define NPY_COMPLEX128_FMT NPY_CLONGDOUBLE_FMT
#endif
#elif NPY_BITSOF_LONGDOUBLE == 80
#ifndef NPY_FLOAT80
#define NPY_FLOAT80 NPY_LONGDOUBLE
#define NPY_COMPLEX160 NPY_CLONGDOUBLE
        typedef npy_longdouble npy_float80;
        typedef npy_clongdouble npy_complex160;
#    define PyFloat80ScalarObject PyLongDoubleScalarObject
#    define PyComplex160ScalarObject PyCLongDoubleScalarObject
#    define PyFloat80ArrType_Type PyLongDoubleArrType_Type
#    define PyComplex160ArrType_Type PyCLongDoubleArrType_Type
#define NPY_FLOAT80_FMT NPY_LONGDOUBLE_FMT
#define NPY_COMPLEX160_FMT NPY_CLONGDOUBLE_FMT
#endif
#elif NPY_BITSOF_LONGDOUBLE == 96
#ifndef NPY_FLOAT96
#define NPY_FLOAT96 NPY_LONGDOUBLE
#define NPY_COMPLEX192 NPY_CLONGDOUBLE
        typedef npy_longdouble npy_float96;
        typedef npy_clongdouble npy_complex192;
#    define PyFloat96ScalarObject PyLongDoubleScalarObject
#    define PyComplex192ScalarObject PyCLongDoubleScalarObject
#    define PyFloat96ArrType_Type PyLongDoubleArrType_Type
#    define PyComplex192ArrType_Type PyCLongDoubleArrType_Type
#define NPY_FLOAT96_FMT NPY_LONGDOUBLE_FMT
#define NPY_COMPLEX192_FMT NPY_CLONGDOUBLE_FMT
#endif
#elif NPY_BITSOF_LONGDOUBLE == 128
#ifndef NPY_FLOAT128
#define NPY_FLOAT128 NPY_LONGDOUBLE
#define NPY_COMPLEX256 NPY_CLONGDOUBLE
        typedef npy_longdouble npy_float128;
        typedef npy_clongdouble npy_complex256;
#    define PyFloat128ScalarObject PyLongDoubleScalarObject
#    define PyComplex256ScalarObject PyCLongDoubleScalarObject
#    define PyFloat128ArrType_Type PyLongDoubleArrType_Type
#    define PyComplex256ArrType_Type PyCLongDoubleArrType_Type
#define NPY_FLOAT128_FMT NPY_LONGDOUBLE_FMT
#define NPY_COMPLEX256_FMT NPY_CLONGDOUBLE_FMT
#endif
#elif NPY_BITSOF_LONGDOUBLE == 256
#define NPY_FLOAT256 NPY_LONGDOUBLE
#define NPY_COMPLEX512 NPY_CLONGDOUBLE
        typedef npy_longdouble npy_float256;
        typedef npy_clongdouble npy_complex512;
#    define PyFloat256ScalarObject PyLongDoubleScalarObject
#    define PyComplex512ScalarObject PyCLongDoubleScalarObject
#    define PyFloat256ArrType_Type PyLongDoubleArrType_Type
#    define PyComplex512ArrType_Type PyCLongDoubleArrType_Type
#define NPY_FLOAT256_FMT NPY_LONGDOUBLE_FMT
#define NPY_COMPLEX512_FMT NPY_CLONGDOUBLE_FMT
#endif

/* datetime typedefs */
typedef npy_int64 npy_timedelta;
typedef npy_int64 npy_datetime;
#define NPY_DATETIME_FMT NPY_INT64_FMT
#define NPY_TIMEDELTA_FMT NPY_INT64_FMT

/* End of typedefs for numarray style bit-width names */

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_NPY_COMMON_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/npy_cpu.h

```plaintext
/*
 * This set (target) cpu specific macros:
 *      - Possible values:
 *              NPY_CPU_X86
 *              NPY_CPU_AMD64
 *              NPY_CPU_PPC
 *              NPY_CPU_PPC64
 *              NPY_CPU_PPC64LE
 *              NPY_CPU_SPARC
 *              NPY_CPU_S390
 *              NPY_CPU_IA64
 *              NPY_CPU_HPPA
 *              NPY_CPU_ALPHA
 *              NPY_CPU_ARMEL
 *              NPY_CPU_ARMEB
 *              NPY_CPU_SH_LE
 *              NPY_CPU_SH_BE
 *              NPY_CPU_ARCEL
 *              NPY_CPU_ARCEB
 *              NPY_CPU_RISCV64
 *              NPY_CPU_LOONGARCH
 *              NPY_CPU_WASM
 */
#ifndef NUMPY_CORE_INCLUDE_NUMPY_NPY_CPU_H_
#define NUMPY_CORE_INCLUDE_NUMPY_NPY_CPU_H_

#include "numpyconfig.h"

#if defined( __i386__ ) || defined(i386) || defined(_M_IX86)
    /*
     * __i386__ is defined by gcc and Intel compiler on Linux,
     * _M_IX86 by VS compiler,
     * i386 by Sun compilers on opensolaris at least
     */
    #define NPY_CPU_X86
#elif defined(__x86_64__) || defined(__amd64__) || defined(__x86_64) || defined(_M_AMD64)
    /*
     * both __x86_64__ and __amd64__ are defined by gcc
     * __x86_64 defined by sun compiler on opensolaris at least
     * _M_AMD64 defined by MS compiler
     */
    #define NPY_CPU_AMD64
#elif defined(__powerpc64__) && defined(__LITTLE_ENDIAN__)
    #define NPY_CPU_PPC64LE
#elif defined(__powerpc64__) && defined(__BIG_ENDIAN__)
    #define NPY_CPU_PPC64
#elif defined(__ppc__) || defined(__powerpc__) || defined(_ARCH_PPC)
    /*
     * __ppc__ is defined by gcc, I remember having seen __powerpc__ once,
     * but can't find it ATM
     * _ARCH_PPC is used by at least gcc on AIX
     * As __powerpc__ and _ARCH_PPC are also defined by PPC64 check
     * for those specifically first before defaulting to ppc
     */
    #define NPY_CPU_PPC
#elif defined(__sparc__) || defined(__sparc)
    /* __sparc__ is defined by gcc and Forte (e.g. Sun) compilers */
    #define NPY_CPU_SPARC
#elif defined(__s390__)
    #define NPY_CPU_S390
#elif defined(__ia64)
    #define NPY_CPU_IA64
#elif defined(__hppa)
    #define NPY_CPU_HPPA
#elif defined(__alpha__)
    #define NPY_CPU_ALPHA
#elif defined(__arm__) || defined(__aarch64__) || defined(_M_ARM64)
    /* _M_ARM64 is defined in MSVC for ARM64 compilation on Windows */
    #if defined(__ARMEB__) || defined(__AARCH64EB__)
        #if defined(__ARM_32BIT_STATE)
            #define NPY_CPU_ARMEB_AARCH32
        #elif defined(__ARM_64BIT_STATE)
            #define NPY_CPU_ARMEB_AARCH64
        #else
            #define NPY_CPU_ARMEB
        #endif
    #elif defined(__ARMEL__) || defined(__AARCH64EL__) || defined(_M_ARM64)
        #if defined(__ARM_32BIT_STATE)
            #define NPY_CPU_ARMEL_AARCH32
        #elif defined(__ARM_64BIT_STATE) || defined(_M_ARM64)
            #define NPY_CPU_ARMEL_AARCH64
        #else
            #define NPY_CPU_ARMEL
        #endif
    #else
        # error Unknown ARM CPU, please report this to numpy maintainers with \
	information about your platform (OS, CPU and compiler)
    #endif
#elif defined(__sh__) && defined(__LITTLE_ENDIAN__)
    #define NPY_CPU_SH_LE
#elif defined(__sh__) && defined(__BIG_ENDIAN__)
    #define NPY_CPU_SH_BE
#elif defined(__MIPSEL__)
    #define NPY_CPU_MIPSEL
#elif defined(__MIPSEB__)
    #define NPY_CPU_MIPSEB
#elif defined(__or1k__)
    #define NPY_CPU_OR1K
#elif defined(__mc68000__)
    #define NPY_CPU_M68K
#elif defined(__arc__) && defined(__LITTLE_ENDIAN__)
    #define NPY_CPU_ARCEL
#elif defined(__arc__) && defined(__BIG_ENDIAN__)
    #define NPY_CPU_ARCEB
#elif defined(__riscv) && defined(__riscv_xlen) && __riscv_xlen == 64
    #define NPY_CPU_RISCV64
#elif defined(__loongarch__)
    #define NPY_CPU_LOONGARCH
#elif defined(__EMSCRIPTEN__)
    /* __EMSCRIPTEN__ is defined by emscripten: an LLVM-to-Web compiler */
    #define NPY_CPU_WASM
#else
    #error Unknown CPU, please report this to numpy maintainers with \
    information about your platform (OS, CPU and compiler)
#endif

/*
 * Except for the following architectures, memory access is limited to the natural
 * alignment of data types otherwise it may lead to bus error or performance regression.
 * For more details about unaligned access, see https://www.kernel.org/doc/Documentation/unaligned-memory-access.txt.
*/
#if defined(NPY_CPU_X86) || defined(NPY_CPU_AMD64) || defined(__aarch64__) || defined(__powerpc64__)
    #define NPY_ALIGNMENT_REQUIRED 0
#endif
#ifndef NPY_ALIGNMENT_REQUIRED
    #define NPY_ALIGNMENT_REQUIRED 1
#endif

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_NPY_CPU_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/npy_endian.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY_NPY_ENDIAN_H_
#define NUMPY_CORE_INCLUDE_NUMPY_NPY_ENDIAN_H_

/*
 * NPY_BYTE_ORDER is set to the same value as BYTE_ORDER set by glibc in
 * endian.h
 */

#if defined(NPY_HAVE_ENDIAN_H) || defined(NPY_HAVE_SYS_ENDIAN_H)
    /* Use endian.h if available */

    #if defined(NPY_HAVE_ENDIAN_H)
    #include <endian.h>
    #elif defined(NPY_HAVE_SYS_ENDIAN_H)
    #include <sys/endian.h>
    #endif

    #if defined(BYTE_ORDER) && defined(BIG_ENDIAN) && defined(LITTLE_ENDIAN)
        #define NPY_BYTE_ORDER    BYTE_ORDER
        #define NPY_LITTLE_ENDIAN LITTLE_ENDIAN
        #define NPY_BIG_ENDIAN    BIG_ENDIAN
    #elif defined(_BYTE_ORDER) && defined(_BIG_ENDIAN) && defined(_LITTLE_ENDIAN)
        #define NPY_BYTE_ORDER    _BYTE_ORDER
        #define NPY_LITTLE_ENDIAN _LITTLE_ENDIAN
        #define NPY_BIG_ENDIAN    _BIG_ENDIAN
    #elif defined(__BYTE_ORDER) && defined(__BIG_ENDIAN) && defined(__LITTLE_ENDIAN)
        #define NPY_BYTE_ORDER    __BYTE_ORDER
        #define NPY_LITTLE_ENDIAN __LITTLE_ENDIAN
        #define NPY_BIG_ENDIAN    __BIG_ENDIAN
    #endif
#endif

#ifndef NPY_BYTE_ORDER
    /* Set endianness info using target CPU */
    #include "npy_cpu.h"

    #define NPY_LITTLE_ENDIAN 1234
    #define NPY_BIG_ENDIAN 4321

    #if defined(NPY_CPU_X86)                  \
            || defined(NPY_CPU_AMD64)         \
            || defined(NPY_CPU_IA64)          \
            || defined(NPY_CPU_ALPHA)         \
            || defined(NPY_CPU_ARMEL)         \
            || defined(NPY_CPU_ARMEL_AARCH32) \
            || defined(NPY_CPU_ARMEL_AARCH64) \
            || defined(NPY_CPU_SH_LE)         \
            || defined(NPY_CPU_MIPSEL)        \
            || defined(NPY_CPU_PPC64LE)       \
            || defined(NPY_CPU_ARCEL)         \
            || defined(NPY_CPU_RISCV64)       \
            || defined(NPY_CPU_LOONGARCH)     \
            || defined(NPY_CPU_WASM)
        #define NPY_BYTE_ORDER NPY_LITTLE_ENDIAN

    #elif defined(NPY_CPU_PPC)                \
            || defined(NPY_CPU_SPARC)         \
            || defined(NPY_CPU_S390)          \
            || defined(NPY_CPU_HPPA)          \
            || defined(NPY_CPU_PPC64)         \
            || defined(NPY_CPU_ARMEB)         \
            || defined(NPY_CPU_ARMEB_AARCH32) \
            || defined(NPY_CPU_ARMEB_AARCH64) \
            || defined(NPY_CPU_SH_BE)         \
            || defined(NPY_CPU_MIPSEB)        \
            || defined(NPY_CPU_OR1K)          \
            || defined(NPY_CPU_M68K)          \
            || defined(NPY_CPU_ARCEB)
        #define NPY_BYTE_ORDER NPY_BIG_ENDIAN

    #else
        #error Unknown CPU: can not set endianness
    #endif

#endif

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_NPY_ENDIAN_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/npy_interrupt.h

```plaintext
/*
 * This API is only provided because it is part of publicly exported
 * headers. Its use is considered DEPRECATED, and it will be removed
 * eventually.
 * (This includes the _PyArray_SigintHandler and _PyArray_GetSigintBuf
 * functions which are however, public API, and not headers.)
 *
 * Instead of using these non-threadsafe macros consider periodically
 * querying `PyErr_CheckSignals()` or `PyOS_InterruptOccurred()` will work.
 * Both of these require holding the GIL, although cpython could add a
 * version of `PyOS_InterruptOccurred()` which does not. Such a version
 * actually exists as private API in Python 3.10, and backported to 3.9 and 3.8,
 * see also https://bugs.python.org/issue41037 and
 * https://github.com/python/cpython/pull/20599).
 */

#ifndef NUMPY_CORE_INCLUDE_NUMPY_NPY_INTERRUPT_H_
#define NUMPY_CORE_INCLUDE_NUMPY_NPY_INTERRUPT_H_

#ifndef NPY_NO_SIGNAL

#include <setjmp.h>
#include <signal.h>

#ifndef sigsetjmp

#define NPY_SIGSETJMP(arg1, arg2) setjmp(arg1)
#define NPY_SIGLONGJMP(arg1, arg2) longjmp(arg1, arg2)
#define NPY_SIGJMP_BUF jmp_buf

#else

#define NPY_SIGSETJMP(arg1, arg2) sigsetjmp(arg1, arg2)
#define NPY_SIGLONGJMP(arg1, arg2) siglongjmp(arg1, arg2)
#define NPY_SIGJMP_BUF sigjmp_buf

#endif

#    define NPY_SIGINT_ON {                                             \
                   PyOS_sighandler_t _npy_sig_save;                     \
                   _npy_sig_save = PyOS_setsig(SIGINT, _PyArray_SigintHandler); \
                   if (NPY_SIGSETJMP(*((NPY_SIGJMP_BUF *)_PyArray_GetSigintBuf()), \
                                 1) == 0) {                             \

#    define NPY_SIGINT_OFF }                                      \
        PyOS_setsig(SIGINT, _npy_sig_save);                       \
        }

#else  /* NPY_NO_SIGNAL  */

#define NPY_SIGINT_ON
#define NPY_SIGINT_OFF

#endif  /* HAVE_SIGSETJMP */

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_NPY_INTERRUPT_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/npy_math.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY_NPY_MATH_H_
#define NUMPY_CORE_INCLUDE_NUMPY_NPY_MATH_H_

#include <numpy/npy_common.h>

#include <math.h>

/* By adding static inline specifiers to npy_math function definitions when
   appropriate, compiler is given the opportunity to optimize */
#if NPY_INLINE_MATH
#define NPY_INPLACE NPY_INLINE static
#else
#define NPY_INPLACE
#endif


#ifdef __cplusplus
extern "C" {
#endif

/*
 * NAN and INFINITY like macros (same behavior as glibc for NAN, same as C99
 * for INFINITY)
 *
 * XXX: I should test whether INFINITY and NAN are available on the platform
 */
NPY_INLINE static float __npy_inff(void)
{
    const union { npy_uint32 __i; float __f;} __bint = {0x7f800000UL};
    return __bint.__f;
}

NPY_INLINE static float __npy_nanf(void)
{
    const union { npy_uint32 __i; float __f;} __bint = {0x7fc00000UL};
    return __bint.__f;
}

NPY_INLINE static float __npy_pzerof(void)
{
    const union { npy_uint32 __i; float __f;} __bint = {0x00000000UL};
    return __bint.__f;
}

NPY_INLINE static float __npy_nzerof(void)
{
    const union { npy_uint32 __i; float __f;} __bint = {0x80000000UL};
    return __bint.__f;
}

#define NPY_INFINITYF __npy_inff()
#define NPY_NANF __npy_nanf()
#define NPY_PZEROF __npy_pzerof()
#define NPY_NZEROF __npy_nzerof()

#define NPY_INFINITY ((npy_double)NPY_INFINITYF)
#define NPY_NAN ((npy_double)NPY_NANF)
#define NPY_PZERO ((npy_double)NPY_PZEROF)
#define NPY_NZERO ((npy_double)NPY_NZEROF)

#define NPY_INFINITYL ((npy_longdouble)NPY_INFINITYF)
#define NPY_NANL ((npy_longdouble)NPY_NANF)
#define NPY_PZEROL ((npy_longdouble)NPY_PZEROF)
#define NPY_NZEROL ((npy_longdouble)NPY_NZEROF)

/*
 * Useful constants
 */
#define NPY_E         2.718281828459045235360287471352662498  /* e */
#define NPY_LOG2E     1.442695040888963407359924681001892137  /* log_2 e */
#define NPY_LOG10E    0.434294481903251827651128918916605082  /* log_10 e */
#define NPY_LOGE2     0.693147180559945309417232121458176568  /* log_e 2 */
#define NPY_LOGE10    2.302585092994045684017991454684364208  /* log_e 10 */
#define NPY_PI        3.141592653589793238462643383279502884  /* pi */
#define NPY_PI_2      1.570796326794896619231321691639751442  /* pi/2 */
#define NPY_PI_4      0.785398163397448309615660845819875721  /* pi/4 */
#define NPY_1_PI      0.318309886183790671537767526745028724  /* 1/pi */
#define NPY_2_PI      0.636619772367581343075535053490057448  /* 2/pi */
#define NPY_EULER     0.577215664901532860606512090082402431  /* Euler constant */
#define NPY_SQRT2     1.414213562373095048801688724209698079  /* sqrt(2) */
#define NPY_SQRT1_2   0.707106781186547524400844362104849039  /* 1/sqrt(2) */

#define NPY_Ef        2.718281828459045235360287471352662498F /* e */
#define NPY_LOG2Ef    1.442695040888963407359924681001892137F /* log_2 e */
#define NPY_LOG10Ef   0.434294481903251827651128918916605082F /* log_10 e */
#define NPY_LOGE2f    0.693147180559945309417232121458176568F /* log_e 2 */
#define NPY_LOGE10f   2.302585092994045684017991454684364208F /* log_e 10 */
#define NPY_PIf       3.141592653589793238462643383279502884F /* pi */
#define NPY_PI_2f     1.570796326794896619231321691639751442F /* pi/2 */
#define NPY_PI_4f     0.785398163397448309615660845819875721F /* pi/4 */
#define NPY_1_PIf     0.318309886183790671537767526745028724F /* 1/pi */
#define NPY_2_PIf     0.636619772367581343075535053490057448F /* 2/pi */
#define NPY_EULERf    0.577215664901532860606512090082402431F /* Euler constant */
#define NPY_SQRT2f    1.414213562373095048801688724209698079F /* sqrt(2) */
#define NPY_SQRT1_2f  0.707106781186547524400844362104849039F /* 1/sqrt(2) */

#define NPY_El        2.718281828459045235360287471352662498L /* e */
#define NPY_LOG2El    1.442695040888963407359924681001892137L /* log_2 e */
#define NPY_LOG10El   0.434294481903251827651128918916605082L /* log_10 e */
#define NPY_LOGE2l    0.693147180559945309417232121458176568L /* log_e 2 */
#define NPY_LOGE10l   2.302585092994045684017991454684364208L /* log_e 10 */
#define NPY_PIl       3.141592653589793238462643383279502884L /* pi */
#define NPY_PI_2l     1.570796326794896619231321691639751442L /* pi/2 */
#define NPY_PI_4l     0.785398163397448309615660845819875721L /* pi/4 */
#define NPY_1_PIl     0.318309886183790671537767526745028724L /* 1/pi */
#define NPY_2_PIl     0.636619772367581343075535053490057448L /* 2/pi */
#define NPY_EULERl    0.577215664901532860606512090082402431L /* Euler constant */
#define NPY_SQRT2l    1.414213562373095048801688724209698079L /* sqrt(2) */
#define NPY_SQRT1_2l  0.707106781186547524400844362104849039L /* 1/sqrt(2) */

/*
 * Integer functions.
 */
NPY_INPLACE npy_uint npy_gcdu(npy_uint a, npy_uint b);
NPY_INPLACE npy_uint npy_lcmu(npy_uint a, npy_uint b);
NPY_INPLACE npy_ulong npy_gcdul(npy_ulong a, npy_ulong b);
NPY_INPLACE npy_ulong npy_lcmul(npy_ulong a, npy_ulong b);
NPY_INPLACE npy_ulonglong npy_gcdull(npy_ulonglong a, npy_ulonglong b);
NPY_INPLACE npy_ulonglong npy_lcmull(npy_ulonglong a, npy_ulonglong b);

NPY_INPLACE npy_int npy_gcd(npy_int a, npy_int b);
NPY_INPLACE npy_int npy_lcm(npy_int a, npy_int b);
NPY_INPLACE npy_long npy_gcdl(npy_long a, npy_long b);
NPY_INPLACE npy_long npy_lcml(npy_long a, npy_long b);
NPY_INPLACE npy_longlong npy_gcdll(npy_longlong a, npy_longlong b);
NPY_INPLACE npy_longlong npy_lcmll(npy_longlong a, npy_longlong b);

NPY_INPLACE npy_ubyte npy_rshiftuhh(npy_ubyte a, npy_ubyte b);
NPY_INPLACE npy_ubyte npy_lshiftuhh(npy_ubyte a, npy_ubyte b);
NPY_INPLACE npy_ushort npy_rshiftuh(npy_ushort a, npy_ushort b);
NPY_INPLACE npy_ushort npy_lshiftuh(npy_ushort a, npy_ushort b);
NPY_INPLACE npy_uint npy_rshiftu(npy_uint a, npy_uint b);
NPY_INPLACE npy_uint npy_lshiftu(npy_uint a, npy_uint b);
NPY_INPLACE npy_ulong npy_rshiftul(npy_ulong a, npy_ulong b);
NPY_INPLACE npy_ulong npy_lshiftul(npy_ulong a, npy_ulong b);
NPY_INPLACE npy_ulonglong npy_rshiftull(npy_ulonglong a, npy_ulonglong b);
NPY_INPLACE npy_ulonglong npy_lshiftull(npy_ulonglong a, npy_ulonglong b);

NPY_INPLACE npy_byte npy_rshifthh(npy_byte a, npy_byte b);
NPY_INPLACE npy_byte npy_lshifthh(npy_byte a, npy_byte b);
NPY_INPLACE npy_short npy_rshifth(npy_short a, npy_short b);
NPY_INPLACE npy_short npy_lshifth(npy_short a, npy_short b);
NPY_INPLACE npy_int npy_rshift(npy_int a, npy_int b);
NPY_INPLACE npy_int npy_lshift(npy_int a, npy_int b);
NPY_INPLACE npy_long npy_rshiftl(npy_long a, npy_long b);
NPY_INPLACE npy_long npy_lshiftl(npy_long a, npy_long b);
NPY_INPLACE npy_longlong npy_rshiftll(npy_longlong a, npy_longlong b);
NPY_INPLACE npy_longlong npy_lshiftll(npy_longlong a, npy_longlong b);

NPY_INPLACE uint8_t npy_popcountuhh(npy_ubyte a);
NPY_INPLACE uint8_t npy_popcountuh(npy_ushort a);
NPY_INPLACE uint8_t npy_popcountu(npy_uint a);
NPY_INPLACE uint8_t npy_popcountul(npy_ulong a);
NPY_INPLACE uint8_t npy_popcountull(npy_ulonglong a);
NPY_INPLACE uint8_t npy_popcounthh(npy_byte a);
NPY_INPLACE uint8_t npy_popcounth(npy_short a);
NPY_INPLACE uint8_t npy_popcount(npy_int a);
NPY_INPLACE uint8_t npy_popcountl(npy_long a);
NPY_INPLACE uint8_t npy_popcountll(npy_longlong a);

/*
 * C99 double math funcs that need fixups or are blocklist-able
 */
NPY_INPLACE double npy_sin(double x);
NPY_INPLACE double npy_cos(double x);
NPY_INPLACE double npy_tan(double x);
NPY_INPLACE double npy_hypot(double x, double y);
NPY_INPLACE double npy_log2(double x);
NPY_INPLACE double npy_atan2(double x, double y);

/* Mandatory C99 double math funcs, no blocklisting or fixups */
/* defined for legacy reasons, should be deprecated at some point */
#define npy_sinh sinh
#define npy_cosh cosh
#define npy_tanh tanh
#define npy_asin asin
#define npy_acos acos
#define npy_atan atan
#define npy_log log
#define npy_log10 log10
#define npy_cbrt cbrt
#define npy_fabs fabs
#define npy_ceil ceil
#define npy_fmod fmod
#define npy_floor floor
#define npy_expm1 expm1
#define npy_log1p log1p
#define npy_acosh acosh
#define npy_asinh asinh
#define npy_atanh atanh
#define npy_rint rint
#define npy_trunc trunc
#define npy_exp2 exp2
#define npy_frexp frexp
#define npy_ldexp ldexp
#define npy_copysign copysign
#define npy_exp exp
#define npy_sqrt sqrt
#define npy_pow pow
#define npy_modf modf

double npy_nextafter(double x, double y);

double npy_spacing(double x);

/*
 * IEEE 754 fpu handling. Those are guaranteed to be macros
 */

/* use builtins to avoid function calls in tight loops
 * only available if npy_config.h is available (= numpys own build) */
#ifdef HAVE___BUILTIN_ISNAN
    #define npy_isnan(x) __builtin_isnan(x)
#else
    #ifndef NPY_HAVE_DECL_ISNAN
        #define npy_isnan(x) ((x) != (x))
    #else
        #define npy_isnan(x) isnan(x)
    #endif
#endif


/* only available if npy_config.h is available (= numpys own build) */
#ifdef HAVE___BUILTIN_ISFINITE
    #define npy_isfinite(x) __builtin_isfinite(x)
#else
    #ifndef NPY_HAVE_DECL_ISFINITE
        #ifdef _MSC_VER
            #define npy_isfinite(x) _finite((x))
        #else
            #define npy_isfinite(x) !npy_isnan((x) + (-x))
        #endif
    #else
        #define npy_isfinite(x) isfinite((x))
    #endif
#endif

/* only available if npy_config.h is available (= numpys own build) */
#ifdef HAVE___BUILTIN_ISINF
    #define npy_isinf(x) __builtin_isinf(x)
#else
    #ifndef NPY_HAVE_DECL_ISINF
        #define npy_isinf(x) (!npy_isfinite(x) && !npy_isnan(x))
    #else
        #define npy_isinf(x) isinf((x))
    #endif
#endif

#ifndef NPY_HAVE_DECL_SIGNBIT
    int _npy_signbit_f(float x);
    int _npy_signbit_d(double x);
    int _npy_signbit_ld(long double x);
    #define npy_signbit(x) \
        (sizeof (x) == sizeof (long double) ? _npy_signbit_ld (x) \
         : sizeof (x) == sizeof (double) ? _npy_signbit_d (x) \
         : _npy_signbit_f (x))
#else
    #define npy_signbit(x) signbit((x))
#endif

/*
 * float C99 math funcs that need fixups or are blocklist-able
 */
NPY_INPLACE float npy_sinf(float x);
NPY_INPLACE float npy_cosf(float x);
NPY_INPLACE float npy_tanf(float x);
NPY_INPLACE float npy_expf(float x);
NPY_INPLACE float npy_sqrtf(float x);
NPY_INPLACE float npy_hypotf(float x, float y);
NPY_INPLACE float npy_log2f(float x);
NPY_INPLACE float npy_atan2f(float x, float y);
NPY_INPLACE float npy_powf(float x, float y);
NPY_INPLACE float npy_modff(float x, float* y);

/* Mandatory C99 float math funcs, no blocklisting or fixups */
/* defined for legacy reasons, should be deprecated at some point */

#define npy_sinhf sinhf
#define npy_coshf coshf
#define npy_tanhf tanhf
#define npy_asinf asinf
#define npy_acosf acosf
#define npy_atanf atanf
#define npy_logf logf
#define npy_log10f log10f
#define npy_cbrtf cbrtf
#define npy_fabsf fabsf
#define npy_ceilf ceilf
#define npy_fmodf fmodf
#define npy_floorf floorf
#define npy_expm1f expm1f
#define npy_log1pf log1pf
#define npy_asinhf asinhf
#define npy_acoshf acoshf
#define npy_atanhf atanhf
#define npy_rintf rintf
#define npy_truncf truncf
#define npy_exp2f exp2f
#define npy_frexpf frexpf
#define npy_ldexpf ldexpf
#define npy_copysignf copysignf

float npy_nextafterf(float x, float y);
float npy_spacingf(float x);

/*
 * long double C99 double math funcs that need fixups or are blocklist-able
 */
NPY_INPLACE npy_longdouble npy_sinl(npy_longdouble x);
NPY_INPLACE npy_longdouble npy_cosl(npy_longdouble x);
NPY_INPLACE npy_longdouble npy_tanl(npy_longdouble x);
NPY_INPLACE npy_longdouble npy_expl(npy_longdouble x);
NPY_INPLACE npy_longdouble npy_sqrtl(npy_longdouble x);
NPY_INPLACE npy_longdouble npy_hypotl(npy_longdouble x, npy_longdouble y);
NPY_INPLACE npy_longdouble npy_log2l(npy_longdouble x);
NPY_INPLACE npy_longdouble npy_atan2l(npy_longdouble x, npy_longdouble y);
NPY_INPLACE npy_longdouble npy_powl(npy_longdouble x, npy_longdouble y);
NPY_INPLACE npy_longdouble npy_modfl(npy_longdouble x, npy_longdouble* y);

/* Mandatory C99 double math funcs, no blocklisting or fixups */
/* defined for legacy reasons, should be deprecated at some point */
#define npy_sinhl sinhl
#define npy_coshl coshl
#define npy_tanhl tanhl
#define npy_fabsl fabsl
#define npy_floorl floorl
#define npy_ceill ceill
#define npy_rintl rintl
#define npy_truncl truncl
#define npy_cbrtl cbrtl
#define npy_log10l log10l
#define npy_logl logl
#define npy_expm1l expm1l
#define npy_asinl asinl
#define npy_acosl acosl
#define npy_atanl atanl
#define npy_asinhl asinhl
#define npy_acoshl acoshl
#define npy_atanhl atanhl
#define npy_log1pl log1pl
#define npy_exp2l exp2l
#define npy_fmodl fmodl
#define npy_frexpl frexpl
#define npy_ldexpl ldexpl
#define npy_copysignl copysignl

npy_longdouble npy_nextafterl(npy_longdouble x, npy_longdouble y);
npy_longdouble npy_spacingl(npy_longdouble x);

/*
 * Non standard functions
 */
NPY_INPLACE double npy_deg2rad(double x);
NPY_INPLACE double npy_rad2deg(double x);
NPY_INPLACE double npy_logaddexp(double x, double y);
NPY_INPLACE double npy_logaddexp2(double x, double y);
NPY_INPLACE double npy_divmod(double x, double y, double *modulus);
NPY_INPLACE double npy_heaviside(double x, double h0);

NPY_INPLACE float npy_deg2radf(float x);
NPY_INPLACE float npy_rad2degf(float x);
NPY_INPLACE float npy_logaddexpf(float x, float y);
NPY_INPLACE float npy_logaddexp2f(float x, float y);
NPY_INPLACE float npy_divmodf(float x, float y, float *modulus);
NPY_INPLACE float npy_heavisidef(float x, float h0);

NPY_INPLACE npy_longdouble npy_deg2radl(npy_longdouble x);
NPY_INPLACE npy_longdouble npy_rad2degl(npy_longdouble x);
NPY_INPLACE npy_longdouble npy_logaddexpl(npy_longdouble x, npy_longdouble y);
NPY_INPLACE npy_longdouble npy_logaddexp2l(npy_longdouble x, npy_longdouble y);
NPY_INPLACE npy_longdouble npy_divmodl(npy_longdouble x, npy_longdouble y,
                           npy_longdouble *modulus);
NPY_INPLACE npy_longdouble npy_heavisidel(npy_longdouble x, npy_longdouble h0);

#define npy_degrees npy_rad2deg
#define npy_degreesf npy_rad2degf
#define npy_degreesl npy_rad2degl

#define npy_radians npy_deg2rad
#define npy_radiansf npy_deg2radf
#define npy_radiansl npy_deg2radl

/*
 * Complex declarations
 */

/*
 * C99 specifies that complex numbers have the same representation as
 * an array of two elements, where the first element is the real part
 * and the second element is the imaginary part.
 */
#define __NPY_CPACK_IMP(x, y, type, ctype)   \
    union {                                  \
        ctype z;                             \
        type a[2];                           \
    } z1;                                    \
                                             \
    z1.a[0] = (x);                           \
    z1.a[1] = (y);                           \
                                             \
    return z1.z;

static NPY_INLINE npy_cdouble npy_cpack(double x, double y)
{
    __NPY_CPACK_IMP(x, y, double, npy_cdouble);
}

static NPY_INLINE npy_cfloat npy_cpackf(float x, float y)
{
    __NPY_CPACK_IMP(x, y, float, npy_cfloat);
}

static NPY_INLINE npy_clongdouble npy_cpackl(npy_longdouble x, npy_longdouble y)
{
    __NPY_CPACK_IMP(x, y, npy_longdouble, npy_clongdouble);
}
#undef __NPY_CPACK_IMP

/*
 * Same remark as above, but in the other direction: extract first/second
 * member of complex number, assuming a C99-compatible representation
 *
 * Those are defineds as static inline, and such as a reasonable compiler would
 * most likely compile this to one or two instructions (on CISC at least)
 */
#define __NPY_CEXTRACT_IMP(z, index, type, ctype)   \
    union {                                         \
        ctype z;                                    \
        type a[2];                                  \
    } __z_repr;                                     \
    __z_repr.z = z;                                 \
                                                    \
    return __z_repr.a[index];

static NPY_INLINE double npy_creal(npy_cdouble z)
{
    __NPY_CEXTRACT_IMP(z, 0, double, npy_cdouble);
}

static NPY_INLINE double npy_cimag(npy_cdouble z)
{
    __NPY_CEXTRACT_IMP(z, 1, double, npy_cdouble);
}

static NPY_INLINE float npy_crealf(npy_cfloat z)
{
    __NPY_CEXTRACT_IMP(z, 0, float, npy_cfloat);
}

static NPY_INLINE float npy_cimagf(npy_cfloat z)
{
    __NPY_CEXTRACT_IMP(z, 1, float, npy_cfloat);
}

static NPY_INLINE npy_longdouble npy_creall(npy_clongdouble z)
{
    __NPY_CEXTRACT_IMP(z, 0, npy_longdouble, npy_clongdouble);
}

static NPY_INLINE npy_longdouble npy_cimagl(npy_clongdouble z)
{
    __NPY_CEXTRACT_IMP(z, 1, npy_longdouble, npy_clongdouble);
}
#undef __NPY_CEXTRACT_IMP

/*
 * Double precision complex functions
 */
double npy_cabs(npy_cdouble z);
double npy_carg(npy_cdouble z);

npy_cdouble npy_cexp(npy_cdouble z);
npy_cdouble npy_clog(npy_cdouble z);
npy_cdouble npy_cpow(npy_cdouble x, npy_cdouble y);

npy_cdouble npy_csqrt(npy_cdouble z);

npy_cdouble npy_ccos(npy_cdouble z);
npy_cdouble npy_csin(npy_cdouble z);
npy_cdouble npy_ctan(npy_cdouble z);

npy_cdouble npy_ccosh(npy_cdouble z);
npy_cdouble npy_csinh(npy_cdouble z);
npy_cdouble npy_ctanh(npy_cdouble z);

npy_cdouble npy_cacos(npy_cdouble z);
npy_cdouble npy_casin(npy_cdouble z);
npy_cdouble npy_catan(npy_cdouble z);

npy_cdouble npy_cacosh(npy_cdouble z);
npy_cdouble npy_casinh(npy_cdouble z);
npy_cdouble npy_catanh(npy_cdouble z);

/*
 * Single precision complex functions
 */
float npy_cabsf(npy_cfloat z);
float npy_cargf(npy_cfloat z);

npy_cfloat npy_cexpf(npy_cfloat z);
npy_cfloat npy_clogf(npy_cfloat z);
npy_cfloat npy_cpowf(npy_cfloat x, npy_cfloat y);

npy_cfloat npy_csqrtf(npy_cfloat z);

npy_cfloat npy_ccosf(npy_cfloat z);
npy_cfloat npy_csinf(npy_cfloat z);
npy_cfloat npy_ctanf(npy_cfloat z);

npy_cfloat npy_ccoshf(npy_cfloat z);
npy_cfloat npy_csinhf(npy_cfloat z);
npy_cfloat npy_ctanhf(npy_cfloat z);

npy_cfloat npy_cacosf(npy_cfloat z);
npy_cfloat npy_casinf(npy_cfloat z);
npy_cfloat npy_catanf(npy_cfloat z);

npy_cfloat npy_cacoshf(npy_cfloat z);
npy_cfloat npy_casinhf(npy_cfloat z);
npy_cfloat npy_catanhf(npy_cfloat z);


/*
 * Extended precision complex functions
 */
npy_longdouble npy_cabsl(npy_clongdouble z);
npy_longdouble npy_cargl(npy_clongdouble z);

npy_clongdouble npy_cexpl(npy_clongdouble z);
npy_clongdouble npy_clogl(npy_clongdouble z);
npy_clongdouble npy_cpowl(npy_clongdouble x, npy_clongdouble y);

npy_clongdouble npy_csqrtl(npy_clongdouble z);

npy_clongdouble npy_ccosl(npy_clongdouble z);
npy_clongdouble npy_csinl(npy_clongdouble z);
npy_clongdouble npy_ctanl(npy_clongdouble z);

npy_clongdouble npy_ccoshl(npy_clongdouble z);
npy_clongdouble npy_csinhl(npy_clongdouble z);
npy_clongdouble npy_ctanhl(npy_clongdouble z);

npy_clongdouble npy_cacosl(npy_clongdouble z);
npy_clongdouble npy_casinl(npy_clongdouble z);
npy_clongdouble npy_catanl(npy_clongdouble z);

npy_clongdouble npy_cacoshl(npy_clongdouble z);
npy_clongdouble npy_casinhl(npy_clongdouble z);
npy_clongdouble npy_catanhl(npy_clongdouble z);


/*
 * Functions that set the floating point error
 * status word.
 */

/*
 * platform-dependent code translates floating point
 * status to an integer sum of these values
 */
#define NPY_FPE_DIVIDEBYZERO  1
#define NPY_FPE_OVERFLOW      2
#define NPY_FPE_UNDERFLOW     4
#define NPY_FPE_INVALID       8

int npy_clear_floatstatus_barrier(char*);
int npy_get_floatstatus_barrier(char*);
/*
 * use caution with these - clang and gcc8.1 are known to reorder calls
 * to this form of the function which can defeat the check. The _barrier
 * form of the call is preferable, where the argument is
 * (char*)&local_variable
 */
int npy_clear_floatstatus(void);
int npy_get_floatstatus(void);

void npy_set_floatstatus_divbyzero(void);
void npy_set_floatstatus_overflow(void);
void npy_set_floatstatus_underflow(void);
void npy_set_floatstatus_invalid(void);

#ifdef __cplusplus
}
#endif

#if NPY_INLINE_MATH
#include "npy_math_internal.h"
#endif

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_NPY_MATH_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/npy_no_deprecated_api.h

```plaintext
/*
 * This include file is provided for inclusion in Cython *.pyd files where
 * one would like to define the NPY_NO_DEPRECATED_API macro. It can be
 * included by
 *
 * cdef extern from "npy_no_deprecated_api.h": pass
 *
 */
#ifndef NPY_NO_DEPRECATED_API

/* put this check here since there may be multiple includes in C extensions. */
#if defined(NUMPY_CORE_INCLUDE_NUMPY_NDARRAYTYPES_H_) || \
    defined(NUMPY_CORE_INCLUDE_NUMPY_NPY_DEPRECATED_API_H) || \
    defined(NUMPY_CORE_INCLUDE_NUMPY_OLD_DEFINES_H_)
#error "npy_no_deprecated_api.h" must be first among numpy includes.
#else
#define NPY_NO_DEPRECATED_API NPY_API_VERSION
#endif

#endif  /* NPY_NO_DEPRECATED_API */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/npy_os.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY_NPY_OS_H_
#define NUMPY_CORE_INCLUDE_NUMPY_NPY_OS_H_

#if defined(linux) || defined(__linux) || defined(__linux__)
    #define NPY_OS_LINUX
#elif defined(__FreeBSD__) || defined(__NetBSD__) || \
            defined(__OpenBSD__) || defined(__DragonFly__)
    #define NPY_OS_BSD
    #ifdef __FreeBSD__
        #define NPY_OS_FREEBSD
    #elif defined(__NetBSD__)
        #define NPY_OS_NETBSD
    #elif defined(__OpenBSD__)
        #define NPY_OS_OPENBSD
    #elif defined(__DragonFly__)
        #define NPY_OS_DRAGONFLY
    #endif
#elif defined(sun) || defined(__sun)
    #define NPY_OS_SOLARIS
#elif defined(__CYGWIN__)
    #define NPY_OS_CYGWIN
#elif defined(_WIN32) || defined(__WIN32__) || defined(WIN32)
    #define NPY_OS_WIN32
#elif defined(_WIN64) || defined(__WIN64__) || defined(WIN64)
    #define NPY_OS_WIN64
#elif defined(__MINGW32__) || defined(__MINGW64__)
    #define NPY_OS_MINGW
#elif defined(__APPLE__)
    #define NPY_OS_DARWIN
#elif defined(__HAIKU__)
    #define NPY_OS_HAIKU
#else
    #define NPY_OS_UNKNOWN
#endif

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_NPY_OS_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/_numpyconfig.h

```plaintext
#define NPY_HAVE_ENDIAN_H 1
#define NPY_SIZEOF_SHORT SIZEOF_SHORT
#define NPY_SIZEOF_INT SIZEOF_INT
#define NPY_SIZEOF_LONG SIZEOF_LONG
#define NPY_SIZEOF_FLOAT 4
#define NPY_SIZEOF_COMPLEX_FLOAT 8
#define NPY_SIZEOF_DOUBLE 8
#define NPY_SIZEOF_COMPLEX_DOUBLE 16
#define NPY_SIZEOF_LONGDOUBLE 16
#define NPY_SIZEOF_COMPLEX_LONGDOUBLE 32
#define NPY_SIZEOF_PY_INTPTR_T 8
#define NPY_SIZEOF_OFF_T 8
#define NPY_SIZEOF_PY_LONG_LONG 8
#define NPY_SIZEOF_LONGLONG 8
#define NPY_NO_SMP 0
#define NPY_HAVE_DECL_ISNAN
#define NPY_HAVE_DECL_ISINF
#define NPY_HAVE_DECL_ISFINITE
#define NPY_HAVE_DECL_SIGNBIT
#define NPY_USE_C99_COMPLEX 1
#define NPY_HAVE_COMPLEX_DOUBLE 1
#define NPY_HAVE_COMPLEX_FLOAT 1
#define NPY_HAVE_COMPLEX_LONG_DOUBLE 1
#define NPY_USE_C99_FORMATS 1
#define NPY_VISIBILITY_HIDDEN __attribute__((visibility("hidden")))
#define NPY_ABI_VERSION 0x01000009
#define NPY_API_VERSION 0x00000010

#ifndef __STDC_FORMAT_MACROS
#define __STDC_FORMAT_MACROS 1
#endif
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/numpyconfig.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY_NPY_NUMPYCONFIG_H_
#define NUMPY_CORE_INCLUDE_NUMPY_NPY_NUMPYCONFIG_H_

#include "_numpyconfig.h"

/*
 * On Mac OS X, because there is only one configuration stage for all the archs
 * in universal builds, any macro which depends on the arch needs to be
 * hardcoded.
 *
 * Note that distutils/pip will attempt a universal2 build when Python itself
 * is built as universal2, hence this hardcoding is needed even if we do not
 * support universal2 wheels anymore (see gh-22796).
 * This code block can be removed after we have dropped the setup.py based
 * build completely.
 */
#ifdef __APPLE__
    #undef NPY_SIZEOF_LONG
    #undef NPY_SIZEOF_PY_INTPTR_T

    #ifdef __LP64__
        #define NPY_SIZEOF_LONG         8
        #define NPY_SIZEOF_PY_INTPTR_T  8
    #else
        #define NPY_SIZEOF_LONG         4
        #define NPY_SIZEOF_PY_INTPTR_T  4
    #endif

    #undef NPY_SIZEOF_LONGDOUBLE
    #undef NPY_SIZEOF_COMPLEX_LONGDOUBLE
    #ifdef HAVE_LDOUBLE_IEEE_DOUBLE_LE
      #undef HAVE_LDOUBLE_IEEE_DOUBLE_LE
    #endif
    #ifdef HAVE_LDOUBLE_INTEL_EXTENDED_16_BYTES_LE
      #undef HAVE_LDOUBLE_INTEL_EXTENDED_16_BYTES_LE
    #endif

    #if defined(__arm64__)
        #define NPY_SIZEOF_LONGDOUBLE         8
        #define NPY_SIZEOF_COMPLEX_LONGDOUBLE 16
        #define HAVE_LDOUBLE_IEEE_DOUBLE_LE 1
    #elif defined(__x86_64)
        #define NPY_SIZEOF_LONGDOUBLE         16
        #define NPY_SIZEOF_COMPLEX_LONGDOUBLE 32
        #define HAVE_LDOUBLE_INTEL_EXTENDED_16_BYTES_LE 1
    #elif defined (__i386)
        #define NPY_SIZEOF_LONGDOUBLE         12
        #define NPY_SIZEOF_COMPLEX_LONGDOUBLE 24
    #elif defined(__ppc__) || defined (__ppc64__)
        #define NPY_SIZEOF_LONGDOUBLE         16
        #define NPY_SIZEOF_COMPLEX_LONGDOUBLE 32
    #else
        #error "unknown architecture"
    #endif
#endif


/**
 * To help with the NPY_NO_DEPRECATED_API macro, we include API version
 * numbers for specific versions of NumPy. To exclude all API that was
 * deprecated as of 1.7, add the following before #including any NumPy
 * headers:
 *   #define NPY_NO_DEPRECATED_API  NPY_1_7_API_VERSION
 */
#define NPY_1_7_API_VERSION 0x00000007
#define NPY_1_8_API_VERSION 0x00000008
#define NPY_1_9_API_VERSION 0x00000008
#define NPY_1_10_API_VERSION 0x00000008
#define NPY_1_11_API_VERSION 0x00000008
#define NPY_1_12_API_VERSION 0x00000008
#define NPY_1_13_API_VERSION 0x00000008
#define NPY_1_14_API_VERSION 0x00000008
#define NPY_1_15_API_VERSION 0x00000008
#define NPY_1_16_API_VERSION 0x00000008
#define NPY_1_17_API_VERSION 0x00000008
#define NPY_1_18_API_VERSION 0x00000008
#define NPY_1_19_API_VERSION 0x00000008
#define NPY_1_20_API_VERSION 0x0000000e
#define NPY_1_21_API_VERSION 0x0000000e
#define NPY_1_22_API_VERSION 0x0000000f
#define NPY_1_23_API_VERSION 0x00000010
#define NPY_1_24_API_VERSION 0x00000010

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_NPY_NUMPYCONFIG_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/old_defines.h

```plaintext
/* This header is deprecated as of NumPy 1.7 */
#ifndef NUMPY_CORE_INCLUDE_NUMPY_OLD_DEFINES_H_
#define NUMPY_CORE_INCLUDE_NUMPY_OLD_DEFINES_H_

#if defined(NPY_NO_DEPRECATED_API) && NPY_NO_DEPRECATED_API >= NPY_1_7_API_VERSION
#error The header "old_defines.h" is deprecated as of NumPy 1.7.
#endif

#define NDARRAY_VERSION NPY_VERSION

#define PyArray_MIN_BUFSIZE NPY_MIN_BUFSIZE
#define PyArray_MAX_BUFSIZE NPY_MAX_BUFSIZE
#define PyArray_BUFSIZE NPY_BUFSIZE

#define PyArray_PRIORITY NPY_PRIORITY
#define PyArray_SUBTYPE_PRIORITY NPY_PRIORITY
#define PyArray_NUM_FLOATTYPE NPY_NUM_FLOATTYPE

#define NPY_MAX PyArray_MAX
#define NPY_MIN PyArray_MIN

#define PyArray_TYPES       NPY_TYPES
#define PyArray_BOOL        NPY_BOOL
#define PyArray_BYTE        NPY_BYTE
#define PyArray_UBYTE       NPY_UBYTE
#define PyArray_SHORT       NPY_SHORT
#define PyArray_USHORT      NPY_USHORT
#define PyArray_INT         NPY_INT
#define PyArray_UINT        NPY_UINT
#define PyArray_LONG        NPY_LONG
#define PyArray_ULONG       NPY_ULONG
#define PyArray_LONGLONG    NPY_LONGLONG
#define PyArray_ULONGLONG   NPY_ULONGLONG
#define PyArray_HALF        NPY_HALF
#define PyArray_FLOAT       NPY_FLOAT
#define PyArray_DOUBLE      NPY_DOUBLE
#define PyArray_LONGDOUBLE  NPY_LONGDOUBLE
#define PyArray_CFLOAT      NPY_CFLOAT
#define PyArray_CDOUBLE     NPY_CDOUBLE
#define PyArray_CLONGDOUBLE NPY_CLONGDOUBLE
#define PyArray_OBJECT      NPY_OBJECT
#define PyArray_STRING      NPY_STRING
#define PyArray_UNICODE     NPY_UNICODE
#define PyArray_VOID        NPY_VOID
#define PyArray_DATETIME    NPY_DATETIME
#define PyArray_TIMEDELTA   NPY_TIMEDELTA
#define PyArray_NTYPES      NPY_NTYPES
#define PyArray_NOTYPE      NPY_NOTYPE
#define PyArray_CHAR        NPY_CHAR
#define PyArray_USERDEF     NPY_USERDEF
#define PyArray_NUMUSERTYPES NPY_NUMUSERTYPES

#define PyArray_INTP        NPY_INTP
#define PyArray_UINTP       NPY_UINTP

#define PyArray_INT8    NPY_INT8
#define PyArray_UINT8   NPY_UINT8
#define PyArray_INT16   NPY_INT16
#define PyArray_UINT16  NPY_UINT16
#define PyArray_INT32   NPY_INT32
#define PyArray_UINT32  NPY_UINT32

#ifdef NPY_INT64
#define PyArray_INT64   NPY_INT64
#define PyArray_UINT64  NPY_UINT64
#endif

#ifdef NPY_INT128
#define PyArray_INT128 NPY_INT128
#define PyArray_UINT128 NPY_UINT128
#endif

#ifdef NPY_FLOAT16
#define PyArray_FLOAT16  NPY_FLOAT16
#define PyArray_COMPLEX32  NPY_COMPLEX32
#endif

#ifdef NPY_FLOAT80
#define PyArray_FLOAT80  NPY_FLOAT80
#define PyArray_COMPLEX160  NPY_COMPLEX160
#endif

#ifdef NPY_FLOAT96
#define PyArray_FLOAT96  NPY_FLOAT96
#define PyArray_COMPLEX192  NPY_COMPLEX192
#endif

#ifdef NPY_FLOAT128
#define PyArray_FLOAT128  NPY_FLOAT128
#define PyArray_COMPLEX256  NPY_COMPLEX256
#endif

#define PyArray_FLOAT32    NPY_FLOAT32
#define PyArray_COMPLEX64  NPY_COMPLEX64
#define PyArray_FLOAT64    NPY_FLOAT64
#define PyArray_COMPLEX128 NPY_COMPLEX128


#define PyArray_TYPECHAR        NPY_TYPECHAR
#define PyArray_BOOLLTR         NPY_BOOLLTR
#define PyArray_BYTELTR         NPY_BYTELTR
#define PyArray_UBYTELTR        NPY_UBYTELTR
#define PyArray_SHORTLTR        NPY_SHORTLTR
#define PyArray_USHORTLTR       NPY_USHORTLTR
#define PyArray_INTLTR          NPY_INTLTR
#define PyArray_UINTLTR         NPY_UINTLTR
#define PyArray_LONGLTR         NPY_LONGLTR
#define PyArray_ULONGLTR        NPY_ULONGLTR
#define PyArray_LONGLONGLTR     NPY_LONGLONGLTR
#define PyArray_ULONGLONGLTR    NPY_ULONGLONGLTR
#define PyArray_HALFLTR         NPY_HALFLTR
#define PyArray_FLOATLTR        NPY_FLOATLTR
#define PyArray_DOUBLELTR       NPY_DOUBLELTR
#define PyArray_LONGDOUBLELTR   NPY_LONGDOUBLELTR
#define PyArray_CFLOATLTR       NPY_CFLOATLTR
#define PyArray_CDOUBLELTR      NPY_CDOUBLELTR
#define PyArray_CLONGDOUBLELTR  NPY_CLONGDOUBLELTR
#define PyArray_OBJECTLTR       NPY_OBJECTLTR
#define PyArray_STRINGLTR       NPY_STRINGLTR
#define PyArray_STRINGLTR2      NPY_STRINGLTR2
#define PyArray_UNICODELTR      NPY_UNICODELTR
#define PyArray_VOIDLTR         NPY_VOIDLTR
#define PyArray_DATETIMELTR     NPY_DATETIMELTR
#define PyArray_TIMEDELTALTR    NPY_TIMEDELTALTR
#define PyArray_CHARLTR         NPY_CHARLTR
#define PyArray_INTPLTR         NPY_INTPLTR
#define PyArray_UINTPLTR        NPY_UINTPLTR
#define PyArray_GENBOOLLTR      NPY_GENBOOLLTR
#define PyArray_SIGNEDLTR       NPY_SIGNEDLTR
#define PyArray_UNSIGNEDLTR     NPY_UNSIGNEDLTR
#define PyArray_FLOATINGLTR     NPY_FLOATINGLTR
#define PyArray_COMPLEXLTR      NPY_COMPLEXLTR

#define PyArray_QUICKSORT   NPY_QUICKSORT
#define PyArray_HEAPSORT    NPY_HEAPSORT
#define PyArray_MERGESORT   NPY_MERGESORT
#define PyArray_SORTKIND    NPY_SORTKIND
#define PyArray_NSORTS      NPY_NSORTS

#define PyArray_NOSCALAR       NPY_NOSCALAR
#define PyArray_BOOL_SCALAR    NPY_BOOL_SCALAR
#define PyArray_INTPOS_SCALAR  NPY_INTPOS_SCALAR
#define PyArray_INTNEG_SCALAR  NPY_INTNEG_SCALAR
#define PyArray_FLOAT_SCALAR   NPY_FLOAT_SCALAR
#define PyArray_COMPLEX_SCALAR NPY_COMPLEX_SCALAR
#define PyArray_OBJECT_SCALAR  NPY_OBJECT_SCALAR
#define PyArray_SCALARKIND     NPY_SCALARKIND
#define PyArray_NSCALARKINDS   NPY_NSCALARKINDS

#define PyArray_ANYORDER     NPY_ANYORDER
#define PyArray_CORDER       NPY_CORDER
#define PyArray_FORTRANORDER NPY_FORTRANORDER
#define PyArray_ORDER        NPY_ORDER

#define PyDescr_ISBOOL      PyDataType_ISBOOL
#define PyDescr_ISUNSIGNED  PyDataType_ISUNSIGNED
#define PyDescr_ISSIGNED    PyDataType_ISSIGNED
#define PyDescr_ISINTEGER   PyDataType_ISINTEGER
#define PyDescr_ISFLOAT     PyDataType_ISFLOAT
#define PyDescr_ISNUMBER    PyDataType_ISNUMBER
#define PyDescr_ISSTRING    PyDataType_ISSTRING
#define PyDescr_ISCOMPLEX   PyDataType_ISCOMPLEX
#define PyDescr_ISPYTHON    PyDataType_ISPYTHON
#define PyDescr_ISFLEXIBLE  PyDataType_ISFLEXIBLE
#define PyDescr_ISUSERDEF   PyDataType_ISUSERDEF
#define PyDescr_ISEXTENDED  PyDataType_ISEXTENDED
#define PyDescr_ISOBJECT    PyDataType_ISOBJECT
#define PyDescr_HASFIELDS   PyDataType_HASFIELDS

#define PyArray_LITTLE NPY_LITTLE
#define PyArray_BIG NPY_BIG
#define PyArray_NATIVE NPY_NATIVE
#define PyArray_SWAP NPY_SWAP
#define PyArray_IGNORE NPY_IGNORE

#define PyArray_NATBYTE NPY_NATBYTE
#define PyArray_OPPBYTE NPY_OPPBYTE

#define PyArray_MAX_ELSIZE NPY_MAX_ELSIZE

#define PyArray_USE_PYMEM NPY_USE_PYMEM

#define PyArray_RemoveLargest PyArray_RemoveSmallest

#define PyArray_UCS4 npy_ucs4

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_OLD_DEFINES_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/oldnumeric.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY_OLDNUMERIC_H_
#define NUMPY_CORE_INCLUDE_NUMPY_OLDNUMERIC_H_

/* FIXME -- this file can be deleted? */

#include "arrayobject.h"

#ifndef PYPY_VERSION
#ifndef REFCOUNT
#  define REFCOUNT NPY_REFCOUNT
#  define MAX_ELSIZE 16
#endif
#endif

#define PyArray_UNSIGNED_TYPES
#define PyArray_SBYTE NPY_BYTE
#define PyArray_CopyArray PyArray_CopyInto
#define _PyArray_multiply_list PyArray_MultiplyIntList
#define PyArray_ISSPACESAVER(m) NPY_FALSE
#define PyScalarArray_Check PyArray_CheckScalar

#define CONTIGUOUS NPY_CONTIGUOUS
#define OWN_DIMENSIONS 0
#define OWN_STRIDES 0
#define OWN_DATA NPY_OWNDATA
#define SAVESPACE 0
#define SAVESPACEBIT 0

#undef import_array
#define import_array() { if (_import_array() < 0) {PyErr_Print(); PyErr_SetString(PyExc_ImportError, "numpy.core.multiarray failed to import"); } }

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_OLDNUMERIC_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/random/bitgen.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY_RANDOM_BITGEN_H_
#define NUMPY_CORE_INCLUDE_NUMPY_RANDOM_BITGEN_H_

#pragma once
#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>

/* Must match the declaration in numpy/random/<any>.pxd */

typedef struct bitgen {
  void *state;
  uint64_t (*next_uint64)(void *st);
  uint32_t (*next_uint32)(void *st);
  double (*next_double)(void *st);
  uint64_t (*next_raw)(void *st);
} bitgen_t;


#endif  /* NUMPY_CORE_INCLUDE_NUMPY_RANDOM_BITGEN_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/random/distributions.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY_RANDOM_DISTRIBUTIONS_H_
#define NUMPY_CORE_INCLUDE_NUMPY_RANDOM_DISTRIBUTIONS_H_

#ifdef __cplusplus
extern "C" {
#endif

#include <Python.h>
#include "numpy/npy_common.h"
#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>

#include "numpy/npy_math.h"
#include "numpy/random/bitgen.h"

/*
 * RAND_INT_TYPE is used to share integer generators with RandomState which
 * used long in place of int64_t. If changing a distribution that uses
 * RAND_INT_TYPE, then the original unmodified copy must be retained for
 * use in RandomState by copying to the legacy distributions source file.
 */
#ifdef NP_RANDOM_LEGACY
#define RAND_INT_TYPE long
#define RAND_INT_MAX LONG_MAX
#else
#define RAND_INT_TYPE int64_t
#define RAND_INT_MAX INT64_MAX
#endif

#ifdef _MSC_VER
#define DECLDIR __declspec(dllexport)
#else
#define DECLDIR extern
#endif

#ifndef MIN
#define MIN(x, y) (((x) < (y)) ? x : y)
#define MAX(x, y) (((x) > (y)) ? x : y)
#endif

#ifndef M_PI
#define M_PI 3.14159265358979323846264338328
#endif

typedef struct s_binomial_t {
  int has_binomial; /* !=0: following parameters initialized for binomial */
  double psave;
  RAND_INT_TYPE nsave;
  double r;
  double q;
  double fm;
  RAND_INT_TYPE m;
  double p1;
  double xm;
  double xl;
  double xr;
  double c;
  double laml;
  double lamr;
  double p2;
  double p3;
  double p4;
} binomial_t;

DECLDIR float random_standard_uniform_f(bitgen_t *bitgen_state);
DECLDIR double random_standard_uniform(bitgen_t *bitgen_state);
DECLDIR void random_standard_uniform_fill(bitgen_t *, npy_intp, double *);
DECLDIR void random_standard_uniform_fill_f(bitgen_t *, npy_intp, float *);

DECLDIR int64_t random_positive_int64(bitgen_t *bitgen_state);
DECLDIR int32_t random_positive_int32(bitgen_t *bitgen_state);
DECLDIR int64_t random_positive_int(bitgen_t *bitgen_state);
DECLDIR uint64_t random_uint(bitgen_t *bitgen_state);

DECLDIR double random_standard_exponential(bitgen_t *bitgen_state);
DECLDIR float random_standard_exponential_f(bitgen_t *bitgen_state);
DECLDIR void random_standard_exponential_fill(bitgen_t *, npy_intp, double *);
DECLDIR void random_standard_exponential_fill_f(bitgen_t *, npy_intp, float *);
DECLDIR void random_standard_exponential_inv_fill(bitgen_t *, npy_intp, double *);
DECLDIR void random_standard_exponential_inv_fill_f(bitgen_t *, npy_intp, float *);

DECLDIR double random_standard_normal(bitgen_t *bitgen_state);
DECLDIR float random_standard_normal_f(bitgen_t *bitgen_state);
DECLDIR void random_standard_normal_fill(bitgen_t *, npy_intp, double *);
DECLDIR void random_standard_normal_fill_f(bitgen_t *, npy_intp, float *);
DECLDIR double random_standard_gamma(bitgen_t *bitgen_state, double shape);
DECLDIR float random_standard_gamma_f(bitgen_t *bitgen_state, float shape);

DECLDIR double random_normal(bitgen_t *bitgen_state, double loc, double scale);

DECLDIR double random_gamma(bitgen_t *bitgen_state, double shape, double scale);
DECLDIR float random_gamma_f(bitgen_t *bitgen_state, float shape, float scale);

DECLDIR double random_exponential(bitgen_t *bitgen_state, double scale);
DECLDIR double random_uniform(bitgen_t *bitgen_state, double lower, double range);
DECLDIR double random_beta(bitgen_t *bitgen_state, double a, double b);
DECLDIR double random_chisquare(bitgen_t *bitgen_state, double df);
DECLDIR double random_f(bitgen_t *bitgen_state, double dfnum, double dfden);
DECLDIR double random_standard_cauchy(bitgen_t *bitgen_state);
DECLDIR double random_pareto(bitgen_t *bitgen_state, double a);
DECLDIR double random_weibull(bitgen_t *bitgen_state, double a);
DECLDIR double random_power(bitgen_t *bitgen_state, double a);
DECLDIR double random_laplace(bitgen_t *bitgen_state, double loc, double scale);
DECLDIR double random_gumbel(bitgen_t *bitgen_state, double loc, double scale);
DECLDIR double random_logistic(bitgen_t *bitgen_state, double loc, double scale);
DECLDIR double random_lognormal(bitgen_t *bitgen_state, double mean, double sigma);
DECLDIR double random_rayleigh(bitgen_t *bitgen_state, double mode);
DECLDIR double random_standard_t(bitgen_t *bitgen_state, double df);
DECLDIR double random_noncentral_chisquare(bitgen_t *bitgen_state, double df,
                                           double nonc);
DECLDIR double random_noncentral_f(bitgen_t *bitgen_state, double dfnum,
                                   double dfden, double nonc);
DECLDIR double random_wald(bitgen_t *bitgen_state, double mean, double scale);
DECLDIR double random_vonmises(bitgen_t *bitgen_state, double mu, double kappa);
DECLDIR double random_triangular(bitgen_t *bitgen_state, double left, double mode,
                                 double right);

DECLDIR RAND_INT_TYPE random_poisson(bitgen_t *bitgen_state, double lam);
DECLDIR RAND_INT_TYPE random_negative_binomial(bitgen_t *bitgen_state, double n,
                                 double p);

DECLDIR int64_t random_binomial(bitgen_t *bitgen_state, double p,
                                int64_t n, binomial_t *binomial);

DECLDIR int64_t random_logseries(bitgen_t *bitgen_state, double p);
DECLDIR int64_t random_geometric(bitgen_t *bitgen_state, double p);
DECLDIR RAND_INT_TYPE random_geometric_search(bitgen_t *bitgen_state, double p);
DECLDIR RAND_INT_TYPE random_zipf(bitgen_t *bitgen_state, double a);
DECLDIR int64_t random_hypergeometric(bitgen_t *bitgen_state,
                                      int64_t good, int64_t bad, int64_t sample);
DECLDIR uint64_t random_interval(bitgen_t *bitgen_state, uint64_t max);

/* Generate random uint64 numbers in closed interval [off, off + rng]. */
DECLDIR uint64_t random_bounded_uint64(bitgen_t *bitgen_state, uint64_t off,
                                       uint64_t rng, uint64_t mask,
                                       bool use_masked);

/* Generate random uint32 numbers in closed interval [off, off + rng]. */
DECLDIR uint32_t random_buffered_bounded_uint32(bitgen_t *bitgen_state,
                                                uint32_t off, uint32_t rng,
                                                uint32_t mask, bool use_masked,
                                                int *bcnt, uint32_t *buf);
DECLDIR uint16_t random_buffered_bounded_uint16(bitgen_t *bitgen_state,
                                                uint16_t off, uint16_t rng,
                                                uint16_t mask, bool use_masked,
                                                int *bcnt, uint32_t *buf);
DECLDIR uint8_t random_buffered_bounded_uint8(bitgen_t *bitgen_state, uint8_t off,
                                              uint8_t rng, uint8_t mask,
                                              bool use_masked, int *bcnt,
                                              uint32_t *buf);
DECLDIR npy_bool random_buffered_bounded_bool(bitgen_t *bitgen_state, npy_bool off,
                                              npy_bool rng, npy_bool mask,
                                              bool use_masked, int *bcnt,
                                              uint32_t *buf);

DECLDIR void random_bounded_uint64_fill(bitgen_t *bitgen_state, uint64_t off,
                                        uint64_t rng, npy_intp cnt,
                                        bool use_masked, uint64_t *out);
DECLDIR void random_bounded_uint32_fill(bitgen_t *bitgen_state, uint32_t off,
                                        uint32_t rng, npy_intp cnt,
                                        bool use_masked, uint32_t *out);
DECLDIR void random_bounded_uint16_fill(bitgen_t *bitgen_state, uint16_t off,
                                        uint16_t rng, npy_intp cnt,
                                        bool use_masked, uint16_t *out);
DECLDIR void random_bounded_uint8_fill(bitgen_t *bitgen_state, uint8_t off,
                                       uint8_t rng, npy_intp cnt,
                                       bool use_masked, uint8_t *out);
DECLDIR void random_bounded_bool_fill(bitgen_t *bitgen_state, npy_bool off,
                                      npy_bool rng, npy_intp cnt,
                                      bool use_masked, npy_bool *out);

DECLDIR void random_multinomial(bitgen_t *bitgen_state, RAND_INT_TYPE n, RAND_INT_TYPE *mnix,
                                double *pix, npy_intp d, binomial_t *binomial);

/* multivariate hypergeometric, "count" method */
DECLDIR int random_multivariate_hypergeometric_count(bitgen_t *bitgen_state,
                              int64_t total,
                              size_t num_colors, int64_t *colors,
                              int64_t nsample,
                              size_t num_variates, int64_t *variates);

/* multivariate hypergeometric, "marginals" method */
DECLDIR void random_multivariate_hypergeometric_marginals(bitgen_t *bitgen_state,
                                   int64_t total,
                                   size_t num_colors, int64_t *colors,
                                   int64_t nsample,
                                   size_t num_variates, int64_t *variates);

/* Common to legacy-distributions.c and distributions.c but not exported */

RAND_INT_TYPE random_binomial_btpe(bitgen_t *bitgen_state,
                                   RAND_INT_TYPE n,
                                   double p,
                                   binomial_t *binomial);
RAND_INT_TYPE random_binomial_inversion(bitgen_t *bitgen_state,
                                        RAND_INT_TYPE n,
                                        double p,
                                        binomial_t *binomial);
double random_loggam(double x);
static NPY_INLINE double next_double(bitgen_t *bitgen_state) {
    return bitgen_state->next_double(bitgen_state->state);
}

#ifdef __cplusplus
}
#endif

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_RANDOM_DISTRIBUTIONS_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/__ufunc_api.h

```plaintext

#ifdef _UMATHMODULE

extern NPY_NO_EXPORT PyTypeObject PyUFunc_Type;

extern NPY_NO_EXPORT PyTypeObject PyUFunc_Type;

NPY_NO_EXPORT  PyObject * PyUFunc_FromFuncAndData \
       (PyUFuncGenericFunction *, void **, char *, int, int, int, int, const char *, const char *, int);
NPY_NO_EXPORT  int PyUFunc_RegisterLoopForType \
       (PyUFuncObject *, int, PyUFuncGenericFunction, const int *, void *);
NPY_NO_EXPORT  int PyUFunc_GenericFunction \
       (PyUFuncObject *NPY_UNUSED(ufunc), PyObject *NPY_UNUSED(args), PyObject *NPY_UNUSED(kwds), PyArrayObject **NPY_UNUSED(op));
NPY_NO_EXPORT  void PyUFunc_f_f_As_d_d \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_d_d \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_f_f \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_g_g \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_F_F_As_D_D \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_F_F \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_D_D \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_G_G \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_O_O \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_ff_f_As_dd_d \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_ff_f \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_dd_d \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_gg_g \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_FF_F_As_DD_D \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_DD_D \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_FF_F \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_GG_G \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_OO_O \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_O_O_method \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_OO_O_method \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_On_Om \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  int PyUFunc_GetPyValues \
       (char *, int *, int *, PyObject **);
NPY_NO_EXPORT  int PyUFunc_checkfperr \
       (int, PyObject *, int *);
NPY_NO_EXPORT  void PyUFunc_clearfperr \
       (void);
NPY_NO_EXPORT  int PyUFunc_getfperr \
       (void);
NPY_NO_EXPORT  int PyUFunc_handlefperr \
       (int, PyObject *, int, int *);
NPY_NO_EXPORT  int PyUFunc_ReplaceLoopBySignature \
       (PyUFuncObject *, PyUFuncGenericFunction, const int *, PyUFuncGenericFunction *);
NPY_NO_EXPORT  PyObject * PyUFunc_FromFuncAndDataAndSignature \
       (PyUFuncGenericFunction *, void **, char *, int, int, int, int, const char *, const char *, int, const char *);
NPY_NO_EXPORT  int PyUFunc_SetUsesArraysAsData \
       (void **NPY_UNUSED(data), size_t NPY_UNUSED(i));
NPY_NO_EXPORT  void PyUFunc_e_e \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_e_e_As_f_f \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_e_e_As_d_d \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_ee_e \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_ee_e_As_ff_f \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  void PyUFunc_ee_e_As_dd_d \
       (char **, npy_intp const *, npy_intp const *, void *);
NPY_NO_EXPORT  int PyUFunc_DefaultTypeResolver \
       (PyUFuncObject *, NPY_CASTING, PyArrayObject **, PyObject *, PyArray_Descr **);
NPY_NO_EXPORT  int PyUFunc_ValidateCasting \
       (PyUFuncObject *, NPY_CASTING, PyArrayObject **, PyArray_Descr **);
NPY_NO_EXPORT  int PyUFunc_RegisterLoopForDescr \
       (PyUFuncObject *, PyArray_Descr *, PyUFuncGenericFunction, PyArray_Descr **, void *);
NPY_NO_EXPORT  PyObject * PyUFunc_FromFuncAndDataAndSignatureAndIdentity \
       (PyUFuncGenericFunction *, void **, char *, int, int, int, int, const char *, const char *, const int, const char *, PyObject *);

#else

#if defined(PY_UFUNC_UNIQUE_SYMBOL)
#define PyUFunc_API PY_UFUNC_UNIQUE_SYMBOL
#endif

#if defined(NO_IMPORT) || defined(NO_IMPORT_UFUNC)
extern void **PyUFunc_API;
#else
#if defined(PY_UFUNC_UNIQUE_SYMBOL)
void **PyUFunc_API;
#else
static void **PyUFunc_API=NULL;
#endif
#endif

#define PyUFunc_Type (*(PyTypeObject *)PyUFunc_API[0])
#define PyUFunc_FromFuncAndData \
        (*(PyObject * (*)(PyUFuncGenericFunction *, void **, char *, int, int, int, int, const char *, const char *, int)) \
         PyUFunc_API[1])
#define PyUFunc_RegisterLoopForType \
        (*(int (*)(PyUFuncObject *, int, PyUFuncGenericFunction, const int *, void *)) \
         PyUFunc_API[2])
#define PyUFunc_GenericFunction \
        (*(int (*)(PyUFuncObject *NPY_UNUSED(ufunc), PyObject *NPY_UNUSED(args), PyObject *NPY_UNUSED(kwds), PyArrayObject **NPY_UNUSED(op))) \
         PyUFunc_API[3])
#define PyUFunc_f_f_As_d_d \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[4])
#define PyUFunc_d_d \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[5])
#define PyUFunc_f_f \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[6])
#define PyUFunc_g_g \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[7])
#define PyUFunc_F_F_As_D_D \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[8])
#define PyUFunc_F_F \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[9])
#define PyUFunc_D_D \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[10])
#define PyUFunc_G_G \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[11])
#define PyUFunc_O_O \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[12])
#define PyUFunc_ff_f_As_dd_d \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[13])
#define PyUFunc_ff_f \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[14])
#define PyUFunc_dd_d \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[15])
#define PyUFunc_gg_g \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[16])
#define PyUFunc_FF_F_As_DD_D \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[17])
#define PyUFunc_DD_D \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[18])
#define PyUFunc_FF_F \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[19])
#define PyUFunc_GG_G \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[20])
#define PyUFunc_OO_O \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[21])
#define PyUFunc_O_O_method \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[22])
#define PyUFunc_OO_O_method \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[23])
#define PyUFunc_On_Om \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[24])
#define PyUFunc_GetPyValues \
        (*(int (*)(char *, int *, int *, PyObject **)) \
         PyUFunc_API[25])
#define PyUFunc_checkfperr \
        (*(int (*)(int, PyObject *, int *)) \
         PyUFunc_API[26])
#define PyUFunc_clearfperr \
        (*(void (*)(void)) \
         PyUFunc_API[27])
#define PyUFunc_getfperr \
        (*(int (*)(void)) \
         PyUFunc_API[28])
#define PyUFunc_handlefperr \
        (*(int (*)(int, PyObject *, int, int *)) \
         PyUFunc_API[29])
#define PyUFunc_ReplaceLoopBySignature \
        (*(int (*)(PyUFuncObject *, PyUFuncGenericFunction, const int *, PyUFuncGenericFunction *)) \
         PyUFunc_API[30])
#define PyUFunc_FromFuncAndDataAndSignature \
        (*(PyObject * (*)(PyUFuncGenericFunction *, void **, char *, int, int, int, int, const char *, const char *, int, const char *)) \
         PyUFunc_API[31])
#define PyUFunc_SetUsesArraysAsData \
        (*(int (*)(void **NPY_UNUSED(data), size_t NPY_UNUSED(i))) \
         PyUFunc_API[32])
#define PyUFunc_e_e \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[33])
#define PyUFunc_e_e_As_f_f \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[34])
#define PyUFunc_e_e_As_d_d \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[35])
#define PyUFunc_ee_e \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[36])
#define PyUFunc_ee_e_As_ff_f \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[37])
#define PyUFunc_ee_e_As_dd_d \
        (*(void (*)(char **, npy_intp const *, npy_intp const *, void *)) \
         PyUFunc_API[38])
#define PyUFunc_DefaultTypeResolver \
        (*(int (*)(PyUFuncObject *, NPY_CASTING, PyArrayObject **, PyObject *, PyArray_Descr **)) \
         PyUFunc_API[39])
#define PyUFunc_ValidateCasting \
        (*(int (*)(PyUFuncObject *, NPY_CASTING, PyArrayObject **, PyArray_Descr **)) \
         PyUFunc_API[40])
#define PyUFunc_RegisterLoopForDescr \
        (*(int (*)(PyUFuncObject *, PyArray_Descr *, PyUFuncGenericFunction, PyArray_Descr **, void *)) \
         PyUFunc_API[41])
#define PyUFunc_FromFuncAndDataAndSignatureAndIdentity \
        (*(PyObject * (*)(PyUFuncGenericFunction *, void **, char *, int, int, int, int, const char *, const char *, const int, const char *, PyObject *)) \
         PyUFunc_API[42])

static NPY_INLINE int
_import_umath(void)
{
  PyObject *numpy = PyImport_ImportModule("numpy.core._multiarray_umath");
  PyObject *c_api = NULL;

  if (numpy == NULL) {
      PyErr_SetString(PyExc_ImportError,
                      "numpy.core._multiarray_umath failed to import");
      return -1;
  }
  c_api = PyObject_GetAttrString(numpy, "_UFUNC_API");
  Py_DECREF(numpy);
  if (c_api == NULL) {
      PyErr_SetString(PyExc_AttributeError, "_UFUNC_API not found");
      return -1;
  }

  if (!PyCapsule_CheckExact(c_api)) {
      PyErr_SetString(PyExc_RuntimeError, "_UFUNC_API is not PyCapsule object");
      Py_DECREF(c_api);
      return -1;
  }
  PyUFunc_API = (void **)PyCapsule_GetPointer(c_api, NULL);
  Py_DECREF(c_api);
  if (PyUFunc_API == NULL) {
      PyErr_SetString(PyExc_RuntimeError, "_UFUNC_API is NULL pointer");
      return -1;
  }
  return 0;
}

#define import_umath() \
    do {\
        UFUNC_NOFPE\
        if (_import_umath() < 0) {\
            PyErr_Print();\
            PyErr_SetString(PyExc_ImportError,\
                    "numpy.core.umath failed to import");\
            return NULL;\
        }\
    } while(0)

#define import_umath1(ret) \
    do {\
        UFUNC_NOFPE\
        if (_import_umath() < 0) {\
            PyErr_Print();\
            PyErr_SetString(PyExc_ImportError,\
                    "numpy.core.umath failed to import");\
            return ret;\
        }\
    } while(0)

#define import_umath2(ret, msg) \
    do {\
        UFUNC_NOFPE\
        if (_import_umath() < 0) {\
            PyErr_Print();\
            PyErr_SetString(PyExc_ImportError, msg);\
            return ret;\
        }\
    } while(0)

#define import_ufunc() \
    do {\
        UFUNC_NOFPE\
        if (_import_umath() < 0) {\
            PyErr_Print();\
            PyErr_SetString(PyExc_ImportError,\
                    "numpy.core.umath failed to import");\
        }\
    } while(0)

#endif
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/ufuncobject.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY_UFUNCOBJECT_H_
#define NUMPY_CORE_INCLUDE_NUMPY_UFUNCOBJECT_H_

#include <numpy/npy_math.h>
#include <numpy/npy_common.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * The legacy generic inner loop for a standard element-wise or
 * generalized ufunc.
 */
typedef void (*PyUFuncGenericFunction)
            (char **args,
             npy_intp const *dimensions,
             npy_intp const *strides,
             void *innerloopdata);

/*
 * The most generic one-dimensional inner loop for
 * a masked standard element-wise ufunc. "Masked" here means that it skips
 * doing calculations on any items for which the maskptr array has a true
 * value.
 */
typedef void (PyUFunc_MaskedStridedInnerLoopFunc)(
                char **dataptrs, npy_intp *strides,
                char *maskptr, npy_intp mask_stride,
                npy_intp count,
                NpyAuxData *innerloopdata);

/* Forward declaration for the type resolver and loop selector typedefs */
struct _tagPyUFuncObject;

/*
 * Given the operands for calling a ufunc, should determine the
 * calculation input and output data types and return an inner loop function.
 * This function should validate that the casting rule is being followed,
 * and fail if it is not.
 *
 * For backwards compatibility, the regular type resolution function does not
 * support auxiliary data with object semantics. The type resolution call
 * which returns a masked generic function returns a standard NpyAuxData
 * object, for which the NPY_AUXDATA_FREE and NPY_AUXDATA_CLONE macros
 * work.
 *
 * ufunc:             The ufunc object.
 * casting:           The 'casting' parameter provided to the ufunc.
 * operands:          An array of length (ufunc->nin + ufunc->nout),
 *                    with the output parameters possibly NULL.
 * type_tup:          Either NULL, or the type_tup passed to the ufunc.
 * out_dtypes:        An array which should be populated with new
 *                    references to (ufunc->nin + ufunc->nout) new
 *                    dtypes, one for each input and output. These
 *                    dtypes should all be in native-endian format.
 *
 * Should return 0 on success, -1 on failure (with exception set),
 * or -2 if Py_NotImplemented should be returned.
 */
typedef int (PyUFunc_TypeResolutionFunc)(
                                struct _tagPyUFuncObject *ufunc,
                                NPY_CASTING casting,
                                PyArrayObject **operands,
                                PyObject *type_tup,
                                PyArray_Descr **out_dtypes);

/*
 * Legacy loop selector. (This should NOT normally be used and we can expect
 * that only the `PyUFunc_DefaultLegacyInnerLoopSelector` is ever set).
 * However, unlike the masked version, it probably still works.
 *
 * ufunc:             The ufunc object.
 * dtypes:            An array which has been populated with dtypes,
 *                    in most cases by the type resolution function
 *                    for the same ufunc.
 * out_innerloop:     Should be populated with the correct ufunc inner
 *                    loop for the given type.
 * out_innerloopdata: Should be populated with the void* data to
 *                    be passed into the out_innerloop function.
 * out_needs_api:     If the inner loop needs to use the Python API,
 *                    should set the to 1, otherwise should leave
 *                    this untouched.
 */
typedef int (PyUFunc_LegacyInnerLoopSelectionFunc)(
                            struct _tagPyUFuncObject *ufunc,
                            PyArray_Descr **dtypes,
                            PyUFuncGenericFunction *out_innerloop,
                            void **out_innerloopdata,
                            int *out_needs_api);


typedef struct _tagPyUFuncObject {
        PyObject_HEAD
        /*
         * nin: Number of inputs
         * nout: Number of outputs
         * nargs: Always nin + nout (Why is it stored?)
         */
        int nin, nout, nargs;

        /*
         * Identity for reduction, any of PyUFunc_One, PyUFunc_Zero
         * PyUFunc_MinusOne, PyUFunc_None, PyUFunc_ReorderableNone,
         * PyUFunc_IdentityValue.
         */
        int identity;

        /* Array of one-dimensional core loops */
        PyUFuncGenericFunction *functions;
        /* Array of funcdata that gets passed into the functions */
        void **data;
        /* The number of elements in 'functions' and 'data' */
        int ntypes;

        /* Used to be unused field 'check_return' */
        int reserved1;

        /* The name of the ufunc */
        const char *name;

        /* Array of type numbers, of size ('nargs' * 'ntypes') */
        char *types;

        /* Documentation string */
        const char *doc;

        void *ptr;
        PyObject *obj;
        PyObject *userloops;

        /* generalized ufunc parameters */

        /* 0 for scalar ufunc; 1 for generalized ufunc */
        int core_enabled;
        /* number of distinct dimension names in signature */
        int core_num_dim_ix;

        /*
         * dimension indices of input/output argument k are stored in
         * core_dim_ixs[core_offsets[k]..core_offsets[k]+core_num_dims[k]-1]
         */

        /* numbers of core dimensions of each argument */
        int *core_num_dims;
        /*
         * dimension indices in a flatted form; indices
         * are in the range of [0,core_num_dim_ix)
         */
        int *core_dim_ixs;
        /*
         * positions of 1st core dimensions of each
         * argument in core_dim_ixs, equivalent to cumsum(core_num_dims)
         */
        int *core_offsets;
        /* signature string for printing purpose */
        char *core_signature;

        /*
         * A function which resolves the types and fills an array
         * with the dtypes for the inputs and outputs.
         */
        PyUFunc_TypeResolutionFunc *type_resolver;
        /*
         * A function which returns an inner loop written for
         * NumPy 1.6 and earlier ufuncs. This is for backwards
         * compatibility, and may be NULL if inner_loop_selector
         * is specified.
         */
        PyUFunc_LegacyInnerLoopSelectionFunc *legacy_inner_loop_selector;
        /*
         * This was blocked off to be the "new" inner loop selector in 1.7,
         * but this was never implemented. (This is also why the above
         * selector is called the "legacy" selector.)
         */
        #ifndef Py_LIMITED_API
            vectorcallfunc vectorcall;
        #else
            void *vectorcall;
        #endif

        /* Was previously the `PyUFunc_MaskedInnerLoopSelectionFunc` */
        void *_always_null_previously_masked_innerloop_selector;

        /*
         * List of flags for each operand when ufunc is called by nditer object.
         * These flags will be used in addition to the default flags for each
         * operand set by nditer object.
         */
        npy_uint32 *op_flags;

        /*
         * List of global flags used when ufunc is called by nditer object.
         * These flags will be used in addition to the default global flags
         * set by nditer object.
         */
        npy_uint32 iter_flags;

        /* New in NPY_API_VERSION 0x0000000D and above */

        /*
         * for each core_num_dim_ix distinct dimension names,
         * the possible "frozen" size (-1 if not frozen).
         */
        npy_intp *core_dim_sizes;

        /*
         * for each distinct core dimension, a set of UFUNC_CORE_DIM* flags
         */
        npy_uint32 *core_dim_flags;

        /* Identity for reduction, when identity == PyUFunc_IdentityValue */
        PyObject *identity_value;

        /* New in NPY_API_VERSION 0x0000000F and above */

        /* New private fields related to dispatching */
        void *_dispatch_cache;
        /* A PyListObject of `(tuple of DTypes, ArrayMethod/Promoter)` */
        PyObject *_loops;
} PyUFuncObject;

#include "arrayobject.h"
/* Generalized ufunc; 0x0001 reserved for possible use as CORE_ENABLED */
/* the core dimension's size will be determined by the operands. */
#define UFUNC_CORE_DIM_SIZE_INFERRED 0x0002
/* the core dimension may be absent */
#define UFUNC_CORE_DIM_CAN_IGNORE 0x0004
/* flags inferred during execution */
#define UFUNC_CORE_DIM_MISSING 0x00040000

#define UFUNC_ERR_IGNORE 0
#define UFUNC_ERR_WARN   1
#define UFUNC_ERR_RAISE  2
#define UFUNC_ERR_CALL   3
#define UFUNC_ERR_PRINT  4
#define UFUNC_ERR_LOG    5

        /* Python side integer mask */

#define UFUNC_MASK_DIVIDEBYZERO 0x07
#define UFUNC_MASK_OVERFLOW 0x3f
#define UFUNC_MASK_UNDERFLOW 0x1ff
#define UFUNC_MASK_INVALID 0xfff

#define UFUNC_SHIFT_DIVIDEBYZERO 0
#define UFUNC_SHIFT_OVERFLOW     3
#define UFUNC_SHIFT_UNDERFLOW    6
#define UFUNC_SHIFT_INVALID      9


#define UFUNC_OBJ_ISOBJECT      1
#define UFUNC_OBJ_NEEDS_API     2

   /* Default user error mode */
#define UFUNC_ERR_DEFAULT                               \
        (UFUNC_ERR_WARN << UFUNC_SHIFT_DIVIDEBYZERO) +  \
        (UFUNC_ERR_WARN << UFUNC_SHIFT_OVERFLOW) +      \
        (UFUNC_ERR_WARN << UFUNC_SHIFT_INVALID)

#if NPY_ALLOW_THREADS
#define NPY_LOOP_BEGIN_THREADS do {if (!(loop->obj & UFUNC_OBJ_NEEDS_API)) _save = PyEval_SaveThread();} while (0);
#define NPY_LOOP_END_THREADS   do {if (!(loop->obj & UFUNC_OBJ_NEEDS_API)) PyEval_RestoreThread(_save);} while (0);
#else
#define NPY_LOOP_BEGIN_THREADS
#define NPY_LOOP_END_THREADS
#endif

/*
 * UFunc has unit of 0, and the order of operations can be reordered
 * This case allows reduction with multiple axes at once.
 */
#define PyUFunc_Zero 0
/*
 * UFunc has unit of 1, and the order of operations can be reordered
 * This case allows reduction with multiple axes at once.
 */
#define PyUFunc_One 1
/*
 * UFunc has unit of -1, and the order of operations can be reordered
 * This case allows reduction with multiple axes at once. Intended for
 * bitwise_and reduction.
 */
#define PyUFunc_MinusOne 2
/*
 * UFunc has no unit, and the order of operations cannot be reordered.
 * This case does not allow reduction with multiple axes at once.
 */
#define PyUFunc_None -1
/*
 * UFunc has no unit, and the order of operations can be reordered
 * This case allows reduction with multiple axes at once.
 */
#define PyUFunc_ReorderableNone -2
/*
 * UFunc unit is an identity_value, and the order of operations can be reordered
 * This case allows reduction with multiple axes at once.
 */
#define PyUFunc_IdentityValue -3


#define UFUNC_REDUCE 0
#define UFUNC_ACCUMULATE 1
#define UFUNC_REDUCEAT 2
#define UFUNC_OUTER 3


typedef struct {
        int nin;
        int nout;
        PyObject *callable;
} PyUFunc_PyFuncData;

/* A linked-list of function information for
   user-defined 1-d loops.
 */
typedef struct _loop1d_info {
        PyUFuncGenericFunction func;
        void *data;
        int *arg_types;
        struct _loop1d_info *next;
        int nargs;
        PyArray_Descr **arg_dtypes;
} PyUFunc_Loop1d;


#include "__ufunc_api.h"

#define UFUNC_PYVALS_NAME "UFUNC_PYVALS"

/*
 * THESE MACROS ARE DEPRECATED.
 * Use npy_set_floatstatus_* in the npymath library.
 */
#define UFUNC_FPE_DIVIDEBYZERO  NPY_FPE_DIVIDEBYZERO
#define UFUNC_FPE_OVERFLOW      NPY_FPE_OVERFLOW
#define UFUNC_FPE_UNDERFLOW     NPY_FPE_UNDERFLOW
#define UFUNC_FPE_INVALID       NPY_FPE_INVALID

#define generate_divbyzero_error() npy_set_floatstatus_divbyzero()
#define generate_overflow_error() npy_set_floatstatus_overflow()

  /* Make sure it gets defined if it isn't already */
#ifndef UFUNC_NOFPE
/* Clear the floating point exception default of Borland C++ */
#if defined(__BORLANDC__)
#define UFUNC_NOFPE _control87(MCW_EM, MCW_EM);
#else
#define UFUNC_NOFPE
#endif
#endif

#ifdef __cplusplus
}
#endif

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_UFUNCOBJECT_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/include/numpy/utils.h

```plaintext
#ifndef NUMPY_CORE_INCLUDE_NUMPY_UTILS_H_
#define NUMPY_CORE_INCLUDE_NUMPY_UTILS_H_

#ifndef __COMP_NPY_UNUSED
    #if defined(__GNUC__)
        #define __COMP_NPY_UNUSED __attribute__ ((__unused__))
    #elif defined(__ICC)
        #define __COMP_NPY_UNUSED __attribute__ ((__unused__))
    #elif defined(__clang__)
        #define __COMP_NPY_UNUSED __attribute__ ((unused))
    #else
        #define __COMP_NPY_UNUSED
    #endif
#endif

#if defined(__GNUC__) || defined(__ICC) || defined(__clang__)
    #define NPY_DECL_ALIGNED(x) __attribute__ ((aligned (x)))
#elif defined(_MSC_VER)
    #define NPY_DECL_ALIGNED(x) __declspec(align(x))
#else
    #define NPY_DECL_ALIGNED(x)
#endif

/* Use this to tag a variable as not used. It will remove unused variable
 * warning on support platforms (see __COM_NPY_UNUSED) and mangle the variable
 * to avoid accidental use */
#define NPY_UNUSED(x) __NPY_UNUSED_TAGGED ## x __COMP_NPY_UNUSED
#define NPY_EXPAND(x) x

#define NPY_STRINGIFY(x) #x
#define NPY_TOSTRING(x) NPY_STRINGIFY(x)

#define NPY_CAT__(a, b) a ## b
#define NPY_CAT_(a, b) NPY_CAT__(a, b)
#define NPY_CAT(a, b) NPY_CAT_(a, b)

#endif  /* NUMPY_CORE_INCLUDE_NUMPY_UTILS_H_ */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/core/tests/data/generate_umath_validation_data.cpp

```plaintext
#include <algorithm>
#include <fstream>
#include <iostream>
#include <cmath>
#include <random>
#include <cstdio>
#include <ctime>
#include <vector>

struct ufunc {
    std::string name;
    double (*f32func)(double);
    long double (*f64func)(long double);
    float f32ulp;
    float f64ulp;
};

template <typename T>
T
RandomFloat(T a, T b)
{
    T random = ((T)rand()) / (T)RAND_MAX;
    T diff = b - a;
    T r = random * diff;
    return a + r;
}

template <typename T>
void
append_random_array(std::vector<T> &arr, T min, T max, size_t N)
{
    for (size_t ii = 0; ii < N; ++ii)
        arr.emplace_back(RandomFloat<T>(min, max));
}

template <typename T1, typename T2>
std::vector<T1>
computeTrueVal(const std::vector<T1> &in, T2 (*mathfunc)(T2))
{
    std::vector<T1> out;
    for (T1 elem : in) {
        T2 elem_d = (T2)elem;
        T1 out_elem = (T1)mathfunc(elem_d);
        out.emplace_back(out_elem);
    }
    return out;
}

/*
 * FP range:
 * [-inf, -maxflt, -1., -minflt, -minden, 0., minden, minflt, 1., maxflt, inf]
 */

#define MINDEN std::numeric_limits<T>::denorm_min()
#define MINFLT std::numeric_limits<T>::min()
#define MAXFLT std::numeric_limits<T>::max()
#define INF std::numeric_limits<T>::infinity()
#define qNAN std::numeric_limits<T>::quiet_NaN()
#define sNAN std::numeric_limits<T>::signaling_NaN()

template <typename T>
std::vector<T>
generate_input_vector(std::string func)
{
    std::vector<T> input = {MINDEN,  -MINDEN, MINFLT, -MINFLT, MAXFLT,
                            -MAXFLT, INF,     -INF,   qNAN,    sNAN,
                            -1.0,    1.0,     0.0,    -0.0};

    // [-1.0, 1.0]
    if ((func == "arcsin") || (func == "arccos") || (func == "arctanh")) {
        append_random_array<T>(input, -1.0, 1.0, 700);
    }
    // (0.0, INF]
    else if ((func == "log2") || (func == "log10")) {
        append_random_array<T>(input, 0.0, 1.0, 200);
        append_random_array<T>(input, MINDEN, MINFLT, 200);
        append_random_array<T>(input, MINFLT, 1.0, 200);
        append_random_array<T>(input, 1.0, MAXFLT, 200);
    }
    // (-1.0, INF]
    else if (func == "log1p") {
        append_random_array<T>(input, -1.0, 1.0, 200);
        append_random_array<T>(input, -MINFLT, -MINDEN, 100);
        append_random_array<T>(input, -1.0, -MINFLT, 100);
        append_random_array<T>(input, MINDEN, MINFLT, 100);
        append_random_array<T>(input, MINFLT, 1.0, 100);
        append_random_array<T>(input, 1.0, MAXFLT, 100);
    }
    // [1.0, INF]
    else if (func == "arccosh") {
        append_random_array<T>(input, 1.0, 2.0, 400);
        append_random_array<T>(input, 2.0, MAXFLT, 300);
    }
    // [-INF, INF]
    else {
        append_random_array<T>(input, -1.0, 1.0, 100);
        append_random_array<T>(input, MINDEN, MINFLT, 100);
        append_random_array<T>(input, -MINFLT, -MINDEN, 100);
        append_random_array<T>(input, MINFLT, 1.0, 100);
        append_random_array<T>(input, -1.0, -MINFLT, 100);
        append_random_array<T>(input, 1.0, MAXFLT, 100);
        append_random_array<T>(input, -MAXFLT, -100.0, 100);
    }

    std::random_shuffle(input.begin(), input.end());
    return input;
}

int
main()
{
    srand(42);
    std::vector<struct ufunc> umathfunc = {
            {"sin", sin, sin, 2.37, 3.3},
            {"cos", cos, cos, 2.36, 3.38},
            {"tan", tan, tan, 3.91, 3.93},
            {"arcsin", asin, asin, 3.12, 2.55},
            {"arccos", acos, acos, 2.1, 1.67},
            {"arctan", atan, atan, 2.3, 2.52},
            {"sinh", sinh, sinh, 1.55, 1.89},
            {"cosh", cosh, cosh, 2.48, 1.97},
            {"tanh", tanh, tanh, 1.38, 1.19},
            {"arcsinh", asinh, asinh, 1.01, 1.48},
            {"arccosh", acosh, acosh, 1.16, 1.05},
            {"arctanh", atanh, atanh, 1.45, 1.46},
            {"cbrt", cbrt, cbrt, 1.94, 1.82},
            //{"exp",exp,exp,3.76,1.53},
            {"exp2", exp2, exp2, 1.01, 1.04},
            {"expm1", expm1, expm1, 2.62, 2.1},
            //{"log",log,log,1.84,1.67},
            {"log10", log10, log10, 3.5, 1.92},
            {"log1p", log1p, log1p, 1.96, 1.93},
            {"log2", log2, log2, 2.12, 1.84},
    };

    for (int ii = 0; ii < umathfunc.size(); ++ii) {
        // ignore sin/cos
        if ((umathfunc[ii].name != "sin") && (umathfunc[ii].name != "cos")) {
            std::string fileName =
                    "umath-validation-set-" + umathfunc[ii].name + ".csv";
            std::ofstream txtOut;
            txtOut.open(fileName, std::ofstream::trunc);
            txtOut << "dtype,input,output,ulperrortol" << std::endl;

            // Single Precision
            auto f32in = generate_input_vector<float>(umathfunc[ii].name);
            auto f32out = computeTrueVal<float, double>(f32in,
                                                        umathfunc[ii].f32func);
            for (int jj = 0; jj < f32in.size(); ++jj) {
                txtOut << "np.float32" << std::hex << ",0x"
                       << *reinterpret_cast<uint32_t *>(&f32in[jj]) << ",0x"
                       << *reinterpret_cast<uint32_t *>(&f32out[jj]) << ","
                       << ceil(umathfunc[ii].f32ulp) << std::endl;
            }

            // Double Precision
            auto f64in = generate_input_vector<double>(umathfunc[ii].name);
            auto f64out = computeTrueVal<double, long double>(
                    f64in, umathfunc[ii].f64func);
            for (int jj = 0; jj < f64in.size(); ++jj) {
                txtOut << "np.float64" << std::hex << ",0x"
                       << *reinterpret_cast<uint64_t *>(&f64in[jj]) << ",0x"
                       << *reinterpret_cast<uint64_t *>(&f64out[jj]) << ","
                       << ceil(umathfunc[ii].f64ulp) << std::endl;
            }
            txtOut.close();
        }
    }
    return 0;
}
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/numpy/f2py/src/fortranobject.h

```plaintext
#ifndef Py_FORTRANOBJECT_H
#define Py_FORTRANOBJECT_H
#ifdef __cplusplus
extern "C" {
#endif

#include <Python.h>

#ifndef NPY_NO_DEPRECATED_API
#define NPY_NO_DEPRECATED_API NPY_API_VERSION
#endif
#ifdef FORTRANOBJECT_C
#define NO_IMPORT_ARRAY
#endif
#define PY_ARRAY_UNIQUE_SYMBOL _npy_f2py_ARRAY_API
#include "numpy/arrayobject.h"
#include "numpy/npy_3kcompat.h"

#ifdef F2PY_REPORT_ATEXIT
#include <sys/timeb.h>
// clang-format off
extern void f2py_start_clock(void);
extern void f2py_stop_clock(void);
extern void f2py_start_call_clock(void);
extern void f2py_stop_call_clock(void);
extern void f2py_cb_start_clock(void);
extern void f2py_cb_stop_clock(void);
extern void f2py_cb_start_call_clock(void);
extern void f2py_cb_stop_call_clock(void);
extern void f2py_report_on_exit(int, void *);
// clang-format on
#endif

#ifdef DMALLOC
#include "dmalloc.h"
#endif

/* Fortran object interface */

/*
123456789-123456789-123456789-123456789-123456789-123456789-123456789-12

PyFortranObject represents various Fortran objects:
Fortran (module) routines, COMMON blocks, module data.

Author: Pearu Peterson <pearu@cens.ioc.ee>
*/

#define F2PY_MAX_DIMS 40
#define F2PY_MESSAGE_BUFFER_SIZE 300  // Increase on "stack smashing detected"

typedef void (*f2py_set_data_func)(char *, npy_intp *);
typedef void (*f2py_void_func)(void);
typedef void (*f2py_init_func)(int *, npy_intp *, f2py_set_data_func, int *);

/*typedef void* (*f2py_c_func)(void*,...);*/

typedef void *(*f2pycfunc)(void);

typedef struct {
    char *name; /* attribute (array||routine) name */
    int rank;   /* array rank, 0 for scalar, max is F2PY_MAX_DIMS,
                   || rank=-1 for Fortran routine */
    struct {
        npy_intp d[F2PY_MAX_DIMS];
    } dims;              /* dimensions of the array, || not used */
    int type;            /* PyArray_<type> || not used */
    int elsize;                /* Element size || not used */
    char *data;          /* pointer to array || Fortran routine */
    f2py_init_func func; /* initialization function for
                            allocatable arrays:
                            func(&rank,dims,set_ptr_func,name,len(name))
                            || C/API wrapper for Fortran routine */
    char *doc;           /* documentation string; only recommended
                            for routines. */
} FortranDataDef;

typedef struct {
    PyObject_HEAD
    int len;              /* Number of attributes */
    FortranDataDef *defs; /* An array of FortranDataDef's */
    PyObject *dict;       /* Fortran object attribute dictionary */
} PyFortranObject;

#define PyFortran_Check(op) (Py_TYPE(op) == &PyFortran_Type)
#define PyFortran_Check1(op) (0 == strcmp(Py_TYPE(op)->tp_name, "fortran"))

extern PyTypeObject PyFortran_Type;
extern int
F2PyDict_SetItemString(PyObject *dict, char *name, PyObject *obj);
extern PyObject *
PyFortranObject_New(FortranDataDef *defs, f2py_void_func init);
extern PyObject *
PyFortranObject_NewAsAttr(FortranDataDef *defs);

PyObject *
F2PyCapsule_FromVoidPtr(void *ptr, void (*dtor)(PyObject *));
void *
F2PyCapsule_AsVoidPtr(PyObject *obj);
int
F2PyCapsule_Check(PyObject *ptr);

extern void *
F2PySwapThreadLocalCallbackPtr(char *key, void *ptr);
extern void *
F2PyGetThreadLocalCallbackPtr(char *key);

#define ISCONTIGUOUS(m) (PyArray_FLAGS(m) & NPY_ARRAY_C_CONTIGUOUS)
#define F2PY_INTENT_IN 1
#define F2PY_INTENT_INOUT 2
#define F2PY_INTENT_OUT 4
#define F2PY_INTENT_HIDE 8
#define F2PY_INTENT_CACHE 16
#define F2PY_INTENT_COPY 32
#define F2PY_INTENT_C 64
#define F2PY_OPTIONAL 128
#define F2PY_INTENT_INPLACE 256
#define F2PY_INTENT_ALIGNED4 512
#define F2PY_INTENT_ALIGNED8 1024
#define F2PY_INTENT_ALIGNED16 2048

#define ARRAY_ISALIGNED(ARR, SIZE) ((size_t)(PyArray_DATA(ARR)) % (SIZE) == 0)
#define F2PY_ALIGN4(intent) (intent & F2PY_INTENT_ALIGNED4)
#define F2PY_ALIGN8(intent) (intent & F2PY_INTENT_ALIGNED8)
#define F2PY_ALIGN16(intent) (intent & F2PY_INTENT_ALIGNED16)

#define F2PY_GET_ALIGNMENT(intent) \
    (F2PY_ALIGN4(intent)           \
             ? 4                   \
             : (F2PY_ALIGN8(intent) ? 8 : (F2PY_ALIGN16(intent) ? 16 : 1)))
#define F2PY_CHECK_ALIGNMENT(arr, intent) \
    ARRAY_ISALIGNED(arr, F2PY_GET_ALIGNMENT(intent))
#define F2PY_ARRAY_IS_CHARACTER_COMPATIBLE(arr) ((PyArray_DESCR(arr)->type_num == NPY_STRING && PyArray_DESCR(arr)->elsize >= 1) \
                                                 || PyArray_DESCR(arr)->type_num == NPY_UINT8)
#define F2PY_IS_UNICODE_ARRAY(arr) (PyArray_DESCR(arr)->type_num == NPY_UNICODE)

extern PyArrayObject *
ndarray_from_pyobj(const int type_num, const int elsize_, npy_intp *dims,
                   const int rank, const int intent, PyObject *obj,
                   const char *errmess);

extern PyArrayObject *
array_from_pyobj(const int type_num, npy_intp *dims, const int rank,
                 const int intent, PyObject *obj);
extern int
copy_ND_array(const PyArrayObject *in, PyArrayObject *out);

#ifdef DEBUG_COPY_ND_ARRAY
extern void
dump_attrs(const PyArrayObject *arr);
#endif

  extern int f2py_describe(PyObject *obj, char *buf);

  /* Utility CPP macros and functions that can be used in signature file
     expressions. See signature-file.rst for documentation.
  */

#define f2py_itemsize(var) (PyArray_DESCR((capi_ ## var ## _as_array))->elsize)
#define f2py_size(var, ...) f2py_size_impl((PyArrayObject *)(capi_ ## var ## _as_array), ## __VA_ARGS__, -1)
#define f2py_rank(var) var ## _Rank
#define f2py_shape(var,dim) var ## _Dims[dim]
#define f2py_len(var) f2py_shape(var,0)
#define f2py_fshape(var,dim) f2py_shape(var,rank(var)-dim-1)
#define f2py_flen(var) f2py_fshape(var,0)
#define f2py_slen(var) capi_ ## var ## _len

  extern npy_intp f2py_size_impl(PyArrayObject* var, ...);

#ifdef __cplusplus
}
#endif
#endif /* !Py_FORTRANOBJECT_H */
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/pandas-2.0.3.dist-info/AUTHORS.md

```
About the Copyright Holders
===========================

*   Copyright (c) 2008-2011 AQR Capital Management, LLC

    AQR Capital Management began pandas development in 2008. Development was
    led by Wes McKinney. AQR released the source under this license in 2009.
*   Copyright (c) 2011-2012, Lambda Foundry, Inc.

    Wes is now an employee of Lambda Foundry, and remains the pandas project
    lead.
*   Copyright (c) 2011-2012, PyData Development Team

    The PyData Development Team is the collection of developers of the PyData
    project. This includes all of the PyData sub-projects, including pandas. The
    core team that coordinates development on GitHub can be found here:
    https://github.com/pydata.

Full credits for pandas contributors can be found in the documentation.

Our Copyright Policy
====================

PyData uses a shared copyright model. Each contributor maintains copyright
over their contributions to PyData. However, it is important to note that
these contributions are typically only changes to the repositories. Thus,
the PyData source code, in its entirety, is not the copyright of any single
person or institution. Instead, it is the collective copyright of the
entire PyData Development Team. If individual contributors want to maintain
a record of what changes/contributions they have specific copyright on,
they should indicate their copyright in the commit message of the change
when they commit the change to one of the PyData repositories.

With this in mind, the following banner should be used in any source code
file to indicate the copyright and license terms:

```
#-----------------------------------------------------------------------------
# Copyright (c) 2012, PyData Development Team
# All rights reserved.
#
# Distributed under the terms of the BSD Simplified License.
#
# The full license is in the LICENSE file, distributed with this software.
#-----------------------------------------------------------------------------
```

Other licenses can be found in the LICENSES directory.

License
=======

pandas is distributed under a 3-clause ("Simplified" or "New") BSD
license. Parts of NumPy, SciPy, numpydoc, bottleneck, which all have
BSD-compatible licenses, are included. Their licenses follow the pandas
license.
```

-----------

Path: ./deft_env/lib/python3.8/site-packages/seaborn-0.13.2.dist-info/LICENSE.md

```
Copyright (c) 2012-2023, Michael L. Waskom
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the project nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

-----------

Path: ./README.md

```
# DeftRL
```

-----------

