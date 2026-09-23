import { expect, test } from "bun:test"
import { hasToken } from "@/alias.ts"

test("hasToken is a boolean", () => {
  expect(typeof hasToken).toBe("boolean")
})
