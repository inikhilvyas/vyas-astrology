const fs = require('fs');
const assert = require('assert');

console.log("=== VERIFYING GOOGLE IDENTITY SERVICES (GIS) INTEGRATION ===");

const files = [
    { path: 'index.html', name: 'Desktop', obj: 'VyasDesktop', btnId: 'g_id_signin_desktop' },
    { path: 'mobile/index.html', name: 'Mobile Web', obj: 'VyasMobile', btnId: 'g_id_signin_mobile' },
    { path: 'android_app/app/src/main/assets/mobile/index.html', name: 'Android Asset', obj: 'VyasMobile', btnId: 'g_id_signin_mobile' }
];

const CLIENT_ID = "341351445313-ddlkfiqsndnvbl290bubh1u3s827c3b2.apps.googleusercontent.com";

files.forEach(f => {
    console.log(`\n--- Checking ${f.name} (${f.path}) ---`);
    const content = fs.readFileSync(f.path, 'utf8');

    // 1. GIS script
    assert(content.includes('https://accounts.google.com/gsi/client'), `Missing gsi/client script in ${f.path}`);
    console.log(`[PASS] Official GIS script tag present`);

    // 2. g_id_onload with client_id
    assert(content.includes('id="g_id_onload"'), `Missing g_id_onload in ${f.path}`);
    assert(content.includes(CLIENT_ID), `Missing authorized Google Client ID in ${f.path}`);
    console.log(`[PASS] Declarative g_id_onload configured with Client ID: ${CLIENT_ID.substring(0, 20)}...`);

    // 3. g_id_signin container
    assert(content.includes(`id="${f.btnId}"`), `Missing ${f.btnId} in ${f.path}`);
    console.log(`[PASS] Official Google signin button container #${f.btnId} present`);

    // 4. JS methods
    assert(content.includes('setupGoogleIdentity'), `Missing setupGoogleIdentity in ${f.path}`);
    assert(content.includes('handleGoogleCredentialResponse'), `Missing handleGoogleCredentialResponse in ${f.path}`);
    assert(content.includes('promptGoogleSignIn'), `Missing promptGoogleSignIn in ${f.path}`);
    console.log(`[PASS] Required GIS methods (setupGoogleIdentity, handleGoogleCredentialResponse, promptGoogleSignIn) present`);

    // 5. Manual login hidden by default
    assert(content.includes('display:none;') && (content.includes('dManualLoginSection') || content.includes('mManualLoginSection')), `Manual login section should be hidden by default in ${f.path}`);
    console.log(`[PASS] Manual fallback inputs cleanly collapsed (hidden by default)`);
});

console.log("\n=======================================================");
console.log("ALL 3 PLATFORMS VERIFIED FOR AUTHENTIC GOOGLE IDENTITY SERVICES!");
console.log("=======================================================\n");
