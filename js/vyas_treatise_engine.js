var fs = require('fs');

var treatiseData = [];
try {
    treatiseData = require('./vyas_treatise_sutras.js');
} catch (e) {
    console.warn('vyas_treatise_sutras load notice:', e.message);
}

var VyasTreatiseEngine = {
    getAll: function() {
        return treatiseData;
    },
    search: function(query, limit) {
        limit = limit || 10;
        if (!query) return [];
        var q = query.toLowerCase().trim();
        var results = [];
        var seen = {};

        for (var i = 0; i < treatiseData.length; i++) {
            var item = treatiseData[i];
            var cond = (item.cond || '').toLowerCase();
            var pred = (item.pred || '').toLowerCase();
            var src = (item.source || '').toLowerCase();

            if (cond.indexOf(q) !== -1 || pred.indexOf(q) !== -1 || src.indexOf(q) !== -1) {
                var k = item.cond;
                if (!seen[k]) {
                    seen[k] = true;
                    results.push(item);
                    if (results.length >= limit) break;
                }
            }
        }
        return results;
    },
    getRemediesForPlanet: function(planetName) {
        if (!planetName) return [];
        var p = planetName.trim();
        return this.search(p, 20);
    },
    getYantraForNeed: function(needQuery) {
        if (!needQuery) return [];
        return this.search(needQuery, 10);
    }
};

if (typeof window !== 'undefined') {
    window.VyasTreatiseEngine = VyasTreatiseEngine;
}
if (typeof global !== 'undefined') {
    global.VyasTreatiseEngine = VyasTreatiseEngine;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VyasTreatiseEngine;
}

