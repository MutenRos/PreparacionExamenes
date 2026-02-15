const fs = require('fs');
const issues = JSON.parse(fs.readFileSync('/tmp/audit-issues.json', 'utf8'));

// Categorizar
const categories = {
  loremIpsum: [],        // Archivos con Lorem ipsum (contenido vacío)
  syntaxErrors: [],      // Errores de sintaxis (${}, merge conflicts)
  todoPlaceholder: [],   // TODOs en ejercicios (normal en cursos)
  mergeConflicts: [],    // Conflictos de merge
  small: [],             // Archivos pequeños
};

for (const item of issues) {
  for (const prob of item.problems) {
    if (prob.includes('Lorem ipsum')) {
      categories.loremIpsum.push(item.file);
    } else if (prob.includes('<<<') || prob.includes('===') || prob.includes('>>>')) {
      categories.mergeConflicts.push(item.file);
    } else if (prob.includes('SYNTAX') && prob.includes('$')) {
      categories.syntaxErrors.push(item.file);
    } else if (prob.includes('SMALL')) {
      categories.small.push(item.file);
    }
  }
}

// Deduplicar
for (const key in categories) {
  categories[key] = [...new Set(categories[key])];
}

console.log('╔══════════════════════════════════════════════════════════════╗');
console.log('║              CATEGORIZACIÓN DE PROBLEMAS                     ║');
console.log('╚══════════════════════════════════════════════════════════════╝\n');

console.log(`🔴 CRÍTICO - Lorem Ipsum (cursos vacíos): ${categories.loremIpsum.length}`);
for (const f of categories.loremIpsum.slice(0, 10)) console.log(`   - ${f}`);
if (categories.loremIpsum.length > 10) console.log(`   ... y ${categories.loremIpsum.length - 10} más`);

console.log(`\n🔴 CRÍTICO - Merge conflicts: ${categories.mergeConflicts.length}`);
for (const f of categories.mergeConflicts) console.log(`   - ${f}`);

console.log(`\n🟡 MEDIO - Errores sintaxis \${}: ${categories.syntaxErrors.length}`);
for (const f of categories.syntaxErrors.slice(0, 10)) console.log(`   - ${f}`);
if (categories.syntaxErrors.length > 10) console.log(`   ... y ${categories.syntaxErrors.length - 10} más`);

console.log(`\n🟡 MEDIO - Archivos pequeños: ${categories.small.length}`);
for (const f of categories.small) console.log(`   - ${f}`);

// Exportar lista para procesar
fs.writeFileSync('/tmp/lorem-ipsum-files.json', JSON.stringify(categories.loremIpsum, null, 2));
fs.writeFileSync('/tmp/syntax-files.json', JSON.stringify(categories.syntaxErrors, null, 2));
fs.writeFileSync('/tmp/merge-conflicts.json', JSON.stringify(categories.mergeConflicts, null, 2));

console.log('\n\nArchivos exportados para procesamiento.');
