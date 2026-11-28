# Linux Disk Expand Migration Skill for OpenCode | Linux 磁盘扩容迁移 Skill

> 📝 **背景故事**: 这个 Skill 诞生于一次真实的"磁盘告急"事件。一位 ROS 开发者在编译项目时发现根分区使用率已达 78%，而 VMware 扩容后的 36GB 空间因位于扩展分区外无法直接合并。在 **Kimi K2.5** 的协助下，通过创建新分区 + 数据迁移 + 软链接的方案成功化解危机。本 Skill 记录了完整的操作流程和安全规范。

An OpenCode agent skill for safely expanding Linux disk space when standard partition resizing isn't possible.

## Overview

This skill guides you through creating a new data partition and migrating personal files when your root partition is full but unallocated space cannot be directly merged due to partition layout constraints (common in VMware/VirtualBox scenarios).

## Installation

### Option 1: Project-local (recommended for team sharing)
```bash
# 在其他项目中测试安装
mkdir -p .opencode/skills/linux-disk-expand-migration
curl -o .opencode/skills/linux-disk-expand-migration/SKILL.md \
  https://raw.githubusercontent.com/YOUR_USERNAME/linux-disk-expand-migration/main/SKILL.md
```

### Option 2: Global installation
```bash
mkdir -p ~/.config/opencode/skills/linux-disk-expand-migration
cp SKILL.md ~/.config/opencode/skills/linux-disk-expand-migration/
```

### Option 3: Claude-compatible locations
```bash
mkdir -p .claude/skills/linux-disk-expand-migration
cp SKILL.md .claude/skills/linux-disk-expand-migration/
```

## Usage

Once installed, OpenCode agents will automatically detect this skill when working in your project. The skill provides step-by-step guidance for:

1. **Assessment** - Check current disk layout and identify migration candidates
2. **Partition Creation** - Use GParted to create new partition from unallocated space
3. **Filesystem Setup** - Format, mount, and configure fstab for persistence
4. **Data Migration** - Safely move data using rsync with backup preservation
5. **Symlink Creation** - Create transparent symlinks for seamless access
6. **Verification** - Test and validate the new configuration

## When to Use | 使用场景

✅ **Use this skill when | 适合使用本 Skill:**
- Root partition is nearly full (>70%) | 根分区快满了（>70%）
- VMware/VirtualBox disk has been expanded | VMware/VirtualBox 已扩容虚拟磁盘
- Unallocated space exists outside extended partition | 未分配空间在扩展分区外
- GParted cannot resize across partition boundaries | GParted 无法跨越分区边界扩容
- You want system/data separation for easier maintenance | 希望系统/数据分离便于维护

❌ **Don't use when | 不适合使用:**
- Unallocated space IS contiguous with root (use GParted resize) | 未分配空间与根分区连续
- Using LVM (use lvextend instead) | 使用 LVM
- Production servers without maintenance windows | 无维护窗口的生产服务器
- You need a single filesystem (consider backup/reinstall) | 需要单一文件系统

## Typical Workflow | 典型工作流程

### 真实案例 | Real Case
```bash
# 初始状态 - 编译 ROS 项目时空间告急
$ df -h
/dev/sda5        29G   22G  6.3G   78% /
# 编译失败！No space left on device...

# VMware 扩容到 66GB 后，GParted 显示 36GB 未分配空间
# 但无法直接扩展到 /dev/sda5（位于扩展分区内）
# 解决方案：创建 /dev/sda3，迁移数据，使用软链接

# 使用本 Skill 后 | After using this skill
$ df -h
/dev/sda5        29G   22G  6.3G   78% /      # 系统盘，只装软件
/dev/sda3        36G   67M   34G    1% /data  # 数据盘，放个人文件

# 个人目录透明地指向新分区
$ ls -la ~
Documents -> /data/Documents
Downloads -> /data/Downloads
Pictures -> /data/Pictures
...

# 编译成功！ROS 工作空间留在快速 SSD，大文件移到数据盘
```

## Safety Features

- Always backs up original data before migration
- Preserves original directories with `.backup` suffix until verified
- Validates fstab configuration before relying on it
- Provides troubleshooting for common issues
- Clear rollback instructions

## Supported Scenarios

### VMware/VirtualBox Disk Expansion
The most common use case - you've expanded the virtual disk in hypervisor settings but the space appears as unallocated outside the extended partition.

### Physical Disk with Free Space
Physical drives with unallocated space that cannot be merged due to partition ordering.

### Dual-Boot Systems
Systems where partition constraints prevent easy resizing.

## What Gets Migrated

**Moved to data partition:**
- Documents, Downloads, Pictures, Videos, Music
- Projects directory
- Desktop contents
- Large personal datasets

**Stays on system partition:**
- OS and system files
- Installed applications
- Development workspaces (ROS, catkin_ws, etc.)
- Configuration files
- Package manager caches

## IDE Compatibility

Most applications transparently follow symlinks:
- ✅ VS Code
- ✅ JetBrains IDEs (PyCharm, CLion, IntelliJ)
- ✅ Terminal file managers
- ✅ File explorers
- ⚠️ May need to re-open recent files (path changes)

## Troubleshooting

See the SKILL.md for detailed troubleshooting section covering:
- Device busy errors
- fstab mount failures
- Permission issues
- Symlink conflicts

## Requirements

- Linux system with ext4 filesystem
- sudo/root access
- GParted installed
- Basic Linux command line knowledge

## License

MIT License - See LICENSE file

## Contributing

Contributions welcome! Please ensure:
1. Test on multiple Linux distributions
2. Update SKILL.md with any new scenarios
3. Add troubleshooting entries for issues encountered
4. Keep safety warnings prominent

## Acknowledgments | 致谢

本 Skill 的诞生源于一次真实的 ROS 开发环境磁盘扩容需求。在解决过程中，开发者与 **Kimi K2.5** 进行了多轮协作，包括：
- 分析 GParted 分区限制的技术方案
- 设计数据迁移的安全流程
- 处理软链接冲突等边界情况
- 验证 ROS/IDE 兼容性

这种"人机协作"模式展示了 AI 辅助系统管理的最佳实践：AI 提供技术方案和步骤指导，人类进行实际操作和验证决策。

## Disclaimer | 免责声明

⚠️ **Warning**: This operation involves partitioning and data migration. Always backup critical data before proceeding. While this skill provides safety measures, disk operations carry inherent risks.

**警告**: 本操作涉及分区和数据迁移。操作前务必备份关键数据。虽然本 Skill 提供了安全措施，但磁盘操作存在固有风险。

## Related Tools

- [GParted](https://gparted.org/) - Graphical partition editor
- [rsync](https://rsync.samba.org/) - Fast incremental file transfer
- [blkid](https://linux.die.net/man/8/blkid) - Locate/block device attributes

---

**Remember**: When in doubt, backup first!