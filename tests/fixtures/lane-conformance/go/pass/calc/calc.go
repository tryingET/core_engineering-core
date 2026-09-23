// Package calc is the go lane conformance fixture.
package calc

import "fmt"

// Add returns the sum of a and b.
func Add(a, b int) int {
	return a + b
}

// Describe renders an addition.
func Describe(a, b int) string {
	return fmt.Sprintf("%d + %d = %d", a, b, Add(a, b))
}
