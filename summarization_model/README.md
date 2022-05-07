# run_mlm.py 
model pretraining을 위한 python script  
- model_training_command.txt 파일 내 command 복사 -> cmd 창에서 실행  
  - PATH로 설정되어 있는 arg는 적절한 디렉토리 설정 필요
  - tokenizer_name: GitHub 내 output/tokenizer 폴더의 디렉토리 사용
  - num_of_workers: preprocessing에 사용할 CPU processor 수, CPU 사양 및 processor 수 확인하여 적절한 수 설정 필요(i7 16 processor에서 8로 설정했을 때 CPU usage 60%)
  - batch_size: GPU 사양 따라 적절히 설정, out of memory 나면 줄여보기
