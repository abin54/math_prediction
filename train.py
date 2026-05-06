import subprocess
import sys
import os

def check_and_install(package, import_name=None):
    if import_name is None:
        import_name = package
    try:
        __import__(import_name)
        print(f"  [OK] {package} is already installed.")
    except ImportError:
        print(f"  [WAIT] Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def run_script(script_path):
    print(f"\n>>> Executing {script_path}...")
    subprocess.check_call([sys.executable, script_path])

def main():
    print("="*80)
    print("  SOVEREIGN AI: MULTI-ENGINE TRAINING PIPELINE")
    print("  Models: Prophet, Chronos (Amazon), NeuralForecast (N-HiTS), XGBoost")
    print("="*80)

    # 1. Check/Install Dependencies
    # Note: Chronos install is slightly different
    deps = [
        ("prophet", "prophet"),
        ("neuralforecast", "neuralforecast"),
        ("xgboost", "xgboost"),
        ("torch", "torch"),
        ("git+https://github.com/amazon-science/chronos-forecasting.git", "chronos")
    ]
    
    for pkg, imp in deps:
        try:
            check_and_install(pkg, imp)
        except Exception as e:
            print(f"  [ERROR] Failed to install {pkg}: {e}")

    # 2. Run Data Preparation
    run_script("scripts/prepare_data.py")

    # 3. Run Training Scripts
    scripts = [
        "scripts/train_prophet.py",
        "scripts/train_xgboost.py",
        # Chronos and NeuralForecast might be very slow/resource intensive, 
        # so we'll check if they are requested specifically or just run them.
        "scripts/train_chronos.py",
        "scripts/train_neuralforecast.py"
    ]

    for script in scripts:
        if os.path.exists(script):
            try:
                run_script(script)
            except Exception as e:
                print(f"  [FAILURE] {script} encountered an error: {e}")

    print("\n" + "="*80)
    print("  TRAINING COMPLETE. Forecasts saved in models/forecasts/")
    print("="*80)

if __name__ == "__main__":
    main()
