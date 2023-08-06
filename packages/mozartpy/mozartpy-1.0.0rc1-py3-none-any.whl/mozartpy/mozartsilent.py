import subprocess

# Mozart Silent Exe 설치 경로
MozartSilentPath = r"C:\Program Files (x86)\VMS\Mozart\v2\Client\Bin\MozartSilent.exe"
ModelPath = r"C:\Users\vms\Downloads\silent_sample_model\model\MyModel.vmodel"
OutputFilePath = r"C:\Users\vms\Downloads\silent_sample_model\model"
Experiment = 'Experiment 2'
noLinkedModel = "noLinkedModel"
ArgsFile = r"C:\Users\vms\Downloads\silent_sample_model\model\SampleArgs.txt"

# Mozart Silent 실행
command = f'{MozartSilentPath} "{ModelPath}" -exp:"{Experiment}"'
result = subprocess.run(command, capture_output=True)

# 실행 결과 확인
if result.returncode == 0:
    print("MozartSilent.exe 실행 성공")
    print(result.stdout.decode('cp1252'))  # 표준 출력 결과
    print(result.stderr.decode('cp1252'))  # 표준 에러 결과

else:
    print("MozartSilent.exe 실행 실패")

print(MozartSilentPath)

# -exp:"{Experiment}" -{noLinkedModel}