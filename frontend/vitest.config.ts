import { defineConfig } from "vitest/config";
import path from "node:path";

export default defineConfig({
  // Match Next/React 17+ automatic JSX runtime in tests
  esbuild: {
    jsx: "automatic",
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "."),
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./vitest.setup.ts"],
    include: ["tests/**/*.test.tsx"],
  },
});
