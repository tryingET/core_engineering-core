// expect: vet self-assignment of x
package calc

// Assign assigns x to itself.
func Assign() int {
	x := 1
	x = x
	return x
}
