#!/usr/bin/env python3
"""
SENTINEL - VPS Readiness Check
Verifica se todos os componentes necessários para deployment VPS estão prontos.
"""
import sys
from pathlib import Path
from typing import List, Tuple


class Color:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def check_file_exists(file_path: str, description: str) -> bool:
    """Verifica se arquivo existe"""
    exists = Path(file_path).exists()
    status = f"{Color.GREEN}OK{Color.END}" if exists else f"{Color.RED}FAIL{Color.END}"
    print(f"[{status}] {description}: {file_path}")
    return exists


def check_directory_exists(dir_path: str, description: str) -> bool:
    """Verifica se diretório existe"""
    exists = Path(dir_path).is_dir()
    status = f"{Color.GREEN}OK{Color.END}" if exists else f"{Color.RED}FAIL{Color.END}"
    print(f"[{status}] {description}: {dir_path}")
    return exists


def main():
    """Executa todas as verificações"""
    print(f"\n{Color.BOLD}{'='*60}{Color.END}")
    print(f"{Color.BOLD}SENTINEL - VPS Deployment Readiness Check{Color.END}")
    print(f"{Color.BOLD}{'='*60}{Color.END}\n")

    checks: List[Tuple[bool, str]] = []

    # === Core Application ===
    print(f"{Color.BLUE}{Color.BOLD}[1] Core Application Files{Color.END}")
    checks.append((check_file_exists("app/main.py", "Main application"), "Critical"))
    checks.append((check_file_exists("app/config.py", "Configuration"), "Critical"))
    checks.append((check_file_exists("requirements.txt", "Dependencies"), "Critical"))
    checks.append((check_file_exists(".env.example", "Environment example"), "Important"))
    print()

    # === Security Components ===
    print(f"{Color.BLUE}{Color.BOLD}[2] Security Components{Color.END}")
    checks.append((check_file_exists("app/core/security.py", "Security module"), "Critical"))
    checks.append((check_file_exists("app/middleware/auth.py", "Auth middleware"), "Critical"))
    checks.append((check_file_exists("app/middleware/security_headers.py", "Security headers"), "Critical"))
    checks.append((check_file_exists("app/api/v1/auth.py", "Auth endpoints"), "Critical"))
    checks.append((check_file_exists("app/core/environments.py", "Environment configs"), "Important"))
    print()

    # === Monitoring & Health ===
    print(f"{Color.BLUE}{Color.BOLD}[3] Monitoring & Health Checks{Color.END}")
    checks.append((check_file_exists("app/api/v1/health.py", "Health check endpoints"), "Critical"))
    checks.append((check_file_exists("app/core/backup.py", "Backup system"), "Critical"))
    print()

    # === Docker Configuration ===
    print(f"{Color.BLUE}{Color.BOLD}[4] Docker Configuration{Color.END}")
    checks.append((check_file_exists("Dockerfile", "Dockerfile"), "Important"))
    checks.append((check_file_exists("docker-compose.yml", "Docker Compose"), "Important"))
    checks.append((check_file_exists(".dockerignore", "Docker ignore"), "Important"))
    print()

    # === Nginx Configuration ===
    print(f"{Color.BLUE}{Color.BOLD}[5] Nginx Configuration{Color.END}")
    checks.append((check_directory_exists("deployment/nginx", "Nginx directory"), "Critical"))
    checks.append((check_file_exists("deployment/nginx/nginx.conf", "Nginx config"), "Critical"))
    print()

    # === Systemd Configuration ===
    print(f"{Color.BLUE}{Color.BOLD}[6] Systemd Service{Color.END}")
    checks.append((check_directory_exists("deployment/systemd", "Systemd directory"), "Critical"))
    checks.append((check_file_exists("deployment/systemd/sentinel.service", "Service file"), "Critical"))
    print()

    # === Fail2ban Configuration ===
    print(f"{Color.BLUE}{Color.BOLD}[7] Fail2ban Configuration{Color.END}")
    checks.append((check_directory_exists("deployment/fail2ban", "Fail2ban directory"), "Critical"))
    checks.append((check_file_exists("deployment/fail2ban/sentinel.conf", "Fail2ban filter"), "Critical"))
    checks.append((check_file_exists("deployment/fail2ban/jail.local", "Fail2ban jail"), "Critical"))
    print()

    # === Deployment Scripts ===
    print(f"{Color.BLUE}{Color.BOLD}[8] Deployment Scripts{Color.END}")
    checks.append((check_directory_exists("deployment/scripts", "Scripts directory"), "Critical"))
    checks.append((check_file_exists("deployment/scripts/deploy_vps.sh", "VPS deployment script"), "Critical"))
    checks.append((check_file_exists("deployment/scripts/setup_ssl.sh", "SSL setup script"), "Critical"))
    checks.append((check_file_exists("deployment/scripts/test_deployment.sh", "Test script"), "Important"))
    print()

    # === Documentation ===
    print(f"{Color.BLUE}{Color.BOLD}[9] Documentation{Color.END}")
    checks.append((check_file_exists("DEPLOYMENT_VPS.md", "VPS deployment guide"), "Critical"))
    checks.append((check_file_exists("DOCKER_DEPLOYMENT.md", "Docker deployment guide"), "Important"))
    checks.append((check_file_exists("SEGURANCA_FASE2_VPS.md", "Security Phase 2 docs"), "Important"))
    checks.append((check_file_exists("SEGURANCA_IMPLEMENTADA.md", "Security Phase 1 docs"), "Important"))
    print()

    # === Database Scripts ===
    print(f"{Color.BLUE}{Color.BOLD}[10] Database Scripts{Color.END}")
    checks.append((check_file_exists("scripts/create_users_table.py", "Create users table"), "Critical"))
    checks.append((check_file_exists("scripts/create_default_admin.py", "Create admin user"), "Critical"))
    print()

    # === Summary ===
    print(f"\n{Color.BOLD}{'='*60}{Color.END}")
    print(f"{Color.BOLD}SUMMARY{Color.END}")
    print(f"{Color.BOLD}{'='*60}{Color.END}\n")

    critical_checks = [c for c in checks if c[1] == "Critical"]
    important_checks = [c for c in checks if c[1] == "Important"]

    critical_passed = sum(1 for c in critical_checks if c[0])
    critical_total = len(critical_checks)

    important_passed = sum(1 for c in important_checks if c[0])
    important_total = len(important_checks)

    total_passed = critical_passed + important_passed
    total_checks = critical_total + important_total

    print(f"Critical checks: {critical_passed}/{critical_total}")
    print(f"Important checks: {important_passed}/{important_total}")
    print(f"Total: {total_passed}/{total_checks}")
    print()

    # Calculate readiness percentage
    readiness = (total_passed / total_checks * 100) if total_checks > 0 else 0

    if critical_passed == critical_total:
        print(f"{Color.GREEN}{Color.BOLD}>> ALL CRITICAL COMPONENTS READY!{Color.END}")
        print(f"{Color.GREEN}Readiness: {readiness:.1f}%{Color.END}")
        print()

        if important_passed < important_total:
            print(f"{Color.YELLOW}Note: Some optional components are missing but deployment can proceed.{Color.END}")
            print()

        print(f"{Color.BOLD}Next Steps:{Color.END}")
        print("1. Configure your .env file (copy from .env.example)")
        print("2. Generate a strong SECRET_KEY")
        print("3. Update CORS_ORIGINS with your domain")
        print("4. Choose deployment method:")
        print("   - Traditional: sudo ./deployment/scripts/deploy_vps.sh")
        print("   - Docker: docker compose up -d")
        print("5. Configure SSL with: ./deployment/scripts/setup_ssl.sh")
        print("6. Test deployment with: ./deployment/scripts/test_deployment.sh")
        print()

        print(f"{Color.GREEN}{Color.BOLD}SUCCESS: Your SENTINEL is PRODUCTION-READY!{Color.END}\n")
        return 0

    else:
        print(f"{Color.RED}{Color.BOLD}>> CRITICAL COMPONENTS MISSING!{Color.END}")
        print(f"{Color.RED}Readiness: {readiness:.1f}%{Color.END}")
        print()
        print(f"{Color.YELLOW}Missing critical files must be created before deployment.{Color.END}")
        print(f"{Color.YELLOW}Please check the implementation or re-run the setup.{Color.END}")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
