// expect: test --- FAIL: TestBroken
package calc

import "testing"

func TestBroken(t *testing.T) {
	if Add(1, 1) != 3 {
		t.Fatal("expected 3")
	}
}
