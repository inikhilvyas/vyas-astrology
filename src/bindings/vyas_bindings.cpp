#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(vyas_bindings, m) {
    // Placeholder: expose a dummy function
    m.def("hello", []() { return std::string("VYAS bindings ready"); });
}
