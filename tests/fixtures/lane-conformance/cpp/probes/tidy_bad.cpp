// expect: tidy modernize-use-nullptr
// expect: justfile-ci modernize-use-nullptr
#include <cstddef>

namespace demo {
const int *nothing() { return NULL; }
} // namespace demo
