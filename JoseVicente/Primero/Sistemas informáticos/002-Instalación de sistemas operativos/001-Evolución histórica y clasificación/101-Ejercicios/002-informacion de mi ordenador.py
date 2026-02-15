#!/usr/bin/env python3
# system_report.py
# Programa multiplataforma para generar un informe legible y JSON con info del sistema.
# Español: José Vicente style ;)
# Requiere Python 3.6+. Opcional: psutil para información más completa.

import platform
import sys
import os
import json
import shutil
import socket
import uuid
import subprocess
from datetime import datetime

# Intentar importar psutil; si no está, seguiremos con alternativas
try:
    import psutil
    HAS_PSUTIL = True
except Exception:
    HAS_PSUTIL = False

def now_iso():
    return datetime.now().isoformat(sep=' ', timespec='seconds')

def run_cmd(cmd):
    """Ejecuta un comando y devuelve (retcode, stdout)"""
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, text=True, timeout=8)
        return result.returncode, result.stdout.strip() or result.stderr.strip()
    except Exception as e:
        return -1, str(e)

def get_basic():
    info = {}
    info['timestamp'] = now_iso()
    info['platform_system'] = platform.system()
    info['platform_release'] = platform.release()
    info['platform_version'] = platform.version()
    info['architecture'] = platform.machine()
    info['platform'] = platform.platform()
    info['uname'] = None
    try:
        info['uname'] = ' '.join(platform.uname())
    except Exception:
        pass
    info['hostname'] = socket.gethostname()
    try:
        info['fqdn'] = socket.getfqdn()
    except Exception:
        info['fqdn'] = info['hostname']
    info['node_id'] = hex(uuid.getnode())
    info['python_version'] = sys.version.replace('\n', ' ')
    info['python_executable'] = sys.executable
    return info

def get_cpu():
    cpu = {}
    cpu['logical_cores'] = os.cpu_count()
    try:
        cpu['processor'] = platform.processor()
    except Exception:
        cpu['processor'] = None

    # intento de más detalle en Linux leyendo /proc/cpuinfo
    if platform.system().lower() == 'linux':
        try:
            with open('/proc/cpuinfo', 'r', encoding='utf-8', errors='ignore') as f:
                cpu['/proc/cpuinfo_sample'] = '\n'.join(f.readlines()[:30])
        except Exception:
            cpu['/proc/cpuinfo_sample'] = None

    if HAS_PSUTIL:
        try:
            cpu['physical_cores'] = psutil.cpu_count(logical=False)
            cpu['cpu_freq'] = psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            cpu['cpu_percent_sample'] = psutil.cpu_percent(interval=0.5)
        except Exception:
            pass
    return cpu

def get_memory():
    mem = {}
    if HAS_PSUTIL:
        try:
            vm = psutil.virtual_memory()._asdict()
            sm = psutil.swap_memory()._asdict()
            mem['virtual_memory'] = vm
            mem['swap_memory'] = sm
        except Exception:
            pass
    else:
        # fallback: solo memoria disponible via os.sysconf (Unix)
        try:
            if hasattr(os, 'sysconf'):
                sc_pages = os.sysconf('SC_PHYS_PAGES')
                sc_page_size = os.sysconf('SC_PAGE_SIZE')
                total = sc_pages * sc_page_size
                mem['total_bytes_estimate'] = total
        except Exception:
            pass
    return mem

def get_disks():
    disks = {}
    try:
        disks['cwd'] = os.getcwd()
    except Exception:
        disks['cwd'] = None

    # uso shutil.disk_usage para raíz y cwd
    try:
        root = os.path.abspath(os.sep)
        disks['root_usage'] = dict(zip(['total','used','free'], shutil.disk_usage(root)))
    except Exception:
        disks['root_usage'] = None

    try:
        disks['cwd_usage'] = dict(zip(['total','used','free'], shutil.disk_usage(os.getcwd())))
    except Exception:
        disks['cwd_usage'] = None

    if HAS_PSUTIL:
        try:
            parts = []
            for p in psutil.disk_partitions(all=False):
                try:
                    usage = psutil.disk_usage(p.mountpoint)._asdict()
                except Exception:
                    usage = None
                parts.append({
                    'device': p.device,
                    'mountpoint': p.mountpoint,
                    'fstype': p.fstype,
                    'opts': p.opts,
                    'usage': usage
                })
            disks['partitions'] = parts
        except Exception:
            pass
    return disks

def get_network():
    net = {}
    try:
        net['ip_addresses'] = socket.gethostbyname_ex(socket.gethostname())[2]
    except Exception:
        net['ip_addresses'] = []
    # obtener interfaces con psutil si está
    if HAS_PSUTIL:
        try:
            addrs = {}
            for ifname, snic in psutil.net_if_addrs().items():
                addrs[ifname] = []
                for s in snic:
                    addrs[ifname].append({
                        'family': str(s.family),
                        'address': s.address,
                        'netmask': s.netmask,
                        'broadcast': s.broadcast
                    })
            net['interfaces'] = addrs
            net['net_io_counters'] = psutil.net_io_counters()._asdict()
        except Exception:
            pass
    # público (simple): consulta a resolver hostname de google (no hace petición HTTP)
    try:
        # intento resolver A record de example.com (no salir a web); si se permite DNS, devolvemos la IP
        ip = socket.gethostbyname('example.com')
        net['example_com_resolves_to'] = ip
    except Exception:
        net['example_com_resolves_to'] = None
    return net

def get_users_processes():
    info = {}
    if HAS_PSUTIL:
        try:
            info['logged_users'] = [u._asdict() for u in psutil.users()]
        except Exception:
            info['logged_users'] = None
        try:
            procs = []
            for p in psutil.process_iter(['pid','name','username','cpu_percent','memory_percent']):
                try:
                    procs.append(p.info)
                except Exception:
                    pass
            # ordenar por uso CPU decendente y limitar
            procs_sorted = sorted(procs, key=lambda x: x.get('cpu_percent',0) or 0, reverse=True)[:20]
            info['top_processes_by_cpu'] = procs_sorted
        except Exception:
            info['top_processes_by_cpu'] = None
    else:
        # fallback, mostrar procesos via 'tasklist' (Windows) o 'ps -eo' (Unix)
        try:
            if platform.system().lower().startswith('win'):
                rc, out = run_cmd(['tasklist'])
                info['process_list_raw'] = out[:4000]
            else:
                rc, out = run_cmd(['ps', '-eo', 'pid,pcpu,pmem,user,args', '--sort=-pcpu'])
                info['process_list_raw'] = out.splitlines()[:25]
        except Exception:
            info['process_list_raw'] = None
    return info

def get_python_env():
    env = {}
    env['executable'] = sys.executable
    env['version'] = sys.version
    env['path'] = sys.path
    try:
        import pkgutil
        pkgs = sorted([m.name for m in pkgutil.iter_modules()])
        env['installed_modules_sample'] = pkgs[:60]  # no listar todo para no saturar
    except Exception:
        env['installed_modules_sample'] = None
    return env

def detect_gpu():
    gpu = {}
    # Intento nvidia-smi
    try:
        rc, out = run_cmd(['nvidia-smi', '--query-gpu=name,memory.total,driver_version', '--format=csv,noheader'])
        if rc == 0 and out:
            lines = out.splitlines()
            gpu['nvidia'] = [l.strip() for l in lines]
    except Exception:
        pass
    # CUDA visible env
    try:
        gpu['CUDA_VISIBLE_DEVICES'] = os.environ.get('CUDA_VISIBLE_DEVICES')
    except Exception:
        pass
    # intento rocm (rocm-smi)
    try:
        rc, out = run_cmd(['rocm-smi'])
        if rc == 0:
            gpu['rocm-smi'] = out.splitlines()[:8]
    except Exception:
        pass
    if not gpu:
        gpu['note'] = 'No se detectó GPU con nvidia-smi/rocm-smi. Puede que no haya GPU dedicada o que no estén instaladas herramientas.'
    return gpu

def generate_report_text(data):
    # Construimos un informe legible y conciso
    lines = []
    lines.append("INFORME DEL SISTEMA".center(78, '='))
    lines.append(f"Generado: {data['basic'].get('timestamp')}")
    lines.append("")
    # Básico
    b = data['basic']
    lines.append("1) Información Básica")
    lines.append(f"   - Sistema: {b.get('platform_system')} {b.get('platform_release')} ({b.get('architecture')})")
    lines.append(f"   - Plataforma: {b.get('platform')}")
    lines.append(f"   - Hostname: {b.get('hostname')} (FQDN: {b.get('fqdn')})")
    lines.append(f"   - Nodo ID (MAC): {b.get('node_id')}")
    lines.append(f"   - Ejecutable Python: {b.get('python_executable')}")
    lines.append("")
    # CPU
    lines.append("2) CPU")
    cpu = data.get('cpu', {})
    lines.append(f"   - Procesador (platform): {cpu.get('processor')}")
    lines.append(f"   - Cores (logical): {cpu.get('logical_cores')}, (physical if available): {cpu.get('physical_cores') if cpu.get('physical_cores') is not None else 'N/D'}")
    if cpu.get('cpu_freq'):
        fq = cpu['cpu_freq']
        lines.append(f"   - Frecuencia (MHz): current={fq.get('current')}, min={fq.get('min')}, max={fq.get('max')}")
    if cpu.get('cpu_percent_sample') is not None:
        lines.append(f"   - Uso de CPU (muestra breve): {cpu.get('cpu_percent_sample')}%")
    lines.append("")
    # Memoria
    lines.append("3) Memoria")
    mem = data.get('memory', {})
    if mem.get('virtual_memory'):
        vm = mem['virtual_memory']
        lines.append(f"   - RAM total: {vm.get('total')} bytes, disponible: {vm.get('available')} bytes, usado: {vm.get('used')} bytes ({vm.get('percent')}%)")
    elif mem.get('total_bytes_estimate'):
        lines.append(f"   - RAM total (estimada): {mem.get('total_bytes_estimate')} bytes")
    lines.append("")
    # Discos
    lines.append("4) Discos")
    d = data.get('disks', {})
    if d.get('root_usage'):
        ru = d['root_usage']
        lines.append(f"   - Raíz total={ru['total']} used={ru['used']} free={ru['free']}")
    if d.get('partitions'):
        lines.append("   - Particiones montadas (muestra):")
        for p in d['partitions'][:8]:
            lines.append(f"     * {p['mountpoint']} ({p['device']}) tipo={p['fstype']} uso={p['usage']}")
    lines.append("")
    # Red
    lines.append("5) Red")
    net = data.get('network', {})
    lines.append(f"   - IPs detectadas: {', '.join(net.get('ip_addresses') or [])}")
    if net.get('interfaces'):
        lines.append("   - Interfaces (muestra):")
        for ifn, addrs in list(net['interfaces'].items())[:6]:
            lines.append(f"     * {ifn}: {len(addrs)} direcciones")
    lines.append("")
    # Usuarios y procesos
    lines.append("6) Usuarios & procesos")
    up = data.get('users_processes', {})
    if up.get('logged_users'):
        lines.append(f"   - Usuarios logueados: {len(up.get('logged_users'))}")
    if up.get('top_processes_by_cpu'):
        lines.append("   - Procesos top por CPU:")
        for p in up['top_processes_by_cpu'][:8]:
            lines.append(f"     PID {p.get('pid')} {p.get('name')} user={p.get('username')} cpu%={p.get('cpu_percent')} mem%={p.get('memory_percent')}")
    lines.append("")
    # GPU
    lines.append("7) GPU")
    gpu = data.get('gpu', {})
    if 'nvidia' in gpu:
        lines.append("   - GPUs NVIDIA:")
        for g in gpu['nvidia']:
            lines.append(f"     {g}")
    else:
        lines.append(f"   - {gpu.get('note','No info')}")
    lines.append("")
    # Python env
    lines.append("8) Entorno Python")
    py = data.get('python_env', {})
    lines.append(f"   - Versión: {py.get('version')}")
    if py.get('installed_modules_sample'):
        lines.append(f"   - Módulos (muestra): {', '.join(py['installed_modules_sample'][:12])}")
    lines.append("")
    lines.append("="*78)
    return '\n'.join(lines)

def main(save_text="system_report.txt", save_json="system_report.json"):
    data = {}
    data['basic'] = get_basic()
    data['cpu'] = get_cpu()
    data['memory'] = get_memory()
    data['disks'] = get_disks()
    data['network'] = get_network()
    data['users_processes'] = get_users_processes()
    data['python_env'] = get_python_env()
    data['gpu'] = detect_gpu()

    # Generar texto legible
    report_text = generate_report_text(data)

    # Guardar archivos
    try:
        with open(save_text, 'w', encoding='utf-8') as f:
            f.write(report_text)
    except Exception as e:
        print("Error guardando archivo de texto:", e)

    try:
        with open(save_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Error guardando JSON:", e)

    # Mostrar por pantalla encabezado y ruta de archivos guardados
    print("="*60)
    print("INFORME GENERADO")
    print(f"  - Texto legible: {os.path.abspath(save_text)}")
    print(f"  - JSON:         {os.path.abspath(save_json)}")
    print("="*60)
    print("\nResumen (primeras líneas):\n")
    for ln in report_text.splitlines()[:40]:
        print(ln)
    print("\nSi deseas más detalle instala 'psutil' con:\n    pip install psutil\n")

if __name__ == '__main__':
    main()

