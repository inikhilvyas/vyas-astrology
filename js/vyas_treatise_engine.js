// vyas_treatise_engine.js - Pure Browser & Node.js Universal Engine
(function (global) {
    var treatiseData = [];
    if (typeof NIKHIL_VYAS_TREATISE_SUTRAS !== 'undefined') {
        treatiseData = NIKHIL_VYAS_TREATISE_SUTRAS;
    } else if (typeof window !== 'undefined' && window.NIKHIL_VYAS_TREATISE_SUTRAS) {
        treatiseData = window.NIKHIL_VYAS_TREATISE_SUTRAS;
    } else if (typeof require !== 'undefined') {
        try {
            treatiseData = require('./vyas_treatise_sutras.js');
        } catch (e) { }
    }

    var VyasTreatiseEngine = {
        getAll: function () {
            if ((!treatiseData || treatiseData.length === 0) && typeof NIKHIL_VYAS_TREATISE_SUTRAS !== 'undefined') {
                treatiseData = NIKHIL_VYAS_TREATISE_SUTRAS;
            }
            return treatiseData || [];
        },
        search: function (query, limit) {
            limit = limit || 15;
            if (!query) return [];
            var data = this.getAll();
            var q = String(query).toLowerCase().trim();
            var results = [];
            var seen = {};

            for (var i = 0; i < data.length; i++) {
                var item = data[i];
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
        getRemediesForPlanet: function (planetName) {
            if (!planetName) return [];
            return this.search(planetName.trim(), 25);
        },
        getYantraForNeed: function (needQuery) {
            if (!needQuery) return [];
            return this.search(needQuery.trim(), 15);
        }
    };

    if (typeof window !== 'undefined') {
        window.VyasTreatiseEngine = VyasTreatiseEngine;
    }
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = VyasTreatiseEngine;
    }
})(typeof window !== 'undefined' ? window : global);
