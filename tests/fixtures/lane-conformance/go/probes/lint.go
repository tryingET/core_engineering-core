// expect: lint (errcheck)
package calc

import "os"

// Cleanup removes a file and ignores the error.
func Cleanup() {
	os.Remove("x")
}
