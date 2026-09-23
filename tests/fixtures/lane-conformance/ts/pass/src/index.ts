// Service entry point bundled by the lane Dockerfile. It uses node:fs, which a
// browser-target bundle silently replaces with an empty object (crash at runtime).
import { existsSync } from "node:fs"
import { hasToken } from "@/alias.ts"

console.log(JSON.stringify({ ok: existsSync("/"), hasToken }))
