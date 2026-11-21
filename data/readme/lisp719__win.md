# win

## Windows

手動で行うこと。

- Windows Update
- Microsoft Store の更新

## Windows のセットアップ

管理者権限で実行する。

```powershell
./bootstrap_win.ps1
```

# WSL

```powershell
wsl --install -d FedoraLinux-42
```

OR

```powershell
wsl --install -d ubuntu
```

OR

```powershell
wsl --install -d archlinux
```

# WSL のセットアップ

```bash
sh bootstrap_wsl.sh
```

archlinux の場合は root で実行したあと、以下も実行する。

```bash
su lisp719
sh bootstrap_wsl.sh
```
