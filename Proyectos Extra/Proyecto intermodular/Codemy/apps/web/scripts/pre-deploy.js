#!/usr/bin/env node

/**
 * Pre-Deploy Checklist Script
 * Verifica que todo esté listo antes de hacer deploy
 */

const fs = require('fs');
const path = require('path');

const COLORS = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
};

function log(message, color = 'reset') {
  console.log(`${COLORS[color]}${message}${COLORS.reset}`);
}

function check(condition, passMessage, failMessage) {
  if (condition) {
    log(`✅ ${passMessage}`, 'green');
    return true;
  } else {
    log(`❌ ${failMessage}`, 'red');
    return false;
  }
}

function warn(message) {
  log(`⚠️  ${message}`, 'yellow');
}

async function main() {
  log('\n🚀 Pre-Deploy Checklist\n', 'blue');

  let allPassed = true;
  const warnings = [];

  // 1. Check package.json
  const packageJsonPath = path.join(__dirname, '../package.json');
  const packageExists = fs.existsSync(packageJsonPath);
  allPassed &= check(
    packageExists,
    'package.json exists',
    'package.json not found'
  );

  if (packageExists) {
    const pkg = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    allPassed &= check(
      pkg.dependencies['next'],
      'Next.js dependency found',
      'Next.js not in dependencies'
    );
    allPassed &= check(
      pkg.dependencies['stripe'],
      'Stripe dependency found',
      'Stripe not in dependencies'
    );
    allPassed &= check(
      pkg.dependencies['@supabase/supabase-js'],
      'Supabase dependency found',
      'Supabase not in dependencies'
    );
  }

  // 2. Check required files
  const requiredFiles = [
    'next.config.ts',
    'src/app/layout.tsx',
    'src/app/page.tsx',
    'src/lib/stripe.ts',
    'public/robots.txt',
    'public/site.webmanifest',
  ];

  requiredFiles.forEach(file => {
    const filePath = path.join(__dirname, '..', file);
    allPassed &= check(
      fs.existsSync(filePath),
      `${file} exists`,
      `${file} not found`
    );
  });

  // 3. Check environment variables
  const envExample = path.join(__dirname, '../../.env.production.example');
  if (fs.existsSync(envExample)) {
    const envContent = fs.readFileSync(envExample, 'utf8');
    const requiredEnvVars = [
      'NEXT_PUBLIC_SUPABASE_URL',
      'NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY',
      'STRIPE_SECRET_KEY',
      'STRIPE_WEBHOOK_SECRET',
    ];

    requiredEnvVars.forEach(envVar => {
      const found = envContent.includes(envVar);
      if (found) {
        log(`✅ ${envVar} documented`, 'green');
      } else {
        warn(`${envVar} not in .env.production.example`);
        warnings.push(`Add ${envVar} to .env.production.example`);
      }
    });
  }

  // 4. Check build
  log('\n📦 Testing build...\n', 'blue');
  const { execSync } = require('child_process');
  
  try {
    execSync('npm run build', {
      cwd: path.join(__dirname, '..'),
      stdio: 'inherit',
    });
    log('✅ Build successful', 'green');
  } catch (error) {
    log('❌ Build failed', 'red');
    allPassed = false;
  }

  // 5. Check TypeScript
  log('\n🔍 Checking TypeScript...\n', 'blue');
  try {
    execSync('npm run type-check', {
      cwd: path.join(__dirname, '..'),
      stdio: 'pipe',
    });
    log('✅ No TypeScript errors', 'green');
  } catch (error) {
    warn('TypeScript errors found (non-blocking)');
    warnings.push('Fix TypeScript errors before deploy');
  }

  // 6. Security checks
  log('\n🔒 Security checks...\n', 'blue');
  
  const gitignore = path.join(__dirname, '../../.gitignore');
  if (fs.existsSync(gitignore)) {
    const gitignoreContent = fs.readFileSync(gitignore, 'utf8');
    check(
      gitignoreContent.includes('.env.local'),
      '.env.local in .gitignore',
      '.env.local NOT in .gitignore - SECURITY RISK!'
    );
    check(
      gitignoreContent.includes('node_modules'),
      'node_modules in .gitignore',
      'node_modules NOT in .gitignore'
    );
  }

  // Summary
  log('\n' + '='.repeat(50) + '\n', 'blue');
  
  if (allPassed && warnings.length === 0) {
    log('🎉 All checks passed! Ready to deploy!', 'green');
    log('\nNext steps:', 'blue');
    log('1. Push to GitHub: git push origin main');
    log('2. Deploy on Vercel: vercel --prod');
    log('3. Configure environment variables in Vercel');
    log('4. Set up Stripe webhooks');
    log('\nSee docs/DEPLOYMENT.md for full guide\n');
    process.exit(0);
  } else {
    if (!allPassed) {
      log('❌ Some critical checks failed', 'red');
    }
    
    if (warnings.length > 0) {
      log('\n⚠️  Warnings:', 'yellow');
      warnings.forEach(w => log(`   - ${w}`, 'yellow'));
    }
    
    log('\nFix issues before deploying\n', 'red');
    process.exit(1);
  }
}

main().catch(error => {
  log(`\n❌ Script error: ${error.message}`, 'red');
  process.exit(1);
});
