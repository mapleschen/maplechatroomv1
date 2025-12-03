import os
import shutil
from PyInstaller.__main__ import run
from PyInstaller.utils.hooks import collect_submodules

def build():
    print("Starting build process...")
    
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('MapleChatroom.spec'):
        os.remove('MapleChatroom.spec')

    # Collect all submodules for complex packages
    print("Collecting hidden imports for dns, eventlet, and engineio...")
    try:
        dns_hidden = collect_submodules('dns')
        eventlet_hidden = collect_submodules('eventlet')
        engineio_hidden = collect_submodules('engineio')
    except Exception as e:
        print(f"Warning during submodule collection: {e}")
        # Fallback or continue with what we have
        dns_hidden = dns_hidden if 'dns_hidden' in locals() else []
        eventlet_hidden = eventlet_hidden if 'eventlet_hidden' in locals() else []
        engineio_hidden = engineio_hidden if 'engineio_hidden' in locals() else []

    hidden_imports = []
    for module in dns_hidden + eventlet_hidden + engineio_hidden:
        hidden_imports.append(f'--hidden-import={module}')

    # PyInstaller arguments
    args = [
        'app.py',
        '--noconfirm',
        '--onefile',
        '--name=MapleChatroom',
        '--add-data=templates;templates',
        '--add-data=static;static',
    ] + hidden_imports
    
    print(f"Running PyInstaller with {len(hidden_imports)} hidden imports...")
    
    # Run PyInstaller directly from Python to avoid shell command length limits
    run(args)
    
    print("\nBuild complete!")
    print(f"Executable is located at: {os.path.abspath('dist/MapleChatroom.exe')}")

if __name__ == '__main__':
    build()
