RD /S /Q external\projects\EffectLib\Debug
RD /S /Q external\projects\EffectLib\Release
RD /S /Q external\projects\EterBase\Debug
RD /S /Q external\projects\EterBase\Release
RD /S /Q external\projects\EterCythonLib\Debug
RD /S /Q external\projects\EterCythonLib\Release
RD /S /Q external\projects\EterDiscordLib\Debug
RD /S /Q external\projects\EterDiscordLib\Release
RD /S /Q external\projects\EterGrnLib\Debug
RD /S /Q external\projects\EterGrnLib\Release
RD /S /Q external\projects\EterImageLib\Debug
RD /S /Q external\projects\EterImageLib\Release
RD /S /Q external\projects\EterLib\Debug
RD /S /Q external\projects\EterLib\Release
RD /S /Q external\projects\EterLocale\Debug
RD /S /Q external\projects\EterLocale\Release
RD /S /Q external\projects\EterPack\Debug
RD /S /Q external\projects\EterPack\Release
RD /S /Q external\projects\EterPythonLib\Debug
RD /S /Q external\projects\EterPythonLib\Release
RD /S /Q external\projects\GameLib\Debug
RD /S /Q external\projects\GameLib\Release
RD /S /Q external\projects\MilesLib\Debug
RD /S /Q external\projects\MilesLib\Release
RD /S /Q external\projects\ScriptLib\Debug
RD /S /Q external\projects\ScriptLib\Release
RD /S /Q external\projects\SpeedTreeLib\Debug
RD /S /Q external\projects\SpeedTreeLib\Release
RD /S /Q external\projects\SphereLib\Debug
RD /S /Q external\projects\SphereLib\Release
RD /S /Q external\projects\TerrainLib\Debug
RD /S /Q external\projects\TerrainLib\Release
RD /S /Q external\projects\UserInterface\Debug
RD /S /Q external\projects\UserInterface\Release
RD /S /Q external\projects\PRTerrainLib\Debug
RD /S /Q external\projects\PRTerrainLib\Release
DEL /F /S /Q /A external\projects\UserInterface\AntrumRelease_x86.exe

RD /S /Q ..\OtherTools\DumpProto\Debug
RD /S /Q ..\OtherTools\DumpProto\Release
RD /S /Q ..\OtherTools\DumpProto\.vs
RD /S /Q ..\OtherTools\dump_proto\Debug
RD /S /Q ..\OtherTools\dump_proto\Release
RD /S /Q ..\OtherTools\dump_proto\.vs
RD /S /Q ..\OtherTools\lzo\Debug
RD /S /Q ..\OtherTools\lzo\Release
RD /S /Q ..\OtherTools\lzo\.vs

RD /S /Q ..\ClientSource\.vs
RD /S /Q ..\ClientSource\ipch
DEL /F /S /Q /A ..\ClientSource\Antrum_Client.v12.suo
DEL /F /S /Q /A ..\ClientSource\Antrum_Client.sdf
DEL /F /S /Q /A ..\ClientSource\Antrum_Client.VC.db

DEL /F /S /Q /A ..\GameSource\source\db\src\.obj
DEL /F /S /Q /A ..\GameSource\source\game\src\.obj
DEL /F /S /Q /A ..\GameSource\source\.vs
