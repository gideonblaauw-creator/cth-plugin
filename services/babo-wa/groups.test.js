import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
  groupCreateResponse,
  parseGroupCreateBody,
  parseGroupDescriptionBody,
  splitGroupCreateParticipants,
} from './groups.js';

describe('groups helpers', () => {
  it('parses create body and normalizes digits', () => {
    const parsed = parseGroupCreateBody({
      name: 'Demo',
      participants: ['5730000000001', '5730000000002@s.whatsapp.net'],
    });
    assert.equal(parsed.name, 'Demo');
    assert.deepEqual(parsed.participants, [
      '5730000000001@s.whatsapp.net',
      '5730000000002@s.whatsapp.net',
    ]);
  });

  it('rejects empty name and >50 participants', () => {
    assert.match(parseGroupCreateBody({ name: '', participants: ['5730000000000'] }).error, /name/);
    const many = Array.from({ length: 51 }, (_, i) => `5730000000${String(i).padStart(3, '0')}`);
    assert.match(parseGroupCreateBody({ name: 'x', participants: many }).error, /50/);
  });

  it('requires group jid for description', () => {
    assert.match(
      parseGroupDescriptionBody({ jid: '5730000000000@s.whatsapp.net', description: 'x' }).error,
      /@g.us/,
    );
  });

  it('maps participant status buckets', () => {
    const { added, failed } = splitGroupCreateParticipants([
      { jid: '5730000000001@s.whatsapp.net', status: 200 },
      { jid: '5730000000002@s.whatsapp.net', status: 403 },
      { jid: '5730000000003@s.whatsapp.net', status: 409 },
    ]);
    assert.deepEqual(added, ['5730000000001@s.whatsapp.net']);
    assert.equal(failed.length, 2);
    assert.equal(failed[0].reason, 'privacy');
    assert.equal(failed[1].reason, 'already in');
  });

  it('builds group create API shape', () => {
    const out = groupCreateResponse({
      id: '120363000000000000@g.us',
      subject: 'Demo',
      participants: [
        { jid: '5730000000001@s.whatsapp.net', status: 200 },
        { jid: '5730000000002@s.whatsapp.net', status: 408 },
      ],
    });
    assert.equal(out.jid, '120363000000000000@g.us');
    assert.equal(out.subject, 'Demo');
    assert.equal(out.added.length, 1);
    assert.equal(out.failed[0].reason, 'left recently');
  });
});