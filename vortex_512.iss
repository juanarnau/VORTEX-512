[Setup]
AppName=VORTEX-512
AppVersion=1.0
DefaultDirName={pf}\VORTEX-512
DefaultGroupName=VORTEX-512
AllowNoIcons=yes
OutputDir=dist
OutputBaseFilename=VORTEX-512-Setup
SetupIconFile=vortex_icon.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\VORTEX-512"; Filename: "{app}\main.exe"; WorkingDir: "{app}"
Name: "{commondesktop}\VORTEX-512"; Filename: "{app}\main.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Opciones adicionales"

[Run]
Filename: "{app}\main.exe"; Description: "Ejecutar VORTEX-512"; Flags: nowait postinstall skipifsilent