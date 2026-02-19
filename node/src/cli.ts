#!/usr/bin/env node
import { writeFile } from 'node:fs/promises';
import { SensrClient, SensrToOmhConverter } from './index.js';

function getArg(name: string): string | undefined {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

function hasFlag(name: string): boolean {
  return process.argv.includes(`--${name}`);
}

function usage(): string {
  return `sensr-to-omh

Usage:
  sensr-to-omh --api-key <key> --user-id <id> --start-date YYYY-MM-DD --end-date YYYY-MM-DD [--base-url <url>] [--out <file>]

Options:
  --api-key       Sensr org API key (X-API-KEY)
  --base-url      Override Sensr base URL (default: https://api.getsensr.io)
  --user-id       Sensr user id
  --start-date    Inclusive start date
  --end-date      Inclusive end date
  --out           Output file (default: stdout)
  --pretty        Pretty-print JSON
`;
}

async function main() {
  if (hasFlag('help') || hasFlag('h')) {
    process.stdout.write(usage());
    process.exit(0);
  }

  const apiKey = getArg('api-key') ?? process.env.SENSR_API_KEY;
  const baseUrl = getArg('base-url') ?? process.env.SENSR_BASE_URL;
  const userId = getArg('user-id') ?? process.env.SENSR_USER_ID;
  const startDate = getArg('start-date') ?? process.env.START_DATE;
  const endDate = getArg('end-date') ?? process.env.END_DATE;
  const outPath = getArg('out');
  const pretty = hasFlag('pretty');

  if (!apiKey || !userId || !startDate || !endDate) {
    process.stderr.write(usage());
    process.stderr.write('\nMissing required args (or env vars).\n');
    process.exit(1);
  }

  const client = new SensrClient({ apiKey, ...(baseUrl ? { baseUrl } : {}) });
  const converter = new SensrToOmhConverter(client);

  const points = await converter.convertAll({ userId, dateRange: { startDate, endDate } });
  const json = JSON.stringify(points, null, pretty ? 2 : 0);

  if (outPath) {
    await writeFile(outPath, json + '\n', 'utf8');
  } else {
    process.stdout.write(json + '\n');
  }
}

main().catch((err) => {
  process.stderr.write(String(err?.stack ?? err) + '\n');
  process.exit(1);
});
