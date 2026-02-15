const fs = require('fs');
const path = require('path');

const coursesDir = './apps/web/src/data/courses';
const lessonsDir = './apps/web/src/data';

// Patrones que indican contenido placeholder
const placeholderPatterns = [
  /Ver documentación completa/i,
  /Ver el curso completo/i,
  /Contenido en desarrollo/i,
  /TODO:/i,
  /FIXME:/i,
  /Lorem ipsum/i,
  /placeholder/i,
  /coming soon/i,
  /próximamente/i,
  /\[pendiente\]/i,
  /content here/i,
  /example content/i,
];

// Patrones de errores de sintaxis
const syntaxPatterns = [
  /\$\{[^}]+\}/g,  // Template literals no escapados en strings
  /<<<<<<</,       // Merge conflicts
  /=======/,
  />>>>>>>/,
];

function analyzeFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const issues = [];
  const fileName = path.basename(filePath);
  
  // Verificar placeholders
  for (const pattern of placeholderPatterns) {
    if (pattern.test(content)) {
      issues.push(`PLACEHOLDER: ${pattern.toString()}`);
    }
  }
  
  // Verificar sintaxis
  for (const pattern of syntaxPatterns) {
    if (pattern.test(content)) {
      issues.push(`SYNTAX: ${pattern.toString()}`);
    }
  }
  
  // Verificar tamaño (archivos muy pequeños pueden estar incompletos)
  const lines = content.split('\n').length;
  if (lines < 20) {
    issues.push(`SMALL: Solo ${lines} líneas`);
  }
  
  // Verificar export
  if (!content.includes('export')) {
    issues.push('NO_EXPORT: Falta export');
  }
  
  return { fileName, issues, lines };
}

function auditDirectory(dir, pattern) {
  const results = { total: 0, withIssues: 0, issues: [] };
  
  const files = fs.readdirSync(dir).filter(f => f.match(pattern));
  
  for (const file of files) {
    const filePath = path.join(dir, file);
    const analysis = analyzeFile(filePath);
    results.total++;
    
    if (analysis.issues.length > 0) {
      results.withIssues++;
      results.issues.push({
        file: analysis.fileName,
        lines: analysis.lines,
        problems: analysis.issues
      });
    }
  }
  
  return results;
}

console.log('╔══════════════════════════════════════════════════════════════╗');
console.log('║         AUDITORÍA COMPLETA DE CURSOS Y LECCIONES            ║');
console.log('╚══════════════════════════════════════════════════════════════╝\n');

// Auditar cursos
console.log('📚 AUDITANDO CURSOS...\n');
const coursesResult = auditDirectory(coursesDir, /\.ts$/);
console.log(`Total archivos de cursos: ${coursesResult.total}`);
console.log(`Con problemas: ${coursesResult.withIssues}`);

if (coursesResult.issues.length > 0) {
  console.log('\n⚠️  CURSOS CON PROBLEMAS:');
  for (const issue of coursesResult.issues) {
    console.log(`\n  📄 ${issue.file} (${issue.lines} líneas)`);
    for (const prob of issue.problems) {
      console.log(`     - ${prob}`);
    }
  }
}

// Auditar lecciones
console.log('\n\n📖 AUDITANDO LECCIONES...\n');
const lessonsResult = auditDirectory(lessonsDir, /^lessons-content-.*\.ts$/);
console.log(`Total archivos de lecciones: ${lessonsResult.total}`);
console.log(`Con problemas: ${lessonsResult.withIssues}`);

if (lessonsResult.issues.length > 0) {
  console.log('\n⚠️  LECCIONES CON PROBLEMAS:');
  for (const issue of lessonsResult.issues) {
    console.log(`\n  📄 ${issue.file} (${issue.lines} líneas)`);
    for (const prob of issue.problems) {
      console.log(`     - ${prob}`);
    }
  }
}

// Resumen
console.log('\n\n' + '═'.repeat(64));
console.log('RESUMEN FINAL');
console.log('═'.repeat(64));
console.log(`Cursos totales: ${coursesResult.total}`);
console.log(`Cursos OK: ${coursesResult.total - coursesResult.withIssues}`);
console.log(`Cursos con problemas: ${coursesResult.withIssues}`);
console.log(`Lecciones totales: ${lessonsResult.total}`);
console.log(`Lecciones OK: ${lessonsResult.total - lessonsResult.withIssues}`);
console.log(`Lecciones con problemas: ${lessonsResult.withIssues}`);

// Exportar lista de problemas para procesar
const allIssues = [...coursesResult.issues, ...lessonsResult.issues];
fs.writeFileSync('/tmp/audit-issues.json', JSON.stringify(allIssues, null, 2));
console.log('\nLista de problemas guardada en /tmp/audit-issues.json');
