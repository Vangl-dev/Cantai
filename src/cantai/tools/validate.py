#!/usr/bin/env python3
"""
Suíte de Validação do Cantai2

Este script executa todas as verificações do projeto.
Execute com: python -m cantai.tools.validate

IMPORTANTE: Este script NÃO altera nenhum arquivo.
Ele apenas identifica e relata problemas.
"""

import json
import time
from pathlib import Path
from typing import Any


class ValidationResult:
    """Resultado de uma validação."""
    
    def __init__(self, name: str):
        self.name = name
        self.errors = []
        self.warnings = []
        self.passed = True
    
    def error(self, message: str):
        self.errors.append(message)
        self.passed = False
    
    def warning(self, message: str):
        self.warnings.append(message)
    
    @property
    def status(self) -> str:
        return "OK" if self.passed else "ERRO"


class ValidationSuite:
    """Suíte de validação do Cantai2."""
    
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.data_dir = project_dir / 'data'
        self.results = {}
        self.start_time = None
        self.end_time = None
    
    def run(self) -> dict:
        """Executa todas as validações."""
        self.start_time = time.time()
        
        print("=" * 60)
        print("SUÍTE DE VALIDAÇÃO DO CANTAI2")
        print("=" * 60)
        
        # Validate required files
        self.validate_required_files()
        
        # Validate CTP
        self.validate_ctp()
        
        # Validate HCC
        self.validate_hcc()
        
        # Validate SH
        self.validate_sh()
        
        # Validate equivalences
        self.validate_equivalences()
        
        # Validate canonical topics
        self.validate_canonical_topics()
        
        self.end_time = time.time()
        
        return self.generate_report()
    
    def validate_required_files(self):
        """Valida se todos os arquivos obrigatórios existem."""
        result = ValidationResult("Arquivos Obrigatórios")
        
        required_files = [
            'data/output/cantai.json',
            'data/output/hcc.json',
            'data/output/sh.json',
            'data/hymn_equivalences.json',
            'data/canonical_topics.json',
        ]
        
        for file_path in required_files:
            full_path = self.project_dir / file_path
            if not full_path.exists():
                result.error(f"Arquivo ausente: {file_path}")
        
        self.results['required_files'] = result
        self.print_result(result)
    
    def validate_ctp(self):
        """Valida o hinário CTP."""
        result = ValidationResult("CTP")
        
        ctp_path = self.data_dir / 'output' / 'cantai.json'
        if not ctp_path.exists():
            result.error("Arquivo CTP não encontrado")
            self.results['ctp'] = result
            self.print_result(result)
            return
        
        try:
            with open(ctp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            result.error(f"JSON inválido: {e}")
            self.results['ctp'] = result
            self.print_result(result)
            return
        
        hymns = data.get('hymns', [])
        
        # Check for duplicates
        numbers = [h['number'] for h in hymns]
        duplicates = [n for n in numbers if numbers.count(n) > 1]
        if duplicates:
            result.warning(f"Números duplicados: {set(duplicates)}")
        
        # Check for empty fields
        for h in hymns:
            if not h.get('title'):
                result.error(f"CTP-{h['number']}: título vazio")
            if not h.get('first_line'):
                result.warning(f"CTP-{h['number']}: primeira linha ausente")
            if not h.get('lyrics'):
                result.error(f"CTP-{h['number']}: letra vazia")
        
        # Check total count
        expected_count = 504
        if len(hymns) != expected_count:
            result.warning(f"Quantidade esperada: {expected_count}, encontrada: {len(hymns)}")
        
        self.results['ctp'] = result
        self.print_result(result)
    
    def validate_hcc(self):
        """Valida o hinário HCC."""
        result = ValidationResult("HCC")
        
        hcc_path = self.data_dir / 'output' / 'hcc.json'
        if not hcc_path.exists():
            result.error("Arquivo HCC não encontrado")
            self.results['hcc'] = result
            self.print_result(result)
            return
        
        try:
            with open(hcc_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            result.error(f"JSON inválido: {e}")
            self.results['hcc'] = result
            self.print_result(result)
            return
        
        hymns = data.get('hymns', [])
        
        # Check for duplicates
        numbers = [h['number'] for h in hymns]
        duplicates = [n for n in numbers if numbers.count(n) > 1]
        if duplicates:
            result.error(f"Números duplicados: {set(duplicates)}")
        
        # Check for empty fields
        for h in hymns:
            if not h.get('title'):
                result.error(f"HCC-{h['number']}: título vazio")
            if not h.get('first_line'):
                result.warning(f"HCC-{h['number']}: primeira linha ausente")
            if not h.get('lyrics'):
                result.error(f"HCC-{h['number']}: letra vazia")
        
        # Check total count
        expected_count = 609
        if len(hymns) != expected_count:
            result.warning(f"Quantidade esperada: {expected_count}, encontrada: {len(hymns)}")
        
        self.results['hcc'] = result
        self.print_result(result)
    
    def validate_sh(self):
        """Valida o hinário SH."""
        result = ValidationResult("SH")
        
        sh_path = self.data_dir / 'output' / 'sh.json'
        if not sh_path.exists():
            result.error("Arquivo SH não encontrado")
            self.results['sh'] = result
            self.print_result(result)
            return
        
        try:
            with open(sh_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            result.error(f"JSON inválido: {e}")
            self.results['sh'] = result
            self.print_result(result)
            return
        
        hymns = data.get('hymns', [])
        
        # Check for duplicates
        numbers = [h['number'] for h in hymns]
        duplicates = [n for n in numbers if numbers.count(n) > 1]
        if duplicates:
            result.error(f"Números duplicados: {set(duplicates)}")
        
        # Check for empty fields
        for h in hymns:
            if not h.get('title'):
                result.error(f"SH-{h['number']}: título vazio")
            if not h.get('first_line'):
                result.warning(f"SH-{h['number']}: primeira linha ausente")
            if not h.get('lyrics'):
                result.error(f"SH-{h['number']}: letra vazia")
        
        # Check total count
        expected_count = 621
        if len(hymns) != expected_count:
            result.warning(f"Quantidade esperada: {expected_count}, encontrada: {len(hymns)}")
        
        self.results['sh'] = result
        self.print_result(result)
    
    def validate_equivalences(self):
        """Valida o mapa de equivalências."""
        result = ValidationResult("Equivalências")
        
        equiv_path = self.data_dir / 'hymn_equivalences.json'
        if not equiv_path.exists():
            result.error("Arquivo de equivalências não encontrado")
            self.results['equivalences'] = result
            self.print_result(result)
            return
        
        try:
            with open(equiv_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            result.error(f"JSON inválido: {e}")
            self.results['equivalences'] = result
            self.print_result(result)
            return
        
        # Load hymnals for cross-reference
        ctp_path = self.data_dir / 'output' / 'cantai.json'
        hcc_path = self.data_dir / 'output' / 'hcc.json'
        sh_path = self.data_dir / 'output' / 'sh.json'
        
        ctp_hymns = set()
        hcc_hymns = set()
        sh_hymns = set()
        
        if ctp_path.exists():
            with open(ctp_path, 'r', encoding='utf-8') as f:
                ctp_hymns = {f"CTP-{h['number']}" for h in json.load(f)['hymns']}
        
        if hcc_path.exists():
            with open(hcc_path, 'r', encoding='utf-8') as f:
                hcc_hymns = {f"HCC-{h['number']}" for h in json.load(f)['hymns']}
        
        if sh_path.exists():
            with open(sh_path, 'r', encoding='utf-8') as f:
                sh_hymns = {f"SH-{h['number']}" for h in json.load(f)['hymns']}
        
        all_hymns = ctp_hymns | hcc_hymns | sh_hymns
        
        # Check each equivalence
        for key, value in data.items():
            # Check if main hymn exists
            if key not in all_hymns:
                result.error(f"Equivalência aponta para hino inexistente: {key}")
            
            # Check equivalents
            if value.get('equivalents'):
                for eq in value['equivalents']:
                    eq_id = eq.get('id')
                    if eq_id and eq_id not in all_hymns:
                        result.error(f"Equivalente inexistente: {eq_id} (de {key})")
        
        self.results['equivalences'] = result
        self.print_result(result)
    
    def validate_canonical_topics(self):
        """Valida o registro canônico de temas."""
        result = ValidationResult("Registro Canônico de Temas")
        
        rct_path = self.data_dir / 'canonical_topics.json'
        if not rct_path.exists():
            result.error("Arquivo de temas canônicos não encontrado")
            self.results['rct'] = result
            self.print_result(result)
            return
        
        try:
            with open(rct_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            result.error(f"JSON inválido: {e}")
            self.results['rct'] = result
            self.print_result(result)
            return
        
        # Check structure
        for key, value in data.items():
            if not isinstance(value, dict):
                result.error(f"Entrada inválida: {key}")
            elif 'ctp' not in value or 'hcc' not in value:
                result.warning(f"Entrada incompleta: {key}")
        
        self.results['rct'] = result
        self.print_result(result)
    
    def print_result(self, result: ValidationResult):
        """Imprime o resultado de uma validação."""
        status = result.status
        errors = len(result.errors)
        warnings = len(result.warnings)
        
        if status == "OK":
            print(f"  {result.name:20} OK")
        else:
            print(f"  {result.name:20} ERRO ({errors} erros, {warnings} avisos)")
    
    def generate_report(self) -> dict:
        """Gera o relatório final."""
        elapsed = self.end_time - self.start_time
        
        total_errors = sum(len(r.errors) for r in self.results.values())
        total_warnings = sum(len(r.warnings) for r in self.results.values())
        
        all_passed = all(r.passed for r in self.results.values())
        
        # Generate report
        report = {
            'status': 'OK' if all_passed else 'ERRO',
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'elapsed_time': elapsed,
            'results': {name: {
                'status': r.status,
                'errors': r.errors,
                'warnings': r.warnings
            } for name, r in self.results.items()}
        }
        
        # Print summary
        print("\n" + "=" * 60)
        print("RESUMO DA VALIDAÇÃO")
        print("=" * 60)
        
        for name, r in self.results.items():
            status = "OK" if r.passed else "ERRO"
            print(f"  {name:20} {status}")
        
        print("\n" + "-" * 60)
        print(f"  Erros:   {total_errors}")
        print(f"  Avisos:  {total_warnings}")
        print(f"  Tempo:   {elapsed:.2f}s")
        print("-" * 60)
        
        if all_passed:
            print("\n  ✅ Sistema íntegro")
        else:
            print("\n  ❌ Problemas encontrados")
        
        print("=" * 60)
        
        # Save report
        self.save_report(report)
        
        return report
    
    def save_report(self, report: dict):
        """Salva o relatório em markdown."""
        reports_dir = self.project_dir / 'reports'
        reports_dir.mkdir(exist_ok=True)
        
        output_path = reports_dir / 'system_validation.md'
        
        lines = []
        lines.append("# Relatório de Validação do Sistema")
        lines.append("")
        lines.append(f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Tempo de execução: {report['elapsed_time']:.2f}s")
        lines.append("")
        lines.append("## Resumo Geral")
        lines.append("")
        lines.append("```")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("")
        lines.append("STATUS GERAL")
        lines.append("")
        
        for name, r in self.results.items():
            status = "OK" if r.passed else "ERRO"
            lines.append(f"{name:15} {status}")
        
        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("")
        lines.append(f"ERROS     {report['total_errors']}")
        lines.append(f"AVISOS    {report['total_warnings']}")
        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("")
        
        if report['status'] == 'OK':
            lines.append("RESULTADO")
            lines.append("")
            lines.append("✅ Sistema íntegro")
        else:
            lines.append("RESULTADO")
            lines.append("")
            lines.append("❌ Problemas encontrados")
        
        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("```")
        lines.append("")
        
        # Detailed results
        lines.append("## Detalhes")
        lines.append("")
        
        for name, r in self.results.items():
            lines.append(f"### {name}")
            lines.append("")
            
            if r.errors:
                lines.append("**Erros:**")
                for e in r.errors:
                    lines.append(f"- {e}")
                lines.append("")
            
            if r.warnings:
                lines.append("**Avisos:**")
                for w in r.warnings:
                    lines.append(f"- {w}")
                lines.append("")
            
            if not r.errors and not r.warnings:
                lines.append("Nenhum problema encontrado.")
                lines.append("")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"\nRelatório salvo em: {output_path}")


def main():
    """Função principal."""
    project_dir = Path(__file__).parent.parent.parent.parent
    suite = ValidationSuite(project_dir)
    suite.run()


if __name__ == '__main__':
    main()
