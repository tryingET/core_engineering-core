import { expect, test } from "bun:test"
import { token } from "@/env.ts"

test("token is optional", () => {
  expect(token === undefined || typeof token === "string").toBe(true)
})
