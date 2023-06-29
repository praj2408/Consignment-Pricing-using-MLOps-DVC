import subprocess

if __name__=="__main__":
    list_files = subprocess.run(["mlflow", "server","--backend-store-uri","sqlite:///mlflow.db","--default-artifact-root","artifacts","--host","127.0.0.1","-p","1234"])
    print(list_files.returncode)