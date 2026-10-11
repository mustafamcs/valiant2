@echo off
@cd data/config/general/wikipedia
@EncryptionDrop.exe

echo %time%
timeout 4 > NUL
echo %time%

@cd ../../../..
@call create_byname config