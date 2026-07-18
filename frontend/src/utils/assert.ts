export function assertDefined<T>(value: T | null | undefined, message?: string): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message ?? "Value is null or undefined");
  }
}

export function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${value}`);
}
