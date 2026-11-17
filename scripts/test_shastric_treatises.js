const fs = require('fs');
const assert = require('assert');

const html = fs.readFileSync('index.html', 'utf8');

// 1. Verify all 4 Knowledge Vaults exist statically in HTML
assert(html.includes('id="vedicKnowledgeVaultBox"'), 'Missing #vedicKnowledgeVaultBox');
assert(html.includes('id="kpKnowledgeVaultBox"'), 'Missing #kpKnowledgeVaultBox');
assert(html.includes('id="jaiminiKnowledgeVaultBox"'), 'Missing #jaiminiKnowledgeVaultBox');
assert(html.includes('id="nadiKnowledgeVaultBox"'), 'Missing #nadiKnowledgeVaultBox');

// 2. Verify specific classical treatises are cited
const citations = [
    'Brihat Parashara Hora Shastra',
    'Phaladeepika',
    'Sarvartha Chintamani',
    '300 Important Combinations',
    'KP Readers',
    'Cuspal Interlinks',
    'Jaimini Upadesha Sutras',
    'K.N. Rao Chara Dasha',
    'Bhrigu Nandi Nadi',
    'Deva Keralam'
];

for (const c of citations) {
    assert(html.includes(c), `Missing treatise citation: ${c}`);
    console.log(`✓ Verified Treatise Citation: ${c}`);
}

// 3. Verify early returns were eliminated in renderKP and renderJaimini
assert(!html.includes('if (!kp) {\n                if (cBody) cBody.innerHTML = \'<tr><td colspan="7" style="text-align:center; padding:24px; color:var(--text-muted);">कुण्डली लोड होने पर 12 कस्प सब-लॉर्ड्स प्रदर्शित होंगे।</td></tr>\';\n                return;'), 'Found old early return in renderKP');
assert(!html.includes('if (!jm) {\n                if (tbody) tbody.innerHTML = \'<tr><td colspan="6" style="text-align:center; padding:24px; color:var(--text-muted);">कुण्डली लोड होने पर 7 चर कारक प्रदर्शित होंगे।</td></tr>\';\n                return;'), 'Found old early return in renderJaimini');

console.log('✓ ALL SHASTRIC TREATISE & KNOWLEDGE VAULT TESTS PASSED!');
