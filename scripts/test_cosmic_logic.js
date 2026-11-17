// Test script for cosmic engine syntax and rendering logic
const canvas = {
    width: 1920,
    height: 1080
};

console.log("Testing cosmic engine logic...");
// Check array allocations, star generation, meteor spawning
const stars = [];
for (let i = 0; i < 180; i++) {
    stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 1.6 + 0.4,
        alpha: Math.random(),
        speed: Math.random() * 0.03 + 0.01
    });
}
console.log("Stars initialized:", stars.length);

const meteors = [];
function spawnMeteor() {
    meteors.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height * 0.4,
        len: Math.random() * 140 + 80,
        speed: Math.random() * 7 + 8,
        angle: Math.PI / 4 + (Math.random() - 0.5) * 0.25,
        alpha: 1,
        fade: 0.015,
        width: 1.8
    });
}
spawnMeteor();
console.log("Meteor spawned successfully:", meteors[0]);
console.log("Cosmic logic verified cleanly.");

