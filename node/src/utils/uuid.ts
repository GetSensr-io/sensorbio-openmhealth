import { randomUUID } from 'node:crypto';

/**
 * Generate UUID v4 string for OMH data point headers.
 */
export function generateUUID(): string {
  return randomUUID();
}
