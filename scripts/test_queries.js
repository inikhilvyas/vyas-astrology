global.window = global;
require('../js/vyas_daivagya_engine.js');

var sampleChart = {
    profile: { asc_sign: 'वृश्चिक', name: 'निखिल व्यास' },
    planet_table: [
        { p: 'सूर्य', r: 'वृश्चिक', d: '3.6', n: 'अनुराधा', h: '1', s: 'मित्र' },
        { p: 'बुध', r: 'वृश्चिक', d: '8.2', n: 'अनुराधा', h: '1', s: 'सम' },
        { p: 'मंगल', r: 'सिंह', d: '3.4', n: 'मघा', h: '10', s: 'मित्र' },
        { p: 'गुरु', r: 'सिंह', d: '1.9', n: 'मघा', h: '10', s: 'मित्र' },
        { p: 'शुक्र', r: 'कन्या', d: '29.4', n: 'चित्रा', h: '11', s: 'नीच' },
        { p: 'शनि', r: 'मीन', d: '14.1', n: 'उत्तराभाद्रपद', h: '5', s: 'सम' },
        { p: 'चन्द्र', r: 'मीन', d: '4.7', n: 'उत्तराभाद्रपद', h: '5', s: 'सम' },
        { p: 'राहु', r: 'कुंभ', d: '0.9', n: 'धनिष्ठा', h: '4', s: 'मित्र' },
        { p: 'केतु', r: 'सिंह', d: '0.9', n: 'मघा', h: '10', s: 'मित्र' }
    ]
};

var queries = [
    'मेरी कुंडली में केमद्रुम योग है?',
    'केमद्रुम योग',
    'गजकेसरी योग',
    'क्या मेरी कुंडली में कोई राजयोग है?',
    'करियर कैसा रहेगा?',
    'मेरी दशा क्या चल रही है?',
    'विवाह कब होगा?'
];

queries.forEach(function(q) {
    var route = window.VyasQueryRouter.detect(q);
    var formatted = window.VyasDaivagyaCore.formatReading(q, sampleChart);
    console.log('Q: "' + q + '" => Route: ' + route + ' | Formatted length: ' + (formatted ? formatted.length : 'NULL'));
});
