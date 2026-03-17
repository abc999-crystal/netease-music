#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

function getEnabledTargets(config) {
  if (!config.targets) {
    return [{ name: 'claude-code', paths: { global: '.claude/skills', project: '.claude/skills' } }];
  }
  return Object.entries(config.targets)
    .filter(([_, target]) => target.enabled)
    .map(([name, target]) => ({ name, paths: target.paths }));
}

function uninstallSkill() {
  console.log('🗑️  Uninstalling AI Coding Skill...\n');
  const config = JSON.parse(fs.readFileSync(path.join(__dirname, '.claude-skill.json'), 'utf8'));
  const enabledTargets = getEnabledTargets(config);

  for (const target of enabledTargets) {
    const globalDir = path.join(os.homedir(), target.paths.global, config.name);
    if (fs.existsSync(globalDir)) {
      fs.rmSync(globalDir, { recursive: true });
      console.log(`  ✓ Removed from ${target.name} (global)`);
    }
  }
  console.log('\n✅ Uninstallation Complete!');
}

try { uninstallSkill(); } catch (error) {
  console.error('\n❌ Failed:', error.message);
  process.exit(1);
}
