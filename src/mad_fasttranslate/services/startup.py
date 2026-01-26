"""StartUp Service"""
from argostranslate import translate, package
from argostranslate.package import get_installed_packages
from ..config import REQUIRED_TRANSLATIONS
import os

class StartupService:
    
    @staticmethod
    def install_missing_models() -> None:
        StartupService._log_package_info()
        StartupService._update_package_index()
        
        installed_pairs = StartupService._get_installed_pairs()
        available_packages = package.get_available_packages()
        
        StartupService._install_required_models(installed_pairs, available_packages)
         
    @staticmethod
    def _log_package_info() -> None:
        installed_package = get_installed_packages()
        print(f"[Startup Service] Installed Packages : {len(installed_package)}")
        
        if not installed_package:
            print("[Startup Service] No Packages Installed.")
            return
        
        first_pkg = installed_package[0]
        pkg_path  = first_pkg.package_path if hasattr(first_pkg, 'package_path') else None
        if pkg_path:
            print(f"[Startup Service] Packages Location : {os.path.dirname(pkg_path)}")
       
     
    @staticmethod
    def _update_package_index() -> None:
         print("[Startup Service] Updating Package Index...")
         package.update_package_index()     
    
    
    @staticmethod
    def _get_installed_pairs() -> set:
        installed_packages = get_installed_packages()
        installed_pairs = set()
        
        for pkg in installed_packages:
            installed_pairs.add((pkg.from_code, pkg.to_code))
        return installed_pairs
    
    @staticmethod
    def _install_required_models(installed_pairs: set, available_packages: list) -> None:
         for from_code, to_code in REQUIRED_TRANSLATIONS:
             if(from_code, to_code) in installed_pairs:
                 print(f"[Startup Service] Models already installed: {from_code} -> {to_code}")
                 continue
             
             pkg = next((p for p in available_packages if p.from_code == from_code and p.to_code == to_code), None)
             
             if not pkg:
                 print(f"[Startup Service] No package found for: {from_code} -> {to_code}")
                 continue
             
             StartupService._install_package(pkg, from_code, to_code)
    @staticmethod
    def _install_package(pkg, from_code, to_code) -> None: 
        try:
            pkg.install()
            print(f"[Startup Service] Successfully Install Package : {from_code} -> {to_code}")
        except Exception as e:
            print(f"[Startup Service] Failed Install Package : {from_code} -> {to_code} Error: {str(e)}")
            