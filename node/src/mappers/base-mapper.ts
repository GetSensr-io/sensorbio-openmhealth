import type { OmhDataPoint, OmhHeader, OmhSchemaId } from '../schemas/types.js';
import { generateUUID } from '../utils/uuid.js';

export abstract class BaseMapper<TSensr, TOmhBody> {
  abstract schemaId: OmhSchemaId;
  abstract map(sensrData: TSensr): OmhDataPoint<TOmhBody>[];

  protected createHeader(id?: string): OmhHeader {
    return {
      id: id || generateUUID(),
      creation_date_time: new Date().toISOString(),
      schema_id: this.schemaId,
      acquisition_provenance: {
        source_name: 'Sensr Bio',
        modality: 'sensed'
      }
    };
  }

  protected createDataPoint(body: TOmhBody, id?: string): OmhDataPoint<TOmhBody> {
    return { header: this.createHeader(id), body };
  }
}
