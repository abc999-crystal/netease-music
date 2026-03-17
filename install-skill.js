#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

function getEnabledTargets(config) {
  if (!config.targets) {
    return [{
      name: 'claude-code',
      paths: { global: '.claude/skills', project: '.claude/skills' }
    }];
  }
  return Object.entries(config.targets)
    .filter(([_, target]) => target.enabled)
    .map(([name, target]) => ({ name, paths: target.paths }));
}

function detectInstallLocation(targetPaths) {
  const isGlobal = process.env.npm_config_global === 'true';
  if (isGlobal) {
    return { type: 'personal', base: path.join(os.homedir(), targetPaths.global) };
  } else {
    let projectRoot = process.cwd();
    while (projectRoot !== path.dirname(projectRoot)) {
      if (fs.existsSync(path.join(projectRoot, 'package.json')) ||
          fs.existsSync(path.join(projectRoot, '.git'))) break;
      projectRoot = path.dirname(projectRoot);
    }
    return { type: 'project', base: path.join(projectRoot, targetPaths.project) };
  }
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (let entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    entry.isDirectory() ? copyDir(srcPath, destPath) : fs.copyFileSync(srcPath, destPath);
  }
}

function updateManifest(skillsDir, config, targetName) {
  const manifestPath = path.join(skillsDir, '.skills-manifest.json');
  let manifest = { skills: {} };
  if (fs.existsSync(manifestPath)) {
    try { manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8')); } catch (e) {}
  }
  manifest.skills[config.name] = {
    version: config.version,
    installedAt: new Date().toISOString(),
    package: config.package,
    path: path.join(skillsDir, config.name),
    target: targetName
  };
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
}

function installToTarget(target, config) {
  console.log(`\n📦 Installing to ${target.name}...`);
  const location = detectInstallLocation(target.paths);
  const targetDir = path.join(location.base, config.name);
  console.log(`  Type: ${location.type}`);
  console.log(`  Directory: ${targetDir}`);

  fs.mkdirSync(targetDir, { recursive: true });

  // Copy SKILL.md (required)
  const skillMdSource = path.join(__dirname, 'SKILL.md');
  if (!fs.existsSync(skillMdSource)) throw new Error('SKILL.md is required');
  fs.copyFileSync(skillMdSource, path.join(targetDir, 'SKILL.md'));
  console.log('  ✓ Copied SKILL.md');

  // Copy additional files
  if (config.files) {
    for (const [source, dest] of Object.entries(config.files)) {
      const sourcePath = path.join(__dirname, source);
      if (!fs.existsSync(sourcePath)) continue;
      const destPath = path.join(targetDir, dest);
      if (fs.statSync(sourcePath).isDirectory()) {
        copyDir(sourcePath, destPath);
        console.log(`  ✓ Copied directory: ${source}`);
      } else {
        fs.mkdirSync(path.dirname(destPath), { recursive: true });
        fs.copyFileSync(sourcePath, destPath);
        console.log(`  ✓ Copied file: ${source}`);
      }
    }
  }

  updateManifest(location.base, config, target.name);
  console.log(`  ✅ Installed to ${target.name}`);
  return targetDir;
}

function installSkill() {
  console.log('🚀 Installing AI Coding Skill...\n');
  const config = JSON.parse(fs.readFileSync(path.join(__dirname, '.claude-skill.json'), 'utf8'));
  const enabledTargets = getEnabledTargets(config);

  if (enabledTargets.length === 0) {
    console.warn('⚠ No targets enabled');
    return;
  }

  console.log(`Installing skill "${config.name}" to ${enabledTargets.length} target(s)`);
  const installedPaths = [];
  for (const target of enabledTargets) {
    try {
      installedPaths.push({ target: target.name, path: installToTarget(target, config) });
    } catch (error) {
      console.error(`\n❌ Failed to install to ${target.name}:`, error.message);
    }
  }

  console.log('\n' + '='.repeat(50));
  console.log('✅ Installation Complete!');
  if (installedPaths.length > 0) {
    console.log('\nInstalled to:');
    installedPaths.forEach(({ target, path }) => console.log(`  • ${target}: ${path}`));
  }
}

try { installSkill(); } catch (error) {
  console.error('\n❌ Failed:', error.message);
  process.exit(1);
}
