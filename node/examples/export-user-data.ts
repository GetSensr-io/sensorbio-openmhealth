import { SensrClient, SensrToOmhConverter } from '../src/index.js';

async function main() {
  const apiKey = process.env.SENSR_API_KEY;
  if (!apiKey) throw new Error('Missing SENSR_API_KEY');

  const baseUrl = process.env.SENSR_BASE_URL;
  const userId = process.env.SENSR_USER_ID ?? 'user_123';
  const startDate = process.env.START_DATE ?? '2026-02-01';
  const endDate = process.env.END_DATE ?? '2026-02-07';

  const client = new SensrClient({ apiKey, baseUrl });
  const converter = new SensrToOmhConverter(client);

  const points = await converter.convertAll({ userId, dateRange: { startDate, endDate } });
  console.log(JSON.stringify(points, null, 2));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
